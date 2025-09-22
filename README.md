# AK Hand Gesture Arduino Controller by AHMD

An advanced hand gesture recognition system developed by AK & AHMD that detects finger count and sends commands to Arduino via serial communication.

## System Components

### Python Application (hand_arduino_controller.py)
- **AKConfigManager**: Configuration management system
- **AHMDHandDetector**: Real-time hand detection and finger counting
- **AKArduinoController**: Serial communication with Arduino
- **AHMDGestureController**: Main application controller

### Arduino Firmware (arduino_hand_controller.ino)
- Real-time LED control based on finger count
- Serial communication protocol
- Special gesture sequences (celebration, reset)
- System heartbeat monitoring

## Features

- Real-time hand detection using MediaPipe
- Finger counting (0-5 fingers) with visual feedback
- Arduino serial communication with LED indicators
- Configurable settings via JSON (ak_config.json)
- Cross-platform support (Windows, macOS, Linux)
- Command-line interface with multiple options
- Debug mode for troubleshooting
- Special gesture handling (0 fingers = reset, 5 fingers = celebration)
- System status monitoring and heartbeat

## Requirements

### Software Requirements
- Python 3.7+
- Arduino IDE (for Arduino programming)
- USB camera or webcam
- Required Python packages (see requirements.txt)

### Hardware Requirements
- Arduino board (Uno, Nano, etc.)
- 5 LEDs with appropriate resistors (220Ω recommended)
- USB cable for Arduino connection
- Breadboard and jumper wires

## Installation

### Python Setup
1. Clone or download this repository
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Arduino Setup
1. Open Arduino IDE
2. Load the `arduino/arduino_hand_controller.ino` file
3. Connect your Arduino board
4. Upload the sketch to your Arduino
5. Wire LEDs to digital pins 2-6 with appropriate resistors

### Hardware Wiring
```
Arduino Pin 2 → LED 1 (+ 220Ω resistor) → GND
Arduino Pin 3 → LED 2 (+ 220Ω resistor) → GND
Arduino Pin 4 → LED 3 (+ 220Ω resistor) → GND
Arduino Pin 5 → LED 4 (+ 220Ω resistor) → GND
Arduino Pin 6 → LED 5 (+ 220Ω resistor) → GND
```

## Usage

### Basic Usage

Run the AK-AHMD system with default settings:
```bash
python hand_arduino_controller.py
```

### Command Line Options

```bash
python hand_arduino_controller.py --help
```

Available options:
- `--config CONFIG_FILE`: Specify configuration file (default: ak_config.json)
- `--port SERIAL_PORT`: Override Arduino serial port
- `--camera CAMERA_INDEX`: Override camera index
- `--debug`: Enable AHMD debug mode

### Examples

```bash
# Use different serial port
python hand_arduino_controller.py --port COM5

# Use different camera
python hand_arduino_controller.py --camera 1

# Enable AHMD debug mode
python hand_arduino_controller.py --debug

# Use custom AK config file
python hand_arduino_controller.py --config my_ak_config.json
```

## Configuration

The AK-AHMD system uses a JSON configuration file (ak_config.json) that is automatically created on first run. You can modify these settings to customize the system behavior:

```json
{
    "serial_port": "COM3",
    "baud_rate": 9600,
    "camera_index": 0,
    "window_name": "AK Hand Gesture Controller",
    "min_detection_confidence": 0.5,
    "min_tracking_confidence": 0.5,
    "serial_timeout": 2,
    "debug_mode": false
}
```

### What is the JSON Configuration File?

The `ak_config.json` file serves as the central configuration hub for the AK-AHMD system. It allows you to:

1. **Customize Hardware Settings**: Configure serial ports, camera devices, and communication parameters
2. **Tune Detection Performance**: Adjust hand detection sensitivity and tracking accuracy
3. **Personalize User Interface**: Modify window names and display preferences
4. **Enable Debugging**: Turn on detailed logging for trtoubleshooting
5. **Save Preferences**: Sore your preferred settings between application runs
6. **Override Defaults**: Change system behavior without modifying the source code

### How It Works

- **Automatic Creation**: If the file doesn't exist, the system creates it with default values
- **Runtime Loading**: Settings are loaded when the application starts
- **Command Line Override**: Command line arguments can temporarily override JSON settings
- **Persistent Storage**: Changes made via command line can be saved back to the JSON file
- **Validation**: The system validates settings and falls back to defaults for invalid values

### Configuration Options

- `serial_port`: Arduino serial port (Windows: COM1, COM2, etc.; Linux/Mac: /dev/ttyUSB0, /dev/cu.usbmodem, etc.)
- `baud_rate`: Serial communication speed (default: 9600)
- `camera_index`: Camera device index (usually 0 for built-in camera, 1 for external USB camera)
- `window_name`: AK display window title shown in the application
- `min_detection_confidence`: AHMD hand detection confidence threshold (0.0-1.0) - lower values detect hands more easily but may have false positives
- `min_tracking_confidence`: AK hand tracking confidence threshold (0.0-1.0) - higher values provide smoother tracking but may lose hands more easily
- `serial_timeout`: AHMD serial communication timeout in seconds - how long to wait for Arduino response
- `debug_mode`: Enable detailed AK-AHMD logging for troubleshooting and development

