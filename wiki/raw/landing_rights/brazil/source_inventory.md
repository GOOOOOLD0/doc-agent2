---
country: Brazil
topic: landing_rights
doc_type: source_inventory
language: zh-CN
review_status: draft
last_reviewed: 2026-07-26
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
| 5 | Act No. 9,526/2021, requirements for obtaining the right to exploit satellites | https://sei.anatel.gov.br/sei/publicacoes/controlador_publicacoes.php?acao=publicacao_visualizar&id_documento=8580171&id_orgao_publicacao=0 | Anatel | 官方 SEI HTML | 是 | 外国卫星开发权申请材料 | 可访问 | 可提取正文 | 不需人工 | 已确认官方 URL 并保存快照；source_id: `br-act-9526-2021`。 |
| 6 | Law No. 5,070/1966, FISTEL Law | https://informacoes.anatel.gov.br/legislacao/leis/474-lei-5070 | Anatel / Brazil Federal Government | 法律 HTML | 是 | TFI、TFF、站点相关费用 | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `br-law-5070-1966`。 |
| 7 | Resolution No. 715/2019, conformity assessment and homologation of telecom products | https://informacoes.anatel.gov.br/legislacao/resolucoes/2019/1350-resolucao-715 | Anatel | 决议 HTML | 是 | 设备认证、Anatel homologation | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `br-res-715-2019`。 |
| 8 | Resolution No. 719/2020, General Licensing Regulation (RGL) | https://informacoes.anatel.gov.br/legislacao/resolucoes/2020/1381-resolucao-719 | Anatel | 决议 HTML | 是 | 地面站、网关站、空间站许可 | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `br-res-719-2020`。 |
| 9 | Resolution No. 720/2020, General Regulation of Grants (RGO) | https://informacoes.anatel.gov.br/legislacao/resolucoes/2020/1382-resolucao-720 | Anatel | 决议 HTML | 是 | 服务授权、授权转让和终止 | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `br-res-720-2020`。 |
| 10 | Resolution No. 777/2025, General Regulation of Telecommunications Services (RGST) | https://informacoes.anatel.gov.br/legislacao/resolucoes/2025/2022-resolucao-777 | Anatel | 决议 HTML | 是 | SCM、SMP、SMGS 服务规则和过渡规则 | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `br-res-777-2025`。 |
| 11 | Resolution No. 477/2007, former SMP regulation | https://informacoes.anatel.gov.br/legislacao/resolucoes/2007/9-resolucao-477 | Anatel | 历史决议 HTML | 是 | 历史 SMP 参考 | 可访问 | 可提取正文 | 不需人工 | 已被 Resolution No. 777/2025 废止，archive only。 |
| 12 | Resolution No. 614/2013, former SCM regulation | https://informacoes.anatel.gov.br/legislacao/resolucoes/2013/465-resolucao-614 | Anatel | 历史决议 HTML | 是 | 历史 SCM 参考 | 可访问 | 可提取正文 | 不需人工 | 已被 Resolution No. 777/2025 废止，archive only。 |
| 13 | Portaria No. 560/1997, Norma No. 16/97 for non-geostationary SMGS | https://informacoes.anatel.gov.br/legislacao/normas-do-mc/185-portaria-560 | Ministry of Communications / Anatel legislation portal | 历史/过渡规范 HTML | 是 | SMGS 历史和过渡规则 | 可访问 | 可提取正文 | 不需人工 | 已纳入月度监控，source_id: `br-portaria-560-1997`。 |
| 14 | Conferência de Direito de Exploração de Satélite | https://www.gov.br/anatel/pt-br/regulado/satelite/conferencia-de-direito-de-exploracao-de-satelite | Anatel | 官方办理页面 HTML | 是 | 申请入口、材料、期限、费用、空间站许可 | 可访问 | 可提取正文 | 不需人工 | 已保存快照并纳入月度监控；source_id: `br-anatel-satellite-rights-page`。 |
| 15 | Manual para Solicitação de Direito de Exploração de Satélite, versão 02 | https://sistemas.anatel.gov.br/anexar-api/publico/anexos/download/e6517bea2f08bd17539dc2d5a0a04793 | Anatel | 官方指南 PDF | 是 | SEI 申请步骤和技术字段 | 可访问 | 可提取正文 | 不需人工 | 2023 年 8 月第 2 版，已保存 PDF；由上游办理页监控是否换版；source_id: `br-anatel-satellite-rights-manual-2023`。 |
| 16 | Serviços de Interesse Coletivo | https://www.gov.br/anatel/pt-br/regulado/outorga/servicos-de-interesse-coletivo | Anatel | 官方办理页面 HTML | 是 | 服务授权、材料、Mosaico 和服务通知 | 可访问 | 可提取正文 | 不需人工 | 已保存快照并纳入月度监控；source_id: `br-anatel-collective-services`。 |
| 17 | Licenciamento de Estações Terrenas | https://www.gov.br/anatel/pt-br/regulado/satelite/licenciamento-de-estacoes-terrenas | Anatel | 官方办理页面 HTML | 是 | 发射型地球站、纯接收 FSS 站和系统入口 | 可访问 | 可提取正文 | 不需人工 | 已保存快照并纳入月度监控；source_id: `br-anatel-earth-station-licensing`。 |
| 18 | Certificação de Produtos | https://www.gov.br/anatel/pt-br/regulado/certificacao-de-produtos | Anatel | 官方办理入口 HTML | 是 | 产品认证和 homologation | 可访问 | 可提取正文 | 不需人工 | 已保存快照并纳入月度监控；source_id: `br-anatel-product-certification`。 |
| 19 | Organismos de Certificação Designados（OCD） | https://www.gov.br/anatel/pt-br/regulado/certificacao-de-produtos/ocds | Anatel | 官方机构名单 HTML | 是 | OCD 角色、名单和 scope | 可访问 | 可提取正文 | 不需人工 | 已保存快照并纳入月度监控；source_id: `br-anatel-ocd-list`。 |

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
11. `br-act-9526-2021`
12. `br-anatel-satellite-rights-page`
13. `br-anatel-satellite-rights-manual-2023`
14. `br-anatel-collective-services`
15. `br-anatel-earth-station-licensing`
16. `br-anatel-product-certification`
17. `br-anatel-ocd-list`

## 4. 仍需人工确认的来源

- 当前没有尚未确认来源身份的核心法规。各来源的法律翻译、合并文本现行性和具体项目适用范围仍需巴西律师或 Anatel 书面确认。

## 5. 仍不足的模块

1. D2D、IoT、用户终端直连等新业务的现行服务分类和频率路径；
2. 各类用户终端的批量许可、站点许可豁免或简化条件；
3. 地球站和用户设备的项目级费用计算；
4. Anatel 对当前项目的实际审批顺序和总周期；
5. 2025-2027 年服务规则过渡条款的逐条生效状态。

## 6. 下一步建议

1. 使用复核后的 `01-10` 文件和 source notes 生成回答，不再直接依据原始 Spacesail 报告下结论；
2. 每月检查新增的 Anatel 办理页面；PDF 指南换版通过其上游办理页发现；
3. 项目启动前向 Anatel 或当地律师确认具体服务分类、终端许可方式、费用和审批周期。
