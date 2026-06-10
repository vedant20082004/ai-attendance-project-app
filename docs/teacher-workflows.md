# Teacher Workflows

This document explains the teacher side of the project from login to attendance records.

For the overall app architecture, read [`architecture.md`](architecture.md). For database details, read [`backend-schema.md`](backend-schema.md).

## Teacher Portal

The teacher portal is controlled by `src/screens/teacher_screen.py`.

The main function is:

```python
teacher_screen()
```

It decides whether to show:

- teacher dashboard
- teacher login
- teacher registration

## Teacher Registration

Teacher registration collects:

- username
- teacher name
- password
- password confirmation

The function `register_teacher()` checks:

1. All required fields are filled.
2. The username is not already taken.
3. The password and confirmation match.

If validation passes, the app calls:

```python
create_teacher(username, password, name)
```

## Password Hashing With bcrypt

The app does not store plain teacher passwords.

In `src/database/db.py`, the password is hashed:

```python
def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()
```

A hash is a one-way representation of the password. During login, the app checks whether the entered password matches the stored hash:

```python
def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())
```

This is an important security concept, even though the overall project is still only a learning app.

## Teacher Login

Teacher login collects:

- username
- password

The app calls:

```python
teacher_login(username, password)
```

That function:

1. Looks up the teacher by username in Supabase.
2. Reads the stored password hash.
3. Uses bcrypt to verify the entered password.
4. Returns the teacher row if the password is correct.
5. Returns `None` if login fails.

On successful login, the app stores:

```python
st.session_state.user_role = "teacher"
st.session_state.teacher_data = teacher
st.session_state.is_logged_in = True
```

This session state is what keeps the teacher logged in while Streamlit reruns.

## Teacher Dashboard

After login, `teacher_dashboard()` appears.

The dashboard has three tabs:

- Take Attendance
- Manage Subjects
- Attendance Records

The active tab is stored in:

```python
st.session_state.current_teacher_tab
```

This is not a browser tab. It is a Streamlit UI state value.

## Manage Subjects

The `Manage Subjects` tab lets the teacher create and share subjects.

## Create A Subject

The create subject dialog asks for:

- subject code
- subject name
- section

The app inserts a row into the `subjects` table:

```python
create_subject(subject_code, name, section, teacher_id)
```

The `teacher_id` comes from the logged-in teacher:

```python
st.session_state.teacher_data["teacher_id"]
```

Each subject belongs to one teacher.

## Subject Cards

Subjects are displayed with `subject_card()`.

Each card shows:

- subject name
- subject code
- section
- number of enrolled students
- number of attendance sessions/classes

The counts come from `get_teacher_subjects()`.

## Share Subject

The teacher can share a subject using:

- the subject code
- a join link
- a QR code

Students can manually enter the subject code or open the shared link.

The shared link uses the query parameter:

```text
join-code
```

When the app sees this query parameter, it guides the student into quick enrollment.

## Take Photo Attendance

Photo attendance is the main teacher workflow.

## Step 1: Select A Subject

The teacher selects one of their subjects from a dropdown.

The selected subject ID is used for enrollment lookup and attendance saving.

## Step 2: Add Photos

The teacher clicks `Add Photos`.

The app opens `add_photos_dialog()`.

Photos can come from:

- camera input
- uploaded image files

Images are stored temporarily in:

```python
st.session_state.attendance_images
```

They are not saved to Supabase. They are used for the current attendance run.

## Step 3: Run Face Analysis

The teacher clicks `Run Face Analysis`.

For each image:

1. The image is converted to RGB.
2. The image becomes a NumPy array.
3. `predict_attendance()` is called.
4. Detected student IDs are collected.

The app then loads enrolled students for the selected subject:

```python
supabase.table("subject_students").select("*, students(*)")
```

This returns enrollment rows plus related student data.

## Step 4: Compare Detected Students With Enrolled Students

The app only marks students from the selected subject.

For each enrolled student:

- if their student ID was detected, they are marked present
- otherwise, they are marked absent

This is important because the face pipeline may know students from the whole database, but attendance should only apply to the selected subject.

## Step 5: Review Attendance

The app builds a pandas DataFrame with:

- name
- ID
- source photo
- status

Then it opens `attendance_result_dialog()`.

The teacher can:

- discard
- confirm and save

## Step 6: Confirm And Save

Attendance is saved only after confirmation.

The app inserts one row per enrolled student into `attendance_logs`.

Each row includes:

- `student_id`
- `subject_id`
- `timestamp`
- `is_present`

This creates one attendance session.

## Voice Attendance

Voice attendance is optional.

The teacher opens it from the `Take Attendance` tab.

## Voice Attendance Requirements

Voice attendance only works for enrolled students who have a stored `voice_embedding`.

A student gets a voice embedding only if they record audio during student registration.

## Voice Attendance Flow

1. Teacher records classroom audio.
2. The app loads enrolled students for the selected subject.
3. The app builds a candidate dictionary of student IDs and voice embeddings.
4. `process_bulk_audio()` splits the audio into speech segments.
5. Each segment is compared against stored voice embeddings.
6. Matching students are marked present.
7. The teacher reviews the result.
8. Logs are saved only after confirmation.

If no enrolled students have voice profiles, the app shows an error.

## Attendance Records

The `Attendance Records` tab shows a summary table.

The app calls:

```python
get_attendance_for_teacher(teacher_id)
```

Then it uses pandas to group records by:

- timestamp
- subject
- subject code

The displayed table shows:

- time
- subject
- subject code
- present count / total count

This is a session summary. It is not currently a detailed per-student audit screen.

## Teacher Workflow Learning Points

- Teacher passwords are hashed before storage.
- Streamlit session state keeps the teacher logged in.
- Subjects belong to teachers through `teacher_id`.
- Enrollment is stored separately in `subject_students`.
- Attendance saves one row per enrolled student.
- The teacher confirms attendance before writing logs.
