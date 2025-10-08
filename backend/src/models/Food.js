const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');

const Food = sequelize.define('Food', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  name: {
    type: DataTypes.STRING(255),
    allowNull: false
  },
  nameVietnamese: {
    type: DataTypes.STRING(255),
    allowNull: true,
    comment: 'Vietnamese name of the food'
  },
  description: {
    type: DataTypes.TEXT,
    allowNull: true
  },
  category: {
    type: DataTypes.STRING(100),
    allowNull: true,
    comment: 'Food category (e.g., rice, meat, vegetable)'
  },
  calories: {
    type: DataTypes.FLOAT,
    allowNull: false,
    comment: 'Calories per 100g'
  },
  protein: {
    type: DataTypes.FLOAT,
    allowNull: false,
    defaultValue: 0,
    comment: 'Protein per 100g (grams)'
  },
  carbs: {
    type: DataTypes.FLOAT,
    allowNull: false,
    defaultValue: 0,
    comment: 'Carbohydrates per 100g (grams)'
  },
  fat: {
    type: DataTypes.FLOAT,
    allowNull: false,
    defaultValue: 0,
    comment: 'Fat per 100g (grams)'
  },
  fiber: {
    type: DataTypes.FLOAT,
    allowNull: true,
    defaultValue: 0,
    comment: 'Fiber per 100g (grams)'
  },
  sugar: {
    type: DataTypes.FLOAT,
    allowNull: true,
    defaultValue: 0,
    comment: 'Sugar per 100g (grams)'
  },
  sodium: {
    type: DataTypes.FLOAT,
    allowNull: true,
    defaultValue: 0,
    comment: 'Sodium per 100g (mg)'
  },
  servingSize: {
    type: DataTypes.FLOAT,
    allowNull: true,
    defaultValue: 100,
    comment: 'Default serving size in grams'
  },
  servingUnit: {
    type: DataTypes.STRING(50),
    allowNull: true,
    defaultValue: 'g',
    comment: 'Serving unit (g, ml, piece, etc.)'
  },
  imageUrl: {
    type: DataTypes.STRING(500),
    allowNull: true
  },
  isVietnamese: {
    type: DataTypes.BOOLEAN,
    defaultValue: true,
    comment: 'Whether this is a Vietnamese food item'
  },
  isVerified: {
    type: DataTypes.BOOLEAN,
    defaultValue: false,
    comment: 'Whether the nutritional data is verified by experts'
  },
  source: {
    type: DataTypes.STRING(255),
    allowNull: true,
    comment: 'Source of nutritional data'
  },
  tags: {
    type: DataTypes.JSON,
    allowNull: true,
    comment: 'Array of tags for search and categorization'
  }
}, {
  tableName: 'foods',
  indexes: [
    {
      fields: ['name']
    },
    {
      fields: ['nameVietnamese']
    },
    {
      fields: ['category']
    },
    {
      fields: ['isVietnamese']
    }
  ]
});

module.exports = Food;
