# Troubleshooting

This page explains common issues and how to debug them.

Start by asking three questions:

1. Did the app start?
2. Did the app connect to Supabase?
3. Did the expected data exist in the expected table?

## Setup Problems

## `StreamlitSecretNotFoundError`

Cause:

- `.streamlit/secrets.toml` is missing.
- `SUPABASE_URL` is missing.
- `SUPABASE_KEY` is missing.
- The file is in the wrong folder.

Fix:

1. Create `.streamlit/secrets.toml`.
2. Add:

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your_anon_public_key_here"
APP_DOMAIN = "http://localhost:8501"
```

3. Restart Streamlit.

`APP_DOMAIN` is optional. If shared links or QR codes point to the wrong place, set it to the domain where your app is running.

Read [`getting-started.md`](getting-started.md) for setup details.

## PowerShell Will Not Activate `.venv`

Cause:

- PowerShell execution policy may block scripts.

Fix options:

- Use a PowerShell session where script execution is allowed.
- Activate from a terminal configured for Python development.
- Run commands with the virtual environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\streamlit.exe run app.py
```

## Package Installation Fails

Cause:

- Some AI/audio packages rely on native dependencies.
- Python version may not have compatible wheels.
- Build tools may be missing.

Fix:

1. Use Python 3.11 if possible.
2. Upgrade packaging tools:

```powershell
python -m pip install --upgrade pip setuptools wheel
```

3. Reinstall:

```powershell
pip install -r requirements.txt
```

## `Microsoft Visual C++ 14.0 or greater is required`

Cause:

- A package is being built from source on Windows.

Fix:

1. Install Visual Studio Build Tools.
2. Include `Desktop development with C++`.
3. Reopen PowerShell.
4. Activate `.venv`.
5. Reinstall requirements.

## Database Problems

## `Could not find the table 'public.students'`

Cause:

- Supabase tables have not been created.
- The app is connected to the wrong Supabase project.

Fix:

1. Open Supabase SQL Editor.
2. Run the schema from [`backend-schema.md`](backend-schema.md).
3. Confirm the table exists in Table Editor.
4. Restart the app.

## Wrong Supabase URL Or Key

Symptoms:

- Login fails even when data exists.
- Inserts fail.
- Supabase returns API errors.

Fix:

1. Open Supabase project settings.
2. Copy the project URL again.
3. Copy the `anon public` key again.
4. Update `.streamlit/secrets.toml`.
5. Restart Streamlit.

## RLS Blocking Reads Or Writes

Cause:

- Supabase Row Level Security is enabled without policies that allow this app's queries.

Symptoms:

- Tables exist, but the app gets empty results.
- Inserts silently fail or return permission errors.
- Login cannot find users that are visible in Supabase.

Fix for local learning:

- Disable RLS using the SQL shown in [`backend-schema.md`](backend-schema.md).

Production note:

- A real app should use proper RLS policies instead of disabling RLS.

## Teacher Login Fails

Check:

- Does the `teachers` table contain the username?
- Was the teacher created through the app, so the password is bcrypt-hashed?
- Are `SUPABASE_URL` and `SUPABASE_KEY` correct?
- Is RLS blocking reads?

If you manually insert a teacher into Supabase with a plain password, login will fail because the app expects a bcrypt hash.

## Subject Creation Fails

Check:

- Does the `subjects` table exist?
- Is `subject_code` unique?
- Is the teacher logged in?
- Does the logged-in teacher have a valid `teacher_id`?

The `subject_code` column is unique, so two subjects cannot use the same code.

## Shared Link Or QR Code Opens The Wrong Domain

Cause:

- `APP_DOMAIN` is missing or set to the wrong value in `.streamlit/secrets.toml`.

Fix:

1. For local testing, use:

```toml
APP_DOMAIN = "http://localhost:8501"
```

2. For a deployed app, set it to the deployed app URL.
3. Restart Streamlit after changing secrets.

