---
country: Mongolia
topic: landing_rights
doc_type: source_inventory
language: zh-CN
review_status: draft
last_reviewed: 2026-07-21
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
| 7 | CRC Resolution No. 37/2022 approval page | https://legalinfo.mn/mn/detail?lawId=16531361633621 | Legalinfo.mn / CRC | HTML | 是 | 决议编号、日期、废止旧决议及附件批准关系 | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `mn-legal-satellite-frequency-rules`。 |
| 8 | Annex to CRC Resolution No. 37/2022 on satellite frequency allocation and technical requirements | https://legalinfo.mn/mn/detail?lawId=16531361657351 | Legalinfo.mn / CRC | HTML | 是 | 双许可、MSS、NTN、设备认证、地球站、费用依据和 ITU 协调 | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `mn-legal-satellite-frequency-rules-annex`；这是包含实质条款的附件页。 |
| 9 | Communications Law of Mongolia | https://legalinfo.mn/mn/detail/523 | Legalinfo.mn | HTML | 是 | 卫星网络许可期限、材料和遴选程序 | 可访问 | 可提取正文 | 不需人工 | 已保存快照并纳入月度监控，source_id: `mn-legal-communications-law`。 |
| 10 | Radio Waves Law of Mongolia | https://legalinfo.mn/mn/detail/443 | Legalinfo.mn | HTML | 是 | 频率持证主体、材料、协调、期限和续期 | 可访问 | 可提取正文 | 不需人工 | 已保存快照并纳入月度监控，source_id: `mn-legal-radio-waves-law`。页面英文译文有旧条款，关键结论以当前蒙古文为准。 |
| 11 | Law on Permits of Mongolia | https://legalinfo.mn/mn/detail?lawId=16530780109311 | Legalinfo.mn | HTML | 是 | 卫星和频率许可清单、一般许可程序 | 可访问 | 可提取正文 | 不需人工 | 已保存快照并纳入月度监控，source_id: `mn-legal-permits-law`。 |
| 12 | Investment Law of Mongolia | https://legalinfo.mn/mn/detail?lawId=9491 | Legalinfo.mn | HTML | 是 | 外国国有法人投资通信行业的许可门槛 | 可访问 | 可提取正文 | 不需人工 | 已保存快照并纳入月度监控，source_id: `mn-legal-investment-law`。33% 门槛不得扩大到所有外国投资者。 |
| 13 | Procedure for setting radio-frequency usage and service fees | https://legalinfo.mn/mn/detail?lawId=16530825397721 | Legalinfo.mn / 数字发展和通信部 | HTML | 是 | 频率费构成、FSS 上行计费原则和监管服务费 | 可访问 | 可提取正文 | 不需人工 | 已保存快照并纳入月度监控，source_id: `mn-legal-radio-frequency-fee-rule`；不能替代具体项目报价。 |

## 3. 可直接用于生成回答的来源

13 个来源均已保存官方页面快照并生成 source note，可按问题选择使用。关键法律结论应优先读取：

1. `mn-legal-satellite-frequency-rules-annex`
2. `mn-legal-communications-law`
3. `mn-legal-radio-waves-law`
4. `mn-legal-permits-law`
5. `mn-legal-investment-law`
6. `mn-legal-radio-frequency-fee-rule`

具体申请材料还应结合 CRC 的卫星网络许可、频率许可和设备合格认证页面。

## 4. 月度监控状态

上述 13 个来源均已写入 `regulatory_sources/sources.json` 且设置为 `monitor: true`。2026-07-21 已为 6 个新增 Legalinfo.mn 来源建立 baseline；后续每月任务会与这些本地快照比较。

## 5. 附件和表格

CRC 频率许可页面中观察到卫星通信、卫星移动通信相关 PDF、DOCX、XLSX 附件，包括卫星站申请表和频率使用站点材料。当前项目尚未加入 PDF/Word/Excel 附件抽取能力，因此第一版只监控包含这些附件链接的 CRC HTML 页面。

后续如果要把附件加入自动监控，需要先补充：

1. PDF 文本抽取；
2. DOCX 文本抽取；
3. XLSX 表格抽取；
4. 附件 URL 失效或重命名时的发现机制。

## 6. 仍不足的模块

1. 第 9.10 项下一轮遴选公告、名额、标准文件和实际申请入口；
2. 外国公司分支机构能否满足频率许可主体资格，以及一般私人外资是否存在其他限制；
3. 频率协调、遴选和签约合并后的实际项目周期；
4. 当前具体费率表、设备认证费及项目参数对应的最终金额；
5. CRC 电子许可系统的实际操作路径；
6. D2D、IoT、宽带互联网、VSAT、MSS 等不同业务形态的分类差异。

## 7. 下一步建议

1. 基于 `source_notes/source_notes_index.md` 生成并人工复核蒙古正式 `01-09` cases 文件；
2. 补充 CRC 频率申请表和卫星站 PDF、DOCX、XLSX 附件抽取；
3. 查找第 9.10 项最新遴选公告、费用表和电子申请系统说明；
4. 就 MSS 豁免范围、NTN/D2D 路径和分支机构资格取得 CRC 书面确认。
