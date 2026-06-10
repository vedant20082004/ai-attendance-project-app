# Code Walkthrough

This guide walks through the project from `app.py` into the main screens, components, database helpers, and AI pipelines.

It is written for beginners who want to understand how the files work together.

## Start At `app.py`

The app begins in:

```text
app.py
```

It imports three screens:

```python
from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen
```

It also imports quick enrollment:

```python
from src.components.dialog_auto_enroll import auto_enroll_dialog
```

## Page Setup

Inside `main()`, the app sets Streamlit page settings:

```python
st.set_page_config(
    page_title="AI Attendance System",
    page_icon="..."
)
```

This controls browser tab title and icon.

## Session-State Routing

The app checks whether `login_type` exists:

```python
if "login_type" not in st.session_state:
    st.session_state["login_type"] = None
```

Then it chooses a screen:

```python
match st.session_state["login_type"]:
    case "teacher":
        teacher_screen()
    case "student":
        student_screen()
    case None:
        home_screen()
```

This is the app's routing system.

Instead of URLs like `/teacher` or `/student`, it uses:

```text
st.session_state["login_type"]
```

## Shared Join Link Handling

At the end of `main()`, the app checks:

```python
join_code = st.query_params.get("join-code")
```

If a shared link contains `join-code`, the app moves the user to the student flow and eventually opens the quick enrollment dialog.

This is how teacher sharing connects to student enrollment.

The share dialog builds that link using:

```python
app_domain = st.secrets.get("APP_DOMAIN", "localhost:8501")
join_url = f"{app_domain}/?join-code={subject_code}"
```

So `APP_DOMAIN` is optional. If it is not configured, shared links point to the local app.

## Home Screen

File:

```text
src/screens/home_screen.py
```

The home screen shows two choices:

- Student Portal
- Teacher Portal

Each portal is displayed as a styled card with an image, short description, and full-width button.

When a user clicks `Enter Student Portal`, the app sets:

```python
st.session_state["login_type"] = "student"
```

When a user clicks `Enter Teacher Portal`, the app sets:

```python
st.session_state["login_type"] = "teacher"
```

Then it calls `st.rerun()`, so `app.py` runs again and shows the correct screen.

## Teacher Screen

File:

```text
src/screens/teacher_screen.py
```

The main function is:

```python
teacher_screen()
```

It decides what to show:

- if `teacher_data` exists, show dashboard
- if login mode is active, show login
- if register mode is active, show registration

## Teacher Registration Code Path

Teacher registration uses:

```python
register_teacher(...)
```

That function validates input and calls:

```python
create_teacher(...)
```

`create_teacher()` lives in:

```text
src/database/db.py
```

It hashes the password and inserts a teacher row into Supabase.

## Teacher Login Code Path

Teacher login uses:

```python
login_teacher(username, password)
```

That calls:

```python
teacher_login(username, password)
```

If login succeeds, the app stores teacher information in session state:

```python
st.session_state.teacher_data = teacher
```

This makes the dashboard appear on the next rerun.

## Teacher Dashboard Tabs

The teacher dashboard uses:

```python
st.session_state.current_teacher_tab
```

Possible values:

- `take_attendance`
- `manage_subjects`
- `attendance_records`

The selected value decides which tab content function runs.

## Manage Subjects Code Path

The manage subjects tab calls:

```python
get_teacher_subjects(teacher_id)
```

That function loads subjects from Supabase and calculates:

- total students
- total classes

Creating a subject opens:

```python
create_subject_dialog(teacher_id)
```

The dialog calls:

```python
create_subject(...)
```

## Photo Attendance Code Path

The photo attendance flow starts in:

```python
teacher_tab_take_attendance()
```

Important state:

```python
st.session_state.attendance_images
```

Photos are added by:

```python
add_photos_dialog()
```

When the teacher runs analysis, each image is passed to:

```python
predict_attendance(img_np)
```

That function lives in:

```text
src/pipelines/face_pipeline.py
```

The teacher screen then compares detected student IDs with enrolled students for the selected subject.

Finally it opens:

```python
attendance_result_dialog(...)
```

Attendance is saved only if the teacher confirms.

## Voice Attendance Code Path

