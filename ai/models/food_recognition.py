import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import os
from typing import Tuple, Dict, List
import logging

logger = logging.getLogger(__name__)

class FoodRecognitionModel:
    """
    Food recognition model using CNN for Vietnamese food classification
    """
    
    def __init__(self, model_path: str = None):
        self.model = None
        self.class_names = [
            'cơm trắng', 'phở bò', 'bún bò huế', 'bánh mì', 'chả cá',
            'gỏi cuốn', 'nem nướng', 'bánh xèo', 'cơm tấm', 'bún chả',
            'chả giò', 'bánh cuốn', 'bún riêu', 'cháo lòng', 'bánh canh',
            'cơm cháy', 'bún mắm', 'bánh tráng nướng', 'bún thịt nướng', 'cơm gà'
        ]
        self.nutrition_database = self._load_nutrition_database()
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            self._create_model()
    
    def _create_model(self):
        """
        Create a CNN model for food recognition
        """
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.Dense(len(self.class_names), activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        logger.info("Food recognition model created successfully")
    
    def load_model(self, model_path: str):
        """
        Load pre-trained model
        """
        try:
            self.model = tf.keras.models.load_model(model_path)
            logger.info(f"Model loaded from {model_path}")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            self._create_model()
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Preprocess image for model input
        """
        try:
            # Load and resize image
            image = Image.open(image_path)
            image = image.convert('RGB')
            image = image.resize((224, 224))
            
            # Convert to numpy array and normalize
            image_array = np.array(image) / 255.0
            image_array = np.expand_dims(image_array, axis=0)
            
            return image_array
        except Exception as e:
            logger.error(f"Image preprocessing failed: {str(e)}")
            raise
    
    def predict(self, image_path: str) -> Tuple[str, float, Dict[str, float]]:
        """
        Predict food from image
        """
        try:
            if self.model is None:
                raise ValueError("Model not loaded")
            
            # Preprocess image
            processed_image = self.preprocess_image(image_path)
            
            # Make prediction
            predictions = self.model.predict(processed_image)
            confidence = float(np.max(predictions))
            predicted_class_idx = int(np.argmax(predictions))
            predicted_food = self.class_names[predicted_class_idx]
            
            # Get nutritional information
            nutritional_info = self.nutrition_database.get(predicted_food, {
                'calories': 200.0,
                'protein': 10.0,
                'carbs': 30.0,
                'fat': 5.0,
                'fiber': 2.0
            })
            
            return predicted_food, confidence, nutritional_info
            
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise
    
    def _load_nutrition_database(self) -> Dict[str, Dict[str, float]]:
        """
        Load Vietnamese food nutrition database
        """
        return {
            'cơm trắng': {
                'calories': 130.0,
                'protein': 2.7,
                'carbs': 28.0,
                'fat': 0.3,
                'fiber': 0.4
            },
            'phở bò': {
                'calories': 350.0,
                'protein': 15.0,
                'carbs': 45.0,
                'fat': 8.0,
                'fiber': 2.0
            },
            'bún bò huế': {
                'calories': 400.0,
                'protein': 18.0,
                'carbs': 50.0,
                'fat': 10.0,
                'fiber': 2.5
            },
            'bánh mì': {
                'calories': 250.0,
                'protein': 8.0,
                'carbs': 45.0,
                'fat': 3.0,
                'fiber': 2.0
            },
            'cơm tấm': {
                'calories': 450.0,
                'protein': 20.0,
                'carbs': 55.0,
                'fat': 12.0,
                'fiber': 1.5
            },
            'bún chả': {
                'calories': 380.0,
                'protein': 22.0,
                'carbs': 40.0,
                'fat': 8.0,
                'fiber': 2.0
            },
            'gỏi cuốn': {
                'calories': 120.0,
                'protein': 6.0,
                'carbs': 20.0,
                'fat': 1.0,
                'fiber': 3.0
            },
            'bánh xèo': {
                'calories': 300.0,
                'protein': 8.0,
                'carbs': 35.0,
                'fat': 12.0,
                'fiber': 2.0
            },
            'chả cá': {
                'calories': 200.0,
                'protein': 25.0,
                'carbs': 5.0,
                'fat': 8.0,
                'fiber': 0.5
            },
            'nem nướng': {
                'calories': 180.0,
                'protein': 12.0,
                'carbs': 8.0,
                'fat': 10.0,
                'fiber': 1.0
            }
        }
    
    def train(self, train_data_path: str, epochs: int = 50):
        """
        Train the model with Vietnamese food dataset
        """
        # This would be implemented with actual training data
        # For now, it's a placeholder
        logger.info("Training functionality would be implemented here")
        pass
    
    def save_model(self, model_path: str):
        """
        Save trained model
        """
        if self.model:
            self.model.save(model_path)
            logger.info(f"Model saved to {model_path}")
        else:
            raise ValueError("No model to save")

class NutritionAnalyzer:
    """
    Analyze nutrition patterns and provide recommendations
    """
    
    def __init__(self):
        self.recommendation_rules = self._load_recommendation_rules()
    
    def analyze_daily_nutrition(self, meals: List[Dict]) -> Dict:
        """
        Analyze daily nutrition intake
        """
        total_calories = sum(meal.get('calories', 0) for meal in meals)
        total_protein = sum(meal.get('protein', 0) for meal in meals)
        total_carbs = sum(meal.get('carbs', 0) for meal in meals)
        total_fat = sum(meal.get('fat', 0) for meal in meals)
        
        # Calculate health score
        health_score = self._calculate_health_score(total_calories, total_protein, total_carbs, total_fat)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(total_calories, total_protein, total_carbs, total_fat)
        
        return {
            'total_calories': total_calories,
            'total_protein': total_protein,
            'total_carbs': total_carbs,
            'total_fat': total_fat,
            'health_score': health_score,
            'recommendations': recommendations
        }
    
    def _calculate_health_score(self, calories: float, protein: float, carbs: float, fat: float) -> float:
        """
        Calculate health score based on nutrition intake
        """
        score = 100.0
        
        # Calorie range check (1500-2500 for adults)
        if calories < 1200:
            score -= 20
        elif calories > 3000:
            score -= 15
        elif calories > 2500:
            score -= 10
        
        # Protein check (50-100g for adults)
        if protein < 40:
            score -= 15
        elif protein > 150:
            score -= 10
        
        # Fat check (should be 20-35% of calories)
        fat_percentage = (fat * 9) / calories * 100 if calories > 0 else 0
        if fat_percentage < 15:
            score -= 10
        elif fat_percentage > 40:
            score -= 15
        
        return max(0, min(100, score))
    
    def _generate_recommendations(self, calories: float, protein: float, carbs: float, fat: float) -> List[str]:
        """
        Generate personalized recommendations
        """
        recommendations = []
        
        if calories < 1200:
            recommendations.append("Lượng calo quá thấp. Hãy tăng khẩu phần ăn với thực phẩm lành mạnh.")
        elif calories > 2500:
            recommendations.append("Lượng calo hơi cao. Hãy giảm khẩu phần và tăng hoạt động thể chất.")
        
        if protein < 50:
            recommendations.append("Cần tăng protein. Hãy thêm thịt, cá, đậu, trứng vào bữa ăn.")
        elif protein > 120:
            recommendations.append("Lượng protein hơi cao. Hãy cân bằng với rau củ và trái cây.")
        
        fat_percentage = (fat * 9) / calories * 100 if calories > 0 else 0
        if fat_percentage < 20:
            recommendations.append("Cần tăng chất béo lành mạnh từ dầu olive, bơ, các loại hạt.")
        elif fat_percentage > 35:
            recommendations.append("Lượng chất béo hơi cao. Hãy chọn thực phẩm ít béo hơn.")
        
        if not recommendations:
            recommendations.append("Chế độ dinh dưỡng của bạn rất cân bằng! Hãy duy trì.")
        
        return recommendations
    
    def _load_recommendation_rules(self) -> Dict:
        """
        Load recommendation rules and thresholds
        """
        return {
            'calorie_ranges': {
                'low': 1200,
                'high': 2500,
                'very_high': 3000
            },
            'protein_ranges': {
                'low': 40,
                'high': 120,
                'very_high': 150
            },
            'fat_percentage_ranges': {
                'low': 15,
                'high': 35,
                'very_high': 40
            }
        }
