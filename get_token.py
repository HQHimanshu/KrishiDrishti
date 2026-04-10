"""
Get Fresh Authentication Token for KrishiDrishti
"""
import requests
import sqlite3
import os
from datetime import datetime

BACKEND_URL = "http://localhost:8000"

def get_fresh_token():
    """Get a fresh authentication token"""
    print("=" * 60)
    print("  KrishiDrishti - Get Fresh Token")
    print("=" * 60)
    print()
    
    # Get latest user from database
    db_path = os.path.join(os.path.dirname(__file__), "backend", "krishidrishti.db")
    if not os.path.exists(db_path):
        print(f"[ERROR] Database not found at: {db_path}")
        input("\nPress Enter to exit...")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT phone FROM users ORDER BY created_at DESC LIMIT 1")
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        print("[ERROR] No users found in database")
        input("\nPress Enter to exit...")
        return
    
    phone = user[0]
    print(f"[1/3] Getting OTP for user: {phone}")
    
    # Request OTP
    try:
        res1 = requests.post(
            f"{BACKEND_URL}/api/auth/send-otp",
            json={"phone": phone}
        )
        
        if res1.status_code != 200:
            print(f"[ERROR] Failed to send OTP: {res1.text}")
            input("\nPress Enter to exit...")
            return
        
        otp = res1.json().get("mock_otp", "123456")
        print(f"[OK] OTP received: {otp}")
        
    except Exception as e:
        print(f"[ERROR] Could not connect to backend: {e}")
        print("Make sure backend is running on port 8000")
        input("\nPress Enter to exit...")
        return
    
    # Verify OTP to get token
    print(f"\n[2/3] Verifying OTP...")
    res2 = requests.post(
        f"{BACKEND_URL}/api/auth/verify-otp",
        json={"phone": phone, "otp_code": otp}
    )
    
    if res2.status_code != 200:
        print(f"[ERROR] OTP verification failed: {res2.text}")
        input("\nPress Enter to exit...")
        return
    
    token = res2.json()["access_token"]
    
    # Display token
    print(f"\n[3/3] Token generated successfully!")
    print(f"\n{'='*60}")
    print(f"FRESH TOKEN:")
    print(f"{'='*60}")
    print(token)
    print(f"{'='*60}")
    print(f"\nUser: {phone}")
    print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
    
    print(f"\n{'='*60}")
    print("HOW TO USE THIS TOKEN:")
    print(f"{'='*60}")
    print("\nOption 1: Browser Console (Quick)")
    print("  1. Open http://localhost:5173")
    print("  2. Press F12 to open Developer Console")
    print("  3. Paste this command:")
    print(f'     localStorage.setItem("token", "{token}")')
    print("  4. Press Enter and refresh the page")
    
    print("\nOption 2: Login Normally (Recommended)")
    print(f"  1. Open http://localhost:5173")
    print(f"  2. Login with phone: {phone}")
    print(f"  3. Enter OTP: {otp}")
    print("  4. Token will be automatically set")
    
    print(f"\n{'='*60}")
    print("\nToken expires in 60 minutes")
    print(f"{'='*60}\n")
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    get_fresh_token()
