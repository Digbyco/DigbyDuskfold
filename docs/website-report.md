# Digby House website: final branding and content pass (26 November 2026)

**Status:** built and tested; **not published**. No DNS records, hosting settings or email settings have been touched. Duskfold's app code is unchanged.

## 1. What changed in this pass

### Digby branding

- **Green:** now **#263A31**, a deep heritage green.
  - The brand board's rendered greens measure about #283C31 (app icon, splash screen, quote panel, palette swatch). The board's label "#214C3D" is brighter than what it shows.
  - The footer uses a deeper #1F2F28.
  - Ivory (#F7F4EE) and green still alternate in roughly equal measure.
- **Official artwork,** lifted from the brand board rather than redrawn: each mark is separated from the board's ivory background into a transparent PNG, in green and in ivory (`src/brand/`). It appears as:
  - the **master logo** (ornament, DIGBY, rule), large on the home page (up to 640 px wide);
  - the **wordmark** in the header, and the master logo in ivory in the footer;
  - the **publisher's mark** (DIGBY · D · THOUGHTFULLY MADE seal) with the principles on Home and About;
  - the **favicon and home-screen icon**, from the board's Digby app icon;
  - the **sharing image**, from the master logo.
- **Quality note:** the board is 1536 × 1024 px, so the master logo source is only about 300 px wide. It looks good at normal sizes but slightly soft on high-resolution screens. **The original vector or high-resolution logo files would make it crisp.** This is not a blocker.

### Duskfold imagery: current app, real flow

- **The latest app is the only source.** All five screens were captured from the current implemented app (branch `claude/trusting-cannon-m5bh6b`, commit `edbd637`), walking its real flow: Unload → Sort → Reflect → Let it drift → Rest.
- **Genuine reflection:**
  - The **Reflect** screen shows **genuine Duskfold AI output** recorded in Stage R3 on 24 November (test evening e1-10, fictional).
  - Only the evening's two non-sensitive thoughts are used: a work proposal, and a postponed visit to family. The child-related thoughts were left out.
  - The reflections and the "one thing for tomorrow" suggestion are exactly as recorded.
  - The Unload text is a lightly trimmed excerpt of that test's fictional entry. Sort shows the two thoughts as the app separated them.
  - No AI was called: the browser answered the app's requests with the recorded results. No paid testing.
- **Removed:**
  - the app's Home screen, which still shows the earlier four-step card and the earlier tagline;
  - every earlier description and the "Settle/Fold" names.
  The site now uses only the current five-stage names and approved screen wording.
- **Frames:** iPhone frames are drawn in CSS, so they are crisp at any size and add no image weight.
- **Duskfold mark:** the approved vector from D-144 (`duskfold/assets/images/brand/duskfold-mark.svg`), not the app's provisional traced drawing.

### Content

- **From the brand board** (treated as agreed):
  - the company introduction ("We create simple, meaningful tools that help people understand themselves, build stronger relationships and create lasting change.");
  - the three principles;
  - the tagline;
  - "Good tools don't just solve problems. They change lives."
- **Not used:** the board's earlier Duskfold lines "Evening tools for a calmer mind" and "A calmer end to your day … evidence-informed tools". They are superseded, and "evidence-informed" is an unsupported claim.
- **Everything else** is **proposed copy**, checked against the current app: 22 passages, all in `docs/copy-for-approval.md`.
- **Company details** as confirmed. "Registered in England and Wales" is now stated without a marker: a company number of eight digits with no letter prefix is an England and Wales registration.
- **MailerLite button removed.**
- **Privacy notice:**
  - The open items are now proposals: OVHcloud server logs are described by their purpose; enquiry emails are kept up to two years (your decision); the date fills in automatically when the site is built.
  - The MailerLite section was removed with the button.

## 2. What genuinely prevents publication

1. **Copy approval.** Approve the 22 proposed passages in `docs/copy-for-approval.md`, including the privacy notice and the two-year email retention, or send your agreed copy. Approval is one step: I mark them approved, and `tools/check.py --release` then passes.
2. **Going live.** This needs your approval:
   - upload to the OVHcloud hosting;
   - SSL active;
   - DNS checked so that email is unaffected (§6).

Nothing else blocks the website.

**Would improve it but don't block it:**

- **Original logo files** (vector or high resolution), for crisper logos.
- **The founder photograph.** The About page works without it and shows the publisher's mark in its place. To add the photo, place `founder-portrait.jpg` in `src/brand/` and rebuild; the page switches automatically and shows it in black and white.
- **The live MailerLite link,** if you'd like the early-access button back.

**Files mentioned but not received in this conversation:** the separate logo documents, the founder photograph and the agreed website copy. Only the brand board image arrived.

## 3. Publishing the website now vs releasing Duskfold later

| Requirement                                      | Website now (company site, product "coming soon")                                                        | Duskfold release (later)                                                                        |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Company details (Companies Act trading disclosure) | **Shown on every page**                                                                                  | Same                                                                                            |
| Privacy information                              | **Website notice** (this site and email only): approve the proposed text                                | Duskfold Privacy Policy (`public-pages.md`), with the legal gate D-129 to close                 |
| Terms                                            | Short website terms on `/legal` (proposed)                                                               | Duskfold Terms of Use, with open items (licence agreement, liability, usage-limit changes)      |
| Support page                                     | Holding page at `/support`                                                                               | Full Duskfold support text                                                                      |
| Safety and urgent-help wording                   | **Not published.** Only "not an emergency service; call 999"                                             | Independent clinical review (D-40), which is unchanged                                          |
| Claims                                           | Says "coming soon"; no App Store link; no outcome claims; "designed so that…" for privacy               | App Store listing review; claims verified (D-17)                                                |
| ICO fee                                          | Website alone: enquiry email and server logs                                                             | Reassess before live customer data (D-155)                                                      |
| Cookies and consent                              | None set, so no banner needed                                                                            | n/a                                                                                             |

All Duskfold release gates are unchanged. The website states plainly that Duskfold is not yet available. It does not imply that clinical or legal reviews are complete.

## 4. Testing (all 10 pages; desktop 1440 px, phone 390 px and narrow 360 px)

| Check                                                    | Result                                     |
| -------------------------------------------------------- | ------------------------------------------ |
| axe-core 4.10 accessibility rules                        | **0 violations**                           |
| Keyboard Tab order, visible focus ring at every stop     | Pass                                       |
| Horizontal overflow                                      | None                                       |
| Every image loads (after scrolling)                      | Pass                                       |
| Requests to other websites; console errors               | None; none                                 |
| Internal links, files, titles, descriptions, one h1, `lang` | Pass (`tools/check.py`)                  |
| Folder preview opened from disk                          | All linked pages, images and fonts load    |

**Not tested:**

- Safari or real phones (your check);
- the live server (HTTPS, `.htaccess`), until upload.

## 5. Size

- **Total upload:** 1.1 MB, about 1% of the 100 MB allowance. Fonts 87 KB; screenshots 700 KB; brand artwork about 240 KB; the rest under 60 KB.
- No scripts, no frameworks and no third-party requests.

## 6. Uploading to OVHcloud without affecting email

The upload steps are unchanged from the 25 November report.

1. **Protect email first.** In the Control Panel, open Domain names → digbyhouse.co.uk → DNS zone. Note every MX, TXT, CNAME and SRV record, and change none of them.
2. **Check the hosting.** Confirm the free 100 MB plan is active on the domain. If its activation altered the DNS zone, compare the MX records with your notes, and stop if they differ.
3. **Upload.** Using FileZilla with the hosting's FTP details:
   - upload the **contents** of `site/` into `www`, including the hidden `.htaccess`;
   - remove OVHcloud's placeholder page.
4. **HTTPS.**
   - Enable Let's Encrypt SSL for `digbyhouse.co.uk` and `www.digbyhouse.co.uk`.
   - Once the padlock shows, remove the `#` from the four "STEP 2" lines in `.htaccess` and re-upload it.
5. **Test.** Check every page on a phone. Send email both ways. Recheck the MX records.

## 7. Before resubmitting Apple Developer enrolment

1. ☐ Copy approved, and `python3 tools/check.py --release` passes.
2. ☐ Site live at https://www.digbyhouse.co.uk, with the plain domain redirecting to it.
3. ☐ The legal name on the site, "Digby House Ltd", matches the D‑U‑N‑S record and the enrolment form exactly.
4. ☐ You enrol with an email address at digbyhouse.co.uk, with authority to bind the company.
5. ☐ Email still works.
6. ☐ The site says Duskfold is coming soon, with no App Store link.
