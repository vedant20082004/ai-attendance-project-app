# AI Pipelines

This document explains the face and voice logic in plain English.

## Face Pipeline

File:

- `src/pipelines/face_pipeline.py`

### What It Does

- Detects faces in an image
- Converts each face to a 128-dimensional embedding
- Trains a classifier from stored student face embeddings
- Predicts which student a face belongs to

### Why It Uses Caching

The dlib models are expensive to load, so the app uses `@st.cache_resource`.

### Prediction Flow

1. Get face embeddings from the input image
2. Load all stored student embeddings
3. Train or reuse an SVM classifier
4. Predict the most likely student ID
5. Compare with Euclidean distance threshold `0.6`

### Important Detail

The code treats student IDs as UUID strings. They are not integers.

## Voice Pipeline

File:

- `src/pipelines/voice_pipeline.py`

### What It Does

- Loads audio
- Splits it into speech segments
- Creates a speaker embedding with Resemblyzer
- Compares that embedding to stored student voice profiles

### Similarity

The code uses dot product similarity:

```python
similarity = np.dot(new_embedding, stored_embedding)
```

The threshold is `0.65`.

### Output

The result is a dictionary of recognized student IDs mapped to their best similarity score.

## AI Inputs and Outputs

### Face

- Input: classroom image
- Output: recognized student IDs

### Voice

- Input: classroom audio
- Output: recognized student IDs with scores

## Common AI Failure Modes

- No face found in the image
- Multiple faces in a student login photo
- Student has no stored embedding
- Voice sample too short or too noisy
- Windows build issues for `webrtcvad`
