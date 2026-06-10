# Architecture

This document explains how the project is wired together.

## Entry Flow

The app starts in `app.py`.

High-level flow:

1. Configure page title and icon
2. Initialize `st.session_state.login_type`
3. Render either home, teacher, or student screen
4. Check for `join-code` in the query string
5. Auto-open enrollment when the student comes through a shared link

## Screen Routing

Streamlit does not use normal page routing here. Instead, the app uses session state.

Key value:

- `login_type = None` shows the home screen
- `login_type = "teacher"` shows teacher flows
- `login_type = "student"` shows student flows

## Module Map

- `src/screens/home_screen.py`: landing choice between teacher and student
- `src/screens/teacher_screen.py`: teacher login, dashboard, attendance, subject management
- `src/screens/student_screen.py`: student login, registration, dashboard
- `src/components/*`: dialogs, header, footer, cards
- `src/database/db.py`: all Supabase reads and writes
- `src/pipelines/face_pipeline.py`: face embeddings and classifier
- `src/pipelines/voice_pipeline.py`: voice embeddings and speaker matching
- `src/ui/base_layout.py`: CSS and visual layout styling

## Data Flow

### Teacher Attendance

1. Teacher selects a subject
2. Teacher uploads or captures classroom photos
3. Face pipeline finds faces and predicts student IDs
4. App compares detected IDs against enrolled students
5. Review dialog appears
6. Attendance rows are saved only after confirmation

### Student Login

1. Student uses the camera
2. Face pipeline tries to identify the student
3. If recognized, student logs in
4. If not recognized, student can register

### Enrollment

1. Student enters a subject code or uses a shared join link
2. App looks up the subject
3. App inserts into `subject_students`

## Session State

Important keys:

- `teacher_data`
- `student_data`
- `login_type`
- `teacher_login_type`
- `current_teacher_tab`
- `attendance_images`
- `voice_attendance_results`
- `photo_tab`

These are what keep the app feeling stateful while Streamlit reruns the script.

## Why This Architecture Works

- It keeps UI code separated from database code
- It keeps AI pipelines isolated from app screens
- It uses small dialog components for actions that need confirmation
- It keeps all backend reads and writes in one place
