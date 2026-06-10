# Backend Schema

This project uses Supabase as its backend. The code in `src/database/db.py` assumes a small relational schema.

## Tables

### `teachers`

Used for teacher account login and registration.

Required columns:

- `teacher_id` uuid primary key
- `username` text unique not null
- `password` text not null
- `name` text not null
- `created_at` timestamptz default now()

### `students`

Stores student identity and AI embeddings.

Required columns:

- `student_id` uuid primary key
- `name` text not null
- `face_embedding` jsonb nullable
- `voice_embedding` jsonb nullable
- `created_at` timestamptz default now()

### `subjects`

Stores teacher-created subjects.

Required columns:

- `subject_id` uuid primary key
- `subject_code` text unique not null
- `name` text not null
- `section` text not null
- `teacher_id` uuid foreign key to `teachers.teacher_id`
- `created_at` timestamptz default now()

### `subject_students`

Join table for student enrollment.

Required columns:

- `id` bigint identity primary key
- `student_id` uuid foreign key to `students.student_id`
- `subject_id` uuid foreign key to `subjects.subject_id`
- `created_at` timestamptz default now()

Unique constraint:

- `(student_id, subject_id)`

### `attendance_logs`

Stores attendance records for each student in each subject session.

Required columns:

- `id` bigint identity primary key
- `student_id` uuid foreign key to `students.student_id`
- `subject_id` uuid foreign key to `subjects.subject_id`
- `timestamp` timestamptz not null
- `is_present` boolean not null default false
- `created_at` timestamptz default now()

## Suggested SQL

```sql
-- Enable UUID support
create extension if not exists "pgcrypto";

create table if not exists public.teachers (
  teacher_id uuid primary key default gen_random_uuid(),
  username text not null unique,
  password text not null,
  name text not null,
  created_at timestamptz not null default now()
);

create table if not exists public.students (
  student_id uuid primary key default gen_random_uuid(),
  name text not null,
  face_embedding jsonb,
  voice_embedding jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.subjects (
  subject_id uuid primary key default gen_random_uuid(),
  subject_code text not null unique,
  name text not null,
  section text not null,
  teacher_id uuid not null references public.teachers(teacher_id) on delete cascade,
  created_at timestamptz not null default now()
);

create table if not exists public.subject_students (
  id bigint generated always as identity primary key,
  student_id uuid not null references public.students(student_id) on delete cascade,
  subject_id uuid not null references public.subjects(subject_id) on delete cascade,
  created_at timestamptz not null default now(),
  unique (student_id, subject_id)
);

create table if not exists public.attendance_logs (
  id bigint generated always as identity primary key,
  student_id uuid not null references public.students(student_id) on delete cascade,
  subject_id uuid not null references public.subjects(subject_id) on delete cascade,
  timestamp timestamptz not null,
  is_present boolean not null default false,
  created_at timestamptz not null default now()
);

-- Helpful indexes
create index if not exists idx_subjects_teacher_id on public.subjects(teacher_id);
create index if not exists idx_subject_students_student_id on public.subject_students(student_id);
create index if not exists idx_subject_students_subject_id on public.subject_students(subject_id);
create index if not exists idx_attendance_logs_student_id on public.attendance_logs(student_id);
create index if not exists idx_attendance_logs_subject_id on public.attendance_logs(subject_id);
create index if not exists idx_attendance_logs_timestamp on public.attendance_logs(timestamp);

-- Optional: disable RLS for quick local testing
alter table public.teachers disable row level security;
alter table public.students disable row level security;
alter table public.subjects disable row level security;
alter table public.subject_students disable row level security;
alter table public.attendance_logs disable row level security;
```

## Important Notes

- The app treats IDs as UUID strings, not integers.
- `face_embedding` and `voice_embedding` are stored as JSON arrays.
- Attendance is saved one row per enrolled student per session.
