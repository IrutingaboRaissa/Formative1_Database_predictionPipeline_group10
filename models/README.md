# Models Directory

Place your trained ML model file here:

- `student_performance_model.pkl` (using joblib)
- `student_performance_model.joblib` (alternative)

The prediction script will automatically load the model from this directory.

## How to Save Your Model

```python
import joblib

# After training your model:
joblib.dump(model, 'models/student_performance_model.pkl')
```

## Model Requirements

- Input: 19 features (see prediction/README.md)
- Output: Predicted exam score (0-110)
- Format: Any scikit-learn compatible model
