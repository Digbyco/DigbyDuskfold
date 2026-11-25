# Digby House website: build report (25 November 2026)

**Status: built and tested; not published.** No DNS records, hosting settings or email settings have been touched. Publication needs the founder's approval and the items in §5.

## 1. What was built

- **Pages (10):**
  - Home (`/`)
  - Our Products (`/products/`); the menu leads straight to Duskfold
  - Duskfold (`/products/duskfold/`)
  - About (`/about/`)
  - Contact (`/contact/`)
  - Privacy (`/privacy/`)
  - Legal information (`/legal/`)
  - Duskfold Terms (`/terms/`)
  - Product support (`/support/`)
  - Page not found (`404.html`)
- **Technology:** plain HTML and CSS. No scripts, frameworks, database, cookies, analytics or third-party requests. Fonts (Newsreader and Inter, SIL Open Font License) are self-hosted, with their licences in `assets/fonts/`.
- **Separation from Duskfold:** this repository (`DigbyDuskfold`) is separate from the app. The site has no connection to Duskfold's database, AI or deployment. The app's code was not changed; screenshots were taken from it, read-only.
- **Reserved addresses kept:** `/privacy`, `/terms` and `/support`, recorded for the app in D-148, all exist. Until Duskfold launches they carry holding statements, not the draft Duskfold policies.
- **Palette and type:**
  - Warm ivory and forest green alternate in roughly equal measure.
  - Clay is used for rules and accents. Slate is used only in a darkened form for small text, so that it passes contrast.
  - Duskfold appears in its own midnight navy and gold, only in its product panels.
  - Type: Newsreader (an editorial serif, also used in the app) stands in for Canela; Inter is used for small labels.
- **Imagery:**
  - Five genuine Duskfold screens (Home, Unload, Sort, Let it drift, Rest), captured from the current app with fictional, non-sensitive entries.
  - Developer-only labels were hidden in the captures.
  - The Reflect stage has no screenshot: an example reflection would have to be invented, and could be mistaken for real AI output.
  - The Duskfold mark is drawn from the app's own vector.
- **Future products:** add one page folder and one card (see the README); no redesign is needed.

## 2. Screenshots

Desktop (1440 px wide) and mobile (390 px wide) full-page screenshots of all 10 pages were supplied with this report. In the preview:

- orange dashed outlines mark interim copy;
- blue dashed outlines mark missing assets.

## 3. Asset and hosting size

| Item                                      | Size                       |
| ----------------------------------------- | -------------------------- |
| Fonts (5 WOFF2 files, Latin subset)       | 87 KB                      |
| App screenshots (5 screens × 2 sizes, WebP) | 568 KB                     |
| HTML, CSS, icons, sharing image, sitemap  | about 110 KB               |
| **Total upload**                          | **764 KB (0.75% of 100 MB)** |

Opening the home page downloads under 100 KB before scrolling (measured: 45 KB on desktop, 81 KB on a phone); images further down load only when scrolled to.

## 4. Accessibility and functional testing

All checks were run on the built site with Chromium (Playwright).

| Check                                                         | Result                                                                              |
| ------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| axe-core 4.10 (WCAG A/AA rules), desktop and mobile, all pages  | **0 violations**                                                                    |
| Keyboard: Tab through each page (skip link, menu, links, buttons) | Every stop reachable, with a visible focus ring                                     |
| Horizontal overflow at 1440, 390 and 360 px                   | None                                                                                |
| Requests to other sites                                       | None                                                                                |
| Console errors                                                | None                                                                                |
| Internal links, images, `srcset` files and fonts              | All resolve (`tools/check.py`)                                                      |
| One `h1` per page, `lang="en-GB"`, title and description on every page | Yes                                                                                 |
| Folder preview opened from disk                               | All 8 linked pages, every image and font load                                       |
| Colour contrast                                               | Body text: charcoal on ivory and ivory on forest, both well above 4.5:1 (checked by axe) |

**Not tested here:**

