"""Auditable arithmetic only. No automatic entitlement or limitation decisions."""
import json
import sys
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def number(value):
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError('金额或数量必须是十进制数') from exc
    if not result.is_finite() or result < 0:
        raise ValueError('金额或数量必须有限且非负')
    return result


def money(value):
    return format(value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP), '.2f')


def severance_units(completed_years, remainder_months, remainder_days=0):
    """Calendar service segments must already be verified, not 365-day estimates."""
    for value in (completed_years, remainder_months, remainder_days):
        if type(value) is not int or value < 0:
            raise ValueError('工龄分段必须为非负整数')
    if remainder_months > 11 or remainder_days > 30:
        raise ValueError('输入已核实的整年、剩余整月与不足月天数')
    extra = Decimal('1') if remainder_months >= 6 else (
        Decimal('0.5') if remainder_months or remainder_days else Decimal('0'))
    return Decimal(completed_years) + extra


def calculate_line(item):
    required = ('id', 'request', 'start', 'end', 'basis_source', 'quantity_source',
                'rule_status', 'scenario', 'basis', 'divisor', 'quantity', 'multiplier', 'paid')
    for key in required:
        if key not in item or str(item[key]).strip() == '':
            raise ValueError('缺少字段: ' + key)
    if date.fromisoformat(item['start']) > date.fromisoformat(item['end']):
        raise ValueError('计算期间倒置')
    if item['rule_status'] not in ('已核验', '待核验'):
        raise ValueError('rule_status只能为已核验或待核验')
    basis, divisor, quantity, multiplier, paid = (
        number(item[key]) for key in ('basis', 'divisor', 'quantity', 'multiplier', 'paid'))
    if divisor == 0:
        raise ValueError('divisor必须大于零')
    gross = basis / divisor * quantity * multiplier
    balance = gross - paid
    return dict(item, formula=f'{basis} / {divisor} * {quantity} * {multiplier} - {paid}',
                gross=money(gross), balance=money(balance),
                warning='抵扣超过算得金额，需核对；未自动变成返还请求' if balance < 0 else '')


def calculate_case(items):
    if not isinstance(items, list) or not items:
        raise ValueError('输入应为非空请求明细数组')
    rows, seen, totals = [], set(), {}
    for item in items:
        row = calculate_line(item)
        if row['id'] in seen:
            raise ValueError('请求明细id重复')
        seen.add(row['id'])
        rows.append(row)
        # No cross-scenario total: callers must review legal concurrence themselves.
        key = row['scenario']
        totals[key] = totals.get(key, Decimal('0')) + Decimal(row['balance'])
    return {'status': '纯算术结果，不证明权利成立或时效有效', 'rows': rows,
            'scenario_totals_do_not_add': {key: money(value) for key, value in totals.items()},
            'needs_rule_review': any(row['rule_status'] == '待核验' for row in rows)}


if __name__ == '__main__':
    try:
        with open(sys.argv[1], encoding='utf-8-sig') as stream:
            result = calculate_case(json.load(stream))
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (IndexError, ValueError, TypeError, KeyError, OSError) as exc:
        print('计算未完成: ' + str(exc), file=sys.stderr)
        sys.exit(1)
