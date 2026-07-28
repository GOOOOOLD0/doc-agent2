---
country: Brazil
topic: landing_rights
case_type: answer_template
source_document: official_source_notes_and_Report_Spacesail_EN
language: zh-CN
review_status: draft
last_reviewed: 2026-07-26
---

# 巴西落地许可 Agent 回答模板

## 1. 文件用途

本文件用于指导 Agent 在回答“巴西卫星落地许可需要做什么”时，输出稳定、完整、可追溯的答案。

回答时应优先引用：

1. `wiki/raw/landing_rights/brazil/source_notes/source_notes_index.md`；
2. 与问题相关的单个 source note 和本地原始快照；
3. 巴西案例文件 `00-09`；
4. `wiki/raw/landing_rights/brazil/source_inventory.md`；
5. `regulatory_sources/sources.json` 中已确认且正在监控的 URL。

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

巴西卫星落地许可不是单一许可，而是一组取决于商业模式的授权和合规事项。回答前必须先区分：

1. 仅向巴西持牌企业批发卫星容量；
2. 由巴西本地实体直接向终端用户提供电信服务。

外国卫星通过 FSS、MSS 或 BSS 与巴西地球站通信并提供容量时，原则上需要卫星开发权。卫星容量供应本身不构成电信服务，因此仅批发容量不能自动推出容量提供者还需终端服务授权。

本地实体直接向终端用户提供服务时，通常还需服务授权和具体服务通知。两种场景都可能涉及协调、适用产品 homologation、发射型地球站或空间站许可以及相关费用。

### 3.2 主管机关

巴西核心监管机构是 Anatel。Anatel 负责电信服务授权、外国卫星开发权、无线电频谱、设备认证和站点许可等监管事项。

### 3.3 需要办理的许可和合规事项

| 模块 | 巴西事项 | 作用 | 主要来源 |
|---|---|---|---|
| 外国卫星落地权 | Foreign Satellite Exploitation Rights / Right to Exploit Foreign Satellite | 允许外国卫星在巴西提供容量，并由符合要求的巴西法律代表履行本地代表义务 | `br-res-748-2021`, `br-act-9526-2021`, `br-anatel-satellite-rights-page` |
| 服务授权 | Collective- or restricted-interest service authorization + service notification | 直接向终端用户提供通信服务时适用，具体类别取决于业务 | `br-res-720-2020`, `br-res-777-2025`, `br-anatel-collective-services` |
| 频率协调 | Frequency coordination / coexistence | 提交协调协议，或在允许情形下提交协调努力并接受无保护、不得造成有害干扰的条件 | `br-res-748-2021`, `br-act-9523-2021`, `br-act-9426-2021` |
| 设备认证 | Conformity assessment + Anatel homologation | 受强制评定范围约束的电信产品需按产品规则办理 | `br-res-715-2019`, `br-anatel-product-certification`, `br-anatel-ocd-list` |
| 站点许可 | Station licensing | 发射型地球站需要许可；空间段投入运行后办理空间站许可；纯接收专业 FSS 站有登记路径 | `br-res-719-2020`, `br-anatel-earth-station-licensing`, `br-anatel-satellite-rights-page` |
| 费用 | Authorization fees, FISTEL and annual contributions | 覆盖卫星开发权、服务授权、TFI、TFF、CFRP、Condecine 等 | `br-anatel-satellite-rights-page`, `br-anatel-collective-services`, `br-law-5070-1966` |

### 3.4 申请主体安排

Spacesail 报告中设计了两个本地主体：

1. SBH：用于申请或持有外国卫星开发权，代表外国卫星运营商处理卫星容量进入巴西市场的问题；
2. SBS：用于申请或持有面向终端用户提供服务的服务授权。

回答时必须说明：这是 Spacesail 的项目架构，不是巴西法规要求所有外国卫星项目采用的双公司模式。

法规层面应确认：

1. 外国卫星运营商须指定符合要求的巴西法律代表；
2. 直接提供电信服务的主体须满足巴西本地服务授权资格；
3. 两种角色可能由同一法人承担，但其使用所代表卫星容量时需核对第 748/2021 号决议第 30 条第 2 款的合同结构要求。

