# Developer Guide

This guide is for anyone who wants to extend or maintain the project.

The project is intentionally small and direct so learners can understand it. Try to keep changes in the correct layer instead of mixing UI, database, and AI logic together.

## Important Files

- `app.py`: top-level Streamlit entrypoint and session-state router
- `src/screens/teacher_screen.py`: teacher login, registration, dashboard, attendance, subjects, records
- `src/screens/student_screen.py`: student face login, registration, dashboard, enrollment
- `src/screens/home_screen.py`: first screen where the user chooses student or teacher mode
- `src/components/`: dialogs, subject cards, header, and footer
- `src/database/config.py`: Supabase client setup
- `src/database/db.py`: database helper functions
- `src/pipelines/face_pipeline.py`: face detection, embeddings, classifier, prediction
- `src/pipelines/voice_pipeline.py`: voice embeddings and speaker matching
- `src/ui/base_layout.py`: shared CSS styling
- `docs/`: project documentation
- `src/**/__init__.py`: package marker files that make folder imports explicit

## Keep Responsibilities Separate

### UI changes

Put page-level UI changes in `src/screens/`.

Put reusable dialogs or cards in `src/components/`.

Examples:

- Add a new teacher dashboard section in `teacher_screen.py`.
- Add a new reusable dialog in `src/components/`.
- Update subject card layout in `subject_card.py`.

### Database changes

Put database reads and writes in `src/database/db.py` when possible.

If you add a new table or column, update:

- Supabase schema
- `docs/backend-schema.md`
- any helper functions in `db.py`
- any UI that reads or writes the new field

### AI behavior changes

Put face-recognition changes in `src/pipelines/face_pipeline.py`.

Put voice-recognition changes in `src/pipelines/voice_pipeline.py`.

Examples:

- Change face threshold `0.6`.
- Change voice threshold `0.65`.
- Add more debugging output for embedding generation.

### Styling changes

Put shared visual styling in `src/ui/base_layout.py`.

Avoid scattering large CSS blocks across screen files unless the style belongs only to one local component.

Current styling is split like this:

- `base_layout.py` handles app-wide colors, gradients, typography, buttons, inputs, dialogs, alerts, and dataframe styling.
- `header.py` and `footer.py` use small HTML snippets for the logo and footer.
- `home_screen.py` uses local Markdown/HTML for the two portal cards.
- `subject_card.py` uses local HTML for subject card layout and stat pills.

## Recommended Change Order

1. Understand the workflow in the docs.
2. Find the correct layer.
3. Update the smallest number of files.
4. Test the teacher flow.
5. Test the student flow.
6. Update docs if behavior changed.

## Example: Add A New Subject Field

Suppose you want subjects to include a semester.

Update in this order:

1. Add a `semester` column to the `subjects` table in Supabase.
2. Update [`backend-schema.md`](backend-schema.md).
3. Update `create_subject()` in `src/database/db.py` to insert `semester`.
4. Update `dialog_create_subject.py` to collect semester.
5. Update teacher subject cards if you want to display it.
6. Test subject creation.

## Example: Change Face Attendance Sensitivity

The face threshold is in `src/pipelines/face_pipeline.py`:

```python
resemblance_threshold = 0.6
```

Lower values are stricter. Higher values are more permissive.

If you change this:

- test with the same student in different lighting
- test with different students
- document the change in [`ai-pipelines.md`](ai-pipelines.md)

## Example: Change Voice Attendance Sensitivity

The voice threshold defaults to:

```python
threshold=0.65
```

It is used in `identify_speaker()` and `process_bulk_audio()`.

If you change it:

- test with clean audio
- test with noisy audio
- test with multiple students
- update [`ai-pipelines.md`](ai-pipelines.md)

## Example: Add A Dashboard Statistic

If the statistic is for students:

1. Check what data is already loaded in `student_dashboard()`.
2. If needed, add a helper in `db.py`.
3. Compute the stat in the screen.
4. Display it through a component or local UI block.

If the statistic is for teachers:

1. Check `teacher_dashboard()` and dashboard tab functions.
2. Prefer adding data access in `db.py`.
3. Keep pandas summary logic near the records view if it is only for display.

## Example: Add A Troubleshooting Check

If you discover a new common error:

1. Add the cause and fix to [`troubleshooting.md`](troubleshooting.md).
2. Link to setup, schema, or AI docs if relevant.
3. Keep the explanation beginner-friendly.

## Testing Checklist

After changes, test the flows related to your change.

General checklist:

- App starts with `streamlit run app.py`.
- Secrets are loaded.
- Supabase tables exist.
- Teacher registration works.
- Teacher login works.
- Subject creation works.
- Student registration works.
- Student face login works.
- Manual enrollment works.
- Shared-link enrollment works.
- Photo attendance review appears.
- Attendance saves after confirmation.
- Attendance records display.
- Voice attendance handles missing voice profiles clearly.
- Home screen shows the `Enter Student Portal` and `Enter Teacher Portal` cards correctly.
- Shared subject links use `APP_DOMAIN` when configured.

## Documentation Checklist

Update docs whenever behavior changes.

Useful docs to update:

- setup changes: `getting-started.md`
- schema changes: `backend-schema.md`
- architecture changes: `architecture.md`
- AI logic changes: `ai-pipelines.md`
- workflow changes: `teacher-workflows.md` or `student-workflows.md`
- new errors: `troubleshooting.md`

## Maintenance Notes

- Student IDs and teacher IDs are UUID strings.
- Attendance is saved one row per enrolled student per attendance session.
- Face and voice embeddings are JSON arrays in Supabase.
- The app depends heavily on Streamlit session state.
- This is a learning project, so keep code and docs readable.
