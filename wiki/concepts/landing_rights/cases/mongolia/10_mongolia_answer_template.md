---
country: Mongolia
topic: landing_rights
case_type: answer_template
source_document: Mongolia regulatory source pilot
language: zh-CN
review_status: draft
last_reviewed: 2026-07-07
---

# 蒙古落地许可 Agent 回答模板

## 1. 文件用途

本文件用于指导 Agent 在回答“蒙古卫星落地许可需要做什么”时，输出稳定、完整、可追溯的答案。

回答时应优先引用：

1. `regulatory_sources/mongolia.md`；
2. `wiki/raw/articles/landing_rights/mongolia/source_inventory.md`；
3. `regulatory_sources/sources.json` 中已确认且正在监控的蒙古 URL；
4. `sources/mongolia/` 中的已抓取快照。

## 2. 推荐回答结构

当用户问“蒙古如何获取卫星落地许可”或类似问题时，按以下结构回答：

1. 结论摘要；
2. 主管机关；
3. 需要办理的许可和合规事项；
4. 申请主体和本地安排；
5. 卫星通信网络/服务许可；
6. 无线电频率和频段许可；
7. 设备合格认证；
8. 费用和系统入口；
9. 法规来源；
10. 待确认问题；
11. 建议下一步。

## 3. 标准回答正文

### 3.1 结论摘要

蒙古卫星落地许可目前可按“CRC 许可 + 频率许可 + 设备认证 + 技术规则”四条主线理解。已确认的官方来源显示，蒙古 Communications Regulatory Commission (CRC) 管理通信领域特殊许可、无线电频率使用许可、卫星通信网络建设/运营/服务许可，以及通信设备合格认证。

和巴西不同，当前蒙古来源中尚未确认到一个名称上等同于巴西“外国卫星开发权 / Right to Exploit Foreign Satellite”的独立许可。因此回答时应避免直接套用巴西的许可名称，而应使用蒙古官方页面中出现的许可类别。

### 3.2 主管机关

蒙古核心监管机构是 Communications Regulatory Commission of Mongolia (CRC)。CRC 负责通信服务、通信网络、无线电频率、设备合格认证和相关许可监管。Legalinfo.mn 是蒙古官方法律信息来源，可用于核验基础法律和 CRC 决议。

### 3.3 需要办理的许可和合规事项

| 模块 | 蒙古事项 | 作用 | 主要来源 |
|---|---|---|---|
| 许可总入口 | CRC special permit / ordinary permit framework | 确认通信业务许可类别、CRC 权限和申请入口 | `mn-crc-license-overview`, `mn-crc-laws-catalog` |
| 卫星网络/服务 | Satellite communications network establishment, operation and service license | 处理卫星通信网络建设、运营和服务经营许可问题 | `mn-crc-satellite-network-license` |
| 频率许可 | Radio frequency and frequency band use special license | 使用无线电频率、频段、卫星通信和卫星移动通信频率时的许可材料 | `mn-crc-radio-frequency-license`, `mn-crc-radio-frequency-overview` |
| 技术规则 | Satellite communication system frequency allocation and technical requirements | 核验卫星通信系统频段划分、技术条件和要求 | `mn-legal-satellite-frequency-rules` |
| 设备认证 | Conformity certificate | 通信设备、无线电设备、终端和相关产品取得合格认证 | `mn-crc-equipment-conformity` |
| 基础法律 | Communications Law, Radio Waves Law, Law on Permits | 作为 CRC 许可、频率和通信监管权的法律背景 | `mn-crc-laws-catalog`, `mn-legal-communications-law`, `mn-legal-radio-waves-law`, `mn-legal-permits-law` |

### 3.4 申请主体和本地安排

CRC 频率概览页面显示，公共用途无线电频率可由依蒙古法律设立并运营的法人、组织、公民通过 CRC 许可、权利证书或登记使用。

因此，在回答商业卫星服务落地时，应提示：

1. 申请主体可能需要是蒙古本地依法设立并运营的主体，或与蒙古本地持证主体合作；
2. 当前来源尚未完整确认外国卫星运营商是否可以直接申请所有许可；
3. 不应直接假设蒙古必须采用巴西 SBH/SBS 双主体结构；
4. 外资准入、股权结构、当地代表或合作伙伴要求需要进一步核验。

### 3.5 卫星通信网络/服务许可

CRC 已将“卫星通信网络建设、运营和服务”列为通信许可类别。对应页面显示，该类许可与《许可法》和《通信法》相关，并提到通信网络建设、运营和服务许可通过 selection / tender 类程序授予。

回答时可以说明：

1. 如果业务涉及在蒙古建设、运营或提供卫星通信网络/服务，应先核验是否需要该特殊许可；
2. 该许可可能不是单纯备案，而可能涉及选择程序或竞争性程序；
3. 当前已找到页面确认许可类别，但完整申请材料、费用和审批周期仍需继续核验。

### 3.6 无线电频率和频段许可

CRC 频率页面明确列出“卫星通信”和“卫星移动通信”相关的无线电频率使用许可材料。申请方通常需要准备：

