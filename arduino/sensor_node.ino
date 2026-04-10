/*
 * KrishiDrishti Arduino Firmware - USB SERIAL MODE
 * 
 * Works with: Arduino Uno, Nano, Mega (NO WiFi needed!)
 * 
 * Sensors:
 * - DHT11: Temperature & Humidity (Pin 2)
 * - Soil Moisture: Analog sensor (Pin A0)
 * - Rain Sensor: Digital module (Pin 3)
 * 
 * Output: JSON over USB Serial at 9600 baud
 * Backend reads this via: usb_serial_bridge.py
 * 
 * Wiring:
 * DHT11:
 *   VCC -> 5V
 *   GND -> GND
 *   DATA -> Pin 2
 * 
 * Soil Moisture:
 *   VCC -> 5V
 *   GND -> GND
 *   AOUT -> Pin A0
 * 
 * Rain Sensor:
 *   VCC -> 5V
 *   GND -> GND
 *   DOUT -> Pin 3
 */

#include <DHT.h>
#include <ArduinoJson.h>

// ============ SENSOR PINS ============
#define DHTPIN 2
#define DHTTYPE DHT11
#define SOIL_MOISTURE_PIN A0
#define RAIN_SENSOR_PIN 3

// Sensor Calibration
const int SOIL_MOISTURE_DRY = 800;    // ADC value when dry
const int SOIL_MOISTURE_WET = 300;    // ADC value when wet

// Update interval (milliseconds)
const unsigned long UPDATE_INTERVAL = 5000;  // Send data every 5 seconds

// ============ INITIALIZATION ============
DHT dht(DHTPIN, DHTTYPE);

unsigned long lastUpdate = 0;
int readingCount = 0;

void setup() {
  Serial.begin(9600);
  delay(1000);

  Serial.println("========================================");
  Serial.println("  KrishiDrishti - USB Sensor Node");
  Serial.println("========================================");
  Serial.println("Output: JSON over Serial at 9600 baud");
  Serial.println("");

  // Initialize sensors
  dht.begin();
  pinMode(RAIN_SENSOR_PIN, INPUT);
  
  Serial.println("[OK] Sensors initialized");
  Serial.println("[OK] Starting readings...\n");
  delay(1000);
}

void loop() {
  // Check if it's time to send data
  unsigned long currentMillis = millis();
  if (currentMillis - lastUpdate >= UPDATE_INTERVAL) {
    lastUpdate = currentMillis;
    readAndSendSensors();
  }
}

void readAndSendSensors() {
  readingCount++;
  
  // Read DHT11
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  
  // Check if DHT11 read failed
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("[WARNING] DHT11 read error, using last valid values");
    return;
  }
  
  // Read Soil Moisture (Analog 0-1023)
  int soilMoistureRaw = analogRead(SOIL_MOISTURE_PIN);
  float soilMoisturePercent = mapSoilMoisture(soilMoistureRaw);
  
  // Read Rain Sensor (Digital: LOW = rain detected)
  bool rainDetected = digitalRead(RAIN_SENSOR_PIN) == LOW;
  
  // Print human-readable to Serial (for debugging)
  Serial.println("----------------------------------------");
  Serial.print("Reading #");
  Serial.println(readingCount);
  Serial.print("  Temperature: ");
  Serial.print(temperature);
  Serial.println(" C");
  Serial.print("  Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");
  Serial.print("  Soil Moisture: ");
  Serial.print(soilMoistureRaw);
  Serial.print(" ADC (");
  Serial.print(soilMoisturePercent);
  Serial.println(" %)");
  Serial.print("  Rain: ");
  Serial.println(rainDetected ? "YES" : "NO");
  Serial.println("----------------------------------------");
  
  // Output JSON for backend (usb_serial_bridge.py reads this)
  StaticJsonDocument<256> doc;
  doc["temperature"] = temperature;
  doc["humidity"] = humidity;
  doc["soil_moisture"] = soilMoistureRaw;
  doc["soil_moisture_percent"] = soilMoisturePercent;
  doc["rain_detected"] = rainDetected;
  doc["rain_intensity"] = rainDetected ? 100 : 0;
  doc["ph_level"] = 6.8;  // Fixed (add pH sensor later)
  doc["water_level"] = 75.0;  // Fixed (add ultrasonic sensor later)
  doc["reading_number"] = readingCount;
  
  // Serialize and print JSON (single line, no formatting)
  String jsonString;
  serializeJson(doc, jsonString);
  Serial.println(jsonString);
  Serial.println("");  // Empty line for readability
}

float mapSoilMoisture(int rawValue) {
  // Convert ADC value to percentage (0-100%)
  int constrained = constrain(rawValue, SOIL_MOISTURE_WET, SOIL_MOISTURE_DRY);
  return map(constrained, SOIL_MOISTURE_WET, SOIL_MOISTURE_DRY, 100, 0);
}
