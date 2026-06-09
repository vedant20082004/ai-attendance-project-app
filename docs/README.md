# SnapClass Docs

SnapClass is a Streamlit app for taking attendance with face recognition and optional voice recognition.

## Who These Docs Are For

- Developers who need to run, extend, or debug the app
- Learners who want to understand how the project works end to end
- Maintainers who need a reference for Supabase, AI pipelines, and Streamlit flow

## Reading Order

1. [`getting-started.md`](getting-started.md) to install and run the project
2. [`backend-schema.md`](backend-schema.md) to build the Supabase tables
3. [`architecture.md`](architecture.md) to understand the app structure
4. [`teacher-workflows.md`](teacher-workflows.md) and [`student-workflows.md`](student-workflows.md) for user journeys
5. [`ai-pipelines.md`](ai-pipelines.md) for the face and voice logic
6. [`troubleshooting.md`](troubleshooting.md) when something breaks
7. [`developer-guide.md`](developer-guide.md) for codebase maintenance

## What This App Does

- Teachers create subjects and take attendance
- Students log in using their face
- Voice profiles can be stored for optional audio-based attendance
- Attendance is saved in Supabase

## Core Repo Layout

```text
app.py
src/
  screens/
  components/
  database/
  pipelines/
  ui/
```

## Quick Links

- Setup: [`getting-started.md`](getting-started.md)
- Database: [`backend-schema.md`](backend-schema.md)
- App structure: [`architecture.md`](architecture.md)
- Teacher flows: [`teacher-workflows.md`](teacher-workflows.md)
- Student flows: [`student-workflows.md`](student-workflows.md)
- AI logic: [`ai-pipelines.md`](ai-pipelines.md)
- Troubleshooting: [`troubleshooting.md`](troubleshooting.md)
- Developer notes: [`developer-guide.md`](developer-guide.md)
