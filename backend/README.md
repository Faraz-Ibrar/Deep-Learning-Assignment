# Action Recognition API Backend

FastAPI backend server for the UCF101 action recognition model.

## Prerequisites

- Python 3.9+ installed
- The trained model file `best_ucf101_model.keras` in the parent directory

## Quick Start (Windows)

1. Simply double-click `run_server.bat` or run:
   ```bash
   run_server.bat
   ```

This will:
- Create a virtual environment if it doesn't exist
- Install all dependencies
- Start the server on http://localhost:8000

## Manual Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate it:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check and API info |
| `/health` | GET | Check if model is loaded |
| `/actions` | GET | List supported action classes |
| `/predict` | POST | Predict action from uploaded image |

## Using the Predict Endpoint

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_image.jpg"
```

### Response Format

```json
{
  "success": true,
  "filename": "your_image.jpg",
  "predictions": [
    {"rank": 1, "action": "Basketball", "confidence": 75.23},
    {"rank": 2, "action": "JumpingJack", "confidence": 12.45},
    ...
  ],
  "top_prediction": {
    "action": "Basketball",
    "confidence": 75.23
  }
}
```

## Supported Actions

1. ApplyEyeMakeup
2. Basketball
3. Biking
4. Drumming
5. HorseRiding
6. JumpingJack
7. PizzaTossing
8. PlayingGuitar
9. Swimming
10. WritingOnBoard

## Interactive API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
