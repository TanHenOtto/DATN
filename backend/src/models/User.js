const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');
const bcrypt = require('bcryptjs');

const User = sequelize.define('User', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  email: {
    type: DataTypes.STRING(255),
    allowNull: false,
    unique: true,
    validate: {
      isEmail: true
    }
  },
  password: {
    type: DataTypes.STRING(255),
    allowNull: false,
    validate: {
      len: [6, 255]
    }
  },
  fullName: {
    type: DataTypes.STRING(255),
    allowNull: false
  },
  dateOfBirth: {
    type: DataTypes.DATE,
    allowNull: true
  },
  gender: {
    type: DataTypes.ENUM('male', 'female', 'other'),
    allowNull: true
  },
  height: {
    type: DataTypes.FLOAT,
    allowNull: true,
    comment: 'Height in cm'
  },
  weight: {
    type: DataTypes.FLOAT,
    allowNull: true,
    comment: 'Weight in kg'
  },
  activityLevel: {
    type: DataTypes.ENUM('sedentary', 'lightly_active', 'moderately_active', 'very_active', 'extremely_active'),
    allowNull: true,
    defaultValue: 'moderately_active'
  },
  goal: {
    type: DataTypes.ENUM('lose_weight', 'maintain_weight', 'gain_weight'),
    allowNull: true,
    defaultValue: 'maintain_weight'
  },
  targetWeight: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  targetCalories: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  avatar: {
    type: DataTypes.STRING(500),
    allowNull: true
  },
  isActive: {
    type: DataTypes.BOOLEAN,
    defaultValue: true
  },
  lastLogin: {
    type: DataTypes.DATE,
    allowNull: true
  }
}, {
  tableName: 'users',
  hooks: {
    beforeCreate: async (user) => {
      if (user.password) {
        user.password = await bcrypt.hash(user.password, 12);
      }
    },
    beforeUpdate: async (user) => {
      if (user.changed('password')) {
        user.password = await bcrypt.hash(user.password, 12);
      }
    }
  }
});

// Instance methods
User.prototype.comparePassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};

User.prototype.toJSON = function() {
  const values = Object.assign({}, this.get());
  delete values.password;
  return values;
};

module.exports = User;
