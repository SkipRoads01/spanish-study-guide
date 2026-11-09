# Spanish Study Guide

Single-page static site (`index.html`), built from the user's weekly one-hour iTalki lessons.

- Content lives in the `LESSONS`, `GRAMMAR`, `CHANNELS`, `TASKS` and `HABITS` arrays at the top of the `<script>`. A new lesson is one new `LESSONS` entry; vocabulary, flashcards, quiz and stats pick it up automatically. Lesson filter chips appear once there are two or more lessons.
- Words take `es`, `en` (meanings separated by `;`, the first is used in quizzes), optional `art` (el / la / los / las), `pos` and `kind: 'phrase'` for expressions.
- `PLAN` (+ `PLAN_START`) is the tutor's 8-week program shown at the top of Lessons: 4 two-week stages, each with a challenge; the current week is computed from the date. `HABITS` is the tutor's weekly practice list, target `PRACTICE_TARGET` days/week.
- GRAMMAR entries with `verbs: 'tense'` or `verbs: 'like'` (verbs like gustar) show on the Verbs page instead of Grammar; Verbs also lists every verb. Words with `natural: true` (phrasing the tutor flags as natural) show on the Natural page.
- Lessons can have `corrections: [[what I said, correct version, short note]]`; the correct version gets audio.
- Source for each lesson: iTalki's AI lesson summary (vocabulary, expressions, grammar, error corrections) on the lesson's page, read in the built-in browser panel (the user signs in there; Claude in Chrome hasn't connected). Spanish lessons only (teacher: Profesora Gisela), Mondays 9:00, 60 min. Ignore the Mandarin/Macedonian lessons in the same account.
- Tutor PDFs go in `materials/` and are linked from the lesson's `materials`.
- Audio: recorded ElevenLabs clips in `audio/` + `audio/manifest.json`. After adding content, run `python3 generate_audio.py` yourself (the key is in the git-ignored `.env`) and commit the new clips; don't ask the user to run it. The browser voice is only a fallback, and the user dislikes it.
- Published on GitHub Pages: https://skiproads01.github.io/spanish-study-guide/ (repo SkipRoads01/spanish-study-guide, branch main). Push after each change.
- Progress (learned words, daily practice) is in localStorage under `es.learned`, `es.practice`, `es.challenges` and `es.book` (the flashcard book: cards set aside with the +📕 button; shows as a book deck/filter chip once non-empty).
- The user doesn't want explanatory filler copy on the site.
- Preview: `python3 -m http.server 8124` (see `.claude/launch.json`).
