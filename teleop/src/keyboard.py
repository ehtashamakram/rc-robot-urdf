#!/usr/bin/env python
import sys, select, tty, termios
import rospy
from std_msgs.msg import String
if __name__ == '__main__':
    key_pub = rospy.Publisher('keys', String, queue_size=1)
    rospy.init_node("keyboard_driver")
    rate = rospy.Rate(100)
    old_attr = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())


    msg = """
Control Your rc_truck!
---------------------------
Moving around:
        w    e
   a    s    d
        x    c

w/x : increase/decrease linear velocity
a/d : increase/decrease angular velocity
e/c : dumper up/down
s : force stop

CTRL-C to quit
"""

    print msg
    while not rospy.is_shutdown():
        if select.select([sys.stdin], [], [], 0)[0] == [sys.stdin]:
            key_pub.publish(sys.stdin.read(1))
        rate.sleep()
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attr)
