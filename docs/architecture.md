# Architecture

This document explains how the project is wired together.

The app has four main layers:

```text
Streamlit UI
   |
   v
Screens and components
   |
   v
Database helpers and AI pipelines
   |
   v
Supabase database + local AI models
```

## Entry Point

The app starts in `app.py`.

`app.py` does three important things:

1. Configures the Streamlit page.
2. Initializes `st.session_state["login_type"]`.
3. Chooses which screen to show.

Simplified logic:

```python
match st.session_state["login_type"]:
    case "teacher":
        teacher_screen()
    case "student":
        student_screen()
    case None:
        home_screen()
```

This project does not use Streamlit's built-in multipage routing. Instead, it uses session state to decide which screen to render.

## Streamlit Reruns

Streamlit reruns the script from top to bottom after many user actions, such as clicking a button or uploading a file.

That means normal Python variables may disappear between interactions. To keep important data, the app uses `st.session_state`.

Examples:

- `login_type` remembers whether the user selected teacher or student mode.
- `teacher_data` remembers the logged-in teacher.
- `student_data` remembers the logged-in student.
- `attendance_images` stores photos before attendance is confirmed.
- `voice_attendance_results` stores voice results before saving.

For a beginner explanation, read [`learning-concepts.md`](learning-concepts.md).

## Module Responsibilities

### `app.py`

The top-level app router.

It decides whether to show:

- `home_screen()`
- `teacher_screen()`
- `student_screen()`

It also checks the `join-code` query parameter for shared subject links.

### `src/screens/`

Screen files hold page-level flows.

- `home_screen.py`: lets the user choose student or teacher portal.
- `teacher_screen.py`: handles teacher login, registration, dashboard tabs, attendance, subjects, and records.
- `student_screen.py`: handles student face login, registration, dashboard, enrollment, and attendance stats.

### `src/components/`

Component files hold reusable UI pieces.

Examples:

- subject cards
- header and footer
- create subject dialog
- enrollment dialog
- photo upload dialog
- attendance result dialog
- voice attendance dialog

Recent UI polish lives mostly in these components. The home screen uses custom Markdown blocks for the portal cards, the header and footer use small HTML snippets, and `subject_card.py` renders a styled card with gradients, stat pills, and optional footer actions.

### `src/database/`

Database files hold Supabase setup and helper functions.

- `config.py` creates the Supabase client from Streamlit secrets.
- `db.py` contains most database reads and writes.

### `src/pipelines/`

Pipeline files hold AI-specific logic.

- `face_pipeline.py` handles face detection, embeddings, model training, and prediction.
- `voice_pipeline.py` handles voice embeddings and speaker matching.

### `src/ui/`

UI helper files contain shared styling.

- `base_layout.py` injects CSS into Streamlit pages.

The styling layer now defines app-wide color variables, gradient backgrounds, typography, button styles, form input styles, dialog styling, disabled-button styles, and dataframe borders. This keeps most visual rules centralized instead of repeating them in every screen.

### Python Package Markers

The `src` folders include `__init__.py` files. These files mark folders as Python packages, which makes imports such as `from src.screens.home_screen import home_screen` explicit and reliable.

## End-To-End Flows

## Home Screen Route Selection

1. The app starts with `login_type = None`.
2. `home_screen()` renders two portal cards: Student Portal and Teacher Portal.
3. Clicking `Enter Student Portal` or `Enter Teacher Portal` updates `st.session_state["login_type"]`.
4. `st.rerun()` restarts the script.
5. `app.py` now renders the selected screen.

## Teacher Register/Login

1. The teacher opens the teacher portal.
2. `teacher_screen()` shows either login or registration.
3. Registration calls `create_teacher()`.
4. The password is hashed with bcrypt before saving.
5. Login calls `teacher_login()`.
6. If the password matches, teacher data is stored in `st.session_state.teacher_data`.
7. The teacher dashboard appears.

## Student Face Login/Register

1. The student opens the student portal.
2. Streamlit camera input captures a face photo.
3. The image becomes a NumPy array.
4. `predict_attendance()` tries to recognize the face.
5. If a student ID is detected, the app loads that student and stores it in `st.session_state.student_data`.
6. If not recognized, the registration form appears.
7. Registration stores a face embedding and optional voice embedding.
8. `train_classifier()` clears and refreshes the cached face classifier.

## Manual Enrollment

1. A logged-in student clicks `Enroll in Subject`.
2. The student enters a subject code.
3. The app looks up the subject in Supabase.
4. The app checks whether the student is already enrolled.
5. If not, it inserts into `subject_students`.

## Shared-Link Enrollment

1. A teacher shares a link with a `join-code` query parameter.
2. `dialog_share_subject.py` builds the link from `APP_DOMAIN` in Streamlit secrets, falling back to `localhost:8501`.
3. `app.py` reads `st.query_params.get("join-code")`.
4. If the user is not already in student mode, the app switches to the student portal.
5. Once a student is logged in, `auto_enroll_dialog()` opens.
6. The student confirms enrollment.
7. The app inserts into `subject_students`.

## Face Attendance

1. Teacher selects a subject.
2. Teacher adds photos with camera or upload.
3. Photos are stored temporarily in `st.session_state.attendance_images`.
4. Teacher runs face analysis.
5. The app calls `predict_attendance()` for each image.
6. Detected student IDs are compared against students enrolled in the selected subject.
7. The app builds a review table.
8. Attendance is saved only after confirmation.
9. `create_attendance()` inserts rows into `attendance_logs`.

## Voice Attendance

1. Teacher selects a subject.
2. Teacher opens voice attendance.
3. Teacher records classroom audio.
4. The app loads enrolled students with voice profiles.
5. `process_bulk_audio()` splits audio into speech segments.
6. Each segment is compared to stored voice embeddings.
7. Detected students are marked present.
8. Teacher confirms the review table.
9. Attendance rows are inserted into `attendance_logs`.

## Attendance Records Summary

1. Teacher opens `Attendance Records`.
2. The app fetches attendance logs for subjects owned by that teacher.
3. The code builds a pandas DataFrame.
4. Logs are grouped by timestamp, subject, and subject code.
5. The table shows present count and total count.

## Why This Architecture Works For Learning

- UI code is separate from database helper code.
- AI code is separate from Streamlit screen code.
- Dialogs keep important actions focused.
- Supabase access is mostly centralized in `db.py`.
- Session state makes routing understandable without needing a larger web framework.

For a guided file-by-file explanation, read [`code-walkthrough.md`](code-walkthrough.md).
