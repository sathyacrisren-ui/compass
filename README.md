# Compass

A personal career-and-personality app, built as one web page for an iPhone Home Screen.

- `src/app.html` is the source. `python3 tools/build.py` bakes the O*NET tables from `data/` into `index.html`.
- `node tests/score-test.js` checks the scoring and matching against the built file.
- `python3 tools/serve.py` serves the folder on http://localhost:8644 for testing.

Five questionnaires (177 questions): O*NET Interest Profiler Short Form (60, CC BY 4.0, U.S. Department of Labor),
IPIP Big-Five Factor Markers (50, public domain), and three short scales written for this app
(type 20, work style 20, motivation 27). Careers are the 923 O*NET 31.0 occupations ranked by
correlation between the user's six interest scores and the occupation's interest profile.

The written profile and the mentor chat call the Anthropic API directly from the phone with a key
the user enters under More. The key stays in that browser's localStorage and is never sent anywhere else.
