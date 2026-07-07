---
country: Brazil
topic: landing_rights
doc_type: source_inventory
language: zh-CN
review_status: draft
last_reviewed: 2026-07-06
---

# 巴西卫星落地许可来源清单

## 1. 文件用途

本文件记录巴西卫星落地许可分析可使用的官方来源。它和 `regulatory_sources/brazil.md` 的区别是：

1. 本文件面向知识抽取和回答生成；
2. `regulatory_sources/brazil.md` 面向每月监控和 URL 维护；
3. `regulatory_sources/sources.json` 是机器可读监控配置。

## 2. 来源清单

| 序号 | 来源名称 | URL | 发布机构 | 来源类型 | 是否官方 | 对应模块 | 可访问 | 可提取正文 | 需人工处理 | 备注 |
| -- | ---- | --- | ---- | ---- | ---- | ---- | --- | ----- | ----- | -- |
| 1 | Law No. 9,472/1997, General Telecommunications Law (LGT) | https://informacoes.anatel.gov.br/legislacao/leis/2-lei-9472 | Anatel / Brazil Federal Government | 法律 HTML | 是 | 监管机构、服务授权、频谱/轨道职权 | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `br-law-9472-1997`。 |
| 2 | Resolution No. 748/2021, General Regulation for the Exploitation of Satellites | https://informacoes.anatel.gov.br/legislacao/resolucoes/2021/1595-resolucao-748 | Anatel | 决议 HTML | 是 | 外国卫星开发权、卫星落地权 | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `br-res-748-2021`。 |
| 3 | Act No. 9,523/2021, technical and operational requirements for satellite communication systems | https://informacoes.anatel.gov.br/legislacao/atos-de-requisitos-tecnicos-de-gestao-do-espectro/2021/1598-ato-9523 | Anatel | 技术要求 HTML | 是 | 卫星系统技术要求、频率协调支持 | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `br-act-9523-2021`。 |
| 4 | Act No. 9,426/2021, coexistence parameters between terrestrial and satellite stations | https://informacoes.anatel.gov.br/legislacao/atos-de-requisitos-tecnicos-de-gestao-do-espectro/2021/1597-ato-9426 | Anatel | 技术要求 HTML | 是 | 共存、干扰、频率协调 | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `br-act-9426-2021`。 |
| 5 | Act No. 9,526/2021, requirements for obtaining the right to exploit satellites | 待确认 | Anatel | 待确认 | 待确认 | 外国卫星开发权申请要求 | 无法访问 | 无法提取 | 需人工 | Spacesail 报告中提及，但尚未确认官方 URL；source_id: `br-act-9526-2021`，暂不监控。 |
| 6 | Law No. 5,070/1966, FISTEL Law | https://informacoes.anatel.gov.br/legislacao/leis/474-lei-5070 | Anatel / Brazil Federal Government | 法律 HTML | 是 | TFI、TFF、站点相关费用 | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `br-law-5070-1966`。 |
| 7 | Resolution No. 715/2019, conformity assessment and homologation of telecom products | https://informacoes.anatel.gov.br/legislacao/resolucoes/2019/1350-resolucao-715 | Anatel | 决议 HTML | 是 | 设备认证、Anatel homologation | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `br-res-715-2019`。 |
| 8 | Resolution No. 719/2020, General Licensing Regulation (RGL) | https://informacoes.anatel.gov.br/legislacao/resolucoes/2020/1381-resolucao-719 | Anatel | 决议 HTML | 是 | 地面站、网关站、空间站许可 | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `br-res-719-2020`。 |
| 9 | Resolution No. 720/2020, General Regulation of Grants (RGO) | https://informacoes.anatel.gov.br/legislacao/resolucoes/2020/1382-resolucao-720 | Anatel | 决议 HTML | 是 | 服务授权、授权转让和终止 | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `br-res-720-2020`。 |
| 10 | Resolution No. 777/2025, General Regulation of Telecommunications Services (RGST) | https://informacoes.anatel.gov.br/legislacao/resolucoes/2025/2022-resolucao-777 | Anatel | 决议 HTML | 是 | SCM、SMP、SMGS 服务规则和过渡规则 | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `br-res-777-2025`。 |
| 11 | Resolution No. 477/2007, former SMP regulation | https://informacoes.anatel.gov.br/legislacao/resolucoes/2007/9-resolucao-477 | Anatel | 历史决议 HTML | 是 | 历史 SMP 参考 | 可访问 | 可提取正文 | 不需人工 | 已被 Resolution No. 777/2025 废止，archive only。 |
| 12 | Resolution No. 614/2013, former SCM regulation | https://informacoes.anatel.gov.br/legislacao/resolucoes/2013/465-resolucao-614 | Anatel | 历史决议 HTML | 是 | 历史 SCM 参考 | 可访问 | 可提取正文 | 不需人工 | 已被 Resolution No. 777/2025 废止，archive only。 |
| 13 | Portaria No. 560/1997, Norma No. 16/97 for non-geostationary SMGS | https://informacoes.anatel.gov.br/legislacao/normas-do-mc/185-portaria-560 | Ministry of Communications / Anatel legislation portal | 历史/过渡规范 HTML | 是 | SMGS 历史和过渡规则 | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `br-portaria-560-1997`。 |

## 3. 可直接用于生成回答的来源

以下来源可直接用于生成巴西落地许可回答：

1. `br-law-9472-1997`
2. `br-res-748-2021`
3. `br-act-9523-2021`
4. `br-act-9426-2021`
5. `br-law-5070-1966`
6. `br-res-715-2019`
7. `br-res-719-2020`
8. `br-res-720-2020`
9. `br-res-777-2025`
10. `br-portaria-560-1997`

## 4. 仍需人工确认的来源

- `br-act-9526-2021`: Spacesail 报告中提到 Act No. 9,526/2021，但当前尚未确认到官方 URL。回答中如引用该文件，必须标注“官方 URL 待确认”。

## 5. 仍不足的模块

1. Anatel 实际线上申请系统入口和操作指南；
2. OCD / CPQD 设备认证操作性指南；
3. 站点注册系统和 BDTA/Spectrum-E 具体入口；
4. 费用是否已有更细的官方计算器或最新版费用表。

## 6. 下一步建议

1. 先用 `10_brazil_answer_template.md` 作为 agent 回答巴西问题的标准结构；
2. 后续如找到 Anatel 申请系统、认证指南、费用表，应补入本 source inventory 和 `sources.json`；
3. 若确认 `Act No. 9,526/2021` 官方 URL，再启用月度监控。
