# Student Workflows

This document explains the student side of the project.

For overall architecture, read [`architecture.md`](architecture.md). For AI details, read [`ai-pipelines.md`](ai-pipelines.md).

## Student Portal

The student portal is controlled by `src/screens/student_screen.py`.

The main function is:

```python
student_screen()
```

It decides whether to show:

- student dashboard, if the student is logged in
- face login and registration flow, if the student is not logged in

## Student Face Login

Students log in with the camera.

The camera input is:

```python
photo_source = st.camera_input("Position your face in the center")
```

When the student takes a photo:

1. Pillow opens the photo.
2. NumPy converts it into an array.
3. `predict_attendance()` checks whether the face matches a known student.

The code receives:

```python
detected, all_ids, num_faces = predict_attendance(img)
```

Meaning:

- `detected`: recognized student IDs
- `all_ids`: known student IDs in the trained model
- `num_faces`: number of faces detected in the image

## Face Login Outcomes

### No face found

If `num_faces == 0`, the app shows a warning.

Common causes:

- bad lighting
- face too far from camera
- camera blocked
- face not centered

### Multiple faces found

If `num_faces > 1`, the app shows a warning.

Student login expects one face because it is trying to identify one student account.

### Face recognized

If the face is recognized, the app finds the student row in Supabase and stores:

```python
st.session_state.is_logged_in = True
st.session_state.user_role = "student"
st.session_state.student_data = student
```

Then the dashboard appears.

### Face not recognized

If no match is accepted, the app shows the registration form.

## New Student Registration

Student registration appears when a face is not recognized.

The student enters:

- name
- optional voice recording

## Face Embedding Storage

When the student creates an account, the app calls:

```python
encodings = get_face_embeddings(img)
```

If a face embedding is created, it is converted to a list:

```python
face_emb = encodings[0].tolist()
```

Then it is stored in the `students` table:

```python
create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)
```

The face embedding is a numeric representation of the student's face.

## Optional Voice Enrollment

Voice enrollment is optional.

If the student records audio, the app calls:

```python
voice_emb = get_voice_embedding(audio_data.read())
```

The voice embedding is stored in `students.voice_embedding`.

Students without voice embeddings can still use face login and photo attendance, but they cannot be recognized by voice attendance.

## Classifier Refresh

After a new student is created, the app calls:

```python
train_classifier()
```

This clears and rebuilds the cached face classifier data.

That matters because the newly registered student's face embedding should be available for future recognition.

## Student Dashboard

After login, the student dashboard shows:

- welcome message
- enrolled subjects
- attendance stats
- unenroll button for each subject

The app loads:

```python
subjects = get_student_subjects(student_id)
logs = get_student_attendance(student_id)
```

## Attendance Stats

The dashboard calculates attendance stats from `attendance_logs`.

For each subject:

- `total` means total attendance rows for that student and subject
- `attended` means rows where `is_present` is true

Example:

```text
Total: 5
Attended: 4
```

This means the teacher confirmed attendance 5 times for that subject, and the student was present 4 times.

## Manual Enrollment

Students can manually enroll with a subject code.

Flow:

1. Student clicks `Enroll in Subject`.
2. Student enters a subject code such as `CS101`.
3. The app searches the `subjects` table.
4. The app checks whether the student is already enrolled.
5. If not, it inserts into `subject_students`.

The inserted row connects:

- `student_id`
- `subject_id`

## Auto Enrollment From Shared Link

Teachers can share a join link containing:

```text
join-code
```

When a student opens that link:

1. `app.py` reads the query parameter.
2. The app switches to student mode if needed.
3. The student logs in.
4. `auto_enroll_dialog()` asks whether they want to join the subject.
5. If confirmed, the app inserts into `subject_students`.

This flow is useful because students do not need to manually type the subject code.

## Unenroll

Students can unenroll from a subject on the dashboard.

The app calls:

```python
unenroll_student_to_subject(student_id, subject_id)
```

This deletes the matching row from `subject_students`.

Important:

- It removes the enrollment.
- It does not delete the student.
- It does not delete the subject.
- It does not delete previous attendance logs.

## Student Workflow Learning Points

- Student login uses face recognition instead of passwords.
- Face and voice data are stored as numeric embeddings.
- Session state keeps the student logged in.
- Enrollment is stored in a join table.
- Attendance stats come from saved attendance logs.
- Voice attendance only works if the student registered a voice profile.
