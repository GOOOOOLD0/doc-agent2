---
country: Brazil
topic: landing_rights
case_type: answer_template
source_document: Report_Spacesail_EN
language: zh-CN
review_status: draft
last_reviewed: 2026-07-06
---

# 巴西落地许可 Agent 回答模板

## 1. 文件用途

本文件用于指导 Agent 在回答“巴西卫星落地许可需要做什么”时，输出稳定、完整、可追溯的答案。

回答时应优先引用：

1. 巴西案例文件 `00-09`；
2. `regulatory_sources/brazil.md`；
3. `wiki/raw/articles/landing_rights/brazil/source_inventory.md`；
4. `regulatory_sources/sources.json` 中已确认且正在监控的 URL。

## 2. 推荐回答结构

当用户问“巴西如何获取卫星落地许可”或类似问题时，按以下结构回答：

1. 结论摘要；
2. 主管机关；
3. 需要办理的许可和合规事项；
4. 申请主体安排；
5. 主要申请材料；
6. 频率协调和技术材料；
7. 设备认证和站点许可；
8. 费用；
9. 法规来源；
10. 待确认问题；
11. 建议下一步。

## 3. 标准回答正文

### 3.1 结论摘要

巴西卫星落地许可不是单一许可，而是一组授权和合规事项。对外国卫星系统而言，核心事项通常包括：

1. 外国卫星开发权 / 落地权；
2. 面向终端用户提供电信服务的服务授权；
3. 频率协调和技术要求；
4. 设备认证和 Anatel homologation；
5. 地面站、网关站、空间站或系统级站点许可；
6. FISTEL 等费用缴纳。

### 3.2 主管机关

巴西核心监管机构是 Anatel。Anatel 负责电信服务授权、外国卫星开发权、无线电频谱、设备认证和站点许可等监管事项。

### 3.3 需要办理的许可和合规事项

| 模块 | 巴西事项 | 作用 | 主要来源 |
|---|---|---|---|
| 外国卫星落地权 | Foreign Satellite Exploitation Rights / Right to Exploit Foreign Satellite | 允许巴西本地实体代表外国卫星运营商在巴西销售或使用外国卫星容量 | `br-res-748-2021`, `br-law-9472-1997` |
| 服务授权 | Authorization for Provision of Telecommunications Services | 允许巴西本地服务提供方向终端用户提供通信服务 | `br-res-720-2020`, `br-res-777-2025`, `br-law-9472-1997` |
| 频率协调 | Frequency coordination / coexistence | 证明系统与其他卫星或地面系统完成协调或已作出协调努力 | `br-act-9523-2021`, `br-act-9426-2021` |
| 设备认证 | Equipment certification / homologation | 用户终端、网关、网络设备等需取得 Anatel 认证或批准 | `br-res-715-2019` |
| 站点许可 | Station licensing | 地面站、网关站、空间站或 NGSO 系统按规则取得许可 | `br-res-719-2020`, `br-law-5070-1966` |
| 费用 | FISTEL, TFI, TFF and authorization fees | 覆盖外国卫星开发权、服务授权、安装检查费、运行检查费等 | `br-law-5070-1966`, `07_brazil_fee_list` |

### 3.4 申请主体安排

巴西案例中区分两个本地主体：

1. SBH：用于申请或持有外国卫星开发权，代表外国卫星运营商处理卫星容量进入巴西市场的问题；
2. SBS：用于申请或持有面向终端用户提供服务的服务授权。

回答时应说明：这是 Spacesail 巴西案例中的主体安排，不应直接假设其他国家也必须采用同样结构。

### 3.5 外国卫星开发权申请材料

申请外国卫星开发权时，通常需要准备：

1. 巴西本地实体的 CNPJ；
2. 公司章程；
3. 未被禁止参与政府招标或政府合同的声明；
4. 法律、技术、经济、财务和税务合规能力证明；
5. 卫星通信系统简化技术方案；
6. 遵守适用法规的声明；
7. 原属国主管机构文件及宣誓翻译；
8. 频率协调协议或协调努力证明；
9. 共址协议，如适用；
10. FISTEL 费用支付主体说明；
11. 卫星系统技术信息。

卫星系统技术信息通常包括：系统名称、轨道位置、卫星数量、ITU filing、发射和在巴西运营日期、轨道控制精度、巴西网关站、覆盖区域、频段、TT&C 站和轨道参数。

### 3.6 服务授权申请材料

面向终端用户提供服务时，巴西本地服务主体通常需要申请相应服务授权。可能涉及：

1. SCM，多媒体通信服务；
2. SMP，个人移动服务；
3. SMGS，全球移动卫星服务；
4. 其他具体业务对应的授权类别。

材料通常包括：

1. CNPJ；
2. 公司章程、股权结构和管理人员信息；
3. 根据巴西法律设立并在巴西设有总部的声明；
4. 适格声明；
5. 技术、经济和税务合规能力声明；
6. 是否持有其他集体服务授权的声明。

