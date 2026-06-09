# Teacher Workflows

This document explains the teacher experience from login to attendance records.

## Teacher Login

Teacher login is password-based.

Flow:

1. Enter username and password
2. `teacher_login()` looks up the teacher in Supabase
3. Password is checked with `bcrypt`
4. Teacher data is stored in session state

## Teacher Dashboard

The dashboard has three tabs:

- Take Attendance
- Manage Subjects
- Attendance Records

The selected tab is stored in `st.session_state.current_teacher_tab`.

## Create a Subject

Teacher enters:

- subject code
- subject name
- section

The app inserts a row into `subjects` with the current teacher ID.

## Take Attendance

This is the main workflow.

1. Pick a subject
2. Add photos from camera or upload
3. Run face analysis
4. Review the generated attendance table
5. Confirm and save

## What the App Does Internally

- Finds faces in each image
- Predicts student IDs
- Checks the selected subject’s enrollments
- Marks each enrolled student present or absent
- Saves one attendance log row per student

## Voice Attendance

Teacher can choose voice attendance instead of face attendance.

Flow:

1. Record classroom audio
2. Split speech into segments
3. Match segments to enrolled students who have voice profiles
4. Review the result
5. Confirm and save

## Share Subject

The teacher can share:

- subject code
- copyable join link
- QR code

The shared link uses the `join-code` query parameter.

## Attendance Records

The records page shows:

- class time
- subject
- subject code
- present count
- total count

It is a session summary, not a per-student audit screen.
