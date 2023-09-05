e# Automatic Detect & Extinguish Fire Services (Self-driving fire truck)

This project is created for the 21st 2023 embedded SW contest by undergraduates attending Suwon, Kyungil Univ. 


## Overview

<img src = https://github.com/gonglini/Embedded_sw_contest_2023/assets/65767592/36d6ebdd-c0c3-4b90-a59a-4096cc5b802d.jpeg width="440" height="350" align="right">   
This project aims to ensure fire safety inside buildings, particularly during unoccupied hours like midnight. 
Even in the event of a fire, this autonomous system can detect and extinguish flames automatically while simultaneously alerting the user through a dedicated application.
This code implements motion control of a 1:8 scale car, including moving by joystick or automatically. Supporting libraries provide additional capabilities, such as object detection by the camera to provide accidents.
The software is built on a Jetson Nano platform running Ubuntu 18.04, with the ROS Melodic framework serving as the foundation.
Combining Arduino, C++, and Python nodes, this ROS-based software orchestrates the seamless interaction of various components, ensuring a comprehensive and reliable fire prevention and response system.


## Software settings
```
* Jetpack 4.5.1 / Darknet yoloV4 / ROS Melodic / Dinamixel SDK
* OpenCV 4.5.1 / CUDA 10.0 / CUDNN 8.0 / Tensorflow 2.5.0
```
## Key software configuration

<p align="center"> <img src =https://github.com/gonglini/2023ESWContest_free_1035/assets/65767592/be930881-b53f-496e-818e-85e0f2450f11.jpg  width="930" height="370" ></p>



## Self Driving (Slam navigation)

Self-driving is for patrol where being fired. We used Python to send the goal for ROS SLAM. Cartographer is also used to obtain maps.
We used Rplidar A1 to obtain maps with a laser scan. The car moves to goals serval times where we setup before. There is location information that contains x, y, and z(orientation)

Here's the map and the navigation we got.

  <img src = https://user-images.githubusercontent.com/65767592/235427299-fb32638c-17a3-4ed7-bec6-ed2805b5473b.gif  width="430" height="350"  align="left">
  <img src = https://user-images.githubusercontent.com/65767592/235427736-1006aaee-7dc9-47ca-af52-d081794774f0.jpg   width="370" height="350" align="right">
    
    
## Fire detection  

    
|  Darknet YoloV4  | IR sensor  |
|---|---|
|The project contains object detection by using the darknet yoloV4-tiny. We made customized weight files by machine learning.  We extracted the coordinate value of fire by extracting the coordinate of the bounding box drawn when detecting fire. We modified batch and subdivision for Jsons capability.   |  Fire detection of this project is for fire fighting purposes.  So we considered a way to accurately detect fire through two sensors and then find the coordinate value of the fire.  The fire detection system determines that the fire was truly detected when object detection by the camera  and fire wavelength detection by the flame sensor was performed at the same time.  A flame sensor detects a specific wavelength generated only by fire. (185nm~260nm) It can detect up to flame of in front 1.5m |


  <img src = https://github.com/gonglini/Embedded_sw_contest_2023/assets/65767592/2dbe1e03-f07f-4706-a245-5c3c485cfce0.png  width="380" height="300"  align="left">
  <img src = https://github.com/gonglini/Embedded_sw_contest_2023/assets/65767592/883f5a7d-ad22-4fd4-bbd6-7b733622e32b.gif   width="420" height="300" align="right">

## Fire extinguisher (Robot Arm)
   
The Robot arm processes the fire extinguishing system. When the fire is detected, they get a position where the fire was caused.  

After the extinguishing system gets fire information from the jetson, the robot arm will execute the included water pump.   
We used a Dinamixel actuator AX-12 with a U2D2 module.

 <p align="center"><img src = https://github.com/gonglini/Embedded_sw_contest_2023/assets/65767592/15f0531c-172c-4d51-a259-3555f71480d0.gif width="700" height="300"  ></p> 
    
## Application
  <img src = https://github.com/gonglini/Embedded_sw_contest_2023/assets/65767592/98005e97-6d1a-4589-a7d7-dc19c0718fd5.gif  width="310" height="310"  align="right">

One of the important things is we had to know where and when the fire occurred.  
So our team also made an application for users.   
When the fire occurred, An application announce fire to the user that the situation happened.   
After the robot extinguishes the fire, it announces where the fire occurred.
The application is connected by wifi with ESP8266 which communicates by Web using the GET method.    
It runs as a client While ESP8266 is a Server.    

Here are how the application is processed.    

## External Links and References

* Research used for ROS SLAM Navigation. : https://automaticaddison.com/how-to-set-up-the-ros-navigation-stack-on-a-robot      
                                          : https://github.com/omorobot/omo_r1mini    
                                          : https://github.com/bandasaikrishna/Autonomous_Mobile_Robot    

