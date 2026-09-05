# 劳动仲裁全能助手

**English name:** Employee Labor Arbitration Assistant  
**Skill ID:** `labor-arbitration-assistant`  
**Version:** 0.2.1

![劳动仲裁全能助手LOGO](assets/logo.png)

## 简介

面向中国内地普通劳动者的劳动争议辅助技能。针对欠薪、未签劳动合同、未缴或少缴社保、违法解除、调岗降薪、加班费、年休假和试用期辞退等问题，提供简明行动方案，并可直接生成仲裁申请书、证据目录、质证意见、庭审问答及企业抗辩预测。

The Employee Labor Arbitration Assistant helps employees in Mainland China prepare practical strategies and documents for labor disputes. It supports wage arrears, unsigned contracts, social insurance, dismissal, pay cuts, overtime, annual leave, probation disputes, evidence preparation, hearings, and related proceedings.

本技能采用劳动者一方的办案立场，但属于AI辅助工具，不替代执业律师，不保证案件结果。

## 主要特点

- 根据用户信息完整度自动调整回答难度和篇幅，尽量使用普通人能看懂的语言。
- 用户直接要求文书时，当轮生成完整正文，缺失的个人信息用`【待补】`标示。
- 区分在职保岗与离职维权：在职时优先降低冲突、保存证据；离职后侧重现有材料和申请公司提交内部记录。
- 主动检查欠薪、经济补偿或赔偿、加班、年休假、二倍工资、失业保险损失等潜在请求，同时避免重复计算和虚构事实。
- 默认按全国通用规则先给方案，只有地方差异确会影响结果时再询问地区。

## 如何使用

安装或导入完整技能目录后，可以直接描述事实，也可以直接点名所需文书。信息不完整时无需先填写复杂表格，技能会先给可执行答复，再追问少量关键问题。

推荐提供：是否仍在职、入职和离职时间、工资、争议经过、公司通知原话、已经掌握的主要材料，以及希望继续工作还是拿钱离开。不要在公开聊天中发送完整身份证号码、银行卡号或无关人员隐私。

### 快速示例

```text
公司拖欠我4个月工资，大约1万元，我还在职，现在怎么办？
```

```text
我2024年3月入职，月薪8000元，昨天收到公司辞退通知。请直接写劳动仲裁申请书。
```

```text
我已经申请仲裁，请根据我现有的劳动合同、工资流水和微信通知，整理证据目录和证明目的。
```

更多可复制示例见[使用示例](examples/usage-examples.md)。发布页字段和推广文案见[发布资产说明](PUBLISHING.md)。

## 安装与目录

本项目只提供一个GitHub通用包，不再拆分Codex、WorkBuddy等平台专用包。将压缩包解压后的目录完整导入支持Skill目录的平台；不要只复制`SKILL.md`，否则引用规则、计算脚本和测试材料可能缺失。

```text
labor-arbitration-assistant/
├─ SKILL.md
├─ README.md
├─ PUBLISHING.md
├─ agents/
├─ assets/
├─ examples/
├─ references/
├─ scripts/
└─ tests/
```

## 验证状态

2026-09-05：使用PyYAML 6.0.3运行官方`quick_validate.py`；结构校验通过。14项算术测试、4项技能契约测试和3项发布资产测试均已运行。情景题用于人工验收，题库存在不代表真实模型行为全部通过。具体地方案件、金额、期限和最终文书仍应结合真实材料复核。

免费试用不设技能级次数或功能锁，但不代表宿主平台或模型服务免费。本包不含原始企业文书卷、当事人隐私资料或虚拟环境，不会自动对外发函、投诉或提交仲裁。
