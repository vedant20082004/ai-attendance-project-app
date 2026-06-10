# Learning Concepts

This guide explains the beginner concepts used across the project.

You can read this before the code walkthrough if terms like session state, embedding, classifier, or foreign key are new to you.

## Virtual Environment

A virtual environment is a private Python setup for one project.

This project uses:

```powershell
py -3.11 -m venv .venv
```

The `.venv` folder keeps installed libraries separate from other projects on your computer.

Why it matters:

- Different projects can use different package versions.
- You avoid breaking global Python packages.
- It makes setup easier to repeat.

## Package Dependencies

A dependency is a library your project needs.

This project lists dependencies in:

```text
requirements.txt
```

Installing dependencies:

```powershell
pip install -r requirements.txt
```

For every dependency explanation, read [`library-guide.md`](library-guide.md).

## Streamlit Reruns

Streamlit reruns your Python script from top to bottom after many user interactions.

Examples:

- clicking a button
- uploading a file
- taking a camera photo
- changing a selectbox

This is different from many web frameworks where only a small callback runs.

Because of reruns, the app needs a way to remember important values.

## `st.session_state`

`st.session_state` is Streamlit's memory for the current browser session.

This project uses it for:

- selected portal: `login_type`
- logged-in teacher: `teacher_data`
- logged-in student: `student_data`
- current teacher dashboard tab: `current_teacher_tab`
- attendance photos: `attendance_images`
- voice attendance review data: `voice_attendance_results`
- current photo dialog tab: `photo_tab`

Example:

```python
st.session_state["login_type"] = "student"
```

Without session state, the app would forget who is logged in every time Streamlit reruns.

## Dialogs

A dialog is a popup-like UI element.

Streamlit supports dialogs with:

```python
@st.dialog("Dialog Title")
```

This project uses dialogs for focused actions:

- create subject
- enroll in subject
- quick enrollment
- add photos
- show attendance results
- voice attendance

Dialogs are useful when an action needs confirmation or extra input without changing the whole page.

## Database Tables

A database table stores rows of structured data.

This project uses tables such as:

- `teachers`
- `students`
- `subjects`
- `subject_students`
- `attendance_logs`

Each table has columns that describe the data stored in each row.

## Primary Keys

A primary key uniquely identifies one row in a table.

Examples:

- `teacher_id`
- `student_id`
- `subject_id`

This project uses UUID strings for these IDs.

## Foreign Keys

A foreign key links one table to another.

Example:

```text
subjects.teacher_id -> teachers.teacher_id
```

This means each subject belongs to a teacher.

Foreign keys help the database understand relationships.

## Join Tables

A join table connects two tables in a many-to-many relationship.

This project uses:

```text
subject_students
```

It connects:

- students
- subjects

Why it is needed:

- One student can join many subjects.
- One subject can contain many students.

## Password Hashing

Password hashing converts a password into a one-way hash.

The app uses bcrypt.

Plain password:

```text
hello123
```

Stored hash:

```text
$2b$12$...
```

The app does not need to decrypt the hash. During login, bcrypt checks whether the typed password matches the stored hash.

## Image Arrays

Computers process images as numbers.

When the app receives a camera photo, it uses Pillow to open the image and NumPy to convert it into an array.

Example:

```python
img = np.array(Image.open(photo_source))
```

The face recognition model reads this numeric image data.

## Embeddings

An embedding is a numeric representation of something.

In this project:

- a face embedding represents a student's face
- a voice embedding represents a student's voice

Example idea:

```text
Face image -> [0.12, -0.44, 0.08, ...]
Voice audio -> [0.03, 0.18, -0.22, ...]
```

The numbers do not make sense to humans directly, but they are useful for comparison.

## Face Embeddings

The face model creates a 128-number embedding for each detected face.

Two photos of the same person should produce embeddings that are close to each other.

Photos of different people should produce embeddings that are farther apart.

The app stores face embeddings in:

```text
students.face_embedding
```

## Voice Embeddings

The voice model creates an embedding from audio.

Two recordings of the same speaker should produce embeddings with high similarity.

The app stores voice embeddings in:

```text
students.voice_embedding
```

## Classifiers

A classifier predicts a label.

In this app, the label is a student ID.

The face pipeline trains an SVM classifier using:

- face embeddings as input
- student IDs as labels

Then a new face embedding can be classified as the most likely student.

## Similarity Thresholds

A threshold is a cutoff value.

The app uses thresholds to decide whether a match is good enough.

Face threshold:

```text
0.6 Euclidean distance
```

Lower distance means more similar.

Voice threshold:

```text
0.65 dot product similarity
```

Higher similarity means more similar.

Thresholds matter because AI predictions can be uncertain.

## Caching Expensive Models

Some models are slow to load.

The app uses:

```python
@st.cache_resource
```

This tells Streamlit to load the resource once and reuse it.

The app caches:

- dlib face models
- face classifier data
- Resemblyzer voice encoder

This makes reruns faster.

## Attendance Session

An attendance session means one confirmed attendance run for one subject at one timestamp.

If a subject has 10 enrolled students, one confirmed session creates 10 rows in `attendance_logs`.

Each row says whether one student was present or absent.

## Learning Path

After this page:

1. Read [`library-guide.md`](library-guide.md).
2. Read [`backend-schema.md`](backend-schema.md).
3. Read [`architecture.md`](architecture.md).
4. Read [`code-walkthrough.md`](code-walkthrough.md).
