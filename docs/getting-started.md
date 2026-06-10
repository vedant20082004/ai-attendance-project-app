# Getting Started

This guide explains how to run the project from scratch on Windows.

## What You Need

- Python 3.11 recommended
- Git
- A Supabase project
- A webcam for student login and registration
- A microphone if you want to test voice attendance

## Step 1: Create a Virtual Environment

```powershell
cd C:\Users\vedan\Downloads\ai-attendance-project-app
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
```

If Python 3.11 is not installed, Python 3.12 can work, but the native AI dependencies are usually easier on 3.11.

## Step 2: Install Dependencies

```powershell
pip install -r requirements.txt
```

Important packages in this repo:

- `streamlit` for the UI
- `supabase` for backend access
- `dlib-bin` and `face_recognition_models` for face recognition
- `librosa` and `resemblyzer` for voice embeddings
- `scikit-learn` for the face classifier
- `bcrypt` for teacher passwords
- `segno` for QR codes

## Step 3: Add Secrets

Create `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-supabase-anon-key"
```

Use the anon key first. The code reads secrets in `src/database/config.py`.

### Where to find the anon key

In Supabase:

1. Open your project
2. Go to `Project Settings`
3. Open `API`
4. Copy the `anon public` key
5. Put it into `.streamlit/secrets.toml`

Example:

```toml
SUPABASE_URL = "https://pondipsanatqielyyyoy.supabase.co"
SUPABASE_KEY = "your_anon_public_key_here"
```

## Step 4: Create the Supabase Tables

Follow [`backend-schema.md`](backend-schema.md). The app expects these tables:

- `teachers`
- `students`
- `subjects`
- `subject_students`
- `attendance_logs`

## Step 5: Start the App

```powershell
streamlit run app.py
```

You should see:

- local URL on port 8501
- the home screen

## Step 6: Verify the Happy Path

1. Open the app
2. Register a teacher
3. Log in as that teacher
4. Create a subject
5. Open the student portal
6. Register or log in a student
7. Enroll the student in the subject
8. Add attendance photos
9. Confirm and save attendance

## Common Setup Failures

- Missing secrets file
- Wrong Supabase key
- Missing tables in Supabase
- Native package install errors on Windows
- RLS policies blocking reads/writes

See [`troubleshooting.md`](troubleshooting.md) for fixes.
