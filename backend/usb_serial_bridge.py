"""
Auto-start Arduino USB Serial Bridge for COM6
Automatically fetches JWT token from database
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import serial
import json
import time
import requests
from datetime import datetime

# Configuration
ARDUINO_PORT = "COM6"
BAUD_RATE = 9600
BACKEND_URL = "http://localhost:8000"

def get_latest_user_token():
    """Get JWT token from the most recent login"""
    try:
        # Query the database for the latest user
        import sqlite3
        db_path = os.path.join(os.path.dirname(__file__), "krishidrishti.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get latest user
        cursor.execute("SELECT id, phone FROM users ORDER BY created_at DESC LIMIT 1")
        user = cursor.fetchone()
        
        if user:
            user_id, phone = user
            print(f"[INFO] Found user: {phone} (ID: {user_id})")
            
            # Create a temporary token via API
            response = requests.post(
                f"{BACKEND_URL}/api/auth/send-otp",
                json={"phone": phone}
            )
            
            if response.status_code == 200:
                otp_data = response.json()
                otp = otp_data.get("mock_otp", "123456")
                
                # Verify OTP to get token
                verify_response = requests.post(
                    f"{BACKEND_URL}/api/auth/verify-otp",
                    json={"phone": phone, "otp_code": otp}
                )
                
                if verify_response.status_code == 200:
                    token = verify_response.json()["access_token"]
                    print(f"[OK] Got authentication token")
                    conn.close()
                    return token
        
        conn.close()
        return None
    except Exception as e:
        print(f"[ERROR] Failed to get token: {e}")
        return None

def parse_sensor_data(line):
    """Parse JSON data from Arduino"""
    try:
        line = line.strip()
        if not line or not line.startswith('{'):
            return None
        
        data = json.loads(line)
        
        # Map Arduino fields to backend fields
        sensor_data = {}
        
        # Temperature
        if "temperature" in data:
            sensor_data["temperature"] = float(data["temperature"])
        
        # Humidity
        if "humidity" in data:
            sensor_data["humidity"] = float(data["humidity"])
        
        # Soil moisture
        if "soil_moisture" in data or "soil_moisture_surface" in data:
            soil_val = data.get("soil_moisture") or data.get("soil_moisture_surface")
            sensor_data["soil_moisture_surface"] = float(soil_val)
            sensor_data["soil_moisture_root"] = float(soil_val)
        
        # pH level
        if "ph_level" in data or "ph" in data:
            sensor_data["ph_level"] = float(data.get("ph_level") or data.get("ph"))
        
        # Rain detection
        if "rain_detected" in data or "rain" in data or "rain_detection" in data:
            rain_val = data.get("rain_detected") or data.get("rain") or data.get("rain_detection")
            sensor_data["rain_detected"] = bool(rain_val)
        
        # Water tank level
        if "water_tank_level" in data or "water_level" in data:
            sensor_data["water_tank_level"] = float(data.get("water_tank_level") or data.get("water_level"))
        
        return sensor_data if sensor_data else None
        
    except Exception as e:
        print(f"[WARNING] Parse error: {e}")
        return None

def send_to_backend(sensor_data, token):
    """Send sensor data to backend"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(
            f"{BACKEND_URL}/api/sensors/",
            headers=headers,
            json=sensor_data,
            timeout=10
        )

        if response.status_code in [200, 201]:
            result = response.json()
            print(f"  [OK] Sent (ID: {result.get('id', 'N/A')})")
            return True
        elif response.status_code == 401:
            print("  [WARNING] Token expired! Getting new token...")
            return None  # Signal to refresh token
        elif response.status_code == 422:
            print(f"  [WARNING] Validation error: {response.text[:100]}")
            return False
        else:
            print(f"  [WARNING] Status: {response.status_code} - {response.text[:100]}")
            return False

    except requests.exceptions.ConnectionError:
        print("  [ERROR] Cannot connect to backend! Is it running?")
        return False
    except requests.exceptions.Timeout:
        print("  [ERROR] Request timeout!")
        return False
    except Exception as e:
        print(f"  [ERROR] Send failed: {e}")
        return False

