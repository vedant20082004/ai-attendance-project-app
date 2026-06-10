# AI Attendance System

This is a Streamlit application for AI-assisted classroom attendance.

It supports:

- Teacher login and registration
- Student face-based login and registration
- Subject creation and enrollment
- Face-based attendance capture from classroom photos
- Optional voice-based attendance
- Supabase-backed storage for users, subjects, enrollments, and attendance logs

## Documentation

The full setup and implementation guide lives in [`docs/`](docs/README.md).

Recommended reading order:

1. [`docs/README.md`](docs/README.md)
2. [`docs/getting-started.md`](docs/getting-started.md)
3. [`docs/backend-schema.md`](docs/backend-schema.md)
4. [`docs/architecture.md`](docs/architecture.md)
5. [`docs/troubleshooting.md`](docs/troubleshooting.md)

## Quick Start

### 1. Create a virtual environment

```powershell
cd C:\Users\vedan\Downloads\ai-attendance-project-app
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure secrets

Create `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-supabase-anon-key"
```

### 4. Create the Supabase schema

Run the SQL in [`docs/backend-schema.md`](docs/backend-schema.md) inside Supabase SQL editor.

### 5. Start the app

```powershell
streamlit run app.py
```

## Project Structure

```text
app.py
src/
  screens/
  components/
  database/
  pipelines/
  ui/
docs/
  getting-started.md
  backend-schema.md
  architecture.md
  teacher-workflows.md
  student-workflows.md
  ai-pipelines.md
  troubleshooting.md
  developer-guide.md
```

## Core Stack

- Streamlit for the UI
- Supabase for backend storage
- dlib and face-recognition models for face embeddings
- Resemblyzer and librosa for voice embeddings
- scikit-learn for the face classifier
- bcrypt for teacher passwords
- segno for QR codes

## Notes

- Use the Supabase anon public key in local development
- IDs are UUIDs, not integers
- The app expects the five tables documented in [`docs/backend-schema.md`](docs/backend-schema.md)
- If you hit install or runtime issues, start with [`docs/troubleshooting.md`](docs/troubleshooting.md)
