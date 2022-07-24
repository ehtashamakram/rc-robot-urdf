#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from ackermann_msgs.msg import AckermannDrive
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import Joy

# This ROS Node converts Joystick inputs from the joy node
# into commands for turtlesim or any other robot

# Receives joystick messages (subscribed to Joy topic)
# then converts the joysick inputs into Twist commands
# axis 1 aka left stick vertical controls linear speed
# axis 0 aka left stick horizonal controls angular speed

def callback(data):
    global g_last_twist, g_vel_scales, dumper_twist
    g_last_twist = AckermannDrive()
    dumper_twist = JointTrajectory()
    point = JointTrajectoryPoint()
    if data.axes[3]:
        g_last_twist.speed =  0.3
        twist_pub.publish(g_last_twist)

    if data.axes[1]:
        g_last_twist.speed = -0.3
        twist_pub.publish(g_last_twist)
    
    if data.axes[2]:
        g_last_twist.steering_angle_velocity = 0.5
        g_last_twist.steering_angle = 1
        twist_pub.publish(g_last_twist)

    if data.axes[0]:
        g_last_twist.steering_angle_velocity = 0.5 * -1
        g_last_twist.steering_angle = 1
        twist_pub.publish(g_last_twist)

    if data.axes[4]:
        dumper_twist.header.stamp = rospy.Time.now()
        dumper_twist.joint_names = ['dumper_joint']
        point.positions = [-0.5]
        point.time_from_start = rospy.Duration(1)
        dumper_twist.points.append(point)
        dumper_pub.publish(dumper_twist)

    if data.axes[5]:
        dumper_twist.header.stamp = rospy.Time.now()
        dumper_twist.joint_names = ['dumper_joint']
        point.positions = [0]
        point.time_from_start = rospy.Duration(1)
        dumper_twist.points.append(point)
        dumper_pub.publish(dumper_twist)

# Intializes everything
def start():
    # publishing to "turtle1/cmd_vel" to control turtle1
    global twist_pub, dumper_pub, g_last_twist
    twist_pub = rospy.Publisher('/ackermann_cmd', AckermannDrive, queue_size=1)
    dumper_pub = rospy.Publisher('/dumper_controller/command', JointTrajectory, queue_size=10)
    # subscribed to joystick inputs on topic "joy"
    rospy.Subscriber("joy", Joy, callback)
    # starts the node
    rospy.init_node('joystick_to_twist')
    rospy.spin()
if __name__ == '__main__':
    start()




