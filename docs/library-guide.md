# Library Guide

This guide explains every main dependency in `requirements.txt`.

Each library is explained in three ways:

- what it is
- where this project uses it
- why the project needs it

## `streamlit`

Streamlit is the web app framework used by this project.

It lets you build an interactive web app with normal Python code. Instead of writing HTML, CSS, JavaScript, routes, and backend handlers separately, you call Streamlit functions like:

```python
st.button("Login")
st.camera_input("Take photo")
st.dataframe(df)
```

Where it is used:

- `app.py`
- all files in `src/screens/`
- most files in `src/components/`
- `src/ui/base_layout.py`

Why it is needed:

- It provides the UI.
- It handles buttons, forms, camera input, audio input, file upload, dialogs, and tables.
- It provides `st.session_state`, which the app uses for login state and routing.
- It provides `@st.cache_resource`, which the AI pipelines use to cache expensive models.

## `numpy`

NumPy is a library for numerical computing.

It is commonly used for arrays, vectors, matrix-like data, and math operations.

Where it is used:

- `src/screens/student_screen.py`
- `src/screens/teacher_screen.py`
- `src/pipelines/face_pipeline.py`
- `src/pipelines/voice_pipeline.py`

Why it is needed:

- Images are converted into NumPy arrays before face recognition.
- Face embeddings are stored and compared as numeric arrays.
- Voice embeddings are compared using dot product similarity.
- Euclidean distance is calculated with NumPy.

Example:

```python
img = np.array(Image.open(photo_source))
```

## `pandas`

pandas is a data analysis library.

It is useful for tables, grouping, sorting, and displaying structured data.

Where it is used:

- `src/screens/teacher_screen.py`
- `src/components/dialog_voice_attendance.py`

Why it is needed:

- The app builds attendance result tables.
- The teacher records screen groups attendance logs by timestamp and subject.
- Streamlit can display pandas DataFrames with `st.dataframe()`.

Example:

```python
df = pd.DataFrame(results)
```

## `scikit-learn`

scikit-learn is a machine learning library.

This project uses its Support Vector Classifier, also called SVC or SVM classifier.

Where it is used:

- `src/pipelines/face_pipeline.py`

Why it is needed:

- It trains a classifier from stored student face embeddings.
- It predicts which student ID a new face embedding most likely belongs to.

Example:

```python
clf = SVC(kernel="linear", probability=True, class_weight="balanced")
```

## `dlib-bin`

dlib is a computer vision and machine learning library.

This project uses `dlib-bin`, which is a packaged build of dlib.

Where it is used:

- `src/pipelines/face_pipeline.py`

Why it is needed:

- It detects faces in images.
- It loads the facial landmark model.
- It loads the face recognition model.
- It creates face descriptors used as embeddings.

Important idea:

dlib provides the low-level face recognition tools. The app wraps those tools in simple functions.

## `face_recognition_models`

`face_recognition_models` provides pretrained model files used by dlib.

Where it is used:

- `src/pipelines/face_pipeline.py`

Why it is needed:

- It gives the path to the pose predictor model.
- It gives the path to the face recognition model.

Example:

```python
face_recognition_models.pose_predictor_model_location()
face_recognition_models.face_recognition_model_location()
```

Without these model files, dlib would not know how to create face embeddings.

## `supabase`

The Supabase Python library lets the app talk to the Supabase backend.

Where it is used:

- `src/database/config.py`
- `src/database/db.py`
- some dialog/screen files that perform direct Supabase queries

Why it is needed:

- It creates the database client.
- It reads and writes teachers, students, subjects, enrollments, and attendance logs.

Example:

```python
supabase.table("students").select("*").execute()
```

The project uses Supabase like a database API. It does not write raw SQL from the app for normal operations.

## `bcrypt`

bcrypt is a password hashing library.

Where it is used:

- `src/database/db.py`

Why it is needed:

- Teacher passwords should not be stored as plain text.
- bcrypt converts a password into a secure hash.
- During login, bcrypt checks whether the typed password matches the stored hash.

Example:

```python
bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())
```

## `segno`

segno is a QR code generation library.

Where it is used:

- subject sharing components

Why it is needed:

- Teachers can share subject join information as a QR code.
- Students can scan or open a shared link to enroll.

The join link uses the `join-code` query parameter.

## `pillow`

Pillow is an image processing library.

Where it is used:

- `src/screens/student_screen.py`
- `src/components/dialog_add_photo.py`

Why it is needed:

- It opens uploaded or camera-captured images.
- It converts image files into image objects.
- Images can then be converted into NumPy arrays for face recognition.

Example:

```python
Image.open(photo_source)
```

## `librosa`

librosa is an audio processing library.

Where it is used:

- `src/pipelines/voice_pipeline.py`

Why it is needed:

- It loads audio bytes.
- It resamples audio to 16000 Hz.
- It splits classroom audio into speech segments.

Example:

```python
audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
segments = librosa.effects.split(audio, top_db=30)
```

## `resemblyzer`

Resemblyzer is a speaker embedding library.

Where it is used:

- `src/pipelines/voice_pipeline.py`

Why it is needed:

- It creates numeric voice embeddings from audio.
- The app compares those embeddings to identify speakers.

Example:

```python
encoder = VoiceEncoder()
embedding = encoder.embed_utterance(wav)
```

## `setuptools<70.0.0`

`setuptools` helps Python install and build packages.

The version is pinned below 70 because some older packages can be sensitive to packaging changes.

Where it matters:

- dependency installation

Why it is needed:

- It helps keep package installation more stable for this learning project.

## How The Libraries Work Together

```text
Streamlit handles UI input
   |
   +-- Pillow opens images
   |     |
   |     +-- NumPy converts images to arrays
   |           |
   |           +-- dlib + face_recognition_models create face embeddings
   |                 |
   |                 +-- scikit-learn predicts student IDs
   |
   +-- librosa loads audio
         |
         +-- Resemblyzer creates voice embeddings
               |
               +-- NumPy compares similarity

Supabase stores teachers, students, subjects, enrollments, attendance logs, and embeddings.
bcrypt hashes teacher passwords.
pandas formats attendance results for display.
segno helps create QR codes for sharing subjects.
```

## Next Reading

- For project concepts, read [`learning-concepts.md`](learning-concepts.md).
- For AI details, read [`ai-pipelines.md`](ai-pipelines.md).
- For database details, read [`backend-schema.md`](backend-schema.md).
