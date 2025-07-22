"""
Soil data model for storing soil sensor readings
"""

from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates

Base = declarative_base()

class SoilReading(Base):
    __tablename__ = 'soil_readings'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    location = Column(String(100), nullable=False, default='default')
    
    # Soil nutrients (ppm - parts per million)
    nitrogen = Column(Float, nullable=False)
    phosphorus = Column(Float, nullable=False)
    potassium = Column(Float, nullable=False)
    
    # Soil physical properties
    ph_level = Column(Float, nullable=False)
    moisture_percent = Column(Float, nullable=False)
    temperature_celsius = Column(Float, nullable=False)
    electrical_conductivity = Column(Float, nullable=False)  # mS/cm
    
    # Soil quality indicators
    organic_matter_percent = Column(Float, default=0.0)
    salinity_level = Column(Float, default=0.0)
    
    # System fields
    sensor_id = Column(String(50), nullable=False)
    is_valid = Column(Boolean, default=True)
    notes = Column(String(500), default='')
    
    @validates('ph_level')
    def validate_ph(self, key, ph):
        if ph < 0 or ph > 14:
            raise ValueError("pH must be between 0 and 14")
        return ph
    
    @validates('moisture_percent')
    def validate_moisture(self, key, moisture):
        if moisture < 0 or moisture > 100:
            raise ValueError("Moisture percentage must be between 0 and 100")
        return moisture
    
    @validates('temperature_celsius')
    def validate_temperature(self, key, temp):
        if temp < -50 or temp > 80:
            raise ValueError("Temperature must be between -50 and 80 Celsius")
        return temp
    
    def to_dict(self):
        """Convert soil reading to dictionary"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'location': self.location,
            'nitrogen': self.nitrogen,
            'phosphorus': self.phosphorus,
            'potassium': self.potassium,
            'ph_level': self.ph_level,
            'moisture_percent': self.moisture_percent,
            'temperature_celsius': self.temperature_celsius,
            'electrical_conductivity': self.electrical_conductivity,
            'organic_matter_percent': self.organic_matter_percent,
            'salinity_level': self.salinity_level,
            'sensor_id': self.sensor_id,
            'is_valid': self.is_valid,
            'notes': self.notes
        }
    
    def get_npk_ratio(self):
        """Calculate NPK ratio"""
        total = self.nitrogen + self.phosphorus + self.potassium
        if total == 0:
            return (0, 0, 0)
        return (
            round(self.nitrogen / total * 100, 1),
            round(self.phosphorus / total * 100, 1),
            round(self.potassium / total * 100, 1)
        )
    
    def is_nutrient_deficient(self, config):
        """Check if any nutrients are below optimal levels"""
        deficiencies = []
        
        if self.nitrogen < config.NITROGEN_MIN:
            deficiencies.append('nitrogen')
        if self.phosphorus < config.PHOSPHORUS_MIN:
            deficiencies.append('phosphorus')
        if self.potassium < config.POTASSIUM_MIN:
            deficiencies.append('potassium')
            
        return deficiencies
    
    def get_soil_quality_score(self, config):
        """Calculate overall soil quality score (0-100)"""
        score = 100
        
        # pH score (optimal range 6.0-7.5)
        if self.ph_level < config.SOIL_PH_MIN or self.ph_level > config.SOIL_PH_MAX:
            score -= 20
        
        # Moisture score
        if self.moisture_percent < config.SOIL_MOISTURE_MIN or self.moisture_percent > config.SOIL_MOISTURE_MAX:
            score -= 15
        
        # Temperature score
        if self.temperature_celsius < config.SOIL_TEMP_MIN or self.temperature_celsius > config.SOIL_TEMP_MAX:
            score -= 10
        
        # Nutrient scores
        if self.nitrogen < config.NITROGEN_MIN:
            score -= 15
        if self.phosphorus < config.PHOSPHORUS_MIN:
            score -= 15
        if self.potassium < config.POTASSIUM_MIN:
            score -= 15
        
        # Salinity penalty
        if self.salinity_level > 2.0:  # High salinity
            score -= 10
        
        return max(0, score)
    
    def __repr__(self):
        return f"<SoilReading(id={self.id}, location='{self.location}', timestamp='{self.timestamp}')>"
