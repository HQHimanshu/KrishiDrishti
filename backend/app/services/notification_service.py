import aiosmtplib
from email.message import EmailMessage
from typing import Optional
from twilio.rest import Client
from gtts import gTTS
import os
from app.config import settings
from app.utils.translations import get_alert_message
from app.models import User


# Twilio client (initialized lazily)
_twilio_client = None


def get_twilio_client():
    global _twilio_client
    if _twilio_client is None and settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
        _twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    return _twilio_client


async def send_alert(user: User, message_key: str, data: dict = None) -> dict:
    """Send alert via user's preferred channels with regional language"""

    if data is None:
        data = {}

    # Fetch translations
    message_en = get_alert_message(message_key, "en")
    message_hi = get_alert_message(message_key, "hi")
    message_mr = get_alert_message(message_key, "mr")

    # Get message in user's language
    message = {
        "en": message_en,
        "hi": message_hi,
        "mr": message_mr
    }.get(user.language, message_en)

    results = {
        "whatsapp": None,
        "sms": None,
        "email": None,
        "voice": None
    }

    # Send via WhatsApp (primary channel)
    if user.whatsapp_opt_in:
        try:
            results["whatsapp"] = await send_whatsapp(user.phone, message)
            print(f"[OK] WhatsApp alert sent to {user.phone}")
        except Exception as e:
            print(f"[ERROR] WhatsApp alert failed: {e}")
            results["whatsapp"] = {"status": "FAILED", "error": str(e)}

    # Send via Email (for critical alerts)
    if user.email:
        try:
            email_subject = f"🌾 KrishiDrishti Alert: {message_key.replace('_', ' ').title()}"
            results["email"] = await send_email(user.email, email_subject, message)
            print(f"[OK] Email alert sent to {user.email}")
        except Exception as e:
            print(f"[ERROR] Email alert failed: {e}")
            results["email"] = {"status": "FAILED", "error": str(e)}

    # Send via SMS (fallback)
    if user.sms_opt_in and not results["whatsapp"]:
        try:
            results["sms"] = await send_sms(user.phone, message)
        except Exception as e:
            results["sms"] = {"status": "FAILED", "error": str(e)}

    # Send Voice Alert
    if user.voice_opt_in and settings.VOICE_ALERT_ENABLED:
        try:
            results["voice"] = await send_voice_alert(user.phone, message, user.language)
        except Exception as e:
            results["voice"] = {"status": "FAILED", "error": str(e)}

    return results


async def send_welcome_message(user: User) -> dict:
    """Send welcome message to new user via WhatsApp and Email"""
    
    welcome_msg = f"""🌾 Welcome to KrishiDrishti!

Dear {user.name or 'Farmer'},

Your account has been created successfully!

📱 Phone: {user.phone}
🌍 Language: {user.language.upper()}
📍 Location: {user.location_lat or 19.0760}°N, {user.location_lng or 72.8777}°E
🌾 Crop: {user.crop_type or 'Not set'}

You can now:
✅ Monitor sensor data in real-time
✅ Get AI-powered farming advice
✅ Track water & fertilizer usage
✅ Receive weather alerts

Need help? Ask me anything!

Happy Farming! 🚜
Team KrishiDrishti"""
    
    results = {"whatsapp": None, "email": None}
    
    # Send WhatsApp welcome
    if user.whatsapp_opt_in:
        try:
            results["whatsapp"] = await send_whatsapp(user.phone, welcome_msg)
            print(f"[OK] Welcome WhatsApp sent to {user.phone}")
        except Exception as e:
            print(f"[ERROR] Welcome WhatsApp failed: {e}")
    
    # Send Email welcome
    if user.email:
        try:
            email_subject = "🌾 Welcome to KrishiDrishti - Your AI Farming Assistant!"
            email_body = f"""
<h1>🌾 Welcome to KrishiDrishti!</h1>

<p>Dear <strong>{user.name or 'Farmer'}</strong>,</p>

<p>Your account has been created successfully!</p>

<h3>Account Details:</h3>
<ul>
    <li>📱 Phone: {user.phone}</li>
    <li>🌍 Language: {user.language.upper()}</li>
    <li>📍 Location: {user.location_lat or 19.0760}°N, {user.location_lng or 72.8777}°E</li>
    <li>🌾 Crop: {user.crop_type or 'Not set'}</li>
</ul>

<h3>Features Available:</h3>
<ul>
    <li>✅ Monitor sensor data in real-time</li>
    <li>✅ Get AI-powered farming advice</li>
    <li>✅ Track water & fertilizer usage</li>
    <li>✅ Receive weather alerts</li>
</ul>

<p>Need help? Just ask! You can chat with me anytime via WhatsApp or through the app.</p>

<p><strong>Happy Farming! 🚜</strong><br>
Team KrishiDrishti</p>

<hr>
<p style="font-size: 12px; color: #666;">This is an automated message from KrishiDrishti AI Assistant.</p>
"""
            results["email"] = await send_email(user.email, email_subject, email_body, is_html=True)
            print(f"[OK] Welcome email sent to {user.email}")
        except Exception as e:
            print(f"[ERROR] Welcome email failed: {e}")
    
    return results


