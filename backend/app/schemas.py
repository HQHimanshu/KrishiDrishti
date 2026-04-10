from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date


# User schemas
class UserBase(BaseModel):
    phone: str = Field(..., min_length=10, max_length=15)
    email: Optional[str] = None
    name: Optional[str] = None
    language: str = Field(default="hi", pattern="^(hi|mr|en)$")
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None
    crop_type: Optional[str] = None
    farm_area_acres: Optional[float] = None
    whatsapp_opt_in: bool = True
    sms_opt_in: bool = True
    email_opt_in: bool = False
    voice_opt_in: bool = True


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    language: Optional[str] = Field(default=None, pattern="^(hi|mr|en)$")
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None
    crop_type: Optional[str] = None
    farm_area_acres: Optional[float] = None
    whatsapp_opt_in: Optional[bool] = None
    sms_opt_in: Optional[bool] = None
    email_opt_in: Optional[bool] = None
    voice_opt_in: Optional[bool] = None


# Auth schemas
class OTPRequest(BaseModel):
    phone: str = Field(..., min_length=10, max_length=15)


class OTPVerify(BaseModel):
    phone: str = Field(..., min_length=10, max_length=15)
    otp_code: str = Field(..., min_length=6, max_length=6)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# Sensor schemas
class SensorDataCreate(BaseModel):
    temperature: Optional[float] = Field(None, ge=-10, le=60)
    humidity: Optional[float] = Field(None, ge=0, le=100)
    soil_moisture_surface: Optional[float] = Field(None, ge=0, le=1023)
    soil_moisture_root: Optional[float] = Field(None, ge=0, le=1023)
    ph_level: Optional[float] = Field(None, ge=0, le=14)
    rain_detected: bool = False
    water_tank_level: Optional[float] = Field(None, ge=0, le=100)
    
    @validator('ph_level')
    def validate_ph(cls, v):
        if v is not None and (v < 4 or v > 9):
            raise ValueError("Unusual pH value - check sensor calibration")
        return v


class SensorResponse(BaseModel):
    id: int
    user_id: int
    timestamp: datetime
    temperature: Optional[float]
    humidity: Optional[float]
    soil_moisture_surface: Optional[float]
    soil_moisture_root: Optional[float]
    ph_level: Optional[float]
    rain_detected: bool
    water_tank_level: Optional[float]
    is_synced: bool
    
    class Config:
        from_attributes = True


class SensorHistoryResponse(BaseModel):
    readings: List[SensorResponse]
    total: int


# Advice schemas
class AdviceRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    sensor_data: Optional[dict] = None


class AdviceResponse(BaseModel):
    recommendation: str
    reason: str
    action: str
    risk: Optional[str] = None
    confidence_score: Optional[float] = None
    language: str
    context_sources: Optional[dict] = None
    optimization_tips: Optional[str] = None
    estimated_impact: Optional[str] = None
    sensor_context: Optional[dict] = None
    weather_context: Optional[dict] = None


class AdviceHistoryItem(BaseModel):
    id: int
    question: str
    answer: Optional[str]
    timestamp: datetime
    recommendation_type: Optional[str]
    language: str
    
    class Config:
        from_attributes = True


# Alert schemas
class AlertResponse(BaseModel):
    id: int
    type: str
    channel: str
    message_en: Optional[str]
    message_hi: Optional[str]
    message_mr: Optional[str]
    status: str
    is_read: bool
    timestamp: datetime
    
    class Config:
        from_attributes = True


class AlertTestRequest(BaseModel):
    channel: str = Field(default="all", pattern="^(whatsapp|sms|email|voice|all)$")
    message_key: Optional[str] = "irrigate_now"


# Resource schemas
class ResourceLogCreate(BaseModel):
    date: Optional[date] = None
    water_used_liters: float = Field(default=0, ge=0)
    irrigation_duration_min: int = Field(default=0, ge=0)
    fertilizer_used_grams: float = Field(default=0, ge=0)
    fertilizer_type: Optional[str] = None
    estimated_cost_rupees: float = Field(default=0, ge=0)
    energy_kwh: float = Field(default=0, ge=0)


class ResourceLogResponse(BaseModel):
    id: int
    user_id: int
    date: date
    water_used_liters: float
    irrigation_duration_min: int
    water_saved_liters: float
    fertilizer_used_grams: float
    fertilizer_type: Optional[str]
    estimated_cost_rupees: float
    energy_kwh: float
    
    class Config:
        from_attributes = True


class ResourceSummary(BaseModel):
    total_water_used_liters: float
    total_water_saved_liters: float
    total_fertilizer_used_grams: float
    total_cost_rupees: float
    total_energy_kwh: float
    water_budget_liters: float
    water_usage_percentage: float
    status: str
    message: Optional[str] = None


# Weather schemas
class WeatherResponse(BaseModel):
    temperature: float
    feels_like: float
    humidity: float
    description: str
    wind_speed: float
    pressure: float
    forecast: Optional[list] = None
    alert: Optional[str] = None


# Dashboard schemas
class DashboardMetrics(BaseModel):
    current_sensor_data: Optional[SensorResponse]
    weather: Optional[WeatherResponse]
    resource_summary: Optional[ResourceSummary]
    recent_alerts: List[AlertResponse]
    latest_advice: Optional[AdviceResponse]
