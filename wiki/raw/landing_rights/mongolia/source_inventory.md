---
country: Mongolia
topic: landing_rights
doc_type: source_inventory
language: zh-CN
review_status: draft
last_reviewed: 2026-07-26
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
| 14 | CRC electronic license platform instructions | https://crc.gov.mn/electronic-license-platform | CRC | HTML | 是 | 电子申请入口、新申请、续期和电子签名 | 可访问 | 可提取正文 | 登录后需人工 | 已保存快照并纳入月度监控，source_id: `mn-crc-e-license-instructions`；`customer.crc.gov.mn` 登录页本轮超时。 |
| 15 | CRC license conditions and technical requirements catalog | https://crc.gov.mn/terms-of-the-customer-service-contract | CRC | HTML | 是 | 现行卫星许可条件和技术要求发现入口 | 可访问 | 可提取正文 | 不需人工 | 已保存快照并纳入月度监控，source_id: `mn-crc-license-conditions-catalog`。 |
| 16 | CRC regulatory service fees page | https://crc.gov.mn/zoxicuulaltyn-uilcilgeenii-xols-2 | CRC | HTML | 是 | 现行费用规则和金额表发现入口 | 可访问 | 可提取正文 | 不需人工 | 已保存快照并纳入月度监控，source_id: `mn-crc-regulatory-service-fees`。 |
| 17 | CRC Resolution No. 24/2026 approving the equipment certification procedure | https://legalinfo.mn/mn/detail?lawId=17435913766732 | Legalinfo.mn / CRC | HTML | 是 | 现行设备认证程序批准、旧程序废止 | 可访问 | 可提取正文 | 不需人工 | 已保存快照并纳入月度监控，source_id: `mn-legal-equipment-certification-resolution-2026`。 |
| 18 | Information and communications equipment certification procedure | https://legalinfo.mn/mn/detail?lawId=17435914033652 | Legalinfo.mn / CRC | HTML / DOCX | 是 | 认证主体、材料、审查期限、方案和证书期限 | 可访问 | 可提取正文 | 不需人工 | 已保存 HTML 和 DOCX 并纳入 HTML 月度监控，source_id: `mn-legal-equipment-certification-procedure-2026`。 |
| 19 | Law on Standardization, Technical Regulation and Accreditation of Conformity Assessment | https://legalinfo.mn/mn/detail/13071 | Legalinfo.mn | HTML | 是 | 强制合格评定的一般法律基础 | 可访问 | 可提取正文 | 不需人工 | 已保存快照并纳入月度监控，source_id: `mn-legal-standardization-conformity-law`。 |
| 20 | Fixed and transportable satellite station frequency application form | https://crc.gov.mn/storage/%D0%A0%D0%B0%D0%B4%D0%B8%D0%BE%20%D0%B4%D0%B0%D0%B2%D1%82%D0%B0%D0%BC%D0%B6/last/%D0%A1%D0%90%D0%9D%D0%A1%D0%A0%D0%AB%D0%9D%20%D0%A5%D0%9E%D0%9B%D0%91%D0%9E%D0%9E%D0%9D%D0%AB%20%D2%AE%D0%99%D0%9B%D0%A7%D0%98%D0%9B%D0%93%D0%AD%D0%AD%D0%9D%D0%94%20%D0%A0%D0%90%D0%94%D0%98%D0%9E%20%D0%94%D0%90%D0%92%D0%A2%D0%90%D0%9C%D0%96,%20%D0%A0%D0%90%D0%94%D0%98%D0%9E%20%D0%94%D0%90%D0%92%D0%A2%D0%90%D0%9C%D0%96%D0%98%D0%99%D0%9D%20%D0%97%D0%A3%D0%A0%D0%92%D0%90%D0%A1%20%D0%90%D0%A8%D0%98%D0%93%D0%9B%D0%90%D0%A5%20%D0%A1%D0%A2%D0%90%D0%9D%D0%A6.pdf | CRC | PDF | 是 | 固定站、可搬移站、链路预算、卫星信道和逐站字段 | 可访问 | 可提取文本 | 已人工复核 | 已保存原件和 source note，source_id: `mn-crc-satellite-fixed-frequency-form`；当前脚本不直接监控 PDF。 |
| 21 | Mobile satellite service frequency application form | https://crc.gov.mn/storage/%D0%A0%D0%B0%D0%B4%D0%B8%D0%BE%20%D0%B4%D0%B0%D0%B2%D1%82%D0%B0%D0%BC%D0%B6/last/%D0%A1%D0%90%D0%9D%D0%A1%D0%A0%D0%AB%D0%9D%20%D0%A5%D3%A8%D0%94%D3%A8%D0%9B%D0%93%D3%A8%D3%A8%D0%9D%D0%A2%20%D0%A5%D0%9E%D0%9B%D0%91%D0%9E%D0%9D%D0%AB%20%D2%AE%D0%99%D0%9B%D0%A7%D0%98%D0%9B%D0%93%D0%AD%D0%AD%D0%9D%D0%94%20%D0%A0%D0%90%D0%94%D0%98%D0%9E%20%D0%94%D0%90%D0%92%D0%A2%D0%90%D0%9C%D0%96,%20%D0%A0%D0%90%D0%94%D0%98%D0%9E%20%D0%94%D0%90%D0%92%D0%A2%D0%90%D0%9C%D0%96%D0%98%D0%99%D0%9D%20%D0%97%D0%A3%D0%A0%D0%92%D0%90%D0%A1%20%D0%90%D0%A8%D0%98%D0%93%D0%9B%D0%90%D0%A5%20%D0%A1%D0%A2%D0%90%D0%9D%D0%A6.pdf | CRC | PDF | 是 | MSS 系统、终端、频率和卫星运营商字段 | 可访问 | 可提取文本 | 已人工复核 | 已保存原件和 source note，source_id: `mn-crc-satellite-mobile-frequency-form`；当前脚本不直接监控 PDF。 |
| 22 | Satellite station application spreadsheet | https://crc.gov.mn/storage/media/63982082-f9cb-41be-814c-b46d888ab122.xlsx | CRC | XLSX | 是 | 多站点设备、带宽和坐标清单 | 可访问 | 可提取表格 | 已人工复核 | 已保存原件和 source note，source_id: `mn-crc-satellite-station-annex`；当前脚本不直接监控 XLSX。 |
| 23 | CRC regulatory service fee schedule, Resolution No. 61/2022 as amended by No. 203/2024 | https://crc.gov.mn/storage/documents/November2024/012-61-Ammend203-2024_Attach-Fee-MOJHA-2022-1222.pdf | CRC | PDF | 是 | 卫星网络许可年度监管服务费 | 可访问 | 扫描件 | 已人工复核 | 已保存原件和 source note，source_id: `mn-crc-regulatory-service-fee-schedule`；当前脚本不直接监控 PDF。 |
| 24 | CRC radio-frequency usage and service fee schedule, Resolution No. 94/2023 | https://crc.gov.mn/storage/%D0%97%D0%97%D2%AE%D0%A2%D0%97%D0%93/batoyun/%D0%A0%D0%B0%D0%B4%D0%B8%D0%BE%20%D0%B4%D0%B0%D0%B2%D1%82%D0%B0%D0%BC%D0%B6%D0%B8%D0%B9%D0%BD%20%D1%82%D3%A9%D0%BB%D0%B1%D3%A9%D1%80%D0%B8%D0%B9%D0%BD%20%D1%85%D1%8D%D0%BC%D0%B6%D1%8D%D1%8D%202023%20%D0%BE%D0%BD%D1%8B%2094.pdf | CRC | PDF | 是 | GSO、NGSO、地球站、MSS 和频率权利费 | 可访问 | 扫描件 | 已人工复核 | 已保存原件和 source note，source_id: `mn-crc-radio-frequency-fee-schedule`；需结合 A/37 方法和项目参数。 |
| 25 | CRC equipment certification fee schedule, Resolution No. 13/2020 | https://crc.gov.mn/storage/PDF/2020/2020-togtool13.pdf | CRC | PDF | 是 | 设备认证、续期和补发费用 | 可访问 | 扫描件 | 已人工复核 | 已保存原件和 source note，source_id: `mn-crc-equipment-certification-fee-schedule`；与 2026 程序的适用关系待 CRC 确认。 |
| 26 | CRC official posts search for satellite-related notices | https://crc.gov.mn/posts?q=%D1%81%D0%B0%D0%BD%D1%81%D1%80%D1%8B%D0%BD | CRC | HTML | 是 | 新公告、征求意见和遴选窗口发现 | 可访问 | 可提取正文 | 不需人工 | 已保存快照并纳入月度监控，source_id: `mn-crc-satellite-posts-search`；2026-07-26 未发现第 8.1.9.10 项当前窗口。 |
| 27 | CRC guidance on registering satellite earth stations in the Master International Frequency Register | https://crc.gov.mn/posts/slug1510 | CRC | HTML | 是 | ITU 登记历史背景 | 可访问 | 可提取正文 | 需人工判定时效 | 已保存快照和 source note，source_id: `mn-crc-itu-earth-station-registration-guidance`；2015 年历史资料，不作为现行程序主依据。 |

