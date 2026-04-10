from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from datetime import datetime, timedelta
from app.database import get_db
from app.models import User, OTPVerification
from app.schemas import OTPRequest, OTPVerify, TokenResponse, UserResponse
from app.security import create_access_token, generate_otp, verify_token
from app.utils.validators import validate_phone

router = APIRouter()


@router.post("/send-otp", response_model=dict)
async def send_otp(
    otp_request: OTPRequest,
    db: AsyncSession = Depends(get_db)
):
    """Send OTP to phone number (mock for development)"""
    try:
        # Validate phone number
        if not validate_phone(otp_request.phone):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid phone number format"
            )

        # Generate OTP
        otp_code = generate_otp()

        # Check if user exists, create if not
        result = await db.execute(
            select(User).where(User.phone == otp_request.phone)
        )
        user = result.scalar_one_or_none()

        if not user:
            user = User(phone=otp_request.phone)
            db.add(user)
            await db.commit()
            await db.refresh(user)

        # Store OTP in database
        otp_record = OTPVerification(
            phone=otp_request.phone,
            otp_code=otp_code,
            expires_at=datetime.utcnow() + timedelta(minutes=5)
        )
        db.add(otp_record)
        await db.commit()

        # In production, send SMS via Twilio
        # For development, print OTP to console
        print(f"[OTP] for {otp_request.phone}: {otp_code}")

        return {
            "message": "OTP sent successfully",
            "phone": otp_request.phone,
            "mock_otp": otp_code  # Remove in production
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Send OTP error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp(
    otp_verify: OTPVerify,
    db: AsyncSession = Depends(get_db)
):
    """Verify OTP and return JWT token"""
    try:
        # Find latest OTP for this phone
        result = await db.execute(
            select(OTPVerification)
            .where(OTPVerification.phone == otp_verify.phone)
            .order_by(desc(OTPVerification.created_at))
            .limit(1)
        )
        otp_record = result.scalar_one_or_none()

        if not otp_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No OTP found for this phone number"
            )

        # Clean up old OTP records for this phone
        cleanup_result = await db.execute(
            select(OTPVerification)
            .where(OTPVerification.phone == otp_verify.phone, OTPVerification.id != otp_record.id)
        )
        old_otps = cleanup_result.scalars().all()
        for old_otp in old_otps:
            await db.delete(old_otp)
        await db.commit()

        # Check if OTP is expired
        if datetime.utcnow() > otp_record.expires_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP has expired"
            )

        # Check if OTP matches
        if otp_record.otp_code != otp_verify.otp_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP code"
            )

        # Mark as verified
        otp_record.is_verified = True
        await db.commit()

        # Get or create user
        result = await db.execute(
            select(User).where(User.phone == otp_verify.phone)
        )
        user = result.scalar_one_or_none()

        if not user:
            user = User(phone=otp_verify.phone)
            db.add(user)
            await db.commit()
            await db.refresh(user)

        # Create JWT token
        access_token = create_access_token(
            data={"sub": user.id},
            expires_delta=timedelta(hours=24)
        )

        # Create user response
        user_response = UserResponse.model_validate(user)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_response
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] OTP verification error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    user_id: int = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    """Get current user profile"""

    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse.from_orm(user)


@router.put("/me", response_model=UserResponse)
async def update_user(
    user_update: dict,
    user_id: int = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    """Update user profile"""

    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update fields
    for key, value in user_update.items():
        if hasattr(user, key):
            setattr(user, key, value)

    await db.commit()
    await db.refresh(user)

    return UserResponse.from_orm(user)
