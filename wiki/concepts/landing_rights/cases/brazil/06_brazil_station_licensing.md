---
country: Brazil
topic: station_licensing
case_type: structured_case
source_document: official_source_notes_and_Report_Spacesail_EN
language: zh-CN
review_status: draft
last_reviewed: 2026-07-26
---

# 巴西站点许可

## 1. 基本概念

巴西流程中涉及站点许可。

报告中提到的站点类型包括：

1. Telecommunications Station，电信站；
2. Earth Station，地球站；
3. Gateway，网关站。

## 2. 电信站

Telecommunications Station 是指一组电信设备和设施。

该概念可覆盖多种通信设施，是站点许可制度中的基础概念。

## 3. 地球站

Earth Station 是位于地球表面的站点，用于与卫星通信。

在卫星业务场景中，地球站可能包括网关站、TT&C 站或其他卫星通信地面设施。

## 4. 网关站

Gateway 是连接卫星系统和地面网络的接入站。

对于 NGSO 卫星系统，网关站许可通常是业务落地的重要环节。

## 5. 地球站许可程序

Anatel 当前办理页明确：所有发射型地球站需要许可，并且只有已经取得相应电信服务授权、许可或特许的实体才能办理电台许可。

实际流程通常包括：

1. 在 Anatel 的 BDTA 系统中登记站点；
2. 根据服务和站型使用 Mosaico、STEL 或相关电子系统；
3. 遵守 General Licensing Regulation，RGL；
4. 按具体规则办理单站、简化、豁免或系统性登记；
5. 支付适用费用并取得许可证。

纯接收专业 FSS 地球站有单独的服务通知和登记路径；普通家庭 TVRO 不应与该路径混同。

## 6. 空间站和 NGSO 系统

空间段投入运行后，卫星运营商还需申请卫星或卫星系统的空间站运行许可证。

Anatel 当前办理页的空间站 TFI 口径是：

1. GEO 空间站按卫星；
2. NGSO 空间站按系统。

这不代表所有地球站或用户终端均可自动按整个星座一次性许可。终端和网关的许可方式仍需按站型和现行规则确认。

## 7. 商业运营要求

商业运营应在适用的服务授权、服务通知、频率、产品 homologation 和所需电台许可均有效后进行。不能把纯接收站、发射型地球站、空间站和所有用户终端概括成完全相同的前置条件。

## 8. 费用

与站点相关的费用包括：

| 费用项目 | 金额 |
|---|---:|
| TFI 安装检查费 | R$ 26,816.00 / space station |
| 年度 TFF + CFRP + Condecine | 三项合计为 TFI 的 50% |

上述 TFI 是空间站口径，不应直接套用到每个地球站或用户终端。

## 9. 对其他国家分析的启发

分析其他国家时，需要确认：

1. 网关站是否需要许可；
2. 地球站是否需要许可；
3. TT&C 站是否需要许可；
4. 用户终端是否需要单独站点许可；
5. NGSO 星座是否可以按系统许可；
6. 是否可以批量许可；
7. 站点许可是否是商业运营前置条件。

## 10. 待确认问题模板

对于其他国家，应重点确认：

1. 网关是否必须部署在本国境内；
2. 是否允许境外网关服务本国用户；
3. 地面站许可是否按站点、按系统或按服务办理；
4. 用户终端是否需要单站许可；
5. 是否支持批量许可；
6. 是否存在空间站、地球站、网关站不同收费标准。

## 11. 主要官方依据

1. [Anatel 第 719/2020 号决议](https://informacoes.anatel.gov.br/legislacao/resolucoes/2020/1381-resolucao-719)
2. [Anatel 地球站许可办理页](https://www.gov.br/anatel/pt-br/regulado/satelite/licenciamento-de-estacoes-terrenas)
3. [Anatel 卫星开发权办理页](https://www.gov.br/anatel/pt-br/regulado/satelite/conferencia-de-direito-de-exploracao-de-satelite)
4. [Law No. 5,070/1966](https://informacoes.anatel.gov.br/legislacao/leis/474-lei-5070)

## 12. 证据状态与边界

| 结论 | 状态 | 主要 source notes |
|---|---|---|
| 站点许可位于服务授权之后，所有发射型地球站需要许可 | 已确认 | [[br-anatel-earth-station-licensing]]、[[br-res-719-2020]] |
| 专业纯接收 FSS 站存在关联 SLP 181 的登记路径，普通 TVRO 不属于该场景 | 已确认 | [[br-anatel-earth-station-licensing]] |
| 空间段投入运行后需要办理卫星或卫星系统的空间站运行许可证 | 已确认 | [[br-anatel-satellite-rights-page]]、[[br-res-748-2021]] |
| GEO 空间站按卫星、NGSO 空间站按系统计算公开 TFI | 已确认 | [[br-anatel-satellite-rights-page]] |
| 所有用户终端均可按整个星座一次性许可 | 未获官方依据支持 | 空间站按系统计费不能自动扩展为终端批量许可 |
| 网关、移动平台和用户终端的单站、批量、简化或豁免路径 | 待确认 | 需按服务、发射能力、站型及最新行政规则判断 |

## 13. 相关文件

- [[00_brazil_case_index|返回巴西案例索引]]
- [[01_brazil_landing_overview|巴西落地许可总览]]
- [[11_brazil_report_review|Spacesail 报告复核]]
