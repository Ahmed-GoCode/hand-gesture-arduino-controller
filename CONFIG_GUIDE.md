# AK-AHMD Configuration Guide

## What is ak_config.json?

The `ak_config.json` file is the central configuration system for the AK Hand Gesture Arduino Controller. It's a structured text file that stores all the settings needed to customize how the system behaves.

## Purpose and Benefits

### 1. **Centralized Settings Management**
- All system settings in one place
- Easy to backup and share configurations
- No need to modify source code for customization

### 2. **Hardware Adaptation**
- Configure for different Arduino boards and ports
- Support multiple camera devices
- Adjust for different communication speeds

### 3. **Performance Tuning**
- Fine-tune hand detection sensitivity
- Optimize tracking stability
- Adjust timeouts for your hardware

### 4. **User Customization**
- Personalize window titles and interface
- Enable/disable debug features
- Save preferred settings permanently

### 5. **Troubleshooting Support**
- Enable detailed logging when needed
- Adjust timeouts for debugging
- Test different hardware configurations

## How the System Uses the JSON File

### Startup Process:
1. **File Check**: System looks for `ak_config.json` in the project directory
2. **Auto-Creation**: If not found, creates file with default settings
3. **Loading**: Reads all settings into the AKConfigManager class
4. **Validation**: Ensures all required settings are present
5. **Fallback**: Uses defaults for any missing or invalid settings

### Runtime Behavior:
- Settings are accessed throughout the application
- Command line arguments can override JSON settings temporarily
- Changes can be saved back to the file for persistence

## Configuration Categories

### Hardware Settings
```json
{
    "serial_port": "COM3",        // Arduino connection port
    "baud_rate": 9600,           // Communication speed
    "camera_index": 0            // Which camera to use
}
```

### Detection Settings
```json
{
    "min_detection_confidence": 0.5,  // How easily hands are detected
    "min_tracking_confidence": 0.5    // How stable tracking should be
}
```

### System Settings
```json
{
    "window_name": "AK Hand Gesture Controller",  // Display window title
    "serial_timeout": 2,                          // Communication timeout
    "debug_mode": false                           // Enable detailed logging
}
```

## Common Use Cases

### 1. **Multiple Arduino Setups**
Different computers or USB ports:
```json
{
    "serial_port": "COM5"  // Change for your specific port
}
```

### 2. **External Camera**
Using USB webcam instead of built-in camera:
```json
{
    "camera_index": 1
}
```

### 3. **Sensitive Hand Detection**
For poor lighting or distant hands:
```json
{
    "min_detection_confidence": 0.3,
    "min_tracking_confidence": 0.3
}
```

### 4. **Stable Tracking**
For environments with distractions:
```json
{
    "min_detection_confidence": 0.7,
    "min_tracking_confidence": 0.7
}
```

### 5. **Development Mode**
For debugging and testing:
```json
{
    "debug_mode": true,
    "serial_timeout": 10
}
```

## Best Practices

### 1. **Backup Your Configuration**
```bash
# Keep a backup of working settings
cp ak_config.json ak_config_backup.json
```

### 2. **Test Changes Gradually**
- Change one setting at a time
- Test thoroughly before making more changes
- Keep note of what works best for your setup

### 3. **Use Command Line for Testing**
```bash
# Test different settings without modifying the file
python hand_arduino_controller.py --port COM5 --camera 1 --debug
```

### 4. **Environment-Specific Configs**
Create different config files for different setups:
- `ak_config_home.json` - Home setup
- `ak_config_office.json` - Office setup
- `ak_config_demo.json` - Demonstration setup

## Troubleshooting with JSON Config

### Connection Issues
```json
{
    "serial_timeout": 5,     // Increase timeout
    "debug_mode": true       // See detailed connection logs
}
```

### Detection Problems
```json
{
    "min_detection_confidence": 0.3,  // More sensitive detection
    "debug_mode": true                 // See detection details
}
```

### Performance Issues
```json
{
    "min_tracking_confidence": 0.7,   // More stable tracking
    "serial_timeout": 1                // Faster communication
}
```

## Integration with AK-AHMD System

The JSON configuration integrates seamlessly with the AK-AHMD codebase:

- **AKConfigManager**: Handles loading and saving
- **Command Line Interface**: Can override any setting
- **Error Handling**: Graceful fallback to defaults
- **Runtime Updates**: Settings can be modified and saved during execution

This configuration system makes the AK-AHMD Hand Gesture Controller highly adaptable to different hardware setups, user preferences, and environmental conditions.