# AI Attendance System

This is a learning project that demonstrates how an AI-assisted classroom attendance app can be built with Python, Streamlit, Supabase, face recognition, and optional voice recognition.

The app is not meant to be production-ready. It is meant to help you understand how a real project can connect a user interface, a database, and AI pipelines.

## What The App Does

- Teachers can register, log in, create subjects, share subject join codes, and take attendance.
- Students can register or log in with their face.
- Students can optionally record a voice sample for voice-based attendance.
- Teachers can mark attendance from classroom photos or classroom audio.
- Attendance records are stored in Supabase.

## Main Technologies

- Streamlit for the web interface
- Supabase for database storage
- dlib and `face_recognition_models` for face embeddings
- scikit-learn for the face classifier
- Resemblyzer and librosa for voice embeddings
- bcrypt for teacher password hashing
- pandas and NumPy for data handling

## Documentation

Start with the full docs in [`docs/README.md`](docs/README.md).

Recommended reading order:

1. [`docs/README.md`](docs/README.md)
2. [`docs/getting-started.md`](docs/getting-started.md)
3. [`docs/learning-concepts.md`](docs/learning-concepts.md)
4. [`docs/library-guide.md`](docs/library-guide.md)
5. [`docs/backend-schema.md`](docs/backend-schema.md)
6. [`docs/architecture.md`](docs/architecture.md)
7. [`docs/code-walkthrough.md`](docs/code-walkthrough.md)
8. [`docs/teacher-workflows.md`](docs/teacher-workflows.md)
9. [`docs/student-workflows.md`](docs/student-workflows.md)
10. [`docs/ai-pipelines.md`](docs/ai-pipelines.md)
11. [`docs/troubleshooting.md`](docs/troubleshooting.md)
12. [`docs/developer-guide.md`](docs/developer-guide.md)

## Quick Start

```powershell
cd C:\Users\vedan\Downloads\ai-attendance-project-app
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
streamlit run app.py
```

You also need a `.streamlit/secrets.toml` file with your Supabase project URL and anon key. The optional `APP_DOMAIN` secret controls shared subject links and QR codes. See [`docs/getting-started.md`](docs/getting-started.md) for the complete setup.

## Project Layout

```text
app.py
src/
  __init__.py    marks src as a Python package
  screens/       page-level teacher, student, and home screens
  components/    reusable dialogs, cards, header, and footer
  database/      Supabase connection and database helper functions
  pipelines/     face and voice recognition logic
  ui/            shared Streamlit styling
docs/            beginner-friendly project documentation
```

## Important Learning Note

This project intentionally keeps many ideas visible in the code so learners can study them. A production attendance system would need stronger authentication, authorization, privacy controls, model evaluation, audit logs, deployment hardening, and security reviews.
