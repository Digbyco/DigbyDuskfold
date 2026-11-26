# Digby House website: final amendments (26 November 2026)

**Status:** ready to publish once the two remaining approvals below are given. **Not published.** No DNS, hosting or email settings have been touched; the Duskfold app is unchanged.

## 1. Done in this package

- **Copy:** your copy is used exactly on Home, About and the Duskfold page, and in the Contact and Our Products lines.
  - The quote "Good tools don't just solve problems…" is removed.
  - The product heading, the screenshots, the navigation and the three principles are kept.
- **Founder:** the introduction and role ("Founder of Digby House Ltd") are shown beside the Digby publisher's seal. There is no photograph; that requirement is withdrawn.
- **Mobile footer:**
  - the two link lists sit side by side, with the brand and company details across the width;
  - the spacing is reduced throughout;
  - every link still has a comfortable tap area.
- **App Store spots (four), controlled by one setting** in `src/site-config.json`. The spots are:
  - the homepage Duskfold feature;
  - the top of the Duskfold page;
  - the bottom of the Duskfold page ("Make a little space for yourself.");
  - the products card.

  Before launch they show "Coming soon to the App Store", with no inactive buttons. At launch, setting the listing URL and adding Apple's official badge switches all four, and the page descriptions, at once. This was tested in a throwaway copy: the build refuses a missing or non-App-Store URL and a missing badge. Activation is now step 9a of Duskfold's release checklist.
- **Caching:** every image, font and stylesheet address now carries a content fingerprint, so an updated file is fetched immediately despite the cache rules in `.htaccess`. Pages are never cached.
- **Unchanged:** the #263A31 green, the ivory, the typography, the layout, and the Duskfold presentation.

## 2. Screenshot confirmation

- **Current app:** all five screens were captured from app commit `edbd637`. Since then, no app code, server code or assets have changed; only a checklist document has.
- **Fictional content only:** the Unload entry and the two sorted thoughts come from the fictional test evening e1-10. The two reflections are genuine Duskfold output from that test.
- **Disclosures kept:** "Screens from the Duskfold app, shown with a fictional entry" and "These reflections are genuine Duskfold output from a test evening written with fictional content".

## 3. Product descriptions against the current app: two to flag

The app has not been changed. Everything else in your Duskfold copy matches the app:

- the separate thoughts in Sort;
- a reflection on each chosen thought, plus one optional small step for tomorrow;
- the boats drifting across the water;
- the optional short meditation in Rest;
- the journal kept on the device;
- 18 and over.

1. **"Write or speak freely" (01 Unload).**
   - Speech input is built into the app (on-device recognition, D-127), but it has **not yet been verified on a real iPhone**. That is checklist §6, a launch requirement.
   - The wording is accurate if that verification passes before launch. If speech were dropped, the line would need to change.
2. **"When you choose to use AI…" (privacy section).**
   - In the app, agreeing to AI processing is a condition of beginning new evenings. Without it, you can read earlier evenings but can't start a new one.
   - So AI is a one-time choice to use Duskfold, not a per-use option. "When you use Duskfold's AI features" or "When you agree to AI processing" would match the app exactly.
   - Your decision; the text is unchanged.

## 4. Remaining approvals (short list)

| #   | Item                                                                                                                                                                                                                                                                                                                                                                                            | Blocks publication?                                       |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| 1   | **Website privacy notice** (`/privacy`, in `copy-for-approval.md`), including the **proposed 12 months' retention** for ordinary enquiry emails after the conversation closes. It is kept longer only for a complaint, legal claim or legal obligation.                                                                                                                                        | **Yes:** approve or amend                                 |
| 2   | **Website terms** (`/legal`, five short points)                                                                                                                                                                                                                                                                                                                                                 | **Yes:** approve or amend                                 |
| 3   | **Jurisdiction:** the site says "registered in England and Wales". The company number's format supports this (eight digits, no SC/NI prefix), but Companies House could not be reached from here. Open find-and-update.company-information.service.gov.uk/company/17570148 and confirm the registered office and "England/Wales". | Ten-second check, before upload                           |
| 4   | Official Digby logo files, when available                                                                                                                                                                                                                                                                                                                                                      | No: drop them into `src/brand/` with the same names       |

**What the privacy review established:**

