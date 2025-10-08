-- Health Tracker Database Schema
-- Vietnamese Food Nutrition Tracking System

CREATE DATABASE IF NOT EXISTS health_tracker;
USE health_tracker;

-- Users table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    date_of_birth DATE,
    gender ENUM('male', 'female', 'other'),
    height FLOAT COMMENT 'Height in cm',
    weight FLOAT COMMENT 'Weight in kg',
    activity_level ENUM('sedentary', 'lightly_active', 'moderately_active', 'very_active', 'extremely_active') DEFAULT 'moderately_active',
    goal ENUM('lose_weight', 'maintain_weight', 'gain_weight') DEFAULT 'maintain_weight',
    target_weight FLOAT,
    target_calories INT,
    avatar VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    last_login DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
);

-- Vietnamese Foods table
CREATE TABLE foods (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    name_vietnamese VARCHAR(255),
    description TEXT,
    category VARCHAR(100),
    calories FLOAT NOT NULL COMMENT 'Calories per 100g',
    protein FLOAT NOT NULL DEFAULT 0 COMMENT 'Protein per 100g (grams)',
    carbs FLOAT NOT NULL DEFAULT 0 COMMENT 'Carbohydrates per 100g (grams)',
    fat FLOAT NOT NULL DEFAULT 0 COMMENT 'Fat per 100g (grams)',
    fiber FLOAT DEFAULT 0 COMMENT 'Fiber per 100g (grams)',
    sugar FLOAT DEFAULT 0 COMMENT 'Sugar per 100g (grams)',
    sodium FLOAT DEFAULT 0 COMMENT 'Sodium per 100g (mg)',
    serving_size FLOAT DEFAULT 100 COMMENT 'Default serving size in grams',
    serving_unit VARCHAR(50) DEFAULT 'g' COMMENT 'Serving unit (g, ml, piece, etc.)',
    image_url VARCHAR(500),
    is_vietnamese BOOLEAN DEFAULT TRUE COMMENT 'Whether this is a Vietnamese food item',
    is_verified BOOLEAN DEFAULT FALSE COMMENT 'Whether the nutritional data is verified by experts',
    source VARCHAR(255) COMMENT 'Source of nutritional data',
    tags JSON COMMENT 'Array of tags for search and categorization',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_name (name),
    INDEX idx_name_vietnamese (name_vietnamese),
    INDEX idx_category (category),
    INDEX idx_is_vietnamese (is_vietnamese),
    INDEX idx_calories (calories)
);

-- Meals table
CREATE TABLE meals (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    food_id INT NOT NULL,
    meal_type ENUM('breakfast', 'lunch', 'dinner', 'snack') NOT NULL,
    quantity FLOAT NOT NULL COMMENT 'Quantity consumed',
    unit VARCHAR(50) DEFAULT 'g' COMMENT 'Unit of measurement',
    calories FLOAT NOT NULL COMMENT 'Total calories for this meal',
    protein FLOAT NOT NULL COMMENT 'Total protein for this meal',
    carbs FLOAT NOT NULL COMMENT 'Total carbs for this meal',
    fat FLOAT NOT NULL COMMENT 'Total fat for this meal',
    meal_date DATE NOT NULL,
    meal_time TIME,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, meal_date),
    INDEX idx_meal_type (meal_type),
    INDEX idx_meal_date (meal_date)
);

-- Exercises table
CREATE TABLE exercises (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    name_vietnamese VARCHAR(255),
    description TEXT,
    category ENUM('cardio', 'strength', 'flexibility', 'sports', 'other') NOT NULL,
    calories_per_hour FLOAT NOT NULL COMMENT 'Calories burned per hour for average person',
    intensity ENUM('low', 'moderate', 'high') DEFAULT 'moderate',
    duration_minutes INT DEFAULT 30,
    muscle_groups JSON COMMENT 'Array of muscle groups targeted',
    equipment_needed JSON COMMENT 'Array of equipment needed',
    is_vietnamese BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_name (name),
    INDEX idx_category (category),
    INDEX idx_intensity (intensity)
);

-- User Exercises table
CREATE TABLE user_exercises (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    exercise_id INT NOT NULL,
    duration_minutes INT NOT NULL,
    calories_burned FLOAT NOT NULL,
    exercise_date DATE NOT NULL,
    exercise_time TIME,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, exercise_date),
    INDEX idx_exercise_date (exercise_date)
);

-- Weight tracking table
CREATE TABLE weight_tracking (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    weight FLOAT NOT NULL,
    measurement_date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, measurement_date),
    UNIQUE KEY unique_user_date (user_id, measurement_date)
);

