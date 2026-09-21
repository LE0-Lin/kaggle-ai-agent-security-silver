# 中文说明

> The English [README](README.md) and [technical report](docs/solution-walkthrough.md) are the primary project documentation.

本仓库记录我在 Kaggle **AI Agent Security: Multi-Step Tool Attacks** 比赛中的方案。Kaggle 官方介绍写明比赛由 **OpenAI、Google 和 IEEE** 共同举办，并将 OpenAI 列为 Competition Host。最终成绩为 **184 / 4,186（Top 4.4%）**，获得 Competition Silver Medal，Private Score 为 **16.275**。

- [英文项目主页](README.md)
- [英文技术报告](docs/solution-walkthrough.md)
- [Kaggle 比赛主页](https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks)
- [Kaggle 官方证书](https://www.kaggle.com/certification/competitions/leolin05/ai-agent-security-multi-step-tool-attacks)
- [复现记录](docs/reproducibility.md)

## 方法摘要

最终方案是一个受时间预算约束的在线搜索算法，而不是训练模型。流程如下：

1. 在官方离线环境中分别测试两个候选模板；
2. 每次探测前重置环境；
3. 从工具 trace 中只统计成功的 `email.send`；
4. 用近似评分收益除以运行时间，选择收益率更高的模板；
5. 根据目标模型设置不同的工具调用步数；
6. 生成 2,000 个使用 `example.invalid` 地址的确定性候选。

核心代码位于 [`attack.py`](attack.py)，最终计分 Notebook 归档于 [`notebooks/kaggle_submission_v18.ipynb`](notebooks/kaggle_submission_v18.ipynb)。

## 结果

| 项目 | 结果 |
|---|---:|
| 最终排名 | **184 / 4,186** |
| 奖牌 | **Competition Silver Medal** |
| Public Score | 16.215 |
| Private Score | **16.275** |
| Submission ID | `55905450` |

项目不包含比赛数据、私有评测资产、凭据、真实邮箱地址或线上攻击目标，使用 [MIT License](LICENSE) 开源。
