import sys
import os
from tabulate import tabulate

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database.mysql_manager import MySQLDatabaseManager

def view_predictions():
    
    db = MySQLDatabaseManager()
    
    try:
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            p.prediction_id,
            p.student_id,
            s.gender,
            a.hours_studied,
            a.attendance,
            a.previous_scores,
            p.predicted_score,
            p.actual_score,
            p.confidence_score,
            p.prediction_date
        FROM predictions p
        JOIN students s ON p.student_id = s.student_id
        LEFT JOIN academic_records a ON p.student_id = a.student_id
        ORDER BY p.prediction_date DESC
        LIMIT 20
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        if not results:
            print("\nNo predictions found in database")
            return
        
        print(f"\nTotal Predictions: {len(results)}")
        print("=" * 120)
        
        # Format for display
        table_data = []
        for row in results:
            table_data.append([
                row['prediction_id'],
                row['student_id'],
                row['gender'],
                row['hours_studied'],
                f"{row['attendance']}%",
                row['previous_scores'],
                f"{row['predicted_score']:.2f}",
                row['actual_score'] if row['actual_score'] else 'N/A',
                f"{row['confidence_score']:.4f}",
                row['prediction_date'].strftime('%Y-%m-%d %H:%M')
            ])
        
        headers = [
            'Pred ID', 'Student', 'Gender', 'Hours', 'Attend', 
            'Prev Score', 'Predicted', 'Actual', 'Confidence', 'Date'
        ]
        
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
        
        # Calculate accuracy if actual scores exist
        accurate_predictions = [r for r in results if r['actual_score'] is not None]
        if accurate_predictions:
            errors = [abs(r['predicted_score'] - r['actual_score']) for r in accurate_predictions]
            avg_error = sum(errors) / len(errors)
            print(f"\nAverage Prediction Error: {avg_error:.2f} points")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error viewing predictions: {e}")

if __name__ == "__main__":
    view_predictions()
