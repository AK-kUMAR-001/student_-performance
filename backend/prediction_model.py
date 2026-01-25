"""
ML Prediction Model for Student Performance
Uses Linear Regression to predict performance
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import joblib
import os

class PerformancePredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(self.base_dir, 'trained_model.pkl')
        self.scaler_path = os.path.join(self.base_dir, 'trained_scaler.pkl')
        self.is_trained = False
        self.load_model()
    
    def load_model(self):
        """Load pre-trained model if exists"""
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            try:
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                self.is_trained = True
            except Exception:
                self.is_trained = False
        else:
            self.is_trained = False
    
    def train(self, training_data_path=None):
        """Train the model on historical data"""
        if training_data_path is None:
            training_data_path = os.path.join(self.base_dir, 'training_data.csv')

        try:
            df = pd.read_csv(training_data_path)
            
            # Features for prediction (6 features including extracurricular)
            X = df[['marks_obtained', 'attendance_percentage', 'internal_marks', 'assignment_score', 'certifications', 'competitions']].values
            # Target: performance score (0-100)
            y = df['performance_score'].values
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train model
            self.model.fit(X_scaled, y)
            
            # Save model
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.scaler, self.scaler_path)
            
            self.is_trained = True
            return True
        except Exception as e:
            print(f"Error training model: {e}")
            return False
    
    def predict(self, marks_obtained, attendance_percentage, internal_marks, assignment_score, certifications=0, competitions=0):
        """
        Predict student performance based on academic metrics and extracurricular activities
        
        Args:
            marks_obtained: Final marks (0-100)
            attendance_percentage: Attendance (0-100)
            internal_marks: Internal exam marks (0-50)
            assignment_score: Assignment score (0-20)
            certifications: Number of certifications (default: 0)
            competitions: Number of competitions participated (default: 0)
        
        Returns:
            Dictionary with prediction score and category
        """
        if not self.is_trained:
            # If model not trained, use enhanced rule-based prediction
            return self._rule_based_prediction(marks_obtained, attendance_percentage, internal_marks, assignment_score, certifications, competitions)
        
        try:
            # Prepare features (6 features)
            features = np.array([[marks_obtained, attendance_percentage, internal_marks, assignment_score, certifications, competitions]])
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Predict
            prediction_score = self.model.predict(features_scaled)[0]
            
            # Ensure score is between 0-100
            prediction_score = max(0, min(100, prediction_score))
            
            # Determine category based on enhanced criteria
            if prediction_score >= 75:
                category = 'Good Performance'
            elif prediction_score >= 50:
                category = 'Average Performance'
            else:
                category = 'At-Risk Performance'
            
            return {
                'score': round(prediction_score, 2),
                'category': category,
                'marks': marks_obtained,
                'attendance': attendance_percentage,
                'internal': internal_marks,
                'assignment': assignment_score,
                'certifications': certifications,
                'competitions': competitions
            }
        except Exception as e:
            print(f"Error in prediction: {e}")
            return self._rule_based_prediction(marks_obtained, attendance_percentage, internal_marks, assignment_score, certifications, competitions)
    
    def _rule_based_prediction(self, marks_obtained, attendance_percentage, internal_marks, assignment_score, certifications=0, competitions=0):
        """
        Enhanced rule-based prediction when ML model is not available
        Uses academic score (90% weight) + extracurricular bonus (10% weight)
        """
        # Academic Score Calculation (90% weight)
        # Normalize to 0-100 scale for each component
        marks_normalized = marks_obtained * 0.40  # 40% of academic score
        attendance_normalized = attendance_percentage * 0.30  # 30% of academic score
        internal_normalized = (internal_marks / 50) * 100 * 0.20  # 20% of academic score
        assignment_normalized = (assignment_score / 20) * 100 * 0.10  # 10% of academic score
        
        academic_score = marks_normalized + attendance_normalized + internal_normalized + assignment_normalized
        
        # Extracurricular Bonus (10% weight) - Max 10 bonus points
        # Certifications add +2 points each, competitions add +3 points each
        cert_bonus = min(certifications * 2, 6)  # Max 6 points from certifications
        comp_bonus = min(competitions * 3, 4)   # Max 4 points from competitions
        extracurricular_bonus = cert_bonus + comp_bonus
        
        # Final prediction score
        prediction_score = (academic_score * 0.90) + (extracurricular_bonus * 0.10)
        prediction_score = max(0, min(100, prediction_score))
        
        # Determine category
        if prediction_score >= 75:
            category = 'Good Performance'
        elif prediction_score >= 50:
            category = 'Average Performance'
        else:
            category = 'At-Risk Performance'
        
        return {
            'score': round(prediction_score, 2),
            'category': category,
            'marks': marks_obtained,
            'attendance': attendance_percentage,
            'internal': internal_marks,
            'assignment': assignment_score,
            'certifications': certifications,
            'competitions': competitions
        }

# Global predictor instance
predictor = PerformancePredictor()