## 3. 可直接用于生成回答的来源

27 个来源均已保存官方页面或附件，并生成 source note。关键法律结论应优先读取：

1. `mn-legal-satellite-frequency-rules-annex`
2. `mn-legal-communications-law`
3. `mn-legal-radio-waves-law`
4. `mn-legal-permits-law`
5. `mn-legal-investment-law`
6. `mn-legal-radio-frequency-fee-rule`
7. `mn-legal-equipment-certification-resolution-2026`
8. `mn-legal-equipment-certification-procedure-2026`

具体申请材料还应结合 CRC 的卫星网络许可页、频率许可页、固定/移动卫星申请表和站点 XLSX。费用问题应读取金额表，但不得把单项费用相加后直接称为完整项目成本。

## 4. 月度监控状态

27 个来源均已写入 `regulatory_sources/sources.json`：

1. 20 个现行 HTML 页面设置为 `monitor: true`，后续每月与本地快照比较；
2. 6 个 PDF/XLSX 附件已保存和提取，但当前脚本只支持 HTML，暂设为 `monitor: false`；
3. 2015 年 ITU 登记指导属于历史资料，已归档但不参与月度监控。

## 5. 附件和表格

CRC 频率许可页面中的固定卫星站 PDF、移动卫星业务 PDF 和站点 XLSX 已下载、提取并生成为独立 source note。设备认证程序 DOCX 也已保存。

