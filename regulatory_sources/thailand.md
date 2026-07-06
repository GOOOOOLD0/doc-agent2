# Thailand - satellite landing rights regulatory source pilot

Last URL review: 2026-07-06

Purpose: this file records the first Thailand pilot test for reusing the Brazil monitoring workflow. The goal of this pass is not to declare the Thailand source set complete. It is to identify which official sites can be downloaded by the monitor, which official sites block scripted access, and what must be fixed before Thailand can join the monthly queue.

## Pilot result

- NBTC is the likely core regulator for telecommunications, spectrum, licensing, and satellite-related landing-rights issues, but the tested NBTC pages returned Cloudflare challenge HTML without `--fail` and HTTP 403 in the monitor.
- Royal Gazette is the official publication source for laws and notices, but the tested portal URL also returned Cloudflare challenge HTML without `--fail` and HTTP 403 in the monitor.
- MDES `/law` returned extractable HTML and can be used to test generic HTML capture, but it is a broad auxiliary law catalog and is not yet a confirmed satellite landing-rights source.
- No Thailand source is enabled for monthly monitoring yet. All Thailand entries in `sources.json` have `monitor: false` until stable, specific official URLs are verified.

## Monitoring rule for Thailand

- Do not save Cloudflare challenge pages as regulatory snapshots.
- Prefer stable official document URLs over general portal URLs.
- For NBTC and Royal Gazette, try to identify direct PDF, attachment, API, or document-detail URLs before enabling monthly monitoring.
- Use `generic_html` only for pages where the legal text is present in the downloaded HTML.
- Keep blocked official pages in the register as source-discovery evidence, but leave `monitor: false`.

## Source register

| Source ID | Source | Authority | Official URL | Source format | Capture method | Process step | Status | Monitor | Notes |
|---|---|---|---|---|---|---|---|---|---|
| th-nbtc-portal | NBTC official portal | NBTC | https://www.nbtc.go.th/ | html | generic_html | Regulator source discovery for satellite landing rights, service authorization, spectrum and licensing | access-blocked-cloudflare | false | Returned Cloudflare challenge HTML without `--fail`; monitor records HTTP 403. |
| th-nbtc-telecom-business | NBTC telecommunications business section | NBTC | https://www.nbtc.go.th/Business/commu/telecom.aspx | html | generic_html | Service authorization and telecommunications licensing source discovery | access-blocked-cloudflare | false | Returned Cloudflare challenge HTML without `--fail`; monitor records HTTP 403. |
| th-ratchakitcha-portal | Royal Gazette official portal | Royal Gazette / Secretariat of the Cabinet | https://ratchakitcha.soc.go.th/ | html | generic_html | Official publication source discovery for laws, regulations and NBTC notifications | access-blocked-cloudflare | false | Portal returned Cloudflare challenge HTML without `--fail`; monitor records HTTP 403. Direct PDF URLs may still be usable if discovered separately. |
| th-mdes-law-catalog | MDES law catalog | MDES | https://www.mdes.go.th/law | html | generic_html | Auxiliary legal-source discovery | access-confirmed-non-core | false | Downloaded successfully, but not yet mapped to a satellite landing-rights requirement. |

## Open issues before monthly monitoring

- Find specific NBTC rules or notifications for foreign satellite access, satellite network/channel use, telecommunications service licensing, station licensing, and equipment approval.
- Verify whether NBTC offers direct downloadable PDFs or attachment URLs that bypass the Cloudflare challenge.
- Find Royal Gazette direct PDF URLs for the controlling laws and NBTC notifications.
- Add PDF/Word extraction support if the stable official Thailand sources are documents rather than HTML pages.
- Decide whether the MDES law catalog has any confirmed source value for satellite landing-rights workflow, or should remain discovery-only.

## Pilot commands

Run the accessible generic HTML probe:

```bash
python3 scripts/check_sources.py --source-id th-mdes-law-catalog --include-unmonitored --dry-run
```

Run the blocked-source probe without failing the shell:

```bash
python3 scripts/check_sources.py --source-id th-nbtc-portal --include-unmonitored --dry-run --allow-errors
```
