"""
Plant data model for storing plant health readings
"""

from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates

Base = declarative_base()

class PlantReading(Base):
    __tablename__ = 'plant_readings'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    location = Column(String(100), nullable=False, default='default')
    plant_type = Column(String(100), nullable=False)
    plant_id = Column(String(50), nullable=False)
    
    # Growth measurements
    height_cm = Column(Float, nullable=False)
    leaf_count = Column(Integer, default=0)
    stem_diameter_mm = Column(Float, default=0.0)
    
    # Leaf health indicators
    leaf_color_r = Column(Integer, default=0)  # RGB values
    leaf_color_g = Column(Integer, default=0)
    leaf_color_b = Column(Integer, default=0)
    leaf_chlorophyll_index = Column(Float, default=0.0)  # SPAD units
    
    # Health indicators
    disease_symptoms = Column(Text, default='')
    pest_presence = Column(Boolean, default=False)
    water_stress_level = Column(Float, default=0.0)  # 0-10 scale
    nutrient_deficiency_signs = Column(Text, default='')
    
    # Environmental stress indicators
    heat_stress_score = Column(Float, default=0.0)  # 0-10 scale
    drought_stress_score = Column(Float, default=0.0)  # 0-10 scale
    
    # Growth rate (calculated)
    growth_rate_cm_per_week = Column(Float, default=0.0)
    
    # Overall health score
    health_score = Column(Float, default=100.0)  # 0-100 scale
    
    # System fields
    sensor_id = Column(String(50), nullable=False)
    is_valid = Column(Boolean, default=True)
    notes = Column(String(500), default='')
    
    @validates('height_cm')
    def validate_height(self, key, height):
        if height < 0 or height > 1000:  # Max 10 meters
            raise ValueError("Height must be between 0 and 1000 cm")
        return height
    
    @validates('leaf_color_r', 'leaf_color_g', 'leaf_color_b')
    def validate_rgb(self, key, value):
        if value < 0 or value > 255:
            raise ValueError("RGB values must be between 0 and 255")
        return value
    
    @validates('water_stress_level', 'heat_stress_score', 'drought_stress_score')
    def validate_stress_scores(self, key, score):
        if score < 0 or score > 10:
            raise ValueError("Stress scores must be between 0 and 10")
        return score
    
    @validates('health_score')
    def validate_health_score(self, key, score):
        if score < 0 or score > 100:
            raise ValueError("Health score must be between 0 and 100")
        return score
    
    def to_dict(self):
        """Convert plant reading to dictionary"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'location': self.location,
            'plant_type': self.plant_type,
            'plant_id': self.plant_id,
            'height_cm': self.height_cm,
            'leaf_count': self.leaf_count,
            'stem_diameter_mm': self.stem_diameter_mm,
            'leaf_color_rgb': [self.leaf_color_r, self.leaf_color_g, self.leaf_color_b],
            'leaf_chlorophyll_index': self.leaf_chlorophyll_index,
            'disease_symptoms': self.disease_symptoms,
            'pest_presence': self.pest_presence,
            'water_stress_level': self.water_stress_level,
            'nutrient_deficiency_signs': self.nutrient_deficiency_signs,
            'heat_stress_score': self.heat_stress_score,
            'drought_stress_score': self.drought_stress_score,
            'growth_rate_cm_per_week': self.growth_rate_cm_per_week,
            'health_score': self.health_score,
            'sensor_id': self.sensor_id,
            'is_valid': self.is_valid,
            'notes': self.notes
        }
    
    def get_leaf_color_hex(self):
        """Get leaf color as hex string"""
        return f"#{self.leaf_color_r:02x}{self.leaf_color_g:02x}{self.leaf_color_b:02x}"
    
    def calculate_health_score(self):
        """Calculate overall plant health score based on various indicators"""
        base_score = 100.0
        
        # Deduct points for stress factors
        base_score -= (self.water_stress_level * 5)  # Max -50 points
        base_score -= (self.heat_stress_score * 3)   # Max -30 points
        base_score -= (self.drought_stress_score * 3) # Max -30 points
        
        # Deduct points for diseases and pests
        if self.disease_symptoms:
            base_score -= 20
        if self.pest_presence:
            base_score -= 15
        
        # Deduct points for nutrient deficiencies
        if self.nutrient_deficiency_signs:
            base_score -= 15
        
        # Chlorophyll index bonus/penalty
        if self.leaf_chlorophyll_index > 40:  # Healthy chlorophyll
            base_score += 5
        elif self.leaf_chlorophyll_index < 20:  # Low chlorophyll
            base_score -= 10
        
        # Growth rate consideration
        if self.growth_rate_cm_per_week < 0.5:  # Slow growth
            base_score -= 10
        elif self.growth_rate_cm_per_week > 2.0:  # Good growth
            base_score += 5
        
        return max(0.0, min(100.0, base_score))
    
    def is_healthy(self, threshold=70.0):
        """Check if plant is considered healthy"""
        return self.health_score >= threshold
    
    def get_stress_indicators(self):
        """Get list of active stress indicators"""
        indicators = []
        
        if self.water_stress_level > 5:
            indicators.append('High water stress')
        if self.heat_stress_score > 5:
            indicators.append('Heat stress')
        if self.drought_stress_score > 5:
            indicators.append('Drought stress')
        if self.disease_symptoms:
            indicators.append('Disease symptoms present')
        if self.pest_presence:
            indicators.append('Pest presence detected')
        if self.nutrient_deficiency_signs:
            indicators.append('Nutrient deficiency signs')
        if self.leaf_chlorophyll_index < 20:
            indicators.append('Low chlorophyll levels')
        
        return indicators
    
    def get_growth_status(self):
        """Get growth status description"""
        if self.growth_rate_cm_per_week >= 2.0:
            return "Excellent growth"
        elif self.growth_rate_cm_per_week >= 1.0:
            return "Good growth"
        elif self.growth_rate_cm_per_week >= 0.5:
            return "Moderate growth"
        else:
            return "Slow growth"
    
    def __repr__(self):
        return f"<PlantReading(id={self.id}, plant_type='{self.plant_type}', plant_id='{self.plant_id}', health_score={self.health_score})>"
