from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import numpy as np
import pandas as pd
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Health Tracker AI Service",
    description="AI service for nutrition analysis and recommendations",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class FoodRecognitionRequest(BaseModel):
    image_url: Optional[str] = None
    description: Optional[str] = None

class FoodRecognitionResponse(BaseModel):
    food_name: str
    confidence: float
    estimated_calories: float
    nutritional_info: Dict[str, float]

class NutritionAnalysisRequest(BaseModel):
    user_id: int
    meals: List[Dict[str, Any]]
    date: str

class NutritionAnalysisResponse(BaseModel):
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float
    recommendations: List[str]
    health_score: float

class RecommendationRequest(BaseModel):
    user_id: int
    current_goals: str
    activity_level: str
    dietary_preferences: Optional[List[str]] = None

class RecommendationResponse(BaseModel):
    meal_suggestions: List[Dict[str, Any]]
    exercise_recommendations: List[Dict[str, Any]]
    health_tips: List[str]

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Health Tracker AI Service"
    }

# Food recognition endpoint
@app.post("/recognize-food", response_model=FoodRecognitionResponse)
async def recognize_food(request: FoodRecognitionRequest):
    """
    Recognize food from image or description and provide nutritional information
    """
    try:
        # Placeholder implementation - replace with actual ML model
        if request.image_url:
            # Image-based food recognition would go here
            # For now, return mock data
            return FoodRecognitionResponse(
                food_name="Cơm trắng",
                confidence=0.85,
                estimated_calories=130.0,
                nutritional_info={
                    "protein": 2.7,
                    "carbs": 28.0,
                    "fat": 0.3,
                    "fiber": 0.4
                }
            )
        elif request.description:
            # Text-based food recognition would go here
            return FoodRecognitionResponse(
                food_name="Phở bò",
                confidence=0.92,
                estimated_calories=350.0,
                nutritional_info={
                    "protein": 15.0,
                    "carbs": 45.0,
                    "fat": 8.0,
                    "fiber": 2.0
                }
            )
        else:
            raise HTTPException(status_code=400, detail="Either image_url or description must be provided")
    
    except Exception as e:
        logger.error(f"Food recognition error: {str(e)}")
        raise HTTPException(status_code=500, detail="Food recognition failed")

# Nutrition analysis endpoint
@app.post("/analyze-nutrition", response_model=NutritionAnalysisResponse)
async def analyze_nutrition(request: NutritionAnalysisRequest):
    """
    Analyze daily nutrition intake and provide insights
    """
    try:
        # Calculate total nutrition from meals
        total_calories = sum(meal.get('calories', 0) for meal in request.meals)
        total_protein = sum(meal.get('protein', 0) for meal in request.meals)
        total_carbs = sum(meal.get('carbs', 0) for meal in request.meals)
        total_fat = sum(meal.get('fat', 0) for meal in request.meals)
        
        # Generate recommendations based on nutrition analysis
        recommendations = []
        health_score = 80.0  # Base score
        
        if total_calories < 1200:
            recommendations.append("Bạn cần tăng lượng calo nạp vào. Hãy thêm các bữa ăn nhẹ lành mạnh.")
            health_score -= 10
        elif total_calories > 2500:
            recommendations.append("Lượng calo hơi cao. Hãy cân nhắc giảm khẩu phần ăn.")
            health_score -= 5
            
        if total_protein < 50:
            recommendations.append("Cần tăng lượng protein. Hãy thêm thịt, cá, đậu vào bữa ăn.")
            health_score -= 8
            
        if total_fat > 80:
            recommendations.append("Lượng chất béo hơi cao. Hãy chọn thực phẩm ít béo hơn.")
            health_score -= 5
            
        if not recommendations:
            recommendations.append("Chế độ dinh dưỡng của bạn rất tốt! Hãy duy trì.")
            health_score += 5
            
        return NutritionAnalysisResponse(
            total_calories=total_calories,
            total_protein=total_protein,
            total_carbs=total_carbs,
            total_fat=total_fat,
            recommendations=recommendations,
            health_score=max(0, min(100, health_score))
        )
    
    except Exception as e:
        logger.error(f"Nutrition analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail="Nutrition analysis failed")

# Personalized recommendations endpoint
@app.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """
    Generate personalized meal and exercise recommendations
    """
    try:
        # Generate meal suggestions based on goals and preferences
        meal_suggestions = []
        
        if request.current_goals == "lose_weight":
            meal_suggestions = [
                {
                    "name": "Salad rau củ với ức gà",
                    "calories": 250,
                    "description": "Rau xanh tươi với ức gà nướng, ít calo nhưng giàu protein"
                },
                {
                    "name": "Cá hồi nướng với rau luộc",
                    "calories": 300,
                    "description": "Cá hồi giàu omega-3 với rau củ luộc"
                }
            ]
        elif request.current_goals == "gain_weight":
            meal_suggestions = [
                {
                    "name": "Cơm gà nướng với rau xào",
                    "calories": 500,
                    "description": "Cơm trắng với gà nướng và rau xào dầu"
                },
                {
                    "name": "Bún bò Huế",
                    "calories": 450,
                    "description": "Món bún đậm đà với thịt bò và nước dùng ngon"
                }
            ]
        else:  # maintain_weight
            meal_suggestions = [
                {
                    "name": "Cơm tấm sườn nướng",
                    "calories": 400,
                    "description": "Cơm tấm truyền thống với sườn nướng"
                }
            ]
        
        # Generate exercise recommendations
        exercise_recommendations = [
            {
                "name": "Đi bộ nhanh",
                "duration": "30 phút",
                "calories_burned": 150,
                "description": "Hoạt động nhẹ nhàng, phù hợp mọi lứa tuổi"
            },
            {
                "name": "Yoga",
                "duration": "45 phút",
                "calories_burned": 120,
                "description": "Tăng cường sự dẻo dai và giảm stress"
            }
        ]
        
        # Generate health tips
        health_tips = [
            "Uống đủ 2-3 lít nước mỗi ngày",
            "Ăn 5-6 bữa nhỏ thay vì 3 bữa lớn",
            "Ngủ đủ 7-8 tiếng mỗi đêm",
            "Hạn chế thức ăn nhanh và đồ ngọt"
        ]
        
        return RecommendationResponse(
            meal_suggestions=meal_suggestions,
            exercise_recommendations=exercise_recommendations,
            health_tips=health_tips
        )
    
    except Exception as e:
        logger.error(f"Recommendations error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate recommendations")

# Image upload endpoint for food recognition
@app.post("/upload-food-image")
async def upload_food_image(file: UploadFile = File(...)):
    """
    Upload food image for recognition
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Save file (in production, use cloud storage)
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, f"{datetime.now().timestamp()}_{file.filename}")
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Here you would process the image with your ML model
        # For now, return mock response
        return {
            "message": "Image uploaded successfully",
            "file_path": file_path,
            "food_name": "Cơm trắng",
            "confidence": 0.85
        }
    
    except Exception as e:
        logger.error(f"Image upload error: {str(e)}")
        raise HTTPException(status_code=500, detail="Image upload failed")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
