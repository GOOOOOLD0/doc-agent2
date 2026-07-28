# Codex Repository Instructions

本文件是 Codex 的兼容入口。仓库级完整规则以同目录下的 `AGENT.md` 为准；执行任务前必须读取并遵守 `AGENT.md` 和当前任务对应的 `skills/*/SKILL.md`。

## 核心分工

以下分工适用于 Satellite Landing Rights；其他业务 Skill 的写入边界以各自 `SKILL.md` 为准。

### Codex 或人工维护者

负责正式落地许可知识生产：

- 检索、下载和审查官方来源；
- 创建和更新正式 Source Notes；
- 创建、审核和更新 Evidence Matrix；
- 创建、审核和更新正式 `00-09` 国家案例；
- 执行证据覆盖、结构、链接、版本和格式校验；
- 仅在用户明确要求时执行 Git 提交或推送。

### Hermes

负责正式知识使用：

- 根据正式 Wiki 回答用户问题；
- 按问题选择 `00-09`、Evidence Matrix 和 Source Notes；
- 对缺少资料或可能过期的国家生成 Research/Update 交接清单；
- 将研究候选和生成预览保存到 `.agent_runs/hermes/`；
- 不得直接覆盖正式 Source Notes、Evidence Matrix 或 `00-09`。

### 确定性脚本

负责定时访问、下载、哈希、变化记录、解析和格式检查，不自行生成新的法律结论。

## Satellite Landing Rights

涉及卫星落地许可、外国卫星准入、服务授权、频率、设备认证、地面站、网关、终端、费用或监管程序时，读取：

`skills/satellite-landing-rights/SKILL.md`

正式知识路径：

- 原始资料：`wiki/raw/landing_rights/<country>/`
- Evidence Matrix：`wiki/raw/landing_rights/<country>/evidence_matrix.md`
- 国家案例：`wiki/concepts/landing_rights/cases/<country>/`
- 通用规范：`wiki/concepts/landing_rights/common/`

巴西案例只能作为结构和检查维度参考，不能作为其他国家的事实依据。

## 全局要求

1. 关键结论必须回溯到官方来源、Source Note 或 Evidence Matrix。
2. 已确认信息、分析推断和待确认事项必须分开。
3. 不得编造许可、主体资格、费用、期限、材料或审批结果。
4. 阶段性法定时限不得写成完整项目周期。
5. 收费公式或单项费率不得写成固定项目总金额。
6. 自动生成的正式内容保持 `review_status: draft`。
7. 不覆盖已人工确认的内容，除非用户明确要求。
8. 不自动执行 commit、push、删除文件或发送外部信息。
9. 写入后必须验证路径、frontmatter、一级标题、Source Note 链接、Evidence 覆盖和内部链接。
10. 工作树可能包含用户改动；不得回退或覆盖与当前任务无关的变化。