### 3.5 外国卫星开发权申请材料

申请外国卫星开发权时，通常需要准备：

1. 巴西本地实体的 CNPJ；
2. 公司章程；
3. 未被禁止参与政府招标或政府合同的声明；
4. 技术能力和适当技术人员声明；
5. 卫星通信系统简化技术方案；
6. 遵守适用法规的声明；
7. 原属国主管机构出具、证明空间段获准使用期限和条件的文件及宣誓翻译；
8. 频率协调协议，或在规则允许的未完成协调情形下提交协调努力证明；
9. 共址协议，如适用；
10. 多个法律代表并存时的 FISTEL 和公开价格付款主体说明；
11. 外国运营商指定巴西法律代表的文件；
12. 卫星系统技术信息。

卫星系统技术信息通常包括：系统名称、轨道位置、卫星数量、ITU filing、发射和在巴西运营日期、轨道控制精度、巴西网关站、覆盖区域、频段、极化、TT&C 站和轨道参数。

原属国授权文件与 ITU filing 是不同材料，回答中不得混为一项。

### 3.6 服务授权申请材料

面向终端用户提供服务时，巴西本地服务主体通常需要取得集体利益或限制利益服务授权，并通知具体服务。可能涉及：

1. SCM，多媒体通信服务；
2. SMP，个人移动服务；
3. SLP，限制利益场景；
4. STFC、SeAC 或其他具体业务对应的服务。

SMGS 已进入停止新增并向 SMP 过渡的框架，不能作为不加说明的新申请选项。D2D 和 IoT 应标注为待项目级确认。

材料通常包括：

1. CNPJ；
2. 公司章程、股权结构和管理人员信息；
3. 根据巴西法律设立并在巴西设有总部的声明；
4. 适格声明；
5. 技术、经济和税务合规能力声明；
6. 州或联邦区纳税登记及系统要求的其他信息。

现行集体利益服务授权实行授权与具体服务通知相结合的模式，不能沿用“申请人必须声明未持有其他集体服务授权”的旧式概括。

### 3.7 频率协调和技术要求

回答中应明确：

1. 巴西流程要求关注频率协调；
2. 申请方应保存协调协议、会议纪要、报告或其他协调努力证明；
3. 特定未完成协调情形可在不主张干扰保护且不造成有害干扰的条件下申请；
4. 已核对官方来源未将这种条件统一命名为“secondary authorization”，不得把它写成正式两档授权制度；
5. ITU filing 不等于 Anatel 卫星开发权，也不自动建立巴西国内授权优先权。

### 3.8 设备认证和站点许可

设备认证方面，应先判断产品是否落入强制合格评定范围。适用产品通常先由认证范围匹配的 OCD 完成评定并签发合格证书，再由 Anatel 出具 homologation。CPQD 是多家 OCD 中的一家，不是唯一选择。

站点许可方面，需关注：

1. 所有发射型地球站需要许可；
2. 网关、TT&C 和用户终端按具体站型判断；
3. 纯接收专业 FSS 站有单独的服务通知和登记路径；
4. 空间段投入运行后应办理卫星或卫星系统的空间站许可证；
5. NGSO 空间站 TFI 按系统计算，但这不等于所有用户终端自动按系统许可。

商业运营通常应在相关许可、认证和站点要求完成后进行。

### 3.9 费用

巴西案例中已记录的主要费用包括：

| 费用项目 | 金额 | 说明 |
|---|---:|---|
| Right to Exploit Foreign Satellite | R$ 102,677.00 | 外国卫星开发权 / 落地权费用 |
| Collective-interest service authorization | R$ 400.00 | 集体利益服务授权、调整或转让的一次性公开价格 |
| 空间站 TFI | R$ 26,816.00 | GEO 按卫星、NGSO 按系统 |
| 年度 TFF + CFRP + Condecine | 三项合计为 TFI 的 50% | 不能写成 TFF 单独等于 50% |

回答时应补充：费用需在实际申请时根据 Anatel 最新有效规则复核。

### 3.10 法规来源

回答中建议列出以下已确认来源：

