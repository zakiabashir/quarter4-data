---
title: 1.2 Sensors and Perception
sidebar_position: 2
---

# 1.2 Sensors and Perception

## Overview

Perception is the foundation of Physical AI systems. Without accurate sensing of the environment, an AI system cannot make informed decisions or take appropriate actions. This section explores the various sensors and perception techniques used in Physical AI.

## 2.1 Types of Sensors

### 2.1.1 Vision Sensors

#### Cameras
- **RGB Cameras**: Capture color images
- **Depth Cameras**: Provide distance information (e.g., Kinect, RealSense)
- **Thermal Cameras**: Detect heat signatures
- **High-Speed Cameras**: Capture fast motion

```python
# Example: OpenCV camera capture and processing
import cv2
import numpy as np

class CameraSensor:
    def __init__(self, camera_id=0):
        self.camera = cv2.VideoCapture(camera_id)
        self.frame_width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def capture_frame(self):
        """Capture a single frame from the camera"""
        ret, frame = self.camera.read()
        if ret:
            return frame
        return None

    def detect_edges(self, frame):
        """Apply Canny edge detection"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        return edges
```

#### Event Cameras
- **Neuromorphic sensors**: Detect changes in brightness
- **Microsecond latency**: Extremely fast response
- **Low power consumption**: Efficient for always-on applications

### 2.1.2 Range Sensors

#### LiDAR (Light Detection and Ranging)
- **Principle**: Laser pulses measure distance
- **Applications**: 3D mapping, autonomous vehicles
- **Types**:
  - Mechanical spinning LiDAR
  - Solid-state LiDAR
  - Flash LiDAR

```python
# Example: LiDAR point cloud processing
import numpy as np
import open3d as o3d

class LidarProcessor:
    def __init__(self):
        self.point_cloud = o3d.geometry.PointCloud()

    def process_scan(self, raw_points):
        """Process raw LiDAR scan data"""
        # Convert to Open3D point cloud
        points = np.array(raw_points)
        self.point_cloud.points = o3d.utility.Vector3dVector(points)

        # Remove outliers
        cl, ind = self.point_cloud.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
        return self.point_cloud.select_by_index(ind)

    def segment_planes(self, point_cloud):
        """Segment planes from point cloud"""
        plane_model, inliers = point_cloud.segment_plane(
            distance_threshold=0.01,
            ransac_n=3,
            num_iterations=1000
        )
        return plane_model, inliers
```

#### Radar
- **Advantages**: Works in adverse weather
- **Frequency bands**: 24GHz, 77GHz, 122GHz
- **Applications**: Automotive safety, traffic monitoring

#### Sonar
- **Underwater applications**: Navigation, imaging
- **Medical applications**: Ultrasound imaging
- **Industrial applications**: Level sensing

### 2.1.3 Position and Orientation Sensors

#### IMU (Inertial Measurement Unit)
- **Components**: Accelerometer, gyroscope, magnetometer
- **Purpose**: Track orientation and motion
- **Challenges**: Drift, noise, calibration

```python
# Example: IMU data fusion
import numpy as np
from scipy.spatial.transform import Rotation

class IMUFusion:
    def __init__(self):
        self.accel = np.zeros(3)
        self.gyro = np.zeros(3)
        self.magnet = np.zeros(3)
        self.attitude = Rotation.from_euler('xyz', [0, 0, 0])

    def update(self, accel, gyro, magnet, dt):
        """Update attitude with sensor fusion"""
        # Normalize magnetometer
        magnet_norm = magnet / np.linalg.norm(magnet)

        # Complementary filter
        alpha = 0.98
        gyro_rotation = Rotation.from_euler('xyz', gyro * dt)
        self.attitude = self.attitude * gyro_rotation

        # Correct with accelerometer/magnetometer
        if np.linalg.norm(accel) > 0.1:
            accel_rotation = self.estimate_gravity_rotation(accel, magnet_norm)
            self.attitude = self.attitude * accel_rotation ** alpha
```

#### GPS (Global Positioning System)
- **Accuracy**: 1-5 meters (civilian)
- **Enhanced systems**: DGPS, RTK for centimeter accuracy
- **Limitations**: Indoor, urban canyons

### 2.1.4 Force and Tactile Sensors

#### Pressure Sensors
- **Applications**: Gripping force, weight measurement
- **Technologies**: Piezoelectric, capacitive, resistive

#### Tactile Arrays
- **Skin-like sensors**: Pressure distribution
- **Robotic hands**: Grasping, manipulation
- **Haptic feedback**: Virtual reality

```python
# Example: Tactile sensor array processing
import numpy as np

class TactileArray:
    def __init__(self, rows=8, cols=8):
        self.rows = rows
        self.cols = cols
        self.pressure_map = np.zeros((rows, cols))

    def read_sensors(self):
        """Simulate reading tactile array"""
        # Simulate pressure pattern
        center_x, center_y = self.rows // 2, self.cols // 2
        for i in range(self.rows):
            for j in range(self.cols):
                dist = np.sqrt((i - center_x)**2 + (j - center_y)**2)
                self.pressure_map[i, j] = max(0, 10 - dist) + np.random.normal(0, 0.5)
        return self.pressure_map

    def detect_contact_points(self, threshold=5.0):
        """Detect significant contact points"""
        contacts = np.where(self.pressure_map > threshold)
        return list(zip(contacts[0], contacts[1]))
```

