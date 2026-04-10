"""
Seed script to create test user and sample data
Run: cd backend && venv\Scripts\python.exe seed_data.py
"""
import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base
from app.models import User, SensorReading, Alert, AdviceLog, ResourceLog
from app.security import create_access_token
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

# Create synchronous engine
SYNC_DATABASE_URL = "sqlite:///./krishidrishti.db"
sync_engine = create_engine(SYNC_DATABASE_URL, echo=False)


def seed_database():
    """Create test user and sample data"""
    
    print("🌱 Seeding database...")
    
    # Create tables
    Base.metadata.create_all(bind=sync_engine)
    
    with Session(sync_engine) as db:
        try:
            # Check if test user already exists
            result = db.execute(
                select(User).where(User.phone == "+919876543210")
            )
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                print(f"\n{'='*60}")
                print("✅ TEST USER ALREADY EXISTS!")
                print(f"{'='*60}")
                print(f"📱 Phone: {existing_user.phone}")
                print(f"👤 Name: {existing_user.name}")
                print(f"🌾 Crop: {existing_user.crop_type}")
                print(f"📍 Location: {existing_user.location_lat}, {existing_user.location_lng}")
                print(f"📐 Farm Area: {existing_user.farm_area_acres} acres")
                
                # Generate token for manual testing
                token = create_access_token(data={"sub": existing_user.id})
                print(f"\n🔐 JWT Token (valid for 24h):")
                print(token)
                print(f"\n{'='*60}")
                print("💡 Use phone + OTP 123456 to login")
                print(f"{'='*60}")
                return
            
            # Create test user
            test_user = User(
                phone="+919876543210",
                name="Rajesh Kumar",
                email="rajesh@example.com",
                language="en",
                location_lat=21.1458,  # Nagpur
                location_lng=79.0882,
                crop_type="wheat",
                farm_area_acres=5.0,
                whatsapp_opt_in=True,
                sms_opt_in=True,
                email_opt_in=False,
                voice_opt_in=True
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            
            print(f"✅ Created test user with ID: {test_user.id}")
            
            # Generate sample sensor readings (last 7 days, every hour)
            print("📊 Creating sample sensor readings...")
            sensor_readings = []
            now = datetime.utcnow()
            
            for i in range(7 * 24):  # 7 days hourly
                timestamp = now - timedelta(hours=i)
                reading = SensorReading(
                    user_id=test_user.id,
                    timestamp=timestamp,
                    temperature=28 + random.uniform(-5, 10),
                    humidity=60 + random.uniform(-15, 20),
                    soil_moisture_surface=400 + random.uniform(-100, 200),
                    soil_moisture_root=500 + random.uniform(-150, 250),
                    ph_level=6.5 + random.uniform(-0.5, 0.8),
                    rain_detected=random.choice([True, False, False, False]),
                    water_tank_level=60 + random.uniform(-30, 30),
                    is_synced=True
                )
                sensor_readings.append(reading)
            
            db.add_all(sensor_readings)
            db.commit()
            print(f"✅ Created {len(sensor_readings)} sensor readings")
            
            # Generate sample resource logs
            print("💧 Creating sample resource logs...")
            resource_logs = []
            
            for i in range(7):
                date = now.date() - timedelta(days=i)
                log = ResourceLog(
                    user_id=test_user.id,
                    date=date,
                    water_used_liters=300 + random.uniform(-100, 300),
                    irrigation_duration_min=random.randint(30, 120),
                    water_saved_liters=100 + random.uniform(-50, 200),
                    fertilizer_used_grams=random.choice([0, 0, 0, 500, 1000, 1500]),
                    fertilizer_type=random.choice(["urea", "dap", "npk", None]),
                    estimated_cost_rupees=200 + random.uniform(-100, 500),
                    energy_kwh=random.uniform(2, 8)
                )
                resource_logs.append(log)
            
            db.add_all(resource_logs)
            db.commit()
            print(f"✅ Created {len(resource_logs)} resource logs")
            
            # Generate sample alerts
            print("🔔 Creating sample alerts...")
            alerts = [
                Alert(
                    user_id=test_user.id,
                    timestamp=now - timedelta(hours=2),
                    type="WARNING",
                    channel="whatsapp",
                    message_en="Soil moisture is low. Consider irrigating within 6 hours.",
                    message_hi="मिट्टी की नमी कम है। 6 घंटे के भीतर सिंचाई करें।",
                    message_mr="मातीची ओलावा कमी आहे. ६ तासांच्या आत पाणी द्या."
                ),
                Alert(
                    user_id=test_user.id,
                    timestamp=now - timedelta(hours=8),
                    type="INFO",
                    channel="sms",
                    message_en="Rain expected tomorrow. Delay fertilizer application.",
                    message_hi="कल बारिश की उम्मीद। उर्वरक application स्थगित करें।",
                    message_mr="उद्या पावसाची अपेक्षा. खत टाकणे पुढे ढकला."
                ),
                Alert(
                    user_id=test_user.id,
                    timestamp=now - timedelta(days=2),
                    type="CRITICAL",
                    channel="voice",
                    message_en="High temperature alert! Protect crops from heat stress.",
                    message_hi="उच्च तापमान चेतावनी! फसलों को गर्मी से बचाएं।",
                    message_mr="उच्च तापमान चेतावणी! पिकांना उष्णतेपासून वाचवा."
                )
            ]
            
            db.add_all(alerts)
            db.commit()
            print(f"✅ Created {len(alerts)} alerts")
            
            # Generate sample advice logs
            print("💬 Creating sample advice logs...")
            advice_logs = [
                AdviceLog(
                    user_id=test_user.id,
                    timestamp=now - timedelta(hours=5),
                    question="Should I irrigate my wheat crop now?",
                    answer="Soil moisture levels are adequate (580 ADC). Wait 12-24 hours before irrigation.",
                    context_used={"crop": "wheat", "sensor_data": {"soil_moisture": 580}},
                    confidence_score=82.5,
                    language="en",
                    recommendation_type="WAIT"
                ),
                AdviceLog(
                    user_id=test_user.id,
                    timestamp=now - timedelta(days=1),
                    question="What fertilizer should I use for wheat?",
                    answer="Apply 2kg urea + 1.5kg DAP per acre. Mix well with soil and irrigate lightly.",
                    context_used={"crop": "wheat", "growth_stage": "tillering"},
                    confidence_score=78.0,
                    language="en",
                    recommendation_type="FERTILIZE"
                ),
                AdviceLog(
                    user_id=test_user.id,
                    timestamp=now - timedelta(days=3),
                    question="How to control aphids in wheat?",
                    answer="Spray imidacloprid 0.3ml/L or neem oil 5ml/L in evening.",
                    context_used={"crop": "wheat", "pest_type": "aphids"},
                    confidence_score=75.0,
                    language="en",
                    recommendation_type="PEST_CONTROL"
                )
            ]
            
            db.add_all(advice_logs)
            db.commit()
            print(f"✅ Created {len(advice_logs)} advice logs")
            
            # Generate token for testing
            token = create_access_token(data={"sub": test_user.id})
            
            print(f"\n{'='*60}")
            print("✅ DATABASE SEEDED SUCCESSFULLY!")
            print(f"{'='*60}")
            print(f"\n📋 LOGIN CREDENTIALS:")
            print(f"📱 Phone: {test_user.phone}")
            print(f"👤 Name: {test_user.name}")
            print(f"🌾 Crop: {test_user.crop_type}")
            print(f"📍 Location: Nagpur, Maharashtra")
            print(f"📐 Farm Area: {test_user.farm_area_acres} acres")
            print(f"\n🔐 Sample JWT Token (valid 24h):")
            print(token)
            print(f"\n💡 Use the phone number + OTP (123456) to login")
            print(f"{'='*60}")
            
        except Exception as e:
            print(f"❌ Error seeding database: {e}")
            import traceback
            traceback.print_exc()
            db.rollback()


if __name__ == "__main__":
    seed_database()
