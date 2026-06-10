# Project Documentation

Welcome to the documentation for the AI Attendance System. These docs are written for learning. They explain what the app does, how the code is organized, what each library is used for, and how the face and voice recognition logic works.

This project is a local educational app, not a production attendance platform.

## Who These Docs Are For

### If you are a beginner

Start with the setup guide and concept guide. You do not need to understand every AI detail first. The best path is to run the app, see the workflow, then come back to the code explanations.

### If you are learning full-stack Python

Focus on how Streamlit, Supabase, and the database helper functions work together. The app is a useful example of connecting UI actions to database reads and writes.

### If you are learning AI application logic

Focus on the face and voice pipeline docs. They explain embeddings, matching, thresholds, and why the app stores numeric vectors for students.

### If you want to modify the project

Read the architecture and developer guide before changing files. The project is organized so UI, database, AI, and styling stay in separate places.

## Reading Roadmap

1. [`getting-started.md`](getting-started.md): install, configure, and run the app.
2. [`learning-concepts.md`](learning-concepts.md): learn the basic ideas used in the project.
3. [`library-guide.md`](library-guide.md): understand every dependency in `requirements.txt`.
4. [`backend-schema.md`](backend-schema.md): create and understand the Supabase tables.
5. [`architecture.md`](architecture.md): understand how the app is wired together.
6. [`code-walkthrough.md`](code-walkthrough.md): follow the code from `app.py` into screens, components, database helpers, and AI pipelines.
7. [`teacher-workflows.md`](teacher-workflows.md): understand the teacher side.
8. [`student-workflows.md`](student-workflows.md): understand the student side.
9. [`ai-pipelines.md`](ai-pipelines.md): understand face and voice recognition.
10. [`troubleshooting.md`](troubleshooting.md): fix common setup and runtime problems.
11. [`developer-guide.md`](developer-guide.md): learn how to extend the app safely.

## Project Overview

```text
User opens app
     |
     v
app.py chooses a screen using st.session_state["login_type"]
     |
     +-- Home screen
     |
     +-- Teacher screen
     |      |
     |      +-- teacher login/register
     |      +-- subject management
     |      +-- photo or voice attendance
     |      +-- attendance records
     |
     +-- Student screen
            |
            +-- face login
            +-- new student registration
            +-- subject enrollment
            +-- attendance summary
```

## Main Parts Of The Project

### UI layer

The UI is built with Streamlit. The main UI files are in `src/screens/` and `src/components/`.

- `screens` are page-level flows.
- `components` are reusable UI pieces such as dialogs and cards.

### Database layer

The database is Supabase. The project connects to Supabase in `src/database/config.py`, and most database operations live in `src/database/db.py`.

The app expects these tables:

- `teachers`
- `students`
- `subjects`
- `subject_students`
- `attendance_logs`

### AI pipeline layer

The AI logic is isolated in `src/pipelines/`.

- `face_pipeline.py` detects faces, creates face embeddings, trains a classifier, and predicts student IDs.
- `voice_pipeline.py` creates voice embeddings and compares classroom audio against stored student voice profiles.

### Styling layer

The shared Streamlit styling lives in `src/ui/base_layout.py`. It contains CSS injected into the Streamlit page.

## Terms Used Throughout The Docs

- Student ID: a UUID string from Supabase, not an integer.
- Embedding: a list of numbers that represents a face or voice.
- Attendance session: one confirmed attendance run for one subject at one timestamp.
- Join code: the subject code students use to enroll.
- Join link: a URL containing the `join-code` query parameter.

## Learning Scope

These docs explain how the project works and how to modify it for learning. They do not claim that the app is secure enough for real schools. A production system would need privacy protections, role-based access control, strict database policies, consent handling, secure deployment, and careful AI accuracy testing.