当前监控脚本仍只支持 HTML。附件的更新发现主要依赖其容器页面；后续如要对二进制文件做内容级自动比对，需要补充：

1. PDF 文本抽取；
2. DOCX 文本抽取；
3. XLSX 表格抽取；
4. 附件 URL 失效或重命名时的发现机制。

## 6. 仍不足的模块

1. 第 8.1.9.10 项下一轮遴选公告、名额、标准文件和当前申请窗口；
2. 外国公司分支机构能否满足频率许可主体资格，以及一般私人外资是否存在其他限制；
3. 频率协调、遴选和签约合并后的实际项目周期；
4. 2020 年设备认证收费表在 2026 年新程序下的对应关系，以及项目参数对应的最终金额；
5. CRC 电子许可系统登录后的字段、材料上传和状态流转；
6. D2D、IoT、宽带互联网、VSAT、MSS 等不同业务形态的分类差异。
7. 现行强制合格评定产品清单及卫星终端具体归类；
8. CRC 实时持证人名录和历史卫星网络许可遴选文件。

## 7. 下一步建议

1. 用新增 source notes 复核蒙古正式 `01-09` cases，重点更新设备认证、频率申请字段和费用；
2. 持续监控 CRC 公告检索页，查找第 8.1.9.10 项新遴选公告；
3. 向 CRC 核实 2026 设备认证程序对应的现行收费和强制产品清单；
4. 就 MSS 豁免范围、NTN/D2D 路径、分支机构资格和实际审批顺序取得 CRC 书面确认。
