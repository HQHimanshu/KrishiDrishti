/*
 * KrishiDrishti Sensor Calibration Tool
 * 
 * Run this first to calibrate your soil moisture sensor
 * Then copy the DRY and WET values to sensor_node.ino
 */

#include <ArduinoJson.h>

#define SOIL_MOISTURE_PIN A0

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n🔧 Soil Moisture Sensor Calibration");
  Serial.println("=====================================");
  Serial.println("\nInstructions:");
  Serial.println("1. Keep sensor in AIR (dry) - wait 10 seconds");
  Serial.println("2. Note the 'DRY VALUE' shown");
  Serial.println("3. Put sensor in WATER (wet) - wait 10 seconds");
  Serial.println("4. Note the 'WET VALUE' shown");
  Serial.println("5. Update these values in sensor_node.ino:");
  Serial.println("   - SOIL_MOISTURE_DRY = your dry value");
  Serial.println("   - SOIL_MOISTURE_WET = your wet value");
  Serial.println("\nStarting calibration...\n");
}

void loop() {
  // Read sensor
  int sensorValue = analogRead(SOIL_MOISTURE_PIN);
  
  // Print values
  Serial.print("📊 Raw ADC: ");
  Serial.print(sensorValue);
  Serial.print(" | ");
  
  // Determine state
  if (sensorValue > 700) {
    Serial.println("🟡 DRY (In Air)");
  } else if (sensorValue < 400) {
    Serial.println("🔵 WET (In Water)");
  } else {
    Serial.println("🟢 Medium Moisture");
  }
  
  // Show what values to use
  Serial.print("   → Use DRY value: ");
  Serial.println(max(sensorValue, 800));
  Serial.print("   → Use WET value: ");
  Serial.println(min(sensorValue, 300));
  
  delay(1000);
}
