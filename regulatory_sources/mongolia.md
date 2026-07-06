# Mongolia - satellite landing rights regulatory source pilot

Last URL review: 2026-07-06

Purpose: this file records the first Mongolia pilot test for extending the Brazil regulatory-monitoring workflow. The goal of this pass is to identify official URLs that are relevant to satellite landing rights and can be downloaded by the monthly monitor.

## Pilot result

- The Communications Regulatory Commission of Mongolia (CRC) site returned HTTP 200 and extractable HTML for the tested licensing, radio-frequency, certification, and legal-catalog pages.
- CRC is the core regulator for telecommunications licensing, radio-frequency use, satellite communications network/service licensing, and equipment conformity/certification.
- Legalinfo.mn returned HTTP 200 and extractable HTML for the tested laws and CRC resolution. Some legalinfo law pages are large, so only the directly satellite-specific frequency-resolution page is enabled for monthly monitoring in this first pilot.
- Seven Mongolia sources are enabled for monthly monitoring. Three larger legalinfo law pages are recorded as confirmed URLs but left `monitor: false` until we decide a snapshot-size policy.

## Monitoring rule for Mongolia

- Prefer CRC pages when they contain the practical application workflow and official links to legalinfo.mn.
- Enable legalinfo.mn monitoring for focused, satellite-specific legal acts first.
- Keep very large legalinfo law pages recorded but unmonitored until the monthly snapshot storage policy is decided.
- Do not monitor CRC document attachments directly until PDF/Word extraction support is added. Monitor the containing CRC HTML pages instead.

## Source register

| Source ID | Source | Authority | Official URL | Source format | Capture method | Process step | Status | Monitor | Notes |
|---|---|---|---|---|---|---|---|---|---|
| mn-crc-license-overview | CRC new license applicant overview | CRC | https://crc.gov.mn/for-new-license-applicants/tusgai-zovsoorol-4 | html | generic_html | License categories for telecom service, radio frequency, satellite network/service, and certification | url-confirmed | true | Official index for new license applicants. |
| mn-crc-satellite-network-license | Satellite communications network establishment, operation and service license page | CRC | https://crc.gov.mn/for-new-license-applicants/tusgai-zovsoorol-4/sansryn-xolboony-sulzee-baiguulax-tuunii-asiglalt-uilcilgee-erxlex-3 | html | generic_html | Satellite landing rights; satellite network/service authorization | url-confirmed | true | Correct slug uses `sulzee`; `suljee` returns 404. |
| mn-crc-radio-frequency-license | Radio frequency and frequency band use special license page | CRC | https://crc.gov.mn/for-new-license-applicants/tusgai-zovsoorol-4/radio-davtamz-asiglax-tusgai-zovsoorol | html | generic_html | Frequency authorization; satellite and satellite mobile radio-frequency application materials | url-confirmed | true | Includes satellite communications and satellite mobile sections, legalinfo links, and CRC document/form links. |
| mn-crc-radio-frequency-overview | CRC radio frequency overview | CRC | https://crc.gov.mn/radio-davtamzh/tanilcuulga-3 | html | generic_html | Spectrum management and public-use radio-frequency authorization context | url-confirmed | true | States public-use radio frequencies are used through CRC permits/rights under Mongolian law. |
| mn-crc-equipment-conformity | CRC conformity certificate application page | CRC | https://crc.gov.mn/for-new-license-applicants/batalgaazuulalt-e/toxirlyn-gercilgee-batalgaazuulalt | html | generic_html | Telecommunications equipment conformity/certification requirements | url-confirmed | true | Lists materials for obtaining and extending conformity certificates. |
| mn-crc-laws-catalog | CRC catalog of Mongolian laws | CRC | https://crc.gov.mn/documents/mongol-ulsyn-xuuliud | html | generic_html | Official legal-source catalog | url-confirmed | true | Links to legalinfo.mn for the Communications Law, Radio Waves Law, Law on Permits, and conformity-assessment law. |
| mn-legal-satellite-frequency-rules | CRC Resolution No. 37/2022 on satellite communication system frequency allocation and technical requirements | Legalinfo.mn / CRC | https://legalinfo.mn/mn/detail?lawId=16531361633621 | html | generic_html | Satellite frequency allocation and technical requirements | url-confirmed | true | Directly linked from the CRC radio-frequency license page. |
| mn-legal-communications-law | Communications Law of Mongolia | Legalinfo.mn | https://legalinfo.mn/mn/detail/523 | html | generic_html | General telecommunications authority and licensing powers | url-confirmed-large-html | false | Confirmed but large. Keep recorded; enable after deciding snapshot-size policy. |
| mn-legal-radio-waves-law | Radio Waves Law of Mongolia | Legalinfo.mn | https://legalinfo.mn/mn/detail/443 | html | generic_html | Radio frequency ownership, allocation, and permit basis | url-confirmed-large-html | false | Confirmed but large. Keep recorded; enable after deciding snapshot-size policy. |
| mn-legal-permits-law | Law on Permits of Mongolia | Legalinfo.mn | https://legalinfo.mn/mn/detail?lawId=16530780109311 | html | generic_html | General permit framework | url-confirmed-large-html | false | Confirmed but very large. Keep recorded; enable after deciding snapshot-size policy. |