## Camera Problems

## Webcam Does Not Open

Cause:

- Browser permission blocked.
- Another app is using the camera.
- Browser does not support camera access in the current context.

Fix:

1. Allow camera permission in the browser.
2. Close other camera apps.
3. Refresh the Streamlit page.
4. Try another browser.

## No Face Detected

Cause:

- Face is not visible enough.
- Poor lighting.
- Face is too far away.
- Image is blurry.

Fix:

- Move closer to the camera.
- Use better lighting.
- Face the camera directly.
- Try again with one clear face.

## Multiple Faces Detected During Student Login

Cause:

- More than one face is visible in the student login photo.

Fix:

- Make sure only one student is visible during login or registration.

Teacher attendance photos can contain multiple faces, but student login should contain one face.

## Microphone And Voice Problems

## Microphone Does Not Record

Cause:

- Browser permission blocked.
- No microphone selected.
- Another app is using the microphone.

Fix:

1. Allow microphone permission.
2. Check browser site settings.
3. Check Windows input device settings.
4. Refresh the app.

## Voice Attendance Says No Students Have Voice Profiles

Cause:

- Enrolled students did not record voice samples during registration.

Fix:

- Register a student with optional voice enrollment.
- Confirm `students.voice_embedding` is not empty in Supabase.

## Voice Recognition Misses A Student

Cause:

- Audio is noisy.
- Student spoke too quietly.
- Speech segment was too short.
- Score was below threshold `0.65`.

Fix:

- Record in a quieter place.
- Ask students to speak clearly.
- Test with one student first.
- Check [`ai-pipelines.md`](ai-pipelines.md) for how voice matching works.

## AI Recognition Problems

## Student Face Login Does Not Recognize A Registered Student

Check:

- Does the student row have a `face_embedding`?
- Was the face photo clear during registration?
- Is the current login photo clear?
- Did the app refresh the classifier after registration?

The app calls `train_classifier()` after creating a student. If something interrupted registration, restart the app and try again.

## Face Attendance Misses Students In A Classroom Photo

Cause:

- Faces are too small.
- Faces are turned sideways.
- Lighting is poor.
- The recognition distance is above threshold `0.6`.
- Students are not enrolled in the selected subject.

Fix:

- Use clearer photos.
- Make sure students are enrolled in the subject.
- Test with a smaller group first.
- Confirm `face_embedding` exists for each student.

## Attendance Save Problems

## Attendance Review Appears But Save Fails

Check:

- Does `attendance_logs` exist?
- Do `student_id` and `subject_id` values exist in related tables?
- Is RLS blocking inserts?
- Did the teacher click `Confirm & Save`?

Attendance is not saved when analysis runs. It is saved only after confirmation.

## Attendance Records Are Empty

Cause:

- No attendance sessions have been confirmed.
- Logs were saved for another teacher's subject.
- Supabase reads are blocked.

Fix:

1. Take attendance.
2. Confirm and save.
3. Check `attendance_logs` in Supabase.
4. Return to `Attendance Records`.

## Common Python Errors

## `SyntaxError: f-string: unmatched '['`

Cause:

- A string uses nested single quotes inside an f-string.

Fix:

Use double quotes outside:

```python
f"Welcome {student['name']}"
```

Or store the value first:

```python
name = student["name"]
f"Welcome {name}"
```

## `ValueError: invalid literal for int()`

Cause:

- Code tried to convert a UUID string into an integer.

Fix:

- Treat IDs as strings.

Student IDs, teacher IDs, and subject IDs are UUID strings.

## Beginner Debugging Habits

- Read the exact error message first.
- Check which file and line number the error mentions.
- Confirm the required Supabase table exists.
- Confirm the row exists in Supabase.
- Confirm the app is using the correct Supabase project.
- Test one workflow at a time.
- Restart Streamlit after changing secrets or installing packages.
- Keep real secrets out of docs, screenshots, and commits.
