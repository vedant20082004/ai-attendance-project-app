# Getting Started

This guide explains how to run the project from scratch on Windows using PowerShell.

The goal is not only to run the app, but also to understand what each setup step does.

## What You Need

- Python 3.11 recommended
- Git, if you are cloning the project from a repository
- A Supabase project
- A webcam for student face login and registration
- A microphone if you want to test voice attendance
- PowerShell

Python 3.11 is recommended because the AI libraries used by this project include native packages. Native packages are packages that depend on compiled code. They are often easier to install on Python versions that already have compatible wheels.

## Step 1: Open The Project Folder

```powershell
cd C:\Users\vedan\Downloads\ai-attendance-project-app
```

This command moves your terminal into the project directory. Most project commands should be run from this folder because files like `app.py` and `requirements.txt` live here.

Checkpoint:

- Running `dir` should show `app.py`, `requirements.txt`, `src`, and `docs`.

## Step 2: Create A Virtual Environment

```powershell
py -3.11 -m venv .venv
```

A virtual environment is a private Python environment for this project. It keeps this project's packages separate from packages used by other Python projects.

The folder `.venv` is created in the project directory. It contains a local Python interpreter and installed packages.

## Step 3: Activate The Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, your terminal prompt usually shows `(.venv)`.

This means when you run `python` or `pip`, PowerShell will use the project environment instead of your global Python install.

If PowerShell blocks activation, see [`troubleshooting.md`](troubleshooting.md).

## Step 4: Upgrade Basic Packaging Tools

```powershell
python -m pip install --upgrade pip setuptools wheel
```

These tools help Python install packages.

- `pip` installs packages.
- `setuptools` helps build and install Python packages.
- `wheel` helps install prebuilt packages faster.

This is useful because AI dependencies can be more sensitive than simple Python-only packages.

## Step 5: Install Project Dependencies

```powershell
pip install -r requirements.txt
```

`requirements.txt` is a list of libraries the project needs. This app uses libraries for UI, database access, image processing, face recognition, voice recognition, password hashing, and data tables.

For a full explanation of every dependency, read [`library-guide.md`](library-guide.md).

Checkpoint:

- The command should finish without errors.
- If installation fails on packages related to `dlib`, native builds, or audio, check [`troubleshooting.md`](troubleshooting.md).

## Step 6: Create A Supabase Project

Supabase provides the database for this app. The app stores teachers, students, subjects, enrollments, and attendance logs there.

In Supabase:

1. Create or open a project.
2. Go to `Project Settings`.
3. Open `API`.
4. Copy the project URL.
5. Copy the `anon public` key.

The anon key is used by the local app to talk to Supabase. For this learning project, the docs use the anon key because it is simple for local testing.

## Step 7: Add Streamlit Secrets

Create this file:

```text
.streamlit/secrets.toml
```

Add:

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your_anon_public_key_here"
# Optional. Use this when you want shared join links to point to a deployed app.
# For local testing, the app falls back to localhost:8501.
APP_DOMAIN = "http://localhost:8501"
```

Do not paste real secrets into documentation or screenshots.

The code reads these values in `src/database/config.py`:

```python
supabase: Client = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)
```

This means the app cannot connect to Supabase unless those two keys exist.

`APP_DOMAIN` is optional. It is read by the subject sharing dialog in `src/components/dialog_share_subject.py`. The app uses it to build links like:

```text
http://localhost:8501/?join-code=CS101
```

If `APP_DOMAIN` is not set, the app uses `localhost:8501` as the fallback.

Checkpoint:

- The file path should be exactly `.streamlit/secrets.toml`.
- The key names should be exactly `SUPABASE_URL` and `SUPABASE_KEY`.
- `APP_DOMAIN` is optional, but useful when testing shared links or QR codes.

## Step 8: Create The Database Tables

Open Supabase SQL Editor and run the schema from [`backend-schema.md`](backend-schema.md).

The app expects these tables:

- `teachers`
- `students`
- `subjects`
- `subject_students`
- `attendance_logs`

If these tables do not exist, the app may start but login, registration, enrollment, or attendance saving will fail.

## Step 9: Start The App

```powershell
streamlit run app.py
```

Streamlit should print a local URL, usually:

```text
http://localhost:8501
```

Open that URL in your browser.

What happens internally:

1. Streamlit runs `app.py`.
2. `app.py` configures the page.
3. The app checks `st.session_state["login_type"]`.
4. The home screen appears if no login type is selected.

Read [`architecture.md`](architecture.md) and [`code-walkthrough.md`](code-walkthrough.md) for the full flow.

## First Successful Run Workflow

Use this checklist to confirm the project works end to end.

### 1. Register a teacher

1. Open the app.
2. Choose `Enter Teacher Portal`.
3. Click register instead.
4. Enter username, name, password, and password confirmation.
5. Submit the form.

The app stores the teacher in the `teachers` table. The password is hashed with bcrypt before storage.

### 2. Log in as the teacher

1. Go back to teacher login.
2. Enter the username and password.
3. Submit.

The app checks the username in Supabase and verifies the password hash.

### 3. Create a subject

1. Open `Manage Subjects`.
2. Click `Create New Subject`.
3. Enter a subject code, name, and section.
4. Save.

The app inserts a row into the `subjects` table with the current teacher ID.

### 4. Register a student

1. Log out or go back to home.
2. Choose `Enter Student Portal`.
3. Take a face photo.
4. If the face is not recognized, the registration form appears.
5. Enter the student's name.
6. Optionally record a voice sample.
7. Create the account.

The app stores a face embedding in the `students` table. If audio was recorded, it also stores a voice embedding.

### 5. Enroll the student

Students can enroll in two ways:

- Enter the subject code manually.
- Open a teacher-shared join link that includes `join-code`.

Both methods insert a row into `subject_students`.

### 6. Take photo attendance

1. Log in as the teacher.
2. Open `Take Attendance`.
3. Select a subject.
4. Add one or more classroom photos.
5. Run face analysis.

The app compares detected faces with enrolled students for the selected subject.

### 7. Confirm attendance

The app shows a review table. Attendance is saved only when the teacher clicks `Confirm & Save`.

This creates one row per enrolled student in `attendance_logs`.

### 8. View attendance records

Open the teacher `Attendance Records` tab. The app groups attendance rows by timestamp and subject, then shows present count and total count.

## Next Reading

- For beginner concepts, read [`learning-concepts.md`](learning-concepts.md).
- For database setup details, read [`backend-schema.md`](backend-schema.md).
- For common errors, read [`troubleshooting.md`](troubleshooting.md).