## Official attachments observed but not yet monitored directly

These appear inside the CRC HTML pages and should be revisited after PDF/Word extraction support is added:

- Satellite communications radio-frequency station PDF: `https://crc.gov.mn/storage/%D0%A0%D0%B0%D0%B4%D0%B8%D0%BE%20%D0%B4%D0%B0%D0%B2%D1%82%D0%B0%D0%BC%D0%B6/last/%D0%A1%D0%90%D0%9D%D0%A1%D0%A0%D0%AB%D0%9D%20%D0%A5%D0%9E%D0%9B%D0%91%D0%9E%D0%9E%D0%9D%D0%AB%20%D2%AE%D0%99%D0%9B%D0%A7%D0%98%D0%9B%D0%93%D0%AD%D0%AD%D0%9D%D0%94%20%D0%A0%D0%90%D0%94%D0%98%D0%9E%20%D0%94%D0%90%D0%92%D0%A2%D0%90%D0%9C%D0%96,%20%D0%A0%D0%90%D0%94%D0%98%D0%9E%20%D0%94%D0%90%D0%92%D0%A2%D0%90%D0%9C%D0%96%D0%98%D0%99%D0%9D%20%D0%97%D0%A3%D0%A0%D0%92%D0%90%D0%A1%20%D0%90%D0%A8%D0%98%D0%93%D0%9B%D0%90%D0%A5%20%D0%A1%D0%A2%D0%90%D0%9D%D0%A6.pdf`
- Satellite mobile communications radio-frequency station PDF: `https://crc.gov.mn/storage/%D0%A0%D0%B0%D0%B4%D0%B8%D0%BE%20%D0%B4%D0%B0%D0%B2%D1%82%D0%B0%D0%BC%D0%B6/last/%D0%A1%D0%90%D0%9D%D0%A1%D0%A0%D0%AB%D0%9D%20%D0%A5%D3%A8%D0%94%D3%A8%D0%9B%D0%93%D3%A8%D3%A8%D0%9D%D0%A2%20%D0%A5%D0%9E%D0%9B%D0%91%D0%9E%D0%9E%D0%9D%D0%AB%20%D2%AE%D0%99%D0%9B%D0%A7%D0%98%D0%9B%D0%93%D0%AD%D0%AD%D0%9D%D0%94%20%D0%A0%D0%90%D0%94%D0%98%D0%9E%20%D0%94%D0%90%D0%92%D0%A2%D0%90%D0%9C%D0%96,%20%D0%A0%D0%90%D0%94%D0%98%D0%9E%20%D0%94%D0%90%D0%92%D0%A2%D0%90%D0%9C%D0%96%D0%98%D0%99%D0%9D%20%D0%97%D0%A3%D0%A0%D0%92%D0%90%D0%A1%20%D0%90%D0%A8%D0%98%D0%93%D0%9B%D0%90%D0%A5%20%D0%A1%D0%A2%D0%90%D0%9D%D0%A6.pdf`
- Satellite station application XLSX: `https://crc.gov.mn/storage/media/63982082-f9cb-41be-814c-b46d888ab122.xlsx`
- Satellite communications DOCX form: `https://crc.gov.mn/storage/Tusgai%20zowshoorol%20mayatuud/Radio%20dawtamj/radio%20dawtamj/20170123%20%D0%A2%D0%97-3%204%20%D0%A1%D0%B0%D0%BD%D1%81%D1%80%D1%8B%D0%BD%20%D1%85%D0%BE%D0%BB%D0%B1%D0%BE%D0%BE%20Edit.docx`

## Open issues before expanding Mongolia

- Decide whether to enable monthly monitoring for the large legalinfo law pages, or add a text-only law extractor to reduce snapshot size.
- Add PDF/Word extraction support before monitoring CRC attachments directly.
- Map the monitored source set into the answer template: service/network authorization, frequency authorization, equipment certification, application materials, fees, processing authority, and open questions.

## Pilot commands

Run the Mongolia monitoring queue without writing:

```bash
python3 scripts/check_sources.py --source-id mn-crc-license-overview --source-id mn-crc-satellite-network-license --source-id mn-crc-radio-frequency-license --source-id mn-crc-radio-frequency-overview --source-id mn-crc-equipment-conformity --source-id mn-crc-laws-catalog --source-id mn-legal-satellite-frequency-rules --dry-run
```

Run all enabled sources, including Brazil and Mongolia:

```bash
python3 scripts/check_sources.py --dry-run
```
