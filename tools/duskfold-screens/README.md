# Duskfold screenshots for the website

Captured from the **current Duskfold app**, walking its real evening flow, with no change to the app
and no AI calls. The browser answers the app's requests locally with `recorded.json`: genuine output
recorded in Stage R3 (24 November 2026, fictional test evening e1-10, its two non-sensitive thoughts).

1. In the Duskfold repository, create `.env.local` (ignored by git):
   `EXPO_PUBLIC_SUPABASE_URL=http://localhost:8787` and any placeholder `EXPO_PUBLIC_SUPABASE_ANON_KEY`.
2. Run `npm run web:preview -- --port 8081` there.
3. From this folder: `node journey.js "$(pwd)"`. Screens are written to `shots/` (1179 × 2556).
4. Delete `.env.local` in the Duskfold repository afterwards.

Developer-only overlays (the DEV tab and the "provisional" labels) are hidden in the captures.
