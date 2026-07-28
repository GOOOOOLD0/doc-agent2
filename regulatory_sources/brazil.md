# Brazil - satellite landing rights regulatory source register

Source document: `Report_Spacesail_EN.docx`

Last URL review: 2026-07-26

Purpose: this file is the first maintainable source register for Brazil. Each item should have one monitorable official URL, a fixed capture method, and a mapping to the landing-permit workflow step it affects.

## Monitoring rule

- Frequency: monthly.
- Preferred source: official Anatel legislation HTML pages, because they expose consolidated text and a visible "Ultima atualizacao" field.
- Capture method for `html`: download the page HTML, extract the main legal text plus publication/update metadata, normalize whitespace, then compare with the previously saved normalized text.
- Capture method for `pdf` or `word`: download the file, extract text, store both the original file and normalized text, then compare normalized text.
- Capture method `archive_only`: keep the official URL for traceability, but do not include it in the monthly monitoring queue unless it becomes relevant again.
- If unchanged: append a check log entry with `status: no update`.
- If changed: save the new snapshot and append a check log entry with `status: updated` and a short diff summary.

Suggested local storage convention:

```text
wiki/raw/landing_rights/brazil/sources/<source_id>/snapshots/YYYY-MM-DD/original.html
wiki/raw/landing_rights/brazil/sources/<source_id>/snapshots/YYYY-MM-DD/normalized.txt
wiki/raw/landing_rights/brazil/sources/<source_id>/checks.md
```

## Process map from the existing Brazil report

1. Foreign Satellite Exploitation Rights / landing rights.
2. Authorization for provision of telecommunications services to end users.
3. Equipment certification and approval.
4. Station licensing.
5. Fee and tax compliance.

## Source register

