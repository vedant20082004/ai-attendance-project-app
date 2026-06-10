# Backend Schema

This project uses Supabase as its backend. Supabase gives you a PostgreSQL database and an API that Python can call.

The app stores all long-term data in Supabase:

- teacher accounts
- student profiles
- subject records
- student enrollments
- attendance logs
- face and voice embeddings

## Beginner Database Concepts

### Table

A table is like a spreadsheet. It stores one type of information.

Example: the `students` table stores student records.

### Row

A row is one item in a table.

Example: one student named `Aarav Sharma` is one row in `students`.

### Column

A column is one field in each row.

Example: `name` is a column in `students`.

### Primary Key

A primary key uniquely identifies one row.

This project uses UUID primary keys such as `student_id`, `teacher_id`, and `subject_id`.

### Foreign Key

A foreign key points to a row in another table.

Example: `subjects.teacher_id` points to `teachers.teacher_id`, so the database knows which teacher owns each subject.

### Join Table

A join table connects two other tables.

The `subject_students` table connects students and subjects. A student can enroll in many subjects, and a subject can have many students.

## Important ID Rule

The app treats IDs as UUID strings, not integers.

Example UUID:

```text
6bb6d1bb-9266-46b0-8db3-09d87ddf2cc4
```

Do not convert these IDs with `int()`. They should stay as strings throughout the app.

## Tables

## `teachers`

Stores teacher accounts.

The teacher password is not stored as plain text. It is hashed with bcrypt in `src/database/db.py`.

Required columns:

- `teacher_id` uuid primary key
- `username` text unique not null
- `password` text not null
- `name` text not null
- `created_at` timestamptz default now()

Example row:

| teacher_id | username | password | name | created_at |
| --- | --- | --- | --- | --- |
| UUID string | ananyaroy | bcrypt hash | Ananya Roy | timestamp |

## `students`

Stores student profiles and AI embeddings.

Required columns:

- `student_id` uuid primary key
- `name` text not null
- `face_embedding` jsonb nullable
- `voice_embedding` jsonb nullable
- `created_at` timestamptz default now()

Example row:

| student_id | name | face_embedding | voice_embedding |
| --- | --- | --- | --- |
| UUID string | Hamza Rizvi | `[0.12, -0.44, ...]` | `[0.03, 0.18, ...]` |

`face_embedding` and `voice_embedding` are JSON arrays because embeddings are lists of numbers. Supabase can store those lists naturally in `jsonb` columns.

## `subjects`

Stores teacher-created subjects.

Required columns:

- `subject_id` uuid primary key
- `subject_code` text unique not null
- `name` text not null
- `section` text not null
- `teacher_id` uuid foreign key to `teachers.teacher_id`
- `created_at` timestamptz default now()

Example row:

| subject_id | subject_code | name | section | teacher_id |
| --- | --- | --- | --- | --- |
| UUID string | CS101 | Introduction to Computer Science | A | teacher UUID |

## `subject_students`

Stores which students are enrolled in which subjects.

Required columns:

- `id` bigint identity primary key
- `student_id` uuid foreign key to `students.student_id`
- `subject_id` uuid foreign key to `subjects.subject_id`
- `created_at` timestamptz default now()

Unique constraint:

- `(student_id, subject_id)`

This unique constraint prevents the same student from enrolling in the same subject twice.

Example row:

| id | student_id | subject_id |
| --- | --- | --- |
| 1 | student UUID | subject UUID |

## `attendance_logs`

Stores attendance for each student in each attendance session.

Required columns:

- `id` bigint identity primary key
- `student_id` uuid foreign key to `students.student_id`
- `subject_id` uuid foreign key to `subjects.subject_id`
- `timestamp` timestamptz not null
- `is_present` boolean not null default false
- `created_at` timestamptz default now()

Example row:

| id | student_id | subject_id | timestamp | is_present |
| --- | --- | --- | --- | --- |
| 1 | student UUID | subject UUID | 2026-06-10 10:30:00 | true |

An attendance session means one confirmed attendance run for one subject at one timestamp. The app saves one row per enrolled student for that session.

## Relationships

```text
teachers
  |
  | one teacher owns many subjects
  v
subjects
  |
  | many subjects connect to many students through subject_students
  v
subject_students
  ^
  |
students

attendance_logs connects students + subjects + timestamp + present/absent status
```

## Suggested SQL

Run this in the Supabase SQL editor.

```sql
-- Enables gen_random_uuid(), used for UUID primary keys.
create extension if not exists "pgcrypto";

-- Teacher accounts.
-- Passwords are stored as bcrypt hashes, not plain text.
create table if not exists public.teachers (
  teacher_id uuid primary key default gen_random_uuid(),
  username text not null unique,
  password text not null,
  name text not null,
  created_at timestamptz not null default now()
);

-- Student profiles.
-- Embeddings are stored as jsonb arrays of numbers.
create table if not exists public.students (
  student_id uuid primary key default gen_random_uuid(),
  name text not null,
  face_embedding jsonb,
  voice_embedding jsonb,
  created_at timestamptz not null default now()
);

-- Subjects created by teachers.
-- teacher_id links each subject back to the teacher who created it.
create table if not exists public.subjects (
  subject_id uuid primary key default gen_random_uuid(),
  subject_code text not null unique,
  name text not null,
  section text not null,
  teacher_id uuid not null references public.teachers(teacher_id) on delete cascade,
  created_at timestamptz not null default now()
);

-- Enrollment join table.
-- One row means one student is enrolled in one subject.
create table if not exists public.subject_students (
  id bigint generated always as identity primary key,
  student_id uuid not null references public.students(student_id) on delete cascade,
  subject_id uuid not null references public.subjects(subject_id) on delete cascade,
  created_at timestamptz not null default now(),
  unique (student_id, subject_id)
);

-- Attendance records.
-- One confirmed attendance session creates one row per enrolled student.
create table if not exists public.attendance_logs (
  id bigint generated always as identity primary key,
  student_id uuid not null references public.students(student_id) on delete cascade,
  subject_id uuid not null references public.subjects(subject_id) on delete cascade,
  timestamp timestamptz not null,
  is_present boolean not null default false,
  created_at timestamptz not null default now()
);

-- Helpful indexes for faster lookups.
create index if not exists idx_subjects_teacher_id on public.subjects(teacher_id);
create index if not exists idx_subject_students_student_id on public.subject_students(student_id);
create index if not exists idx_subject_students_subject_id on public.subject_students(subject_id);
create index if not exists idx_attendance_logs_student_id on public.attendance_logs(student_id);
create index if not exists idx_attendance_logs_subject_id on public.attendance_logs(subject_id);
create index if not exists idx_attendance_logs_timestamp on public.attendance_logs(timestamp);

-- Simple local-learning option.
-- For real production apps, use proper RLS policies instead.
alter table public.teachers disable row level security;
alter table public.students disable row level security;
alter table public.subjects disable row level security;
alter table public.subject_students disable row level security;
alter table public.attendance_logs disable row level security;
```

## How The Code Talks To These Tables

The Supabase client is created in `src/database/config.py`.

Most database helper functions are in `src/database/db.py`.

Examples:

- `create_teacher()` inserts into `teachers`.
- `teacher_login()` reads from `teachers`.
- `create_student()` inserts into `students`.
- `create_subject()` inserts into `subjects`.
- `enroll_student_to_subject()` inserts into `subject_students`.
- `create_attendance()` inserts into `attendance_logs`.

For the full app flow, read [`architecture.md`](architecture.md) and [`code-walkthrough.md`](code-walkthrough.md).
