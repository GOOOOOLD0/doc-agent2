---
country: Mongolia
topic: landing_rights
case_type: answer_template
source_document: mongolia_official_sources
language: zh-CN
review_status: draft
last_reviewed: 2026-07-21
---

# 蒙古落地许可 Agent 回答模板

## 1. 文件用途

本文件用于指导 Agent 在回答“蒙古卫星落地许可需要做什么”时，输出稳定、完整、可追溯的答案。

回答时应优先读取：

1. `00_mongolia_case_index.md` 和 `01_mongolia_landing_overview.md`；
2. 与用户问题对应的 `02-09` 正式 cases 文件；
3. `wiki/raw/landing_rights/mongolia/source_notes/source_notes_index.md`；
4. `wiki/raw/landing_rights/mongolia/source_inventory.md`；
5. 必要时回到 `wiki/raw/landing_rights/mongolia/sources/` 中的官方快照核对原文。

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
| 技术规则 | Satellite communication system frequency allocation and technical requirements | 核验双许可、MSS、NTN、设备、地球站、频段和 ITU 要求 | `mn-legal-satellite-frequency-rules-annex` |
| 设备认证 | Conformity certificate | 通信设备、无线电设备、终端和相关产品取得合格认证 | `mn-crc-equipment-conformity` |
| 基础法律 | Communications Law, Radio Waves Law, Law on Permits | 作为 CRC 许可、频率和通信监管权的法律背景 | `mn-crc-laws-catalog`, `mn-legal-communications-law`, `mn-legal-radio-waves-law`, `mn-legal-permits-law` |
| 外资 | Investment Law | 核验外国国有法人投资通信行业的特定许可门槛 | `mn-legal-investment-law` |
| 费用 | Radio-frequency usage and service fee methodology | 核验频率费组成、FSS 计费方向和监管服务费原则 | `mn-legal-radio-frequency-fee-rule` |

### 3.4 申请主体和本地安排

《无线电波法》第 7.1 条规定，公共用途无线电频率由依蒙古法律设立并运营的法人或公民取得 CRC 许可、权利文件并登记后使用。

因此，在回答商业卫星服务落地时，应提示：

1. 频率申请主体必须满足《无线电波法》第 7.1 条，但该条不能直接改写为“必须设立蒙古子公司”；
2. 当前来源尚未完整确认外国卫星运营商是否可以直接申请所有许可；
3. 不应直接假设蒙古必须采用巴西 SBH/SBS 双主体结构；
4. 外资准入、股权结构、当地代表或合作伙伴要求需要进一步核验。

### 3.5 卫星通信网络/服务许可

《许可法》第 8.1 条第 9.10 项将“卫星通信网络建设、运营和服务”列为 CRC 特别许可。《通信法》第 12.1、14.3 条规定该许可向法人授予、有效期五年，并通过至少每年一次的遴选程序授予。

回答时可以说明：

1. 一般卫星网络建设、运营和服务应把第 9.10 项作为核心许可核验；
2. 第 9.10 项通过遴选授予，但下一轮公告、资格和名额仍需确认；
3. MSS 第 4.5 条是否排除第 9.10 项、NTN 第 4.10 条如何适用，必须另行向 CRC 确认；
4. 第 9.3、9.4 项与卫星宽带、IoT、VSAT 和零售服务的关系尚未确认。

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

CRC Resolution No. 37/2022 的主页面只确认附件获批；实质要求位于独立附件页面 `mn-legal-satellite-frequency-rules-annex`。附件明确双许可原则、MSS 和 NTN 专门条款、设备型号认证、地球站和信道资料、土地批准以及 ITU 登记协调要求。

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

1. 频率使用费与频段、带宽、发射功率、业务类别或覆盖范围等因素有关；
2. FSS 频段使用费按地球至空间方向计算，并按频率范围区别处理；
3. 设备认证费用取决于 CRC 收费规则和评估方案；
4. 缺少项目参数、现行费率表和 CRC 缴费通知时，不得给出固定金额。

