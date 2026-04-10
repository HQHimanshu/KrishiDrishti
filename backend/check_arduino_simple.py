"""Quick check Arduino data"""
import sqlite3

conn = sqlite3.connect('krishidrishti.db')
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM sensor_readings")
count = cursor.fetchone()[0]
print(f"\n📊 Total sensor readings: {count}")

cursor.execute("SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT 3")
readings = cursor.fetchall()

if readings:
    print(f"\n✅ Last 3 readings:")
    for i, r in enumerate(readings):
        print(f"\n{'='*50}")
        print(f"#{i+1} ID: {r[0]}")
        print(f"👤 User ID: {r[1]}")
        print(f"⏰ Time: {r[2]}")
        print(f"🌡️  Temp: {r[3]}°C")
        print(f"💧 Humidity: {r[4]}%")
        print(f"🌱 Soil Surface: {r[5]} ADC")
        print(f"🌱 Soil Root: {r[6]} ADC")
        print(f"🧪 pH: {r[7]}")
        print(f"🌧️  Rain: {r[8]}")
        print(f"💧 Tank: {r[9]}%")
else:
    print("\n❌ No readings found!")

conn.close()