async def send_chat_notification(user: User, question: str, answer: str) -> dict:
    """Send chat conversation summary via WhatsApp"""
    
    chat_summary = f"""💬 KrishiDrishti AI Chat Summary

📝 Your Question:
{question[:200]}

💡 AI Response:
{answer[:300]}

Want more details? Check the full conversation in your dashboard!

🌾 Team KrishiDrishti"""
    
    result = {"whatsapp": None}
    
    if user.whatsapp_opt_in:
        try:
            result["whatsapp"] = await send_whatsapp(user.phone, chat_summary)
            print(f"[OK] Chat summary sent via WhatsApp to {user.phone}")
        except Exception as e:
            print(f"[ERROR] chat summary WhatsApp failed: {e}")
    
    return result


async def send_whatsapp(phone: str, message: str) -> dict:
    """Send WhatsApp message via Twilio"""
    client = get_twilio_client()
    
    if client is None:
        # Mock for development
        print(f"[WhatsApp] To: {phone} | Message: {message}")
        return {"status": "MOCK_SENT", "phone": phone}
    
    try:
        message_obj = client.messages.create(
            from_=f"whatsapp:{settings.TWILIO_WHATSAPP_NUMBER}",
            body=message,
            to=f"whatsapp:+91{phone.lstrip('+91')}"
        )
        return {"status": "SENT", "sid": message_obj.sid}
    except Exception as e:
        return {"status": "FAILED", "error": str(e)}


async def send_sms(phone: str, message: str) -> dict:
    """Send SMS via Twilio"""
    client = get_twilio_client()
    
    if client is None:
        # Mock for development
        print(f"[SMS] To: {phone} | Message: {message}")
        return {"status": "MOCK_SENT", "phone": phone}
    
    try:
        message_obj = client.messages.create(
            body=message,
            from_="+1234567890",  # Your Twilio number
            to=f"+91{phone.lstrip('+91')}"
        )
        return {"status": "SENT", "sid": message_obj.sid}
    except Exception as e:
        return {"status": "FAILED", "error": str(e)}


async def send_email(email: str, subject: str, message: str, is_html: bool = False) -> dict:
    """Send email via SMTP with subject and HTML support"""
    if not settings.SMTP_EMAIL or not settings.SMTP_PASSWORD:
        print(f"[Email] To: {email} | Subject: {subject} | Message: {message[:100]}...")
        return {"status": "MOCK_SENT", "email": email, "subject": subject}

    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_EMAIL
        msg["To"] = email
        
        if is_html:
            msg.add_alternative(message, subtype='html')
        else:
            msg.set_content(message)

        await aiosmtplib.send(
            msg,
            hostname=settings.SMTP_SERVER,
            port=settings.SMTP_PORT,
            start_tls=True,
            username=settings.SMTP_EMAIL,
            password=settings.SMTP_PASSWORD
        )
        
        return {"status": "SENT"}
    except Exception as e:
        return {"status": "FAILED", "error": str(e)}


async def send_voice_alert(phone: str, message: str, language: str = "hi") -> dict:
    """Generate and send voice alert using gTTS"""
    try:
        # Create voice file
        lang_code = {
            "hi": "hi",
            "mr": "hi",  # Marathi uses Hindi voice as fallback
            "en": "en"
        }.get(language, "hi")
        
        tts = gTTS(text=message, lang=lang_code, slow=False)
        
        # Save to temp file
        temp_file = f"/tmp/voice_alert_{phone}.mp3"
        tts.save(temp_file)
        
        # In production, you would upload to a server and send SMS with link
        # For now, just log
        print(f"🔊 [Voice Alert] Generated: {temp_file}")
        print(f"   Message: {message}")
        
        return {"status": "GENERATED", "file": temp_file}
    except Exception as e:
        return {"status": "FAILED", "error": str(e)}


async def send_test_alert(channel: str = "all") -> dict:
    """Send test alert to verify notification system"""
    test_message = "KrishiDrishti test alert - कृषिदृष्टि परीक्षण सूचना"
    
    results = {}
    
    if channel in ["whatsapp", "all"]:
        results["whatsapp"] = await send_whatsapp("+919876543210", test_message)
    
    if channel in ["sms", "all"]:
        results["sms"] = await send_sms("+919876543210", test_message)
    
    if channel in ["email", "all"]:
        results["email"] = await send_email("test@example.com", test_message)
    
    if channel in ["voice", "all"]:
        results["voice"] = await send_voice_alert("+919876543210", test_message, "hi")
    
    return results
