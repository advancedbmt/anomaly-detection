# synthetic_data_generator
## TODOS
- batch (DONE)
- real-time (DONE)
- anomaly injection (DONE)
- csv injection (DONE)
- state time line (DONE)
- device info (Partially DONE)
- multiple devices to match SCADA design (Partially DONE)
  1. need to simulate 10 motors
  2. bale counter (one event per)
     a. need to implement vary value
  3. bale scale
     a. bale ID (random hash tag)
     b. bale wright (250 - 750 kg)
  4. production output (10 min)
     a. long fiber (340 - 400 kg)
     b. short fiber (600-700 kg)
     c. herd (1300 - 1500 kg)
  5. hatch (left, right)(TODO)
- incident injection (TODO)
  1. similiar to anomolyinjection
  2. need to inject seeral anomoly to different sensors based on one incident
- Support additional anomoly
  1. hatch open 
- state transaction  (Done)
- realtime data streaming  (Done)
- multi tag support (Done)
    1. modify the Json file format
    2. load the different tags (should work with the existing code)
    3. modify the data generation flow from one sensor and multi sensor
- intergation with MQTT (TODO)
1. waiting for MQTT schema
- intergation with Postgres
- multi device readin
- complex anomoly injection (stage 2)
- month based batch creation (stage 2, test item)

## complex anomoly type

### Bearing Issues
When motor bearings fail, several sensor readings are typically affected:
- Vibration: A significant increase in vibration levels is one of the earliest and most noticeable signs of bearing failure. Sensors may detect irregular or high-frequency vibrations caused by misalignment, pitting, or spalling in the bearings.
- Temperature: Bearing failure often leads to increased friction, which generates heat. Temperature sensors may show a rise in motor or bearing housing temperatures.
- RPM (Rotational Speed): While RPM may not always be directly affected, severe bearing damage can cause fluctuations or instability in rotational speed due to uneven load distribution.
- Power Consumption: As bearings degrade, the motor may require more power to overcome the increased friction, leading to higher energy consumption. Power sensors may detect this change.

### Overheating: (1)
Excessive heat can damage insulation and internal components, often caused by overloading, poor ventilation, or high ambient temperatures.
### Electrical Overload: (1)
When the motor draws more current than it is designed for, it can lead to overheating and damage. This may result from excessive load, low voltage, or short circuits.

### Insulation Breakdown: 
Degraded insulation can lead to short circuits or electrical leakage, often caused by contamination, aging, or overheating.
###Vibration: 
Misalignment, imbalance, or loose components can cause excessive vibration, leading to wear and tear.
### Contamination: 
Dirt, dust, or moisture entering the motor can damage internal components and reduce efficiency.
### Power Supply Issues: 
Voltage imbalances, surges, or poor-quality power can strain the motor and cause failures.
### Mechanical Failures: 
Problems like misaligned shafts, broken couplings, or worn-out parts can disrupt motor operation.
### Rotor or Stator Damage:(1) 
Physical damage to the rotor or stator can result in reduced performance or complete failure.
### unplaned power outage
30 minutes, check powerpoints
