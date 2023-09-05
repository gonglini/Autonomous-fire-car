#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import serial
from detect_demo import detect_fire
import cv2

def result():
    while True:
        robot, x,y = detect_fire()
        if x>0:
            return  robot,x,y     
        else:
            break


def ArmControl(robot,x, y):

    z = 120-(x / 6)
    y = 120-(y / 4)
    g = 1
 

    # 아두이노 포트 개방 & 연결
  #  ser = serial.Serial(port = '/dev/ttyUSB0', baudrate = 9600, timeout = 0.1)
    # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

    if os.name == 'nt':
        import msvcrt
    
        def getch():
            return msvcrt.getch().decode()
    else:
        import sys, tty, termios
    
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
    
        def getch():
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin    # 랜덤 함수
 #   x = random.randint(0, 999)                   # Random of X data 
  #  y = random.randint(0, 999)                   # Random of Y data
   # print(x,y)
    # 좌표 위치 이동을 위한 다이나믹셀 각도 캘리브레이션.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch
        
#----------------------------------------------------------------------------------------------------------------------------------------------
              
    from dynamixel_sdk.port_handler import PortHandler
    from dynamixel_sdk.packet_handler import PacketHandler
    from dynamixel_sdk.robotis_def import COMM_SUCCESS
    # 다이나믹셀 제어 주소
    # Control table address
    ADDR_MX_TORQUE_ENABLE      = 24                # Control table address is different in Dynamixel model
    ADDR_MX_GOAL_POSITION      = 30
    ADDR_MX_PRESENT_POSITION   = 36

    # 다이나믹셀 프로토콜 버젼
    # Protocol version
    PROTOCOL_VERSION            = 1.0              # See which protocol version is used in the Dynamixel

    # Default setting

    #다이나믹셀 통신 속도, 포트 
    BAUDRATE                    = 1000000                
    DEVICENAME                  =  '/dev/ttyUSB0' # 'COM31'
    # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"


    # 다이나믹셀 토크 활성화 / 비활성화
    TORQUE_ENABLE               = 1                 
    TORQUE_DISABLE              = 0


#----------------------------------------------------------------------------------------------------------------------------------------------
    # 다이나믹셀 위치 범위 지정값
    DXL_MINIMUM_POSITION_VALUE  = 1                                        #Set Min & Max Dynamixel Position Value
    DXL_MAXIMUM_POSITION_VALUE  = 1023
#----------------------------------------------------------------------------------------------------------------------------------------------
    
    DXL_MOVING_STATUS_THRESHOLD = 20               

    index = 0

    # 다이나믹셀 위치
    dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE]         # Goal position

    # 다이나믹셀 주소 지정
    portHandler = PortHandler(DEVICENAME)
    packetHandler = PacketHandler(PROTOCOL_VERSION)

    # 다이나믹셀 모듈 포트 활성화
    if portHandler.openPort():
        print("포트 연결에 성공하였습니다.")
    else:
        print("포트 연결에 실패하였습니다.")
        print("아무 키 눌러 종료하십시오...")
        getch()
        quit()

#----------------------------------------------------------------------------------------------------------------------------------------------
        
    # 다이나믹셀 통신속도 설정
    if portHandler.setBaudRate(BAUDRATE):
        print("통신속도 변경 완료.")
    else:
        print("통신속도 변경 실패")
        print("아무 키 눌러 종료하십시오...")
        getch()
        quit()
#----------------------------------------------------------------------------------------------------------------------------------------------
        
    # 다이나믹셀 토크 활성화
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 2, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 3, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)

    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("다이나믹셀을 성공적으로 연결하였습니다.")


    # 랜덤좌표값 출력
    print(f"({x}, {y})")
   
#----------------------------------------------------------------------------------------------------------------------------------------------
    

    #좌표 위치로 Yaw축 회전 (Z축) 
    # Z Axis        
    if (z > 99):
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 1, ADDR_MX_GOAL_POSITION, 512 + int(z))

    elif (z < 99):
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 1, ADDR_MX_GOAL_POSITION, 512 - int(z))

    time.sleep(0.6)
    
    #다이나믹셀 물 분사하기 위한 팔위치 준비자세

    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 4, ADDR_MX_GOAL_POSITION, 1012)
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 5, ADDR_MX_GOAL_POSITION, 12)
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 2, ADDR_MX_GOAL_POSITION, 912)
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 3, ADDR_MX_GOAL_POSITION, 112)
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 6, ADDR_MX_GOAL_POSITION, 512 + int(y) * int(1))

    #물분사(5초)
    print('\n Extinguisher executed.\n')
    time.sleep(3)
     # 요축 좌우 회전 3번 반복
    for i in range(0, 9):
        #좌
        for j in range (0, 40):
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 1, ADDR_MX_GOAL_POSITION, 512 + int(g) * int(2) - (j*2))


        time.sleep(0.5)
        #우
        for j in range (0, 40):
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 1, ADDR_MX_GOAL_POSITION, 432 + int(g) * int(2) + (j*2))

        time.sleep(1)
    
    print('done')
    time.sleep(2)

    #본 위치, 각도로 원위치
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 1, ADDR_MX_GOAL_POSITION, 185)
    #Y Axis
    for i in range (2, 7):
        if i == 4 or i == 5:
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, i, ADDR_MX_GOAL_POSITION, 512 + int(g) * int(2))
            g = g * -1
        
        else:
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, i, ADDR_MX_GOAL_POSITION, 512 + int(g) * int(1))
            g = g * -1

    time.sleep(1)

#----------------------------------------------------------------------------------------------------------------------------------------------
    
    # 포트 연결 해제
    portHandler.closePort()

if __name__ == '__main__':

    
    ans = input('실행할까요?')
    if ans == 'y':
        x = 0
        y = 0
        x, y = result()
        cv2.destroyAllWindows()
        ArmControl(x,y )
    else:
        print('프로그램을 종료합니다')
