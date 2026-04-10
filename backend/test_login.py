"""Test the complete login flow"""
import asyncio
from app.database import get_db
from app.models import User, OTPVerification
from app.security import create_access_token
from app.schemas import UserResponse
from sqlalchemy import select, desc
from datetime import datetime

async def test_login_flow():
    async for db in get_db():
        try:
            phone = "+919876543210"
            otp_code = "123456"
            
            # Find latest OTP
            result = await db.execute(
                select(OTPVerification)
                .where(OTPVerification.phone == phone)
                .order_by(desc(OTPVerification.created_at))
            )
            otp_record = result.scalar_one_or_none()
            
            if not otp_record:
                print("❌ No OTP found")
                return
            
            print(f"✅ OTP found: {otp_record.otp_code}")
            
            # Check expiry
            if datetime.utcnow() > otp_record.expires_at:
                print("❌ OTP expired")
                return
            
            # Check code
            if otp_record.otp_code != otp_code:
                print("❌ OTP code mismatch")
                return
            
            print("✅ OTP valid")
            
            # Mark as verified
            otp_record.is_verified = True
            await db.commit()
            
            # Get user
            result = await db.execute(
                select(User).where(User.phone == phone)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                print("❌ User not found")
                return
            
            print(f"✅ User found: {user.name} (ID: {user.id})")
            
            # Create token
            token = create_access_token(data={"sub": user.id}, expires_delta=None)
            print(f"✅ Token created: {token[:50]}...")
            
            # Create user response
            try:
                user_response = UserResponse.from_orm(user)
                print(f"✅ UserResponse created: {user_response.name}")
            except Exception as e:
                print(f"❌ UserResponse failed: {e}")
                import traceback
                traceback.print_exc()
                return
            
            print("\n✅ LOGIN SUCCESS!")
            print(f"Token: {token}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            break

asyncio.run(test_login_flow())