- Safari and real iPhones and Android phones (the founder's check);
- the live server's behaviour (HTTPS, `.htaccess` and headers), until it is uploaded.

## 5. Outstanding before publication

### A. Inputs that did not arrive with the brief

| #   | Item                                                                                                                                                                        | Where it goes                                                       |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| A1  | **Digby brand board** (master logo, publisher's mark, brand device, favicon): vector or high-resolution files. The repository holds only the Duskfold brand board (`brand_board_v1.webp`). | Home logo (large), header, footer, favicon, sharing image            |
| A2  | **Founder-agreed website copy**                                                                                                                                             | Every passage marked "Draft copy" (25 marked passages across the pages)                     |
| A3  | **Approved black-and-white founder portrait**                                                                                                                               | About                                                               |
| A4  | **Early-access link:** the live MailerLite landing-page URL. MailerLite's landing-page list could not be read from here.                                                    | Duskfold page button (currently inactive)                           |
| A5  | The brand board's descriptions of **Timeless, Trusted, Thoughtful**, if it has them                                                                                         | Home and About                                                      |

Until A1–A3 arrive, the site uses an interim typographic "DIGBY" wordmark and a "D" favicon. No logo has been invented. `tools/check.py --release` refuses to pass until every marker is resolved.

### B. Facts to confirm

- **Place of registration** ("England and Wales" is shown and marked): confirm on Companies House. The Companies Act trading-disclosure rules require it on the website.
- **OVHcloud** retention of web server logs, and your retention period for enquiry emails (privacy notice).
- **Note on the app** (not changed; the app is frozen):
  - the app's Home still shows the earlier four-step ritual card (Unload, Sort, Settle, Fold) and the tagline "Evening tools for a calmer mind";
  - the boat artwork is still marked provisional (O-F1).
  - These are visible in the screenshots. Decide whether that's acceptable for the website.

### C. Legal and privacy status

| Document                                                                                                | Status                                                                                                                                                                                                                                                                                               | On the website                                                                                                                       |
| ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Duskfold Privacy Policy, Terms of Use and Support (`duskfold/docs/review/public-pages.md`)              | Final texts prepared (D-143), **not legally approved**. Open items include the OpenAI transfer wording, lawful bases, deletion-record retention, the liability clause and the licence agreement. Founder self-review route approved in principle (D-155), not completed. Legal gate D-129 open. | **Not published.** Holding statements at `/privacy`, `/terms` and `/support`. They go live when Duskfold does.                       |
| Safety and urgent-help wording (`safetyCopy.ts`, D-142)                                                 | Founder-approved; **independent clinical review outstanding** (D-40 gate closed).                                                                                                                                                                                                                    | **Not published.** Contact and Support carry only a short "not an emergency service; call 999" statement, marked draft for your approval. |
| **Website privacy notice** (new)                                                                        | Drafted from the real set-up: static OVHcloud hosting, no cookies or analytics, OVHcloud Zimbra email in European datacentres (D-159). Four `[OUTSTANDING]` facts.                                                                                                                                   | `/privacy`, marked draft                                                                                                             |
| **Website terms and company information** (new)                                                         | Short, standard terms; statutory company details.                                                                                                                                                                                                                                                   | `/legal`, marked draft                                                                                                               |
| MailerLite early-access                                                                                 | The sign-up page's own notice and consent wording are outside this repository.                                                                                                                                                                                                                      | Privacy section left `[OUTSTANDING]` until the link is confirmed                                                                     |

**ICO fee:** reassess before live customer data or public launch (D-155). The website alone processes only enquiry emails and server logs.

All Duskfold release gates are unchanged.

## 6. Uploading to OVHcloud without affecting email

**Before anything else (protects email):**

1. In the OVHcloud Control Panel, open **Web Cloud → Domain names → digbyhouse.co.uk → DNS zone**.
2. Screenshot or note every **MX**, **SPF/TXT**, **CNAME** (autodiscover, DKIM) and **SRV** record. These carry your Zimbra email.
3. Do not edit or delete any of them.

**Check the free hosting:**

1. Open **Web Cloud → Hosting plans**.
2. Confirm the free 100 MB plan shows as active for digbyhouse.co.uk. OVHcloud's guide says it requires the domain to have no MX Plan attached. Your email is Zimbra (D-160), so this should be fine.
3. If activating the plan changed the DNS zone, compare the MX records with your notes before doing anything else. If they differ, stop and contact OVHcloud support.

**Upload (FTP):**

1. Use the FTP details from OVHcloud's activation email, or **Hosting plans → FTP-SSH**.
2. Install **FileZilla** (free). Connect with host, user, password and port 21. Choose "Require explicit FTP over TLS" if offered.
3. Open the **`www`** folder on the right-hand side.
4. Delete only the placeholder page OVHcloud put there (usually `index.html`).
5. Upload **the contents of `site/`**, not the folder itself, including the hidden `.htaccess` file. In FileZilla: Server → Force showing hidden files.
6. Visit http://www.digbyhouse.co.uk and check each page.

**HTTPS:**

1. In **Hosting plans → General information**, check the **SSL certificate** status. If it's inactive, enable the free **Let's Encrypt** certificate for both `digbyhouse.co.uk` and `www.digbyhouse.co.uk` (under **Multisite**, tick SSL for each).
2. It can take a few hours. OVHcloud notes the domain must already point to the hosting.
3. Once https://www.digbyhouse.co.uk loads with a padlock, edit `.htaccess`: remove the `#` from the four lines under "STEP 2". Re-upload it.
4. Check that http:// and digbyhouse.co.uk both redirect to https://www.digbyhouse.co.uk. If the site shows an error, re-upload the original `.htaccess`.

**Afterwards:**

1. Send yourself a test email to and from hello@digbyhouse.co.uk.
2. Recheck the MX records against your notes.

**Not verified here:** the OVHcloud documentation site was not reachable from this session. Check SSL availability on the free plan, `.htaccess` support and the FTP folder name in the Control Panel. The search results confirm 100 MB, one email account with 5 GB, no database, and FTP details sent by email.

## 7. Checklist before resubmitting Apple Developer enrolment

1. ☐ A1–A5 supplied, draft passages replaced or approved, and `python3 tools/check.py --release` passes.
2. ☐ Website and privacy notice approved by the founder.
3. ☐ Site live at **https://www.digbyhouse.co.uk** with a valid certificate. Every page loads, on a phone too. The plain domain redirects to it.
4. ☐ The site names the legal entity exactly: **Digby House Ltd**, company number 17570148, registered office (it does, on every page).
5. ☐ **D-U-N-S number** registered to exactly "Digby House Ltd" at the registered office. It must match the enrolment form and the website. Allow up to 5 business days from D&B, plus 2 for Apple.
6. ☐ You enrol with a work email at the organisation's domain (hello@digbyhouse.co.uk, or a personal address at digbyhouse.co.uk), and you have authority to bind the company.
7. ☐ Email still works after the website went live (test both directions).
8. ☐ The site says Duskfold is coming soon and is not yet available. It doesn't link to the App Store.
9. ☐ The early-access link works, if it's included.

Apple's guidance: the organisation's website "must be publicly available and functional, and its domain name must be associated with your organization"; the work email must use the organisation's domain; companies need a D‑U‑N‑S number registered to the legal entity.