def main():
    print("=" * 60)
    print("  Arduino USB Serial Bridge - COM6")
    print("=" * 60)
    print()
    
    # Get authentication token
    print("[1/3] Getting authentication token...")
    token = get_latest_user_token()
    
    if not token:
        print("\n[ERROR] Could not get authentication token!")
        print("Please login at http://localhost:5173 first")
        input("\nPress Enter to exit...")
        return
    
    # Open serial connection
    print(f"\n[2/3] Connecting to Arduino on {ARDUINO_PORT} at {BAUD_RATE} baud...")
    try:
        ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
        print(f"[OK] Connected to Arduino!")
    except Exception as e:
        print(f"\n[ERROR] Failed to connect to {ARDUINO_PORT}")
        print(f"Error: {e}")
        print("\nTroubleshooting:")
        print("  1. Check if Arduino is connected to COM6")
        print("  2. Close Arduino Serial Monitor (port may be in use)")
        print("  3. Check Device Manager for correct COM port")
        input("\nPress Enter to exit...")
        return
    
    # Read and send data
    print(f"\n[3/3] Listening for sensor data...")
    print("Press Ctrl+C to stop\n")

    count = 0
    sent_count = 0
    error_count = 0
    consecutive_errors = 0
    last_backend_check = 0

    try:
        while True:
            # Check backend connectivity periodically
            current_time = time.time()
            if current_time - last_backend_check > 30:  # Every 30 seconds
                try:
                    requests.get(f"{BACKEND_URL}/health", timeout=5)
                    if consecutive_errors > 0:
                        print("\n[OK] Backend is responsive again!")
                        consecutive_errors = 0
                except:
                    consecutive_errors += 1
                    if consecutive_errors <= 3:
                        print(f"\n[WARNING] Backend not reachable (attempt {consecutive_errors})")
                    last_backend_check = current_time
                    time.sleep(1)
                    continue
                last_backend_check = current_time

            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                
                if not line or not line.startswith('{'):
                    continue
                
                count += 1
                
                # Parse sensor data
                sensor_data = parse_sensor_data(line)
                
                if sensor_data is None:
                    continue
                
                # Display data
                print(f"\n{'='*60}")
                print(f"[Sensor Reading #{count}] {datetime.now().strftime('%H:%M:%S')}")
                print(f"{'='*60}")
                
                if "temperature" in sensor_data:
                    print(f"  Temperature: {sensor_data['temperature']}°C")
                if "humidity" in sensor_data:
                    print(f"  Humidity: {sensor_data['humidity']}%")
                if "soil_moisture_surface" in sensor_data:
                    print(f"  Soil Moisture: {sensor_data['soil_moisture_surface']} ADC")
                if "ph_level" in sensor_data:
                    print(f"  pH Level: {sensor_data['ph_level']}")
                if "rain_detected" in sensor_data:
                    print(f"  Rain: {'Yes' if sensor_data['rain_detected'] else 'No'}")
                if "water_tank_level" in sensor_data:
                    print(f"  Water Tank: {sensor_data['water_tank_level']}%")
                
                # Send to backend
                success = send_to_backend(sensor_data, token)
                
                if success is None:
                    # Token expired, get new one
                    token = get_latest_user_token()
                    if not token:
                        print("[ERROR] Failed to refresh token!")
                        error_count += 1
                    else:
                        # Retry sending
                        success = send_to_backend(sensor_data, token)
                
                if success:
                    sent_count += 1
                else:
                    error_count += 1
                
                print(f"\n[Summary] Total: {count} | Sent: {sent_count} | Errors: {error_count}")
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print(f"\n\n{'='*60}")
        print("  Stopping USB Serial Bridge...")
        print(f"{'='*60}")
        print(f"  Total readings: {count}")
        print(f"  Successfully sent: {sent_count}")
        print(f"  Errors: {error_count}")
        print(f"{'='*60}")
    finally:
        ser.close()
        print("[OK] Serial port closed")

if __name__ == "__main__":
    main()