1. Law No. 9,472/1997, General Telecommunications Law (LGT): https://informacoes.anatel.gov.br/legislacao/leis/2-lei-9472
2. Resolution No. 748/2021, General Regulation for the Exploitation of Satellites: https://informacoes.anatel.gov.br/legislacao/resolucoes/2021/1595-resolucao-748
3. Act No. 9,523/2021: https://informacoes.anatel.gov.br/legislacao/atos-de-requisitos-tecnicos-de-gestao-do-espectro/2021/1598-ato-9523
4. Act No. 9,426/2021: https://informacoes.anatel.gov.br/legislacao/atos-de-requisitos-tecnicos-de-gestao-do-espectro/2021/1597-ato-9426
5. Act No. 9,526/2021: https://sei.anatel.gov.br/sei/publicacoes/controlador_publicacoes.php?acao=publicacao_visualizar&id_documento=8580171&id_orgao_publicacao=0
6. Law No. 5,070/1966, FISTEL Law: https://informacoes.anatel.gov.br/legislacao/leis/474-lei-5070
7. Resolution No. 715/2019: https://informacoes.anatel.gov.br/legislacao/resolucoes/2019/1350-resolucao-715
8. Resolution No. 719/2020: https://informacoes.anatel.gov.br/legislacao/resolucoes/2020/1381-resolucao-719
9. Resolution No. 720/2020: https://informacoes.anatel.gov.br/legislacao/resolucoes/2020/1382-resolucao-720
10. Resolution No. 777/2025: https://informacoes.anatel.gov.br/legislacao/resolucoes/2025/2022-resolucao-777
11. Anatel 卫星开发权办理页: https://www.gov.br/anatel/pt-br/regulado/satelite/conferencia-de-direito-de-exploracao-de-satelite
12. Anatel 卫星开发权申请手册: https://sistemas.anatel.gov.br/anexar-api/publico/anexos/download/e6517bea2f08bd17539dc2d5a0a04793
13. Anatel 集体利益服务办理页: https://www.gov.br/anatel/pt-br/regulado/outorga/servicos-de-interesse-coletivo
14. Anatel 地球站许可办理页: https://www.gov.br/anatel/pt-br/regulado/satelite/licenciamento-de-estacoes-terrenas
15. Anatel 产品认证办理页: https://www.gov.br/anatel/pt-br/regulado/certificacao-de-produtos
16. Anatel OCD 官方名单: https://www.gov.br/anatel/pt-br/regulado/certificacao-de-produtos/ocds

## 4. 不应直接断言的内容

以下内容必须标注为待确认或需要复核：

1. 具体审批周期；
2. 当前项目采用一个或两个本地主体的最佳结构；
3. 对 D2D、IoT、用户终端直连等新业务形态的具体服务分类；
4. 各类终端是否支持批量许可或豁免；
5. 项目适用的频率、地球站、设备和年度费用明细；
6. 第 777/2025 号决议相关过渡条款的项目适用日期。

## 5. 证据使用规则

Agent 生成回答时必须：

1. 每项关键结论至少能映射到一个官方 source note；
2. 对费用、期限、法规编号和有效期优先回查原始快照；
3. 将来源直接支持的内容标为“已确认”；
4. 将基于业务结构形成的判断标为“项目级推断”；
5. 将公开资料未解决的问题标为“待确认”；
6. 不得使用原 Spacesail 报告补足官方来源没有出现的固定周期、双主体要求、认证机构或终端许可方式；
7. 如果 source note 与 cases 不一致，应停止沿用 cases 结论并提示先更新知识库。

## 6. Agent 最短回答版本

如果用户只需要简短答案，可使用以下版本：

巴西卫星落地合规取决于业务模式。外国卫星在巴西提供容量通常先处理卫星开发权；仅批发容量时，容量供应本身不构成电信服务。若巴西本地实体直接向终端用户提供服务，还需取得相应服务授权并通知具体服务。项目还可能涉及协调、适用产品的 Anatel homologation、发射型地球站和空间站许可及相关费用。主管机关是 Anatel。实际申请前仍需确认具体服务分类、主体结构、终端许可方式、费用和审批周期。

## 7. 相关文件

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
- [[11_brazil_report_review|Spacesail 报告复核]]
