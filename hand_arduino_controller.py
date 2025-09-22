"""
AK Hand Gesture Arduino Controller

An advanced hand gesture recognition system by AHMD that detects finger count
and sends commands to Arduino via serial communication.

Features:
- Real-time hand detection using MediaPipe
- Finger counting (0-5 fingers)
- Arduino serial communication
- Configurable settings
- Cross-platform support

Author: AK & AHMD
License: MIT
"""

import cv2
import mediapipe as mp
import serial
import time
import json
import logging
from datetime import datetime
from typing import Optional, Tuple, List
import argparse


class AKConfigManager:
    """AK Configuration manager for the hand controller system."""
    
    def __init__(self, config_file: str = "ak_config.json"):
        self.config_file = config_file
        self.akDefaultConfig = {
            "serial_port": "COM3",
            "baud_rate": 9600,
            "camera_index": 0,
            "window_name": "AK Hand Gesture Controller",
            "min_detection_confidence": 0.5,
            "min_tracking_confidence": 0.5,
            "serial_timeout": 2,
            "debug_mode": False
        }
        self.config = self.ahmdLoadConfig()
    
    def ahmdLoadConfig(self) -> dict:
        """AHMD method to load configuration from file or create default."""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                return {**self.akDefaultConfig, **config}
        except FileNotFoundError:
            self.akSaveConfig(self.akDefaultConfig)
            return self.akDefaultConfig.copy()
    
    def akSaveConfig(self, config: dict = None) -> None:
        """AK method to save configuration to file."""
        config_to_save = config or self.config
        with open(self.config_file, 'w') as f:
            json.dump(config_to_save, f, indent=4)
    
    def ahmdGetConfig(self, key: str):
        """AHMD method to get configuration value."""
        return self.config.get(key)


