# AK-AHMD Hand Gesture Arduino Controller

## Project Overview

The **AK-AHMD Hand Gesture Arduino Controller** is an intelligent real-time system that bridges computer vision and physical hardware control. Developed by the AK & AHMD team, this project enables users to control Arduino-connected devices using simple hand gestures captured through a webcam.

## What It Does

**🖐️ Gesture Recognition**: Uses advanced MediaPipe technology to detect and count fingers (0-5) in real-time through your camera.

**⚡ Instant Communication**: Sends finger count data from Python application to Arduino via serial communication.

**💡 Visual Feedback**: Controls 5 LEDs connected to Arduino pins, where each LED represents one finger - providing immediate physical feedback for your gestures.

**🎯 Special Features**: 
- **Celebration Mode**: When 5 fingers are detected, triggers a special LED animation sequence
- **Reset Mode**: When no fingers are detected, turns off all LEDs
- **System Monitoring**: Built-in heartbeat system ensures reliable operation

## Technology Stack

- **Frontend**: Python with OpenCV for camera interface and MediaPipe for hand detection
- **Backend**: Arduino firmware with optimized LED control and serial communication
- **Configuration**: JSON-based settings for easy customization
- **Communication**: Serial protocol for real-time data transfer

## Key Benefits

- **Contactless Control**: Operate devices without physical touch
- **Real-time Response**: Instant feedback with minimal latency
- **Easy Setup**: Plug-and-play configuration with automatic device detection
- **Expandable**: Framework can be extended to control servos, motors, or other Arduino-compatible devices
- **Cross-platform**: Works on Windows, macOS, and Linux

## Perfect For

- **Educational Projects**: Learn computer vision and Arduino integration
- **Accessibility Solutions**: Alternative input methods for users with mobility challenges
- **IoT Prototyping**: Quick gesture-based control for smart home devices
- **Interactive Displays**: Engaging demonstrations and exhibitions
- **Research & Development**: Foundation for advanced gesture recognition systems

## Quick Stats

- **Detection Range**: 0-5 fingers with high accuracy
- **Response Time**: <100ms from gesture to LED response
- **Hardware Requirements**: Basic Arduino + 5 LEDs + webcam
- **Software Size**: Lightweight Python application with minimal dependencies

This project demonstrates the seamless integration of modern computer vision with traditional microcontroller programming, creating an intuitive and responsive gesture control system.