### 3.7 频率协调和技术要求

回答中应明确：

1. 巴西流程要求关注频率协调；
2. 申请方应保存协调协议、会议纪要、报告、视频记录或其他协调努力证明；
3. 授权状态可能与协调完成情况有关；
4. 未完成协调时，可能只能取得 secondary 性质的授权，并承担较弱的干扰保护地位。

### 3.8 设备认证和站点许可

设备认证方面，用户终端、网关设备、网络设备、地面站设备和其他电信产品可能需要 Anatel 认证和批准。认证通常通过 Anatel 指定认证机构 OCD 执行。

站点许可方面，需关注：

1. 电信站；
2. 地球站；
3. 网关站；
4. 空间站；
5. NGSO 系统级许可或批量许可可能性。

商业运营通常应在相关许可、认证和站点要求完成后进行。

### 3.9 费用

巴西案例中已记录的主要费用包括：

| 费用项目 | 金额 | 说明 |
|---|---:|---|
| Right to Exploit Foreign Satellite | R$ 102,677.00 | 外国卫星开发权 / 落地权费用 |
| SCM Authorization | R$ 400.00 | 多媒体通信服务授权费用 |
| TFI | R$ 26,816.00 / space station | 安装检查费 |
| TFF | TFI 的 50%，每年 | 运行检查费 |

回答时应补充：费用需在实际申请时根据 Anatel 最新有效规则复核。

### 3.10 法规来源

回答中建议列出以下已确认来源：

1. Law No. 9,472/1997, General Telecommunications Law (LGT): https://informacoes.anatel.gov.br/legislacao/leis/2-lei-9472
2. Resolution No. 748/2021, General Regulation for the Exploitation of Satellites: https://informacoes.anatel.gov.br/legislacao/resolucoes/2021/1595-resolucao-748
3. Act No. 9,523/2021: https://informacoes.anatel.gov.br/legislacao/atos-de-requisitos-tecnicos-de-gestao-do-espectro/2021/1598-ato-9523
4. Act No. 9,426/2021: https://informacoes.anatel.gov.br/legislacao/atos-de-requisitos-tecnicos-de-gestao-do-espectro/2021/1597-ato-9426
5. Law No. 5,070/1966, FISTEL Law: https://informacoes.anatel.gov.br/legislacao/leis/474-lei-5070
6. Resolution No. 715/2019: https://informacoes.anatel.gov.br/legislacao/resolucoes/2019/1350-resolucao-715
7. Resolution No. 719/2020: https://informacoes.anatel.gov.br/legislacao/resolucoes/2020/1381-resolucao-719
8. Resolution No. 720/2020: https://informacoes.anatel.gov.br/legislacao/resolucoes/2020/1382-resolucao-720
9. Resolution No. 777/2025: https://informacoes.anatel.gov.br/legislacao/resolucoes/2025/2022-resolucao-777
10. Portaria No. 560/1997: https://informacoes.anatel.gov.br/legislacao/normas-do-mc/185-portaria-560

## 4. 不应直接断言的内容

以下内容必须标注为待确认或需要复核：

1. Act No. 9,526/2021 的官方 URL；
2. 最新实际申请系统入口；
3. 具体审批周期；
4. 费用是否已有更新；
5. 当前是否仍适用 Spacesail 报告中的主体拆分方案；
6. 对 D2D、IoT、用户终端直连等新业务形态的具体服务分类。

## 5. Agent 最短回答版本

如果用户只需要简短答案，可使用以下版本：

巴西卫星落地许可通常包括两条主线：一是外国卫星开发权，解决外国卫星容量能否进入巴西市场；二是服务授权，解决巴西本地服务提供方能否向终端用户提供电信服务。除此之外，还要处理频率协调、设备认证、地面站/网关站/空间站许可和 FISTEL 相关费用。主管机关是 Anatel。核心法规包括 LGT、Resolution No. 748/2021、Resolution No. 720/2020、Resolution No. 777/2025、Resolution No. 715/2019、Resolution No. 719/2020 和 FISTEL Law。实际申请前仍需复核 Act No. 9,526/2021 的官方 URL、最新费用和 Anatel 线上系统要求。

## 6. 相关文件

- [[00_brazil_case_index|返回巴西案例索引]]
- [[01_brazil_landing_overview|巴西落地许可总览]]
- [[02_brazil_foreign_satellite_rights|巴西外国卫星开发权]]
- [[03_brazil_service_authorization|巴西服务授权]]
- [[04_brazil_frequency_coordination|巴西频率协调]]
- [[05_brazil_equipment_certification|巴西设备认证]]
- [[06_brazil_station_licensing|巴西站点许可]]
- [[07_brazil_fee_list|巴西费用清单]]
- [[08_brazil_regulations|巴西法规依据]]
- [[09_brazil_reusable_experience|巴西案例可复用经验]]
