# Developer Guide

This document is for anyone extending the codebase.

## Important Files

- `app.py`: top-level app router
- `src/database/db.py`: all database operations
- `src/pipelines/face_pipeline.py`: face recognition logic
- `src/pipelines/voice_pipeline.py`: voice recognition logic
- `src/screens/teacher_screen.py`: teacher UI
- `src/screens/student_screen.py`: student UI

## How the Code Is Organized

The app is split into small, focused modules:

- screens handle page-level UI
- components handle reusable dialogs and cards
- database helpers keep Supabase calls in one place
- pipelines handle AI-specific logic
- UI helpers keep the layout styling together

## Safe Extension Rules

- Keep database reads/writes in `db.py`
- Keep AI logic in the pipeline modules
- Keep page flow in the screen modules
- Keep shared visual pieces in `components/`
- Do not mix SQL shape changes into UI code

## Recommended Change Order

1. Understand the existing flow
2. Update the database schema if needed
3. Adjust helper functions
4. Update screen logic
5. Test teacher and student flows separately

## Testing Checklist

- App starts without import errors
- Secrets file is found
- Supabase tables exist
- Teacher registration works
- Teacher login works
- Subject creation works
- Student face login works
- Student registration works
- Enrollment works
- Attendance review dialog works
- Attendance save works

## Maintenance Notes

- IDs are UUID strings from Supabase
- Attendance is saved one row per student per session
- Face embeddings and voice embeddings are stored as JSON arrays
- The app depends on Streamlit session state for navigation
