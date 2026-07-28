---
country: Brazil
topic: report_review
case_type: supplemental_review
source_document: Report_Spacesail_EN_and_official_sources
language: zh-CN
review_status: draft
last_reviewed: 2026-07-24
---

# 《Report_Spacesail_EN》巴西卫星落地许可复核

## 1. 文件用途

本文件记录对 `Report_Spacesail_EN.docx` 的逐项复核结果。原报告用于还原项目设想和初步流程；现行结论以 Anatel 法规、行政法令、官方办理页和申请手册为准。

本次复核日期为 2026 年 7 月 24 日。由于卫星、电信服务和收费规则可能继续调整，实际申请前仍需核对最新合并文本和项目适用条件。

## 2. 结论摘要

原报告的总体方向基本正确：外国卫星进入巴西通常需要处理卫星开发权，并根据业务模式处理服务授权、频率协调、产品认证和电台许可。

但原报告不能直接作为当前执行 SOP，主要原因是：

1. 把卫星开发权和服务授权写成所有项目都必须同时取得，忽略了“仅批发卫星容量”和“直接向终端用户提供电信服务”的差异。
2. 把 SBH 和 SBS 双主体设计写得像法定要求；法规要求的是合格的巴西法律代表和适格的本地服务提供者，不强制使用两个独立公司。
3. 将未完成协调时的“无保护且不得造成有害干扰”条件概括为正式的 primary / secondary 授权类别，表述过度。
4. 将 CPQD 写得过于突出；CPQD 是多家 Anatel 指定认证机构中的一家。
5. 将“所有设备”和“所有站点”概括为必须逐一认证或许可，未区分受强制认证范围约束的产品、发射型地球站、纯接收专业 FSS 站及其他特殊路径。
6. 将年度 TFF 直接写成 TFI 的 50%。Anatel 当前办理页明确的是 TFF、CFRP 和 Condecine 三项合计等于 TFI 的 50%。
7. 未反映第 777/2025 号决议带来的服务分类和 SMGS 向 SMP 过渡。
8. 未提供当前 SEI 申请入口、第 9,526/2021 号行政法令官方链接和 2023 年申请手册。

## 3. 原报告逐项复核

| 原报告主题 | 复核结论 | 修正或补充 |
| --- | --- | --- |
| 外国卫星开发权 | 基本正确 | FSS、MSS、BSS 与巴西地球站通信原则上需要卫星开发权；具体例外和其他卫星应用路径需按第 748/2021 号决议判断。 |
| 两类核心授权 | 有条件正确 | 直接向终端用户提供服务时通常还需服务授权；仅向持牌电信或广播企业、武装部队提供容量时，不应自动断言容量提供者还需服务授权。 |
| SBH / SBS 双主体 | 项目方案，不是通用法律结论 | 外国卫星运营商须指定巴西法律代表；服务提供者须符合巴西本地主体资格。是否由同一法人承担，应结合第 748/2021 号决议第 30 条第 2 款及合同结构判断。 |
| 外国卫星材料 | 大部分正确 | 原属国主管机关授权文件与 ITU filing 是不同材料；还需按第 9,526/2021 号行政法令和 SEI 表单提交公司、声明和技术文件。 |
| 协调材料 | 基本正确但概念需修正 | 法规允许特定未完成协调情形在无保护且不得造成有害干扰的条件下申请，并提交协调努力证明；不宜称为统一的“secondary authorization”。 |
| 服务类型 | 部分过时 | 现行框架是集体利益服务授权加具体服务通知；SMGS 已进入向 SMP 过渡阶段，具体日期和程序需逐条核对第 777/2025 号决议。 |
| 设备认证 | 方向正确但范围过宽 | 受强制合格评定范围约束的电信产品应取得 OCD 证书和 Anatel homologation；产品范围和技术要求需逐型号判断。 |
| CPQD | 不准确 | CPQD 是官方 OCD 名单中的一家，不是法定唯一认证机构。 |
| 地球站许可 | 方向正确但范围过宽 | 所有发射型地球站需要许可；纯接收专业 FSS 站有服务通知和登记路径，普通 TVRO 又属于不同场景。 |
| 空间站许可 | 正确但原报告不完整 | 空间段投入运行后，运营商还应申请卫星或卫星系统的空间站运行许可证。GEO 按卫星、NGSO 按系统处理相关 TFI。 |
| 外国卫星开发权费用 | 已确认 | 当前公开价格为 R$ 102,677，与频段数量和授权期限无关。 |
| 集体利益服务授权费用 | 已确认但名称需泛化 | 现行办理页列明一次性 R$ 400；不应只写为 SCM 专属费用。 |
| TFI | 已确认 | 空间站 TFI 为 R$ 26,816，GEO 按卫星、NGSO 按系统。 |
| TFF | 原报告错误 | TFF 不是单独等于 TFI 的 50%；Anatel 页面明确 TFF、CFRP 和 Condecine 三项年度费用合计为 TFI 的 50%。 |
| 审批周期 | 报告缺失 | 已核对来源未承诺完整项目固定周期，不能自行估算。 |

## 4. 复核后的适用流程

