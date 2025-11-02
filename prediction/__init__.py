import sys
from fetch_and_predict import StudentDataFetcher, PredictionLogger, test_api_connection
from model_loader import ModelLoader


def run_prediction_pipeline(student_id: int = None):

    print("STUDENT PERFORMANCE PREDICTION PIPELINE")
   
    # Step 1: Check API connection
    print("\nChecking API connection...")
    if not test_api_connection():
        print("\nPipeline failed: API not accessible")
        return False
    
    # Step 2: Fetch student data
    print("\nFetching student data...")
    fetcher = StudentDataFetcher()
    
    if student_id:
        student_data = fetcher.get_student_by_id(student_id)
    else:
        student_data = fetcher.get_latest_student()
    
    if not student_data:
        print("\nPipeline failed: Could not fetch student data")
        return False
    
    print(f"Fetched data for Student ID: {student_data['student_id']}")
    
    # Step 3: Load ML model
    print("\nLoading ML model...")
    loader = ModelLoader()
    
    if not loader.load_model():
        print("Model not found. Using dummy model for demonstration...")
        loader.create_dummy_model()
    
    # Step 4: Make prediction
    print("\nMaking prediction...")
    try:
        predicted_score, confidence = loader.predict(student_data)
        print(f"Prediction completed successfully")
    except Exception as e:
        print(f"Pipeline failed: {e}")
        return False
    
    # Step 5: Log prediction
    print("\nLogging prediction to database...")
    logger = PredictionLogger()
    
    # Get actual score if available
    actual_score = None
    if 'academic_record' in student_data:
        actual_score = student_data['academic_record'].get('exam_score')
    
    success = logger.log_prediction(
        student_id=student_data['student_id'],
        predicted_score=predicted_score,
        actual_score=actual_score,
        confidence_score=confidence
    )
    
    if success:
        print("\nPREDICTION PIPELINE COMPLETED SUCCESSFULLY")
        return True
    else:
        print("\nFailed to log prediction")
        return False


if __name__ == "__main__":
    # Check if student ID provided as command line argument
    student_id = None
    if len(sys.argv) > 1:
        try:
            student_id = int(sys.argv[1])
            print(f"\nPredicting for Student ID: {student_id}")
        except ValueError:
            print("Invalid student ID. Using latest student.")
    
    # Run pipeline
    success = run_prediction_pipeline(student_id)
    
    if not success:
        sys.exit(1)



