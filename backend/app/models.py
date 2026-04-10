from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(15), unique=True, nullable=False, index=True)
    email = Column(String(120), nullable=True, index=True)
    name = Column(String(100), nullable=True)
    language = Column(String(5), default="hi")  # hi, mr, en
    location_lat = Column(Float, nullable=True)
    location_lng = Column(Float, nullable=True)
    crop_type = Column(String(50), nullable=True)  # wheat, rice, cotton
    farm_area_acres = Column(Float, nullable=True)
    whatsapp_opt_in = Column(Boolean, default=True)
    sms_opt_in = Column(Boolean, default=True)
    email_opt_in = Column(Boolean, default=False)
    voice_opt_in = Column(Boolean, default=True)
    is_offline_mode = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class SensorReading(Base):
    __tablename__ = "sensor_readings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Sensor values
    temperature = Column(Float, nullable=True)  # Celsius
    humidity = Column(Float, nullable=True)  # Percentage
    soil_moisture_surface = Column(Float, nullable=True)  # ADC 0-1023
    soil_moisture_root = Column(Float, nullable=True)  # ADC 0-1023
    ph_level = Column(Float, nullable=True)  # 0-14
    rain_detected = Column(Boolean, default=False)
    water_tank_level = Column(Float, nullable=True)  # Percentage
    
    # Offline sync flag
    is_synced = Column(Boolean, default=True, index=True)


class ResourceLog(Base):
    __tablename__ = "resource_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    date = Column(Date, server_default=func.now(), index=True)
    
    # Water tracking
    water_used_liters = Column(Float, default=0)
    irrigation_duration_min = Column(Integer, default=0)
    water_saved_liters = Column(Float, default=0)
    
    # Fertilizer tracking
    fertilizer_used_grams = Column(Float, default=0)
    fertilizer_type = Column(String(50), nullable=True)
    
    # Cost/energy
    estimated_cost_rupees = Column(Float, default=0)
    energy_kwh = Column(Float, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    type = Column(String(20), nullable=False)  # CRITICAL, WARNING, INFO
    channel = Column(String(20), nullable=False)  # whatsapp, sms, email, voice
    message_en = Column(Text, nullable=True)
    message_hi = Column(Text, nullable=True)
    message_mr = Column(Text, nullable=True)
    status = Column(String(20), default="PENDING")  # PENDING, SENT, FAILED
    is_read = Column(Boolean, default=False)
    error_message = Column(Text, nullable=True)


class AdviceLog(Base):
    __tablename__ = "advice_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)
    context_used = Column(JSON, nullable=True)
    confidence_score = Column(Float, nullable=True)
    language = Column(String(5), default="hi")
    recommendation_type = Column(String(50), nullable=True)  # IRRIGATE, WAIT, FERTILIZE, etc.


class OTPVerification(Base):
    __tablename__ = "otp_verifications"
    
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(15), nullable=False, index=True)
    otp_code = Column(String(6), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_verified = Column(Boolean, default=False)