| Source ID | Norm | Authority | Official URL | Source format | Capture method | Process step | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| br-law-9472-1997 | Law No. 9,472/1997, General Telecommunications Law (LGT) | Anatel / Brazil Federal Government | https://informacoes.anatel.gov.br/legislacao/leis/2-lei-9472 | html | anatel_html | Landing rights; service authorization; spectrum/orbit powers | url-confirmed | Anatel consolidated legislation page. The page links to Planalto and DOU references. |
| br-res-748-2021 | Resolution No. 748/2021, General Regulation for the Exploitation of Satellites | Anatel | https://informacoes.anatel.gov.br/legislacao/resolucoes/2021/1595-resolucao-748 | html | anatel_html | Landing rights; satellite exploitation framework | url-confirmed | Core regulation for Brazilian and foreign satellite exploitation. |
| br-act-9523-2021 | Act No. 9,523/2021, technical and operational requirements for satellite communication systems | Anatel | https://informacoes.anatel.gov.br/legislacao/atos-de-requisitos-tecnicos-de-gestao-do-espectro/2021/1598-ato-9523 | html | anatel_html | Technical system requirements; frequency coordination support | url-confirmed | The Anatel page showed updates through 2025 in the reviewed version, so this should be actively monitored. |
| br-act-9426-2021 | Act No. 9,426/2021, coexistence parameters between terrestrial and satellite stations | Anatel | https://informacoes.anatel.gov.br/legislacao/atos-de-requisitos-tecnicos-de-gestao-do-espectro/2021/1597-ato-9426 | html | anatel_html | Coexistence / interference; frequency coordination | url-confirmed | Relevant to C-band coexistence between terrestrial stations and fixed-satellite earth stations. |
| br-act-9526-2021 | Act No. 9,526/2021, requirements for obtaining the right to exploit satellites | Anatel | https://sei.anatel.gov.br/sei/publicacoes/controlador_publicacoes.php?acao=publicacao_visualizar&id_documento=8580171&id_orgao_publicacao=0 | html | generic_html | Landing rights application requirements | url-confirmed | Official Anatel SEI publication page confirmed and added to monthly monitoring. |
| br-anatel-satellite-rights-page | Conferência de Direito de Exploração de Satélite | Anatel | https://www.gov.br/anatel/pt-br/regulado/satelite/conferencia-de-direito-de-exploracao-de-satelite | html | generic_html | Landing rights application procedure, documents, term and fees | url-confirmed | Operational page linking the current application instructions and manual; added to monthly monitoring. |
| br-anatel-satellite-rights-manual-2023 | Manual para Solicitação de Direito de Exploração de Satélite, version 02 | Anatel | https://sistemas.anatel.gov.br/anexar-api/publico/anexos/download/e6517bea2f08bd17539dc2d5a0a04793 | pdf | pdf_direct | SEI filing procedure and technical application fields | url-confirmed-reference-copy | Saved locally. Direct PDF monitoring is disabled because the current monitor handles HTML; replacement is tracked through the upstream satellite-rights page. |
| br-anatel-collective-services | Serviços de Interesse Coletivo | Anatel | https://www.gov.br/anatel/pt-br/regulado/outorga/servicos-de-interesse-coletivo | html | generic_html | Collective telecommunications service authorization | url-confirmed | Current application documents, Mosaico process and post-authorization notice; added to monthly monitoring. |
| br-anatel-earth-station-licensing | Licenciamento de Estações Terrenas | Anatel | https://www.gov.br/anatel/pt-br/regulado/satelite/licenciamento-de-estacoes-terrenas | html | generic_html | Earth station licensing and licensing-system access | url-confirmed | Operational guidance for transmitting and receive-only earth stations; added to monthly monitoring. |
| br-anatel-product-certification | Certificação de Produtos | Anatel | https://www.gov.br/anatel/pt-br/regulado/certificacao-de-produtos | html | generic_html | Product certification and Anatel homologation | url-confirmed | Added to monthly monitoring. The initial local baseline used a browser fallback after repeated curl timeouts; future failures are recorded for manual follow-up. |
| br-anatel-ocd-list | Organismos de Certificação Designados | Anatel | https://www.gov.br/anatel/pt-br/regulado/certificacao-de-produtos/ocds | html | generic_html | Designated certification bodies and certification scopes | url-confirmed | Added to monthly monitoring because the list and scopes can change. The initial local baseline used a browser fallback after repeated curl timeouts. |
| br-law-5070-1966 | Law No. 5,070/1966, FISTEL Law | Anatel / Brazil Federal Government | https://informacoes.anatel.gov.br/legislacao/leis/474-lei-5070 | html | anatel_html | Fees: TFI and TFF | url-confirmed | Governs telecom inspection fund fees; relevant to station licensing costs. |
| br-res-715-2019 | Resolution No. 715/2019, conformity assessment and homologation of telecom products | Anatel | https://informacoes.anatel.gov.br/legislacao/resolucoes/2019/1350-resolucao-715 | html | anatel_html | Equipment certification and approval | url-confirmed | Core certification/homologation regulation for telecom products. |
| br-res-719-2020 | Resolution No. 719/2020, General Licensing Regulation (RGL) | Anatel | https://informacoes.anatel.gov.br/legislacao/resolucoes/2020/1381-resolucao-719 | html | anatel_html | Station licensing | url-confirmed | Governs licensing of telecommunications stations. |
| br-res-720-2020 | Resolution No. 720/2020, General Regulation of Grants (RGO) | Anatel | https://informacoes.anatel.gov.br/legislacao/resolucoes/2020/1382-resolucao-720 | html | anatel_html | Service authorization; transfer and extinction of authorizations | url-confirmed | Current general framework for Anatel service grants/outorgas. |
| br-res-777-2025 | Resolution No. 777/2025, General Regulation of Telecommunications Services (RGST) | Anatel | https://informacoes.anatel.gov.br/legislacao/resolucoes/2025/2022-resolucao-777 | html | anatel_html | Service authorization and service-specific rules for SMP, SCM, and SMGS | url-confirmed | Current key service rule. It revokes Resolution 477/2007 and Resolution 614/2013, approves RGST, includes SMP and SCM definitions, and includes SMGS transition provisions. |
| br-res-477-2007 | Resolution No. 477/2007, former SMP regulation | Anatel | https://informacoes.anatel.gov.br/legislacao/resolucoes/2007/9-resolucao-477 | html | archive_only | Historical SMP reference | historical-revoked | Revoked by Resolution 777/2025. Keep for traceability only; do not use as current basis. |
| br-res-614-2013 | Resolution No. 614/2013, former SCM regulation | Anatel | https://informacoes.anatel.gov.br/legislacao/resolucoes/2013/465-resolucao-614 | html | archive_only | Historical SCM reference | historical-revoked | Revoked by Resolution 777/2025. Keep for traceability only; do not use as current basis. |
| br-portaria-560-1997 | Portaria No. 560/1997, Norma No. 16/97 for non-geostationary SMGS | Ministry of Communications / Anatel legislation portal | https://informacoes.anatel.gov.br/legislacao/normas-do-mc/185-portaria-560 | html | anatel_html | SMGS historical / transition source | transitional | Resolution 777/2025 states this norm will be substituted after the transition period specified there. Monitor alongside Resolution 777/2025 while SMGS transition remains relevant. |