Voice attendance opens:

```python
voice_attendance_dialog(selected_subject_id)
```

That dialog:

1. Records audio with Streamlit.
2. Loads enrolled students from Supabase.
3. Builds a dictionary of student voice embeddings.
4. Calls `process_bulk_audio()`.
5. Builds a review table.
6. Saves only after confirmation.

The AI work happens in:

```text
src/pipelines/voice_pipeline.py
```

## Student Screen

File:

```text
src/screens/student_screen.py
```

The main function is:

```python
student_screen()
```

It checks:

```python
if "student_data" in st.session_state:
    student_dashboard()
    return
```

If a student is logged in, the dashboard appears.

If not, the face login and registration flow appears.

## Student Face Login Code Path

The student takes a camera photo:

```python
photo_source = st.camera_input("Position your face in the center")
```

The image is converted:

```python
img = np.array(Image.open(photo_source))
```

Then the app calls:

```python
predict_attendance(img)
```

If one student is detected, the app loads that student and stores:

```python
st.session_state.student_data = student
```

## Student Registration Code Path

If the face is not recognized, the registration form appears.

The app creates a face embedding:

```python
encodings = get_face_embeddings(img)
```

If audio is provided, it creates a voice embedding:

```python
voice_emb = get_voice_embedding(audio_data.read())
```

Then it creates the student:

```python
create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)
```

After creation, it calls:

```python
train_classifier()
```

This refreshes the cached face classifier.

## Student Dashboard Code Path

The dashboard loads:

```python
subjects = get_student_subjects(student_id)
logs = get_student_attendance(student_id)
```

Then it calculates stats:

- total attendance rows
- attended rows where `is_present` is true

Students can also open:

```python
enroll_dialog()
```

or unenroll from a subject.

## Database Helper Layer

File:

```text
src/database/db.py
```

This file contains functions such as:

- `create_teacher()`
- `teacher_login()`
- `get_all_students()`
- `create_student()`
- `create_subject()`
- `get_teacher_subjects()`
- `enroll_student_to_subject()`
- `get_student_subjects()`
- `create_attendance()`

The goal is to keep database operations in one place.

## Supabase Client

File:

```text
src/database/config.py
```

It creates the Supabase client:

```python
supabase: Client = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)
```

If secrets are missing, the app cannot connect to Supabase.

## Face Pipeline Layer

File:

```text
src/pipelines/face_pipeline.py
```

Important functions:

- `load_dlib_models()`
- `get_face_embeddings()`
- `get_trained_model()`
- `train_classifier()`
- `predict_attendance()`

This file should handle face recognition logic, not UI layout.

## Voice Pipeline Layer

File:

```text
src/pipelines/voice_pipeline.py
```

Important functions:

- `load_voice_encoder()`
- `get_voice_embedding()`
- `identify_speaker()`
- `process_bulk_audio()`

This file should handle voice recognition logic, not teacher/student screen layout.

## Styling Layer

File:

```text
src/ui/base_layout.py
```

This file injects CSS into Streamlit.

It controls:

- background colors
- fonts
- button styles
- input styles
- dialog styling
- dataframe styling
- disabled button styling
- gradient home and dashboard backgrounds
- card-like column styling on the home screen

The header and footer components also use small HTML snippets for the university logo and the footer text. The subject card component uses inline HTML for its card layout and stat pills.

## Package Marker Files

The project now includes `__init__.py` files inside the `src` package folders.

Examples:

```text
src/__init__.py
src/screens/__init__.py
src/components/__init__.py
```

These files make Python treat those folders as packages. That supports imports like:

```python
from src.components.header import header_home
```

## Mental Model

```text
User clicks something in Streamlit
   |
   v
screen function handles the interaction
   |
   +-- calls a component for focused UI
   +-- calls db.py for database work
   +-- calls pipeline files for AI work
   |
   v
session state updates or Supabase data changes
   |
   v
Streamlit reruns and redraws the app
```

## Next Reading

- For teacher details, read [`teacher-workflows.md`](teacher-workflows.md).
- For student details, read [`student-workflows.md`](student-workflows.md).
- For AI details, read [`ai-pipelines.md`](ai-pipelines.md).