### 4.1 仅批发卫星容量

当外国卫星运营商仅向巴西持牌电信或广播服务提供者或武装部队提供容量时，核心路径通常是：

1. 确认具体卫星业务和频段是否需要卫星开发权；
2. 指定符合要求的巴西法律代表；
3. 通过 SEI 提交外国卫星开发权申请；
4. 提交第 9,526/2021 号行政法令要求的主体和声明文件；
5. 提交所属国授权文件及宣誓翻译、ITU filing 和系统技术资料；
6. 提交协调协议，或在法规允许的情形下提交协调努力证明并接受无保护、不得造成有害干扰的条件；
7. 支付卫星开发权公开价格；
8. 空间段投入运行后办理空间站许可和相关 Fistel 事项；
9. 按实际部署处理地球站许可和产品 homologation。

卫星容量供应本身不构成电信服务，因此不能仅因销售容量就自动增加面向终端用户的服务授权。

### 4.2 直接向终端用户提供服务

当本地实体直接向终端用户提供宽带、移动或其他电信服务时，在上述卫星开发权路径外通常还需要：

1. 取得集体利益或限制利益电信服务授权，具体取决于业务性质；
2. 在 Mosaico 等系统中通知拟提供的具体服务；
3. 取得或落实服务所依赖的频率使用安排或合格卫星容量合同；
4. 完成发射型地球站、网关和其他电台许可；
5. 对适用产品完成 OCD 合格评定和 Anatel homologation；
6. 遵守具体服务的用户、网络、质量、编号和持续监管义务。

具体应选择 SCM、卫星 SMP、SLP 或其他服务路径，必须根据终端形态、是否移动、业务对象、频率和商业关系逐项判断。

## 5. 仍需项目级确认

1. Spacesail 的首期业务究竟是纯容量批发、固定宽带零售、企业 VSAT、移动卫星、D2D 还是多种业务组合。
2. 巴西法律代表和本地服务提供者是否由同一法人承担；如同一主体使用其代表的卫星容量，应如何满足第 748/2021 号决议第 30 条第 2 款。
3. 目标频段涉及的具体协调对象、协调优先级和可接受的协调努力证明。
4. D2D、IoT 和用户终端直连在第 777/2025 号决议下的服务分类、频率和编号要求。
5. 终端设备是否支持型号认证、批量 station licensing 或豁免。
6. 项目适用的地球站、频率、认证和年度费用明细。
7. SEI、Mosaico、BDTA 和 STEL 在当前项目中的实际先后顺序及审批周期。

## 6. 主要官方依据

1. [Anatel 第 748/2021 号决议](https://informacoes.anatel.gov.br/legislacao/resolucoes/2021/1595-resolucao-748)
2. [Anatel 第 9,526/2021 号行政法令](https://sei.anatel.gov.br/sei/publicacoes/controlador_publicacoes.php?acao=publicacao_visualizar&id_documento=8580171&id_orgao_publicacao=0)
3. [Anatel 卫星开发权办理页](https://www.gov.br/anatel/pt-br/regulado/satelite/conferencia-de-direito-de-exploracao-de-satelite)
4. [Anatel 卫星开发权申请手册](https://sistemas.anatel.gov.br/anexar-api/publico/anexos/download/e6517bea2f08bd17539dc2d5a0a04793)
5. [Anatel 第 720/2020 号决议](https://informacoes.anatel.gov.br/legislacao/resolucoes/2020/1382-resolucao-720)
6. [Anatel 第 777/2025 号决议](https://informacoes.anatel.gov.br/legislacao/resolucoes/2025/2022-resolucao-777)
7. [Anatel 集体利益服务办理页](https://www.gov.br/anatel/pt-br/regulado/outorga/servicos-de-interesse-coletivo)
8. [Anatel 地球站许可办理页](https://www.gov.br/anatel/pt-br/regulado/satelite/licenciamento-de-estacoes-terrenas)
9. [Anatel 第 715/2019 号决议](https://informacoes.anatel.gov.br/legislacao/resolucoes/2019/1350-resolucao-715)
10. [Anatel OCD 官方名单](https://www.gov.br/anatel/pt-br/regulado/certificacao-de-produtos/ocds)

## 7. 使用结论

原报告应保留为项目历史输入，但后续 Agent 回答和其他国家对比不应直接引用其中未经修正的结论。正式回答应优先读取复核后的巴西 `01-10` 文件和对应 source notes。

## 8. 相关文件

- [[00_brazil_case_index|巴西案例索引]]
- [[01_brazil_landing_overview|巴西落地许可总览]]
- [[02_brazil_foreign_satellite_rights|巴西外国卫星开发权]]
- [[03_brazil_service_authorization|巴西服务授权]]
- [[04_brazil_frequency_coordination|巴西频率协调]]
- [[05_brazil_equipment_certification|巴西设备认证]]
- [[06_brazil_station_licensing|巴西站点许可]]
- [[07_brazil_fee_list|巴西费用清单]]
- [[08_brazil_regulations|巴西法规依据]]
- [[10_brazil_answer_template|巴西落地许可 Agent 回答模板]]
