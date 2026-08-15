import math
import rclpy

from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Empty


class MockRobot(Node):

    def __init__(self):
        super().__init__('mock_robot')

        # -----------------------------
        # Telemetry publisher
        # -----------------------------
        self.telemetry_publisher = self.create_publisher(
            String,
            '/telemetry',
            10
        )

        # -----------------------------
        # START command subscriber
        # -----------------------------
        self.start_subscriber = self.create_subscription(
            Empty,
            '/cmd_start',
            self.start_callback,
            10
        )

        # -----------------------------
        # STOP command subscriber
        # -----------------------------
        self.stop_subscriber = self.create_subscription(
            Empty,
            '/cmd_stop',
            self.stop_callback,
            10
        )

        # Publish telemetry every 0.5 seconds
        self.timer = self.create_timer(
            0.5,
            self.publish_telemetry
        )

        # -----------------------------
        # Simulated robot state
        # -----------------------------
        self.battery = 100.0
        self.velocity = 0.0
        self.running = False
        self.time_step = 0

        self.get_logger().info('Mock Robot started')
        self.get_logger().info('Robot state: STOPPED')

    # =================================
    # START command
    # =================================
    def start_callback(self, msg):

        if not self.running:

            self.running = True

            self.get_logger().info(
                'START command received - Robot RUNNING'
            )

    # =================================
    # STOP command
    # =================================
    def stop_callback(self, msg):

        if self.running:

            self.running = False
            self.velocity = 0.0

            self.get_logger().info(
                'STOP command received - Robot STOPPED'
            )

    # =================================
    # Telemetry
    # =================================
    def publish_telemetry(self):

        if self.running:

            # Smooth simulated velocity
            self.velocity = (
                1.25
                + 0.75 * math.sin(
                    self.time_step * 0.15
                )
            )

            # Slowly drain battery
            self.battery -= 0.02

            if self.battery < 0:
                self.battery = 0.0

            self.time_step += 1

        else:

            self.velocity = 0.0

        # Create telemetry message
        msg = String()

        msg.data = (
            f'battery={self.battery:.2f},'
            f'velocity={self.velocity:.2f},'
            f'running={self.running}'
        )

        self.telemetry_publisher.publish(msg)

        self.get_logger().info(
            f'Telemetry: {msg.data}'
        )


def main(args=None):

    rclpy.init(args=args)

    node = MockRobot()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
