---
country: Mongolia
topic: landing_rights
doc_type: source_notes_index
language: zh-CN
review_status: draft
last_reviewed: 2026-07-21
---

# 蒙古卫星落地许可 Source Notes 索引

## 1. 文件用途

本索引汇总蒙古官方来源的逐来源摘要。生成正式 `00-09` cases 文件时，应先读取相关 source note，并回到对应本地快照核对关键条款。

## 2. Source notes

| Source ID | 来源 | 主要用途 | 状态 |
| --- | --- | --- | --- |
| `mn-crc-license-overview` | CRC 新申请人许可总览 | 许可类别和申请入口 | 已提取 |
| `mn-crc-satellite-network-license` | CRC 卫星通信网络许可页 | 卫星网络许可入口和遴选说明 | 已提取 |
| `mn-crc-radio-frequency-license` | CRC 频率许可申请页 | 频率和卫星站申请材料 | 已提取 |
| `mn-crc-radio-frequency-overview` | CRC 频谱管理总览 | 公共用途频率管理背景 | 已提取 |
| `mn-crc-equipment-conformity` | CRC 设备合格认证页 | 设备认证申请材料 | 已提取 |
| `mn-crc-laws-catalog` | CRC 法律目录 | 官方法规发现入口 | 已提取 |
| `mn-legal-satellite-frequency-rules` | CRC 第 37/2022 号决议主页面 | 决议编号、日期和附件批准关系 | 已提取 |
| `mn-legal-satellite-frequency-rules-annex` | 第 37/2022 号决议附件 | 双许可、MSS、NTN、设备、地球站和 ITU 要求 | 已提取，关键来源 |
| `mn-legal-communications-law` | 《通信法》 | 卫星网络许可材料、期限和遴选 | 已提取，关键来源 |
| `mn-legal-radio-waves-law` | 《无线电波法》 | 频率许可主体、材料、期限和续期 | 已提取，关键来源 |
| `mn-legal-permits-law` | 《许可法》 | 许可清单和一般办理程序 | 已提取，关键来源 |
| `mn-legal-investment-law` | 《投资法》 | 外国国有法人 33% 投资许可门槛 | 已提取 |
| `mn-legal-radio-frequency-fee-rule` | 频率使用和服务收费规则 | 费用构成和 FSS 计费原则 | 已提取 |

## 3. 可支持的分析模块

| 分析模块 | 主要 source notes | 当前证据状态 |
| --- | --- | --- |
| 卫星网络和服务特别许可 | `mn-legal-permits-law`、`mn-legal-communications-law`、`mn-legal-satellite-frequency-rules-annex` | 可形成初步结论 |
| 频率许可与持证主体 | `mn-legal-radio-waves-law`、`mn-crc-radio-frequency-license` | 可形成初步结论 |
| 地球站与技术条件 | `mn-legal-satellite-frequency-rules-annex`、`mn-crc-radio-frequency-license` | 可形成初步结论 |
| 设备合格认证 | `mn-legal-satellite-frequency-rules-annex`、`mn-crc-equipment-conformity` | 可形成初步结论 |
| ITU 登记和干扰协调 | `mn-legal-satellite-frequency-rules-annex`、`mn-legal-radio-waves-law` | 可形成初步结论 |
| 本地主体和外资 | `mn-legal-radio-waves-law`、`mn-legal-investment-law` | 部分确认，分支机构和私人外资限制待确认 |
| 费用 | `mn-legal-radio-frequency-fee-rule`、`mn-legal-satellite-frequency-rules-annex` | 仅支持计费原则，不能给出项目报价 |
| MSS、NTN/D2D | `mn-legal-satellite-frequency-rules-annex` | 存在专门条款，许可豁免范围待 CRC 确认 |

## 4. 生成 cases 前的限制

1. 不得把巴西的外国卫星开发权和 SBH/SBS 结构直接套用于蒙古。
2. 不得把“依蒙古法律设立并运营的法人”自动扩展为“只能设立蒙古子公司”；分支机构资格仍需确认。
3. 不得把 MSS 第 4.5 条解释为已经明确豁免所有卫星网络许可。
4. 不得把 NTN 第 4.10 条解释为外国卫星经营者可独立开展 D2D 零售业务。
5. 不得把一般法定审查期限写成完整项目周期。
6. 不得在缺少项目参数和现行费率表时给出固定费用金额。