class AHMDHandDetector:
    """AHMD Hand detection and finger counting system using MediaPipe."""
    
    def __init__(self, min_detection_confidence: float = 0.5, 
                 min_tracking_confidence: float = 0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.akFingerTipIds = [4, 8, 12, 16, 20]
        
    def akDetectHands(self, image) -> Tuple[any, List[List[Tuple[int, int, int]]]]:
        """AK method to detect hands in the image and return landmarks."""
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        
        all_landmarks = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = []
                h, w, c = image.shape
                
                for id, landmark in enumerate(hand_landmarks.landmark):
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    landmarks.append((id, cx, cy))
                
                all_landmarks.append(landmarks)
                
                self.ahmdDrawLandmarks(image, hand_landmarks)
        
        return results, all_landmarks
    
    def ahmdDrawLandmarks(self, image, hand_landmarks):
        """AHMD method to draw hand landmarks on image."""
        self.mp_draw.draw_landmarks(
            image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
            self.mp_draw.DrawingSpec(color=(0, 100, 100), thickness=1, circle_radius=3),
            self.mp_draw.DrawingSpec(color=(0, 100, 100), thickness=1)
        )
    
    def akCountFingers(self, landmarks: List[Tuple[int, int, int]]) -> int:
        """AK method to count the number of extended fingers."""
        if len(landmarks) != 21:
            return 0
        
        fingers = []
        
        if landmarks[self.akFingerTipIds[0]][1] > landmarks[self.akFingerTipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        
        for i in range(1, 5):
            if landmarks[self.akFingerTipIds[i]][2] < landmarks[self.akFingerTipIds[i] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers.count(1)


class AKArduinoController:
    """AK Arduino serial communication controller."""
    
    def __init__(self, port: str, baud_rate: int = 9600, timeout: int = 2):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.arduino = None
        self.isConnected = False
        
    def ahmdConnect(self) -> bool:
        """AHMD method to establish connection to Arduino."""
        try:
            self.arduino = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            time.sleep(2)
            self.isConnected = True
            logging.info(f"AK Arduino connected on {self.port}")
            return True
        except serial.SerialException as e:
            logging.error(f"AHMD Arduino connection failed: {e}")
            self.isConnected = False
            return False
    
    def akSendData(self, data: str) -> bool:
        """AK method to send data to Arduino."""
        if not self.isConnected or not self.arduino:
            return False
        
        try:
            self.arduino.write(bytes(str(data), 'utf-8'))
            return True
        except serial.SerialException as e:
            logging.error(f"AK data transmission failed: {e}")
            return False
    
    def ahmdDisconnect(self) -> None:
        """AHMD method to close Arduino connection."""
        if self.arduino and self.isConnected:
            self.arduino.close()
            self.isConnected = False
            logging.info("AHMD Arduino disconnected")


class AHMDGestureController:
    """AHMD Main controller class for hand gesture recognition and Arduino communication."""
    
    def __init__(self, config: AKConfigManager):
        self.config = config
        self.hand_detector = AHMDHandDetector(
            min_detection_confidence=config.ahmdGetConfig("min_detection_confidence"),
            min_tracking_confidence=config.ahmdGetConfig("min_tracking_confidence")
        )
        self.arduino = AKArduinoController(
            port=config.ahmdGetConfig("serial_port"),
            baud_rate=config.ahmdGetConfig("baud_rate"),
            timeout=config.ahmdGetConfig("serial_timeout")
        )
        self.camera = None
        self.running = False
        
        self.akSetupLogging()
    
    def akSetupLogging(self):
        """AK method to setup logging configuration."""
        level = logging.DEBUG if self.config.ahmdGetConfig("debug_mode") else logging.INFO
        logging.basicConfig(level=level, format='%(asctime)s - AK-AHMD - %(levelname)s - %(message)s')
    
    def ahmdInitializeCamera(self) -> bool:
        """AHMD method to initialize camera."""
        try:
            self.camera = cv2.VideoCapture(self.config.ahmdGetConfig("camera_index"))
            if not self.camera.isOpened():
                logging.error("AHMD camera initialization failed")
                return False
            logging.info("AK camera initialized successfully")
            return True
        except Exception as e:
            logging.error(f"AHMD camera error: {e}")
            return False
    
    def akCleanupResources(self) -> None:
        """AK method to clean up all resources."""
        if self.camera:
            self.camera.release()
        cv2.destroyAllWindows()
        self.arduino.ahmdDisconnect()
        logging.info("AK cleanup completed")
    
    def ahmdProcessFrame(self, frame):
        """AHMD method to process a single frame."""
        frame = cv2.flip(frame, 1)
        results, all_landmarks = self.hand_detector.akDetectHands(frame)
        
        finger_count = 0
        if all_landmarks:
            finger_count = self.hand_detector.akCountFingers(all_landmarks[0])
            
            if self.arduino.isConnected:
                self.arduino.akSendData(finger_count)
        
        return frame, finger_count
    
    def akDrawInterface(self, frame, finger_count):
        """AK method to draw interface elements on frame."""
        current_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        
        cv2.putText(frame, f'AK Fingers: {finger_count}', (20, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f'AHMD Time: {current_time}', (20, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        connection_status = "AK Connected" if self.arduino.isConnected else "AHMD Disconnected"
        cv2.putText(frame, f'Arduino: {connection_status}', (20, 130), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return frame
    
    def ahmdRunMainLoop(self) -> None:
        """AHMD main execution loop."""
        if not self.ahmdInitializeCamera():
            print("AK Error: Could not initialize camera")
            return
        
        if not self.arduino.ahmdConnect():
            print(f"AHMD Warning: Could not connect to Arduino on {self.config.ahmdGetConfig('serial_port')}")
            print("AK continuing in camera-only mode...")
        
        self.running = True
        print("AHMD Hand Gesture Controller started!")
        print("AK Press ESC to exit")
        
        try:
            while self.running:
                ret, frame = self.camera.read()
                if not ret:
                    logging.error("AHMD failed to read from camera")
                    break
                
                frame, finger_count = self.ahmdProcessFrame(frame)
                frame = self.akDrawInterface(frame, finger_count)
                
                cv2.imshow(self.config.ahmdGetConfig("window_name"), frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == 27:
                    break
                
        except KeyboardInterrupt:
            print("\nAHMD interrupted by user")
        except Exception as e:
            logging.error(f"AK runtime error: {e}")
        finally:
            self.akCleanupResources()


def ahmdParseArguments():
    """AHMD function to parse command line arguments."""
    parser = argparse.ArgumentParser(description="AK Hand Gesture Arduino Controller")
    parser.add_argument("--config", default="ak_config.json", 
                       help="AK configuration file path")
    parser.add_argument("--port", help="AHMD Arduino serial port (overrides config)")
    parser.add_argument("--camera", type=int, help="AK camera index (overrides config)")
    parser.add_argument("--debug", action="store_true", 
                       help="AHMD enable debug mode")
    
    return parser.parse_args()


def akApplyCommandOverrides(config: AKConfigManager, args):
    """AK function to apply command line argument overrides."""
    if args.port:
        config.config["serial_port"] = args.port
    if args.camera is not None:
        config.config["camera_index"] = args.camera
    if args.debug:
        config.config["debug_mode"] = True
    
    config.akSaveConfig()


def ahmdMain():
    """AHMD main function with command line argument parsing."""
    args = ahmdParseArguments()
    
    config = AKConfigManager(args.config)
    akApplyCommandOverrides(config, args)
    
    controller = AHMDGestureController(config)
    controller.ahmdRunMainLoop()


if __name__ == "__main__":
    ahmdMain()