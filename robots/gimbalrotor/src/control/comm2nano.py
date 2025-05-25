#!/usr/bin/env python3
import rospy
from std_msgs.msg import Bool, Int16

class ArduinoInterface:
    def __init__(self):
        rospy.init_node('arduino_interface_node', anonymous=True)

        # Publisher to Arduino
        self.pub = rospy.Publisher('/gripper_command', Bool, queue_size=10)

        # Subscriber from Arduino
        rospy.Subscriber('/gripper_status', Bool, self.sensor_ard_callback)
        rospy.Subscriber('/quadrotor/gripper', Bool, self.sensor_cmd_callback)

        self.rate = rospy.Rate(1)  # 1 Hz
        self.gripper_status = False
        self.op_cmd = False
        self.close_cmd = False

    def sensor_ard_callback(self, msg):
        if msg.data:
            # rospy.loginfo("Gripper is ON")
            self.gripper_status = True
        else:
            # rospy.loginfo("Gripper is OFF")
            self.gripper_status = False
            
    def sensor_cmd_callback(self, msg):
        if msg.data:
            rospy.loginfo("Gripper command received: ON")
            self.op_cmd = True
            self.close_cmd = False
        else:
            rospy.loginfo("Gripper command received: OFF")
            self.op_cmd = False
            self.close_cmd = True
            

    def run(self):
        while not rospy.is_shutdown():
            if not self.gripper_status and self.op_cmd:
                # Send command to Arduino to turn ON the gripper
                rospy.loginfo("Sending command to Arduino: Gripper ON")
                self.pub.publish(Bool(data=True))
            elif self.gripper_status and self.close_cmd:
                # Send command to Arduino to turn OFF the gripper
                rospy.loginfo("Sending command to Arduino: Gripper OFF")
                self.pub.publish(Bool(data=False))
            else:
                #same as before
                rospy.loginfo(f'Gripper status unchanged ({self.gripper_status}), no command sent.')
            self.rate.sleep()

if __name__ == '__main__':
    try:
        interface = ArduinoInterface()
        interface.run()
    except rospy.ROSInterruptException:
        pass
