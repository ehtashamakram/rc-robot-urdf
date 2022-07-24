#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from ackermann_msgs.msg import AckermannDrive
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
key_mapping = { 'w': [ 0, 1, 0, 0], 'x': [0, -1, 0, 0], 'a': [1, 1, 1, 0], 'd': [-1, 1, -1, 0], 's': [ 0, 0, 0, 0] }
dumper_key = {'e':[-0.5], 'c':[0.0] }
g_last_twist = None
dumper_twist = None
g_vel_scales = [0.5, 0.3] # default to very slow
dumper_ctrl = [1]

def keys_cb(msg, twist_pub):
    global g_last_twist, g_vel_scales, dumper_twist, dumper_ctrl
    g_last_twist = AckermannDrive()
    dumper_twist = JointTrajectory()
    point = JointTrajectoryPoint()
    if key_mapping.has_key(msg.data[0]):
	    vels = key_mapping[msg.data[0]]
	    g_last_twist.steering_angle_velocity = vels[0] * g_vel_scales[0]
	    g_last_twist.speed = vels[1] * g_vel_scales[1]
	    g_last_twist.steering_angle = vels[2]
            twist_pub.publish(g_last_twist)

    if dumper_key.has_key(msg.data[0]):
	    vels = dumper_key[msg.data[0]]
	    dumper_twist.header.stamp = rospy.Time.now()
	    dumper_twist.joint_names = ['dumper_joint']
	    point.positions = [vels[0] * dumper_ctrl[0]]
	    point.time_from_start = rospy.Duration(1)
	    dumper_twist.points.append(point)
            dumper_pub.publish(dumper_twist)

def start():
    # publishing to "turtle1/cmd_vel" to control turtle1
    global twist_pub, dumper_pub, g_last_twist
    twist_pub = rospy.Publisher('/ackermann_cmd', AckermannDrive, queue_size=1)
    dumper_pub = rospy.Publisher('/dumper_controller/command', JointTrajectory, queue_size=10)
    # subscribed to joystick inputs on topic "joy"
    rospy.Subscriber('keys', String, keys_cb, twist_pub)
    # starts the node
    rospy.init_node('keys_to_twist')
    rospy.spin()
if __name__ == '__main__':
    start()
