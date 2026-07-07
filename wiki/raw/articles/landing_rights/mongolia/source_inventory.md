---
country: Mongolia
topic: landing_rights
doc_type: source_inventory
language: zh-CN
review_status: draft
last_reviewed: 2026-07-07
---

# 蒙古卫星落地许可来源清单

## 1. 文件用途

本文件记录蒙古卫星落地许可分析可使用的官方来源。它和 `regulatory_sources/mongolia.md` 的区别是：

1. 本文件面向知识抽取和回答生成；
2. `regulatory_sources/mongolia.md` 面向每月监控和 URL 维护；
3. `regulatory_sources/sources.json` 是机器可读监控配置。

## 2. 来源清单

| 序号 | 来源名称 | URL | 发布机构 | 来源类型 | 是否官方 | 对应模块 | 可访问 | 可提取正文 | 需人工处理 | 备注 |
| -- | ---- | --- | ---- | ---- | ---- | ---- | --- | ----- | ----- | -- |
| 1 | CRC new license applicant overview | https://crc.gov.mn/for-new-license-applicants/tusgai-zovsoorol-4 | Communications Regulatory Commission of Mongolia (CRC) | HTML | 是 | 许可类别、CRC 职权、特殊许可/普通许可分类 | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `mn-crc-license-overview`。 |
| 2 | Satellite communications network establishment, operation and service license page | https://crc.gov.mn/for-new-license-applicants/tusgai-zovsoorol-4/sansryn-xolboony-sulzee-baiguulax-tuunii-asiglalt-uilcilgee-erxlex-3 | CRC | HTML | 是 | 卫星通信网络建设、运营和服务许可 | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `mn-crc-satellite-network-license`。 |
| 3 | Radio frequency and frequency band use special license page | https://crc.gov.mn/for-new-license-applicants/tusgai-zovsoorol-4/radio-davtamz-asiglax-tusgai-zovsoorol | CRC | HTML | 是 | 无线电频率/频段使用许可、卫星通信和卫星移动通信频率申请材料 | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `mn-crc-radio-frequency-license`。 |
| 4 | CRC radio frequency overview | https://crc.gov.mn/radio-davtamzh/tanilcuulga-3 | CRC | HTML | 是 | 频谱管理原则、公共用途频率的许可/权利基础 | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `mn-crc-radio-frequency-overview`。 |
| 5 | CRC conformity certificate application page | https://crc.gov.mn/for-new-license-applicants/batalgaazuulalt-e/toxirlyn-gercilgee-batalgaazuulalt | CRC | HTML | 是 | 通信设备合格认证、证书申请和续期材料 | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `mn-crc-equipment-conformity`。 |
| 6 | CRC catalog of Mongolian laws | https://crc.gov.mn/documents/mongol-ulsyn-xuuliud | CRC | HTML | 是 | 官方法律目录，链接通信法、无线电波法、许可法等 | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `mn-crc-laws-catalog`。 |
| 7 | CRC Resolution No. 37/2022 on satellite communication system frequency allocation and technical requirements | https://legalinfo.mn/mn/detail?lawId=16531361633621 | Legalinfo.mn / CRC | HTML | 是 | 卫星通信系统频率划分和技术条件要求 | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `mn-legal-satellite-frequency-rules`。 |
| 8 | Communications Law of Mongolia | https://legalinfo.mn/mn/detail/523 | Legalinfo.mn | HTML | 是 | 通信监管职权、通信许可基础 | 可访问 | 可提取正文 | 暂不监控 | 已确认 URL，但页面较大，source_id: `mn-legal-communications-law`，暂不启用月度监控。 |
| 9 | Radio Waves Law of Mongolia | https://legalinfo.mn/mn/detail/443 | Legalinfo.mn | HTML | 是 | 频率国家所有、频率分配和使用许可基础 | 可访问 | 可提取正文 | 暂不监控 | 已确认 URL，但页面较大，source_id: `mn-legal-radio-waves-law`，暂不启用月度监控。 |
| 10 | Law on Permits of Mongolia | https://legalinfo.mn/mn/detail?lawId=16530780109311 | Legalinfo.mn | HTML | 是 | 许可分类、特殊许可/普通许可框架 | 可访问 | 可提取正文 | 暂不监控 | 已确认 URL，但页面很大，source_id: `mn-legal-permits-law`，暂不启用月度监控。 |

## 3. 可直接用于生成回答的来源

以下来源可直接用于生成蒙古落地许可回答：

1. `mn-crc-license-overview`
2. `mn-crc-satellite-network-license`
3. `mn-crc-radio-frequency-license`
4. `mn-crc-radio-frequency-overview`
5. `mn-crc-equipment-conformity`
6. `mn-crc-laws-catalog`
7. `mn-legal-satellite-frequency-rules`

## 4. 已确认但暂不监控的来源

以下来源已确认 URL，但因为 legalinfo.mn 法律正文页面体量较大，第一版暂不纳入月度监控：

1. `mn-legal-communications-law`
2. `mn-legal-radio-waves-law`
3. `mn-legal-permits-law`

回答中可以把它们作为法律背景来源，但应说明其尚未进入自动监控队列。

## 5. 附件和表格

CRC 频率许可页面中观察到卫星通信、卫星移动通信相关 PDF、DOCX、XLSX 附件，包括卫星站申请表和频率使用站点材料。当前项目尚未加入 PDF/Word/Excel 附件抽取能力，因此第一版只监控包含这些附件链接的 CRC HTML 页面。

后续如果要把附件加入自动监控，需要先补充：

1. PDF 文本抽取；
2. DOCX 文本抽取；
3. XLSX 表格抽取；
4. 附件 URL 失效或重命名时的发现机制。

## 6. 仍不足的模块

1. 卫星通信网络/服务特殊许可的完整申请材料清单；
2. 是否必须通过本地实体申请，及外国投资/外资持股限制；
3. 具体审批周期；
4. 监管服务费、频率费、设备认证费的最新金额；
5. CRC 电子许可系统的实际操作路径；
6. D2D、IoT、宽带互联网、VSAT、MSS 等不同业务形态的分类差异。

## 7. 下一步建议

1. 使用 `10_mongolia_answer_template.md` 作为 agent 回答蒙古问题的标准结构；
2. 优先补充 CRC 附件抽取能力，尤其是频率申请表和卫星站 Excel；
3. 决定 legalinfo.mn 大型法律页面的快照体积策略后，再启用 3 部基础法律的月度监控；
4. 如找到费用表、申请系统说明或英文官方材料，应补入本 source inventory 和 `sources.json`。