### Example Configurations

**For Better Hand Detection (Lower Confidence)**:
```json
{
    "min_detection_confidence": 0.3,
    "min_tracking_confidence": 0.3
}
```

**For More Stable Tracking (Higher Confidence)**:
```json
{
    "min_detection_confidence": 0.7,
    "min_tracking_confidence": 0.7
}
```

**For Different Hardware Setup**:
```json
{
    "serial_port": "/dev/ttyUSB0",
    "camera_index": 1,
    "baud_rate": 115200
}
```

**For Development and Debugging**:
```json
{
    "debug_mode": true,
    "serial_timeout": 5
}
```

## Arduino Firmware Details

### AK-AHMD Arduino Functions

The Arduino firmware includes several specialized functions:

- **ahmdInitializeSerial()**: Initialize serial communication
- **akConfigurePins()**: Setup LED pins and built-in LED
- **ahmdValidateFingerCount()**: Validate received finger count data
- **ahmdUpdateLedDisplay()**: Update LED display based on finger count
- **akHandleSpecialGestures()**: Handle special gestures (0 and 5 fingers)
- **ahmdSystemHeartbeat()**: System monitoring and status indication

### Special Gesture Sequences

- **0 Fingers (Reset)**: All LEDs turn off (ahmdResetSequence)
- **5 Fingers (Celebration)**: Sequential LED animation (akCelebrationSequence)
- **System Heartbeat**: Built-in LED blinks every 5 seconds when system is ready

### Hardware Wiring Details

```
Pin Configuration:
- Digital Pin 2: LED 1 (Thumb)
- Digital Pin 3: LED 2 (Index Finger)
- Digital Pin 4: LED 3 (Middle Finger)
- Digital Pin 5: LED 4 (Ring Finger)
- Digital Pin 6: LED 5 (Pinky Finger)
- Built-in LED: System status and activity indicator
```

## How the AK-AHMD System Works

1. **AHMD Hand Detection**: Uses MediaPipe to detect hand landmarks in real-time
2. **AK Finger Counting**: Analyzes landmark positions to count extended fingers (0-5)
3. **Serial Communication**: Sends finger count from Python to Arduino via serial
4. **Arduino LED Control**: Arduino receives data and controls LEDs accordingly
5. **Visual Feedback**: Python displays hand landmarks and finger count on screen
6. **System Monitoring**: Both systems provide status feedback and error handling

### AK Finger Detection Algorithm

- **Thumb**: Checks horizontal position relative to previous joint
- **Other Fingers**: Checks vertical position of fingertip relative to middle joint
- **Range**: Detects 0-5 fingers reliably

## AK-AHMD System Controls

- **ESC**: Exit the AK application
- **Mouse**: Interact with the AHMD OpenCV window

## Troubleshooting

### Common Issues

1. **Camera not found**
   - Check camera connection
   - Try different camera index (--camera 1, 2, etc.)
   - Ensure no other applications are using the camera

2. **Arduino connection failed**
   - Check serial port in Device Manager (Windows) or system settings
   - Ensure Arduino is connected and recognized by the system
   - Try different COM ports (Windows) or /dev/tty* (Linux/Mac)
   - Verify baud rate matches Arduino code (9600)
   - Check Arduino firmware is properly uploaded

3. **AHMD hand detection not working**
   - Ensure good lighting conditions
   - Keep hand within camera view and at appropriate distance
   - Adjust detection confidence in ak_config.json
   - Try different camera angles

4. **LED indicators not responding**
   - Check Arduino wiring connections
   - Verify LED polarity (longer leg is positive)
   - Test individual LEDs with multimeter
   - Check resistor values (220Ω recommended)

5. **Import errors**
   - Install requirements: `pip install -r requirements.txt`
   - Check Python version (3.7+ required)
   - Verify MediaPipe and OpenCV installation

### AHMD Debug Mode

Enable AHMD debug mode for detailed logging:
```bash
python hand_arduino_controller.py --debug
```

### AK System Status

Monitor the Arduino serial output for system status:
- "AK-AHMD Hand Gesture Controller Ready!" - System initialized
- "AK Finger count: X" - Finger detection working
- Built-in LED heartbeat - System operational

## License

This AK-AHMD project is open source and available under the MIT License.

## Contributing

Contributions to the AK-AHMD system are welcome! Please feel free to submit issues, feature requests, or pull requests.

## Acknowledgments

- MediaPipe team for the excellent hand detection library
- OpenCV community for computer vision tools
- Arduino community for microcontroller platform
- AK & AHMD development team
