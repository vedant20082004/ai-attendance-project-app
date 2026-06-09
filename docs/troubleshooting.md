# Troubleshooting

This page covers the most common issues you are likely to see.

## `StreamlitSecretNotFoundError`

Cause:

- `.streamlit/secrets.toml` is missing
- or `SUPABASE_URL` / `SUPABASE_KEY` are missing

Fix:

1. Create `.streamlit/secrets.toml`
2. Add the keys
3. Restart Streamlit

## `Could not find the table 'public.students'`

Cause:

- Supabase tables have not been created yet

Fix:

1. Create the schema from [`backend-schema.md`](backend-schema.md)
2. Refresh the Supabase project
3. Re-run the app

## `Microsoft Visual C++ 14.0 or greater is required`

Cause:

- `webrtcvad` is being built from source on Windows

Fix:

1. Install Visual Studio Build Tools
2. Include Desktop development with C++
3. Reopen PowerShell
4. Reinstall requirements

## `SyntaxError: f-string: unmatched '['`

Cause:

- A string contains nested single quotes inside an f-string

Fix:

- Use double quotes for the outer string or extract the variable first

## `ValueError: invalid literal for int()`

Cause:

- Code tried to convert UUID IDs into integers

Fix:

- Treat IDs as strings

## App Starts But Login Fails

Check:

- Supabase URL is correct
- anon key is correct
- teacher/student rows exist
- RLS policies are not blocking reads/writes

## App Loads But Attendance Saves Fail

Check:

- `attendance_logs` table exists
- `subject_students` has enrollment rows
- `students` has face embeddings
- the teacher confirmed the attendance dialog

