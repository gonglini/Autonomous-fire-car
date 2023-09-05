#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import sys
import rospy
import serial
from geometry_msgs.msg import PoseWithCovarianceStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib import SimpleActionClient
from fire_detector import detect_fire
from Extinguisher import ArmControl

ser = serial.Serial('/dev/ttyUSB0', 9600)

def result():
    while not rospy.is_shutdown():
        robot, x, y = detect_fire()
        if x > 0:
            return x, y

def send_initial_pose(x, y, orientation):
    rospy.init_node('simple_navigation_goals')
    pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=10)
    rospy.sleep(1) 

    pose_msg = PoseWithCovarianceStamped()
    pose_msg.header.stamp = rospy.Time.now()
    pose_msg.header.frame_id = 'map'
    pose_msg.pose.pose.position.x = x
    pose_msg.pose.pose.position.y = y

    # Convert the orientation from radians to quaternion
    q = quaternion_from_euler(0, 0, orientation)
    pose_msg.pose.pose.orientation.x = q[0]
    pose_msg.pose.pose.orientation.y = q[1]
    pose_msg.pose.pose.orientation.z = q[2]
    pose_msg.pose.pose.orientation.w = q[3]

    pub.publish(pose_msg)
    rospy.loginfo("2D Pose Estimate sent!")
    
def main():

    x = -6.1601715087890625
    y = 3.573763370513916
    orientation = -0.009806134033345524

    send_initial_pose(x, y, orientation)

    # Create a SimpleActionClient for move_base
    client = SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    valid_locations = {
        'a': {
            'name': 'goal1',
            'position': [0.5363373756408691,  -4.246832847595215],
            'orientation': [0, 0,  -0.6316955093324425, 0.7752166042398899]
        },
        'b': {
            'name': 'goal2',
            'position': [1.2474347352981567, -7.877311706542969],
            'orientation': [0, 0, 0.18588413660526473, 0.9825716705454698]
        }
    }

    while not rospy.is_shutdown():
        print("\nRobot execute started")

        goal_key = 'a'  
        while True:
            goal = MoveBaseGoal()
            goal.target_pose.header.frame_id = 'map'
            goal.target_pose.header.stamp = rospy.Time.now()
            goal.target_pose.pose.position.x = valid_locations[goal_key]['position'][0]
            goal.target_pose.pose.position.y = valid_locations[goal_key]['position'][1]
            goal.target_pose.pose.orientation.x = valid_locations[goal_key]['orientation'][0]
            goal.target_pose.pose.orientation.y = valid_locations[goal_key]['orientation'][1]
            goal.target_pose.pose.orientation.z = valid_locations[goal_key]['orientation'][2]
            goal.target_pose.pose.orientation.w = valid_locations[goal_key]['orientation'][3]

            print("\nGoal Location: {}".format(valid_locations[goal_key]['name']))

            rospy.loginfo("Sending goal: {}".format(valid_locations[goal_key]['name']))
            client.send_goal(goal)

            while not rospy.is_shutdown():
                s_var = ser.readline()
                var = s_var.decode()[:len(s_var) - 2]

                a, b = result()

                if var == 'Fire_detected!':
                    cv2.destroyAllWindows()
                    client.cancel_goal()
                    print("Fire detected, Robot stopped.")
                    rospy.sleep(2)
                    ArmControl(a, b)
                    break

                if client.get_state() == 3:
                    rospy.loginfo("The robot has arrived at the goal location")

                    if goal_key == 'a':
                        goal_key = 'b' 
                    if goal_key == 'b':
                        goal_key ='a' 
                        

                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    line = sys.stdin.readline().strip()
                    if line.lower() == 'q':
                        print("프로그램을 종료합니다.")
                        sys.exit(0)
                rospy.sleep(0.1)
