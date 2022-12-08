#define USE_ARDUINO_INTERRUPTS true    // Set-up low-level interrupts for most acurate BPM math.
#include <PulseSensorPlayground.h>     // Includes the PulseSensorPlayground Library.   

//  Variables
const int PulseWire = 0;       // PulseSensor PURPLE WIRE connected to ANALOG PIN 0
int Threshold = 550;           // Determine which Signal to "count as a beat" and which to ignore.
                               // Use the "Gettting Started Project" to fine-tune Threshold Value beyond default setting.
                               // Otherwise leave the default "550" value. 
                               
PulseSensorPlayground pulseSensor;  // Creates an instance of the PulseSensorPlayground object called "pulseSensor"
int Signal;

  
void setup() {   

  Serial.begin(9600);          // For Serial Monitor

  // Configure the PulseSensor object, by assigning our variables to it.
  analogReference(EXTERNAL); //Clara
  pulseSensor.analogInput(PulseWire);
  pulseSensor.setThreshold(Threshold);   

  // Double-check the "pulseSensor" object was created and "began" seeing a signal. 
  if (pulseSensor.begin()) {
  //Serial.println("We created a pulseSensor Object !");  //This prints one time at Arduino power-up,  or on Arduino reset.  
  }
}



void loop() {
  //Signal = analogRead(0); 
  
  int myBPM = pulseSensor.getBeatsPerMinute();  // Calls function on our pulseSensor object that returns BPM as an "int".
                                               // "myBPM" hold this BPM value now. 
  int pulse_sample = pulseSensor.getLatestSample();

  //Serial.println(Signal); 
  //Serial.println(pulse_sample);
  Serial.println(String(myBPM) + "," + String(pulse_sample));  

  //if (pulseSensor.sawStartOfBeat()) {            // Constantly test to see if "a beat happened". 
  //Serial.println("♥  A HeartBeat Happened ! "); // If test is "true", print a message "a heartbeat happened".
  //Serial.print("BPM: ");                        // Print phrase "BPM: " 
                         // Print the value inside of myBPM. 
  //Serial.println(myBPM);  
  //}

  delay(20);                    // 20 considered best practice in a simple sketch.

}

  
