# AI Pipelines

This document explains the face and voice logic in beginner-friendly language.

The AI code lives in:

- `src/pipelines/face_pipeline.py`
- `src/pipelines/voice_pipeline.py`

For library explanations, read [`library-guide.md`](library-guide.md). For beginner AI terms like embedding, classifier, and threshold, read [`learning-concepts.md`](learning-concepts.md).

## Big Idea

The app does not store actual face images or voice recordings for recognition. It stores embeddings.

An embedding is a list of numbers that represents important features of something.

- A face embedding represents a face.
- A voice embedding represents a voice.

The app compares new embeddings against stored embeddings to decide who was recognized.

## Face Pipeline

File:

```text
src/pipelines/face_pipeline.py
```

## What The Face Pipeline Does

The face pipeline:

1. Detects faces in an image.
2. Converts each face into a 128-number embedding.
3. Loads stored student face embeddings from Supabase.
4. Trains an SVM classifier.
5. Predicts which student a new face may belong to.
6. Confirms the prediction with a distance threshold.

## Step 1: Image Becomes A NumPy Array

Streamlit and Pillow load a photo. The code converts it into a NumPy array:

```python
img = np.array(Image.open(photo_source))
```

A NumPy array is a grid of pixel values. Computer vision models work with numbers, not image files directly.

## Step 2: dlib Detects Faces

The function `get_face_embeddings(image_np)` calls:

```python
faces = detector(image_np, 1)
```

The detector finds face rectangles in the image.

Possible results:

- no faces
- one face
- multiple faces

Student login expects exactly one face. Teacher attendance photos can contain multiple faces.

## Step 3: Landmark Model Finds Face Structure

For each detected face, the shape predictor finds important facial landmarks.

These landmarks help the recognition model understand the structure of the face.

The code uses:

```python
shape = sp(image_np, face)
```

## Step 4: Face Recognition Model Creates An Embedding

The face recognition model creates a 128-number face descriptor:

```python
face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)
```

The comment in the code calls this a `128 embedding`.

The result is converted into a NumPy array and added to the list of encodings.

## Step 5: Stored Student Embeddings Are Loaded

`get_trained_model()` calls `get_all_students()` from the database layer.

It loops through students and collects:

- `face_embedding` as training input
- `student_id` as the label

This creates:

- `X`: face embeddings
- `y`: student IDs

## Step 6: SVM Classifier Predicts Student ID

The app uses scikit-learn's `SVC`:

```python
clf = SVC(kernel="linear", probability=True, class_weight="balanced")
```

An SVM classifier learns a boundary between known student embeddings.

When a new face embedding comes in, the classifier predicts the most likely student ID.

Important detail:

- If there is only one known student, the app skips classifier prediction and uses that one student ID.
- If there are two or more known students, it uses the classifier.

## Step 7: Euclidean Distance Confirms Match

After prediction, the app compares the new face embedding against the stored embedding for the predicted student:

```python
best_match_score = np.linalg.norm(student_embedding - encoding)
```

This is Euclidean distance.

Lower distance means the embeddings are more similar.

The threshold is:

```python
resemblance_threshold = 0.6
```

If the distance is less than or equal to `0.6`, the app accepts the match.

If the distance is greater than `0.6`, the app rejects the match.

## Face Pipeline Output

`predict_attendance()` returns:

```python
detected_student, all_students, len(encodings)
```

Meaning:

- `detected_student`: dictionary of recognized student IDs
- `all_students`: list of student IDs known to the trained model
- `len(encodings)`: number of faces found in the image

## Why Face Models Are Cached

dlib model loading is expensive. Loading the detector, shape predictor, and recognition model every time would make the app slow.

The app uses:

```python
@st.cache_resource
```

This tells Streamlit to keep the loaded model in memory and reuse it across reruns.

When a new student registers, the app calls `train_classifier()`, which clears the cache and rebuilds the model data.

## Voice Pipeline

File:

```text
src/pipelines/voice_pipeline.py
```

## What The Voice Pipeline Does

The voice pipeline:

1. Loads audio bytes.
2. Converts audio to 16000 Hz.
3. Preprocesses the waveform.
4. Creates a voice embedding with Resemblyzer.
5. Splits classroom audio into speech segments.
6. Compares each segment against stored student voice embeddings.
7. Marks matching students as detected.

## Step 1: Audio Bytes Are Loaded

Streamlit's `st.audio_input()` returns audio data. The app reads the bytes and passes them into the voice pipeline.

The code loads the bytes with librosa:

```python
audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
```

`sr=16000` means the audio is resampled to 16000 samples per second.

## Step 2: Resemblyzer Creates A Voice Embedding

The audio is preprocessed:

```python
wav = preprocess_wav(audio)
```

Then the encoder creates an embedding:

```python
embedding = encoder.embed_utterance(wav)
```

The embedding is converted to a list before storage:

```python
return embedding.tolist()
```

## Step 3: Classroom Audio Is Split Into Segments

For bulk voice attendance, the app splits audio into speech sections:

```python
segments = librosa.effects.split(audio, top_db=30)
```

This helps the app analyze different spoken parts separately.

Very short segments are ignored:

```python
if (end-start) < sr * 0.5:
    continue
```

This skips audio shorter than about half a second.

## Step 4: Dot Product Similarity Compares Voices

The app compares a new voice embedding with stored voice embeddings:

```python
similarity = np.dot(new_embedding, stored_embedding)
```

Higher similarity means the voices are more likely to match.

The threshold is:

```python
threshold = 0.65
```

If the best score is at least `0.65`, the speaker is accepted.

## Voice Pipeline Output

`process_bulk_audio()` returns a dictionary:

```python
{
  "student-id-1": 0.72,
  "student-id-2": 0.81
}
```

The keys are student IDs. The values are similarity scores.

The teacher workflow uses this dictionary to mark students present or absent.

## Common Face Recognition Failure Cases

- The photo is too dark.
- The face is too far away.
- The student is looking away.
- No face is detected.
- Multiple faces are detected during student login.
- A student has no stored face embedding.
- The threshold rejects a weak match.
- The model cache has not refreshed after registration.

## Common Voice Recognition Failure Cases

- The audio is too noisy.
- The sample is too short.
- Multiple students speak at the same time.
- The student did not register a voice profile.
- The microphone permission is blocked.
- The score is below the `0.65` threshold.

## Beginner Debugging Tips

- Check that the student has a `face_embedding` in Supabase.
- Check that the student has a `voice_embedding` if testing voice attendance.
- Try a clearer, brighter face image.
- Try recording voice in a quieter room.
- Use one student first before testing a crowded classroom photo.
- Confirm that IDs are UUID strings, not integers.
- Read [`troubleshooting.md`](troubleshooting.md) for setup and runtime issues.
