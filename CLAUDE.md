# Spanish Study Guide

Single-page static site (`index.html`), built from the user's weekly one-hour iTalki lessons.

- Content lives in the `LESSONS`, `GRAMMAR`, `CHANNELS`, `TASKS` and `HABITS` arrays at the top of the `<script>`. A new lesson is one new `LESSONS` entry; vocabulary, flashcards, quiz and stats pick it up automatically. Lesson filter chips appear once there are two or more lessons.
- Words take `es`, `en` (meanings separated by `;`, the first is used in quizzes), optional `art` (el / la / los / las), `pos` and `kind: 'phrase'` for expressions.
- Tutor PDFs go in `materials/` and are linked from the lesson's `materials`.
- Audio uses the browser's Spanish voice (speechSynthesis); there are no recorded clips.
- Progress (learned words, daily practice) is in localStorage under `es.learned` and `es.practice`.
- The user doesn't want explanatory filler copy on the site.
- Preview: `python3 -m http.server 8124` (see `.claude/launch.json`).