回答时应避免给出未核实金额，只能写“费用需向 CRC 最新费用表或申请系统复核”。

### 3.10 官方来源

回答中建议列出以下已确认来源：

1. CRC new license applicant overview: https://crc.gov.mn/for-new-license-applicants/tusgai-zovsoorol-4
2. CRC satellite communications network establishment, operation and service license page: https://crc.gov.mn/for-new-license-applicants/tusgai-zovsoorol-4/sansryn-xolboony-sulzee-baiguulax-tuunii-asiglalt-uilcilgee-erxlex-3
3. CRC radio frequency and frequency band use special license page: https://crc.gov.mn/for-new-license-applicants/tusgai-zovsoorol-4/radio-davtamz-asiglax-tusgai-zovsoorol
4. CRC radio frequency overview: https://crc.gov.mn/radio-davtamzh/tanilcuulga-3
5. CRC conformity certificate page: https://crc.gov.mn/for-new-license-applicants/batalgaazuulalt-e/toxirlyn-gercilgee-batalgaazuulalt
6. CRC catalog of Mongolian laws: https://crc.gov.mn/documents/mongol-ulsyn-xuuliud
7. CRC Resolution No. 37/2022 approval page: https://legalinfo.mn/mn/detail?lawId=16531361633621
8. Annex to CRC Resolution No. 37/2022: https://legalinfo.mn/mn/detail?lawId=16531361657351
9. Communications Law: https://legalinfo.mn/mn/detail/523
10. Radio Waves Law: https://legalinfo.mn/mn/detail/443
11. Law on Permits: https://legalinfo.mn/mn/detail?lawId=16530780109311
12. Investment Law: https://legalinfo.mn/mn/detail?lawId=9491
13. Radio-frequency usage and service fee methodology: https://legalinfo.mn/mn/detail?lawId=16530825397721

## 4. 不应直接断言的内容

以下内容必须标注为待确认或需要复核：

1. 蒙古是否存在独立的“外国卫星落地权 / foreign satellite exploitation right”许可；
2. 外国卫星运营商能否直接申请，还是必须通过蒙古本地实体；
3. 下一轮第 9.10 项遴选的公告时间、资格、名额和实际申请入口；
4. 具体审批周期；
5. 最新费用金额；
6. CRC 电子许可系统实际提交路径；
7. PDF、DOCX、XLSX 附件中的详细字段；
8. D2D、IoT、VSAT、MSS、宽带互联网等具体业务的分类。

## 5. Agent 最短回答版本

如果用户只需要简短答案，可使用以下版本：

蒙古公开官方资料中未发现名称和结构等同于巴西外国卫星开发权的独立许可。一般项目应核验第 9.10 项卫星通信网络特别许可和第 9.8 项频率许可，并同步处理设备型号认证、地球站及土地批准、卫星信道资料和 ITU/干扰协调。MSS、NTN/D2D、申请主体、服务许可组合、实际总周期和具体费用仍需 CRC 按业务模型书面确认。

## 6. 相关文件

- [[00_mongolia_case_index|返回蒙古案例索引]]
- [[01_mongolia_landing_overview|蒙古落地许可总览]]
- [[02_mongolia_foreign_satellite_rights|蒙古外国卫星准入]]
- [[03_mongolia_service_authorization|蒙古服务授权]]
- [[04_mongolia_frequency_coordination|蒙古频率许可与协调]]
- [[05_mongolia_equipment_certification|蒙古设备合格认证]]
- [[06_mongolia_station_licensing|蒙古站点许可]]
- [[07_mongolia_fee_list|蒙古费用清单]]
- [[08_mongolia_regulations|蒙古法规依据]]
- [[09_mongolia_reusable_experience|蒙古案例可复用经验]]
- [[wiki/raw/landing_rights/mongolia/source_inventory|蒙古来源清单]]
- [[wiki/raw/landing_rights/mongolia/source_notes/source_notes_index|蒙古 Source Notes 索引]]
