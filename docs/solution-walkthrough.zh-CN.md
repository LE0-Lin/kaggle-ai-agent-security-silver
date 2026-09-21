# 中文技术摘要

> 本文件仅提供中文摘要。申请与对外展示以英文 [README](../README.md) 和 [Technical Report](solution-walkthrough.md) 为准。

## 问题

比赛要求提交一个 `AttackAlgorithm`，在离线沙箱中搜索工具调用安全问题。评测器会在全新环境中重新执行候选，只对真实成功的工具调用和不同工具调用单元计分。

## 方法

最终方案集中于 confused-deputy 邮件表面：

- 测试两个短模板，每个模板运行两次；
- 每次运行前调用 `env.reset()`；
- 从 trace 中筛选 `name == "email.send"` 且 `ok is True` 的事件；
- 使用近似收益 `(4 × 成功调用数 + 2 × 成功单元数) / 耗时` 选择模板；
- 对 Gemma-family 目标使用 1 个 tool hop，其余配置使用 8 个；
- 将选中模板扩展为 2,000 个候选，收件人均使用不可真实投递的 `example.invalid` 域名。

## 结果与证据

| 项目 | 结果 |
|---|---:|
| Public Score | 16.215 |
| Private Score | **16.275** |
| 最终排名 | **184 / 4,186** |
| 奖牌 | **Competition Silver Medal** |

- [Kaggle 官方证书](https://www.kaggle.com/certification/competitions/leolin05/ai-agent-security-multi-step-tool-attacks)
- [英文技术报告](solution-walkthrough.md)
- [复现记录](reproducibility.md)