## 2.2 Perception Algorithms

### 2.2.1 Computer Vision

#### Object Detection
- **Traditional methods**: Haar cascades, HOG features
- **Deep learning**: YOLO, R-CNN, SSD
- **Real-time considerations**: EdgeTPU, Jetson

```python
# Example: YOLO object detection
import cv2
import numpy as np

class YOLODetector:
    def __init__(self, config_path, weights_path, class_names):
        self.net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
        self.classes = class_names
        self.confidence_threshold = 0.5
        self.nms_threshold = 0.4

    def detect(self, frame):
        """Detect objects in frame using YOLO"""
        height, width = frame.shape[:2]

        # Create blob from frame
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)

        # Get output layers
        layer_names = self.net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        # Forward pass
        outputs = self.net.forward(output_layers)

        # Process detections
        boxes = []
        confidences = []
        class_ids = []

        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > self.confidence_threshold:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # Apply non-maximum suppression
        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence_threshold, self.nms_threshold)

        # Return detected objects
        detections = []
        if len(indices) > 0:
            for i in indices.flatten():
                x, y, w, h = boxes[i]
                confidence = confidences[i]
                class_id = class_ids[i]
                label = str(self.classes[class_id])
                detections.append({
                    'box': (x, y, x+w, y+h),
                    'confidence': confidence,
                    'label': label
                })

        return detections
```

#### Semantic Segmentation
- **Pixel-level classification**: Each pixel assigned to a class
- **Applications**: Scene understanding, autonomous driving
- **Architectures**: U-Net, DeepLab, Mask R-CNN

### 2.2.2 Sensor Fusion

#### Kalman Filtering
- **Purpose**: Combine noisy sensor measurements
- **Applications**: Tracking, navigation, state estimation
- **Variants**: Extended Kalman Filter, Unscented Kalman Filter

```python
# Example: Kalman filter for position tracking
import numpy as np

class KalmanFilter:
    def __init__(self, dim_x, dim_z):
        self.dim_x = dim_x
        self.dim_z = dim_z

        # State vector [x, y, vx, vy]
        self.x = np.zeros((dim_x, 1))

        # State transition matrix
        self.F = np.eye(dim_x)

        # Measurement matrix
        self.H = np.zeros((dim_z, dim_x))

        # Process noise covariance
        self.Q = np.eye(dim_x)

        # Measurement noise covariance
        self.R = np.eye(dim_z)

        # Error covariance
        self.P = np.eye(dim_x)

    def predict(self):
        """Predict next state"""
        self.x = np.dot(self.F, self.x)
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q
        return self.x

    def update(self, z):
        """Update with measurement"""
        # Innovation
        y = z - np.dot(self.H, self.x)

        # Innovation covariance
        S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R

        # Kalman gain
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))

        # State update
        self.x = self.x + np.dot(K, y)

        # Covariance update
        I_KH = np.eye(self.dim_x) - np.dot(K, self.H)
        self.P = np.dot(I_KH, self.P)

        return self.x
```

#### Particle Filtering
- **Non-linear systems**: Handles non-Gaussian distributions
- **Applications**: Localization, tracking
- **Advantages**: Flexibility, parallelization

### 2.2.3 SLAM (Simultaneous Localization and Mapping)

- **Problem**: Build map while tracking position
- **Types**:
  - Visual SLAM (vSLAM)
  - LiDAR SLAM
  - RGB-D SLAM
- **Algorithms**: EKF-SLAM, FastSLAM, ORB-SLAM

## 2.3 Challenges in Perception

### 2.3.1 Environmental Variability

- **Lighting changes**: Day/night, shadows
- **Weather conditions**: Rain, fog, snow
- **Dynamic environments**: Moving objects, changes

### 2.3.2 Sensor Limitations

- **Noise**: Random measurement errors
- **Resolution**: Limited detail capture
- **Field of view**: Restricted perception area
- **Calibration drift**: Sensor accuracy over time

### 2.3.3 Computational Constraints

- **Real-time requirements**: Processing speed
- **Power limitations**: Mobile applications
- **Memory constraints**: Large data streams

## 2.4 Best Practices

1. **Multi-sensor approaches**: Combine complementary sensors
2. **Redundancy**: Backup systems for critical functions
3. **Regular calibration**: Maintain sensor accuracy
4. **Adaptive algorithms**: Adjust to changing conditions
5. **Error handling**: Graceful degradation

## Key Takeaways

1. Perception is the sensory foundation of Physical AI
2. Multiple sensor types provide complementary information
3. Sensor fusion algorithms combine noisy measurements
4. Real-world perception requires handling uncertainty
5. Computational efficiency is crucial for real-time applications

## Practice Exercises

1. Design a sensor suite for an autonomous delivery drone
2. Implement a simple object detection system using OpenCV
3. Compare the advantages and disadvantages of LiDAR vs radar for autonomous vehicles