## Workflow requirements extracted from the report

### 1. Foreign Satellite Exploitation Rights

- Create or appoint a Brazilian legal entity to represent the foreign satellite operator.
- Register the Brazilian entity with CNPJ.
- Appoint the legal representative before Anatel.
- Prepare corporate, tax, technical, financial, and regulatory declarations.
- Provide simplified technical design of the satellite communication system.
- Provide home-country filing evidence with sworn translation.
- Provide frequency coordination agreements or evidence of coordination efforts.
- Identify the entity responsible for FISTEL fee payment.
- Prepare satellite system details: system name, orbital position, number of satellites, ITU filings, launch and start-of-operation dates in Brazil, orbital control accuracy, gateways, coverage, frequency bands, TT&C stations, and orbital parameters.

Primary sources to monitor:

- `br-law-9472-1997`
- `br-res-748-2021`
- `br-act-9523-2021`
- `br-act-9426-2021`
- `br-act-9526-2021`
- `br-anatel-satellite-rights-page`

### 2. Authorization To Provide Services To End Users

- Create or appoint a Brazilian service provider entity.
- Register with CNPJ.
- Choose applicable service authorization: SCM, SMGS, SMP, or another applicable category.
- Prepare corporate documents, suitability declarations, technical/economic/tax declarations, and declaration on other collective service authorizations.
- Confirm whether small-provider treatment is available.

Primary sources to monitor:

- `br-law-9472-1997`
- `br-res-748-2021`
- `br-res-720-2020`
- `br-res-777-2025`
- `br-anatel-collective-services`

Historical / transitional references:

- `br-res-477-2007` for legacy SMP reports only.
- `br-res-614-2013` for legacy SCM reports only.
- `br-portaria-560-1997` for SMGS transition context.

### 3. Equipment Certification And Approval

- Identify all network, user-terminal, gateway, and station equipment requiring Anatel homologation.
- Use an Anatel-designated certification body (OCD).
- Collect technical documents and test reports required under the conformity assessment framework.

Primary sources to monitor:

- `br-res-715-2019`
- `br-anatel-product-certification`
- `br-anatel-ocd-list`

### 4. Station Licensing

- Register stations in Anatel systems.
- Submit licensing requests through the electronic system.
- Determine whether licensing is individual or block-based.
- Confirm whether non-geostationary systems can be licensed by system.
- Confirm fee treatment when one station supports multiple services.

Primary sources to monitor:

- `br-res-719-2020`
- `br-law-5070-1966`
- `br-anatel-earth-station-licensing`

## Open items for the next pass

- Add source URLs for the electronic systems used in practice, such as station registration/licensing portals and Anatel procedural guidance pages.
- Decide whether to monitor Anatel consolidated HTML pages only, or also monitor DOU/Planalto publication pages as secondary sources.
