import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('calculate', Path(__file__).parents[1] / 'scripts/calculate.py')
calc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calc)


def row(**changes):
    item = dict(id='C1', request='虚构算例', start='2026-08-01', end='2026-08-31',
                basis='6960', divisor='174', quantity='2', multiplier='1.5', paid='0',
                basis_source='算例基数', quantity_source='算例时数', rule_status='待核验', scenario='主位')
    item.update(changes)
    return item


class ArithmeticTests(unittest.TestCase):
    def test_overtime(self):
        self.assertEqual(calc.calculate_line(row())['balance'], '120.00')

    def test_annual_leave_additional_two(self):
        self.assertEqual(calc.calculate_line(row(divisor='21.75', quantity='5', multiplier='2'))['balance'], '3200.00')

    def test_second_wage_only(self):
        self.assertEqual(calc.calculate_line(row(divisor='1', quantity='1', multiplier='1'))['balance'], '6960.00')

    def test_paid_deduction(self):
        self.assertEqual(calc.calculate_line(row(paid='20'))['balance'], '100.00')

    def test_overpayment_visible(self):
        result = calc.calculate_line(row(paid='200'))
        self.assertEqual(result['balance'], '-80.00')
        self.assertTrue(result['warning'])

    def test_half_year_boundary(self):
        self.assertEqual(calc.severance_units(2, 5, 30), calc.Decimal('2.5'))
        self.assertEqual(calc.severance_units(2, 6, 0), calc.Decimal('3'))
        self.assertEqual(calc.severance_units(2, 0, 0), calc.Decimal('2'))

    def test_service_validation(self):
        for values in ((2, 12, 0), (-1, 1, 0), (2, 1, 31), (True, 0, 0)):
            with self.assertRaises(ValueError):
                calc.severance_units(*values)

    def test_no_cross_scenario_total(self):
        result = calc.calculate_case([row(), row(id='C2', scenario='备位', multiplier='2')])
        self.assertEqual(result['scenario_totals_do_not_add'], {'主位': '120.00', '备位': '160.00'})
        self.assertTrue(result['needs_rule_review'])
        self.assertNotIn('total', result)

    def test_invalid_decimal(self):
        for value in ('NaN', 'Infinity', '-1', 'abc'):
            with self.assertRaises(ValueError):
                calc.calculate_line(row(basis=value))

    def test_zero_divisor(self):
        with self.assertRaises(ValueError):
            calc.calculate_line(row(divisor='0'))

    def test_bad_dates(self):
        for changes in ({'start': '2026-09-01'}, {'start': '2026-02-30'}):
            with self.assertRaises(ValueError):
                calc.calculate_line(row(**changes))

    def test_required_evidence(self):
        with self.assertRaises(ValueError):
            calc.calculate_line(row(basis_source=''))

    def test_duplicate_ids(self):
        with self.assertRaises(ValueError):
            calc.calculate_case([row(), row()])

    def test_rounding(self):
        self.assertEqual(calc.calculate_line(row(basis='1.005', divisor='1', quantity='1', multiplier='1'))['balance'], '1.01')


if __name__ == '__main__':
    unittest.main()