| Point                     | Finding                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Email                     | OVHcloud email in European datacentres: confirmed from OVHcloud's own documents (D-159).                                                                                                                                                                                                                                                                                                                                     |
| Hosting logs              | OVHcloud publishes **no fixed retention period** for web hosting logs, so the notice states none and doesn't claim one. If you'd like a period stated, ask OVHcloud support and add it.                                                                                                                                                                                                                                      |
| Lawful bases              | Hosting and security logs, and replying to enquiries: **legitimate interests** (UK GDPR Art. 6(1)(f)).                                                                                                                                                                                                                                                                                                                      |
| Rights                    | Access, rectification, erasure, restriction and objection, plus portability "in some circumstances". A one-month response. The ICO complaint route (website and helpline) is stated without asking people to come to us first.                                                                                                                                                                                             |
| No cookies or tracking    | Verified in this build: no scripts, and **0 cookies and 0 browser storage** after visiting every page at all three widths; no third-party requests. The live server's response headers can only be checked after upload (§6, step 6).                                                                                                                                                                                      |
| No unverified claims      | No "anonymous" description of app accounts, and no AI-provider retention claims. No legal or regulatory clearance is claimed. The urgent-support limitation stays on Contact and Support.                                                                                                                                                                                                                                   |

## 5. Testing (all 10 pages; desktop 1440 px, phone 390 px and narrow 360 px)

- **Accessibility:** axe-core reports **0 violations**. Keyboard focus is visible at every stop.
- **Layout and loading:** no horizontal overflow; every image loads.
- **Privacy:** no external requests, no console errors, no cookies, no storage.
- **Links and pages:** all internal links and files resolve. Each page has a title, a description and a single main heading.
- **Folder preview:** opens from disk with every linked page, image and font.
- **Size:** 1.15 MB in total, about 1.1% of the 100 MB allowance.

## 6. Publication steps (after approval)

**1. Protect email first**

1. OVHcloud Control Panel → **Web Cloud → Domain names → digbyhouse.co.uk → DNS zone**.
2. Screenshot the whole zone. Note especially every **MX** record (where mail is delivered), **TXT** records containing `v=spf1` or DKIM keys, and any **CNAME** or **SRV** records for autodiscover or mail.
3. **Change none of them.**

**2. Check the hosting**

1. **Web Cloud → Hosting plans:** confirm the free 100 MB plan is active for digbyhouse.co.uk.
2. If activating it changed the DNS zone, compare the MX and TXT records with your screenshot. If they differ, stop and contact OVHcloud support before going further.

**3. Upload**

1. Get the FTP details from the activation email, or from **Hosting plans → FTP-SSH**.
2. In **FileZilla**: File → Site Manager. Enter the host, port 21, encryption "Require explicit FTP over TLS", and your username and password.
3. Turn on Server → **Force showing hidden files**, so `.htaccess` uploads too.
4. Open the **`www`** folder on the right. Delete only OVHcloud's placeholder page.
5. Drag in the **contents** of the `site/` folder, not the folder itself.

**4. Turn on HTTPS**

1. **Hosting plans → General information → SSL certificate**: if it isn't active, order the free **Let's Encrypt** certificate.
2. Under **Multisite**, make sure both `digbyhouse.co.uk` and `www.digbyhouse.co.uk` are listed with **SSL enabled**.
3. Allow a few hours. It needs the domain to point to the hosting already.
4. When **https://www.digbyhouse.co.uk** shows a padlock, open `.htaccess` in a text editor and remove the `#` from the four lines under "STEP 2". Save and re-upload it.
5. Check that `http://digbyhouse.co.uk` and `http://www.digbyhouse.co.uk` both end up at **https://www.digbyhouse.co.uk**. If anything shows an error, re-upload the original `.htaccess`.

**5. Test the site**

On your phone and computer, open every page. Check the menu, the footer links, the email links and the Duskfold page images.

**6. Check for cookies (one minute)**

1. In Chrome on your computer, open the site and press **F12 → Application → Cookies**. It should be empty.
2. Then open **Network**, reload, click the first request, and look under **Response Headers**: there should be no `set-cookie`.
3. If OVHcloud adds one, tell me before relying on the privacy notice's "no cookies" line.

**7. Test email**

1. From a personal address (for example Gmail), send a message to hello@digbyhouse.co.uk and check it arrives.
2. Reply from hello@digbyhouse.co.uk and check the reply arrives back.
3. Recheck the DNS zone against your screenshot.

## 7. Apple Developer enrolment (after publication)

1. ☐ Site live at https://www.digbyhouse.co.uk, every page working.
2. ☐ The legal name on the site, "Digby House Ltd", matches the D‑U‑N‑S record and the enrolment form exactly.
3. ☐ You enrol with an email address at digbyhouse.co.uk, with authority to bind the company.
4. ☐ Email works in both directions.
5. ☐ The site says Duskfold is coming soon, with no App Store link (correct until launch).
