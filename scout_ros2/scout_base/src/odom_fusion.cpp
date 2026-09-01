#include "rclcpp/rclcpp.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "tf2/LinearMath/Quaternion.h"
#include "tf2_geometry_msgs/tf2_geometry_msgs.h"
#include "message_filters/subscriber.h"
#include "message_filters/time_synchronizer.h"
#include "message_filters/sync_policies/approximate_time.h"

class OdometryFusion : public rclcpp::Node
{
public:
    OdometryFusion() : Node("odometry_fusion")
    {
        rclcpp::SensorDataQoS qos;
        rclcpp::SystemDefaultsQoS sys_qos;
        laser_odom_sub_.subscribe(this, "/laser/odom" ,qos.get_rmw_qos_profile());
        wheel_odom_sub_.subscribe(this, "/wheel/odom" ,qos.get_rmw_qos_profile());
        
        sync_ = std::make_shared<message_filters::Synchronizer<SyncPolicy>>(SyncPolicy(5), laser_odom_sub_, wheel_odom_sub_);
        sync_->registerCallback(std::bind(&OdometryFusion::odomCallback, this, std::placeholders::_1, std::placeholders::_2));
        
        fused_odom_pub_ = this->create_publisher<nav_msgs::msg::Odometry>("/odom", 10);
    }

private:
    using SyncPolicy = message_filters::sync_policies::ApproximateTime<nav_msgs::msg::Odometry, nav_msgs::msg::Odometry>;
    
    void odomCallback(const nav_msgs::msg::Odometry::ConstSharedPtr& laser_msg, const nav_msgs::msg::Odometry::ConstSharedPtr& wheel_msg)
    {
        nav_msgs::msg::Odometry fused_odom = *wheel_msg;
        
        double laser_yaw = extractYawFromOdom(laser_msg);
        tf2::Quaternion q;
        q.setRPY(0, 0, laser_yaw);
        fused_odom.pose.pose.orientation = tf2::toMsg(q);
        
        fused_odom.header.stamp = wheel_msg->header.stamp;
        
        fused_odom_pub_->publish(fused_odom);
    }

    double extractYawFromOdom(const nav_msgs::msg::Odometry::ConstSharedPtr& msg)
    {
        tf2::Quaternion q;
        tf2::fromMsg(msg->pose.pose.orientation, q);
        double roll, pitch, yaw;
        tf2::Matrix3x3(q).getRPY(roll, pitch, yaw);
        return yaw;
    }

    message_filters::Subscriber<nav_msgs::msg::Odometry> laser_odom_sub_;
    message_filters::Subscriber<nav_msgs::msg::Odometry> wheel_odom_sub_;
    std::shared_ptr<message_filters::Synchronizer<SyncPolicy>> sync_;
    
    rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr fused_odom_pub_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<OdometryFusion>());
    rclcpp::shutdown();
    return 0;
}