1. 组织结构、管理层和业务介绍；
2. 申请无线电频率许可的必要性说明；
3. 计划开展的业务说明；
4. 拟使用设备的技术参数；
5. 设备合格认证信息，例如 conformity certificate 或供应商声明；
6. 无线电设备部署图、技术方案、工作原理、框图；
7. 无线电发射设备的地理位置和覆盖范围图；
8. 业务可行性或市场调研；
9. 在目标地区开展业务的商业计划；
10. 项目实施时间表；
11. 如使用两个或更多地球站，应按站点分别填写申请表；
12. 卫星站或相关技术信息表格附件。

回答时应补充：CRC 页面中提到的 PDF、DOCX、XLSX 附件尚未被项目自动抽取，正式申请前需要人工下载并核对表格字段。

### 3.7 技术规则

Legalinfo.mn 上的 CRC Resolution No. 37/2022 批准了“卫星通信系统使用的无线电频段划分、技术条件和要求”。该文件应作为蒙古卫星系统频率和技术方案核验的核心来源之一。

回答时应提示申请方至少准备：

1. 使用频段；
2. 卫星系统类型；
3. 地面站或终端部署方式；
4. 发射功率、带宽、调制方式、天线增益等技术参数；
5. 与既有系统的兼容和干扰控制说明；
6. 与 CRC 频率申请表要求一致的站点资料。

### 3.8 设备合格认证

CRC 设备合格认证页面显示，申请通信设备 conformity certificate 通常需要：

1. 正式申请函；
2. 认证申请表；
3. 制造商或供应商符合性声明；
4. 制造商或供应商授权文件；
5. 近 6 年内的测试报告，包括健康安全、EMC、RF 等；
6. 企业登记证和章程副本；
7. 设备使用说明和配置说明；
8. 产品外部和内部结构图片；
9. 用户手册；
10. 证书样本；
11. 设备详细信息，包括名称、型号、制造商、技术类型、生产国、用途、工作频段、输出功率、调制方式、信道间隔、天线增益等；
12. 必要时提交设备样品和其他材料。

流程上，CRC 页面列出材料准备、递交、审查、签订证书使用合同/缴费、对认证产品使用符合性标志等步骤。

### 3.9 费用和系统入口

当前已确认的蒙古来源尚未整理出类似巴西费用清单中的固定金额。已知信息包括：

1. CRC 网站存在监管服务费、电子系统等入口；
2. 设备认证费用取决于 CRC 相关收费规则和评估方案；
3. 频率许可、卫星通信网络/服务许可和设备认证费用仍需进一步从 CRC 费用表或申请系统核验。

回答时应避免给出未核实金额，只能写“费用需向 CRC 最新费用表或申请系统复核”。

### 3.10 法规来源

回答中建议列出以下已确认来源：

1. CRC new license applicant overview: https://crc.gov.mn/for-new-license-applicants/tusgai-zovsoorol-4
2. CRC satellite communications network establishment, operation and service license page: https://crc.gov.mn/for-new-license-applicants/tusgai-zovsoorol-4/sansryn-xolboony-sulzee-baiguulax-tuunii-asiglalt-uilcilgee-erxlex-3
3. CRC radio frequency and frequency band use special license page: https://crc.gov.mn/for-new-license-applicants/tusgai-zovsoorol-4/radio-davtamz-asiglax-tusgai-zovsoorol
4. CRC radio frequency overview: https://crc.gov.mn/radio-davtamzh/tanilcuulga-3
5. CRC conformity certificate page: https://crc.gov.mn/for-new-license-applicants/batalgaazuulalt-e/toxirlyn-gercilgee-batalgaazuulalt
6. CRC catalog of Mongolian laws: https://crc.gov.mn/documents/mongol-ulsyn-xuuliud
7. CRC Resolution No. 37/2022 on satellite communication system frequency allocation and technical requirements: https://legalinfo.mn/mn/detail?lawId=16531361633621

## 4. 不应直接断言的内容

以下内容必须标注为待确认或需要复核：

1. 蒙古是否存在独立的“外国卫星落地权 / foreign satellite exploitation right”许可；
2. 外国卫星运营商能否直接申请，还是必须通过蒙古本地实体；
3. 申请是否必须参加 selection / tender，以及适用范围；
4. 具体审批周期；
5. 最新费用金额；
6. CRC 电子许可系统实际提交路径；
7. PDF、DOCX、XLSX 附件中的详细字段；
8. D2D、IoT、VSAT、MSS、宽带互联网等具体业务的分类。

## 5. Agent 最短回答版本

如果用户只需要简短答案，可使用以下版本：

蒙古卫星落地许可目前应按 CRC 许可体系处理，而不是直接套用巴西的外国卫星开发权。核心事项包括：向 CRC 核验是否需要“卫星通信网络建设、运营和服务”特殊许可；申请无线电频率/频段使用许可，尤其是卫星通信或卫星移动通信频率；按 CRC Resolution No. 37/2022 核验卫星通信系统频率划分和技术条件；对终端、地面站、网关或其他通信设备办理 CRC conformity certificate。费用、审批周期、本地实体要求和 CRC 附件表格仍需进一步确认。

## 6. 相关文件

- [[00_mongolia_case_index|返回蒙古案例索引]]
- `regulatory_sources/mongolia.md`
- `wiki/raw/articles/landing_rights/mongolia/source_inventory.md`
