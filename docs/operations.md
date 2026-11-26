# Digby House: operational responsibilities for the website and email

These are standing duties for Digby House Ltd (owner: the founder). They put into practice what the website privacy notice says. They are founder decisions, not independent legal advice.

## 1. Enquiry email retention: 12 months (founder approval, 26 November 2026)

- **Rule:** ordinary enquiry emails to hello@digbyhouse.co.uk, including replies sent, are deleted 12 months after the conversation has ended.
- **Exceptions:** an email is kept longer only while there is a documented reason, and is deleted when the reason ends:
  - a complaint;
  - a legal claim, or one that is reasonably expected;
  - a legal obligation, such as a tax or accounting record or a data protection request that must be evidenced.
  Note the reason and the review date in a short private log.
- **How:**
  - **Once a month,** sort the mailbox (inbox, sent, archive and any folders) by date. Delete conversations whose last message is more than 12 months old, apart from the exceptions.
  - Then empty the deleted-items folder.
- **Consistent with** Duskfold's records of processing (ROPA P7: 12 months after the enquiry is resolved, D-157).

## 2. Privacy notice facts to keep true

| The notice says                                                         | Keep it true by                                                                                                                                                               |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| No cookies, analytics, advertising, tracking or scripts                 | Not adding any, in the site or the hosting settings. After upload, check once that the server sends no `set-cookie` (publication instructions, step 6).                       |
| Everything is served from our own hosting                               | Not embedding third-party fonts, maps, videos or forms                                                                                                                        |
| OVHcloud hosting and email under its data processing agreement          | Keeping the OVHcloud contract. If either the website host or the email provider changes, update the notice first.                                                             |
| Email stored in OVHcloud's European datacentres; group access from the EEA, UK and Canada | Re-reading OVHcloud's sub-processor list once a year (last checked: list dated 16 October 2025, read 20 November 2026, D-159)                                                  |
| Server logs kept by OVHcloud only as long as needed; no copies kept by us | Not downloading or storing raw access logs. If you ever need them for an incident, delete them when it's closed.                                                              |
| Requests answered within one month                                      | Following Duskfold's rights-request procedure (`duskfold/docs/review/rights-request-procedure.md`) for any website or email request                                           |

## 3. When the notice must be updated

Update `src/pages/privacy/index.html`, including its "Last updated" date, and republish if any of these is added or changes:

- analytics, cookies or embedded content;
- a contact form or a mailing-list sign-up linked from the site;
- the hosting or email provider;
- the retention rule.

The Duskfold privacy policy is separate, and is published at `/privacy` only at Duskfold's launch (Duskfold release checklist §9a).
