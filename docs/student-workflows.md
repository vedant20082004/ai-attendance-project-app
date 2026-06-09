# Student Workflows

This document explains the student side of SnapClass.

## Student Login

Students log in with the camera.

Flow:

1. Open student portal
2. Capture face image
3. AI checks whether the face exists in the student table
4. If found, student logs in
5. If not found, student can register

## Student Registration

If the face is not recognized:

1. Enter name
2. Optionally record a voice sample
3. The app stores face and voice embeddings
4. Student is logged in automatically

## Student Dashboard

Students can see:

- enrolled subjects
- total attendance count
- attended count
- unenroll button for each subject

## Enroll in a Subject

Students can enroll in two ways:

- manually enter a subject code
- open a teacher-shared join link

Both flows insert a row into `subject_students`.

## Attendance View

Student attendance is computed from `attendance_logs`.

For each subject:

- total = number of attendance rows
- attended = number of rows where `is_present` is true

## Unenroll

Students can remove themselves from a subject.

That deletes the matching row from `subject_students`.