-- AI Recommendations table
CREATE TABLE ai_recommendations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    recommendation_type ENUM('meal', 'exercise', 'health_tip') NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
    is_read BOOLEAN DEFAULT FALSE,
    is_applied BOOLEAN DEFAULT FALSE,
    expires_at DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_type (user_id, recommendation_type),
    INDEX idx_priority (priority),
    INDEX idx_created_at (created_at)
);

-- User Goals table
CREATE TABLE user_goals (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    goal_type ENUM('weight_loss', 'weight_gain', 'muscle_gain', 'endurance', 'flexibility') NOT NULL,
    target_value FLOAT,
    target_unit VARCHAR(50),
    target_date DATE,
    current_value FLOAT,
    current_unit VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_active (user_id, is_active),
    INDEX idx_goal_type (goal_type)
);

-- Insert sample Vietnamese foods
INSERT INTO foods (name, name_vietnamese, category, calories, protein, carbs, fat, fiber, sugar, sodium, is_vietnamese, is_verified, source) VALUES
('White Rice', 'Cơm trắng', 'grains', 130, 2.7, 28, 0.3, 0.4, 0.1, 1, TRUE, TRUE, 'Viện Dinh dưỡng Quốc gia'),
('Pho Bo', 'Phở bò', 'noodles', 350, 15, 45, 8, 2, 3, 800, TRUE, TRUE, 'Viện Dinh dưỡng Quốc gia'),
('Bun Bo Hue', 'Bún bò Huế', 'noodles', 400, 18, 50, 10, 2.5, 4, 900, TRUE, TRUE, 'Viện Dinh dưỡng Quốc gia'),
('Banh Mi', 'Bánh mì', 'bread', 250, 8, 45, 3, 2, 5, 400, TRUE, TRUE, 'Viện Dinh dưỡng Quốc gia'),
('Com Tam', 'Cơm tấm', 'rice_dish', 450, 20, 55, 12, 1.5, 2, 600, TRUE, TRUE, 'Viện Dinh dưỡng Quốc gia'),
('Bun Cha', 'Bún chả', 'noodles', 380, 22, 40, 8, 2, 3, 700, TRUE, TRUE, 'Viện Dinh dưỡng Quốc gia'),
('Goi Cuon', 'Gỏi cuốn', 'appetizer', 120, 6, 20, 1, 3, 2, 200, TRUE, TRUE, 'Viện Dinh dưỡng Quốc gia'),
('Banh Xeo', 'Bánh xèo', 'pancake', 300, 8, 35, 12, 2, 3, 500, TRUE, TRUE, 'Viện Dinh dưỡng Quốc gia'),
('Cha Ca', 'Chả cá', 'fish', 200, 25, 5, 8, 0.5, 1, 400, TRUE, TRUE, 'Viện Dinh dưỡng Quốc gia'),
('Nem Nuong', 'Nem nướng', 'meat', 180, 12, 8, 10, 1, 1, 350, TRUE, TRUE, 'Viện Dinh dưỡng Quốc gia');

-- Insert sample exercises
INSERT INTO exercises (name, name_vietnamese, category, calories_per_hour, intensity, muscle_groups, equipment_needed, is_vietnamese) VALUES
('Walking', 'Đi bộ', 'cardio', 200, 'low', '["legs", "core"]', '[]', TRUE),
('Running', 'Chạy bộ', 'cardio', 600, 'high', '["legs", "core", "arms"]', '[]', TRUE),
('Cycling', 'Đạp xe', 'cardio', 400, 'moderate', '["legs", "core"]', '["bicycle"]', TRUE),
('Swimming', 'Bơi lội', 'cardio', 500, 'moderate', '["full_body"]', '["pool"]', TRUE),
('Yoga', 'Yoga', 'flexibility', 200, 'low', '["full_body"]', '["yoga_mat"]', TRUE),
('Push-ups', 'Hít đất', 'strength', 300, 'moderate', '["chest", "arms", "core"]', '[]', TRUE),
('Squats', 'Squat', 'strength', 250, 'moderate', '["legs", "glutes"]', '[]', TRUE),
('Badminton', 'Cầu lông', 'sports', 350, 'moderate', '["arms", "legs", "core"]', '["racket", "shuttlecock"]', TRUE),
('Football', 'Bóng đá', 'sports', 500, 'high', '["legs", "core", "arms"]', '["ball"]', TRUE),
('Tai Chi', 'Thái cực quyền', 'flexibility', 150, 'low', '["full_body"]', '[]', TRUE);
