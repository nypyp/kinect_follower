# ! /usr/bin/env pyhton
"""
    订阅depth_yolo发布的目标tf广播信息，查找并转换时间最近的TF信息
    获取目标的x,y,z信息，根据目标坐标信息计算线速度和角速度并发布

    实现流程：
        1. 导包
        2. 初始化ros节点
        3. 创建TF订阅对象
        4. 处理订阅的TF
"""
import rospy
import tf2_ros
from geometry_msgs.msg import TransformStamped, Twist
import math

if __name__== "__main__":
    #2 初始化ros节点
    rospy.init_node("kinect_follower")
    #3 创建TF订阅对象
    buffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(buffer)
    #4 处理订阅到的TF
    rate = rospy.Rate(10)
    #创建速度发布对象
    pub = rospy.Publisher("/cmd_vel",Twist,queue_size=1000)
    while not rospy.is_shutdown():
        rate.sleep()
        try:
            trans = buffer.lookup_transform("/camera_depth_optical_frame","people1",rospy.Time(0))
            rospy.loginfo("相对坐标：(%.2f,%.2f,%.2f)",
                          trans.transform.translation.x,
                          trans.transform.translation.y,
                          trans.transform.translation.z
                          )
            twist = Twist()
            twist.linear.x = 0.5 * math.sqrt(math.pow(trans.transform.translation.x,2) + math.pow(trans.transform.translation.y,2))
            twist.angular.z = 4 * math.atan2(trans.transform.translation.y, trans.transform.translation.x)
            pub.publish(twist)
        except Exception as e:
            rospy.logwarn("WORN: %s",e)
