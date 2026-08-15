import rclpy

from PyQt5.QtCore import QObject, pyqtSignal

from std_msgs.msg import String
from std_msgs.msg import Empty


class ROSWorker(QObject):

    telemetry_received = pyqtSignal(float, float, bool)
    connection_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.node = None
        self.start_publisher = None
        self.stop_publisher = None

    def setup_ros(self):

        # Initialize ROS2
        rclpy.init()

        # Create ROS2 node
        self.node = rclpy.create_node(
            'dashboard_interface'
        )

        # START publisher
        self.start_publisher = self.node.create_publisher(
            Empty,
            '/cmd_start',
            10
        )

        # STOP publisher
        self.stop_publisher = self.node.create_publisher(
            Empty,
            '/cmd_stop',
            10
        )

        # Telemetry subscriber
        self.node.create_subscription(
            String,
            '/telemetry',
            self.telemetry_callback,
            10
        )

        self.connection_changed.emit(True)

        self.node.get_logger().info(
            'ROS Worker connected'
        )

    def telemetry_callback(self, msg):

        try:

            # Expected:
            # battery=96.50,velocity=1.25,running=True

            data = msg.data.split(',')

            battery = float(
                data[0].split('=')[1]
            )

            velocity = float(
                data[1].split('=')[1]
            )

            running = (
                data[2].split('=')[1].lower()
                == 'true'
            )

            self.telemetry_received.emit(
                battery,
                velocity,
                running
            )

        except Exception as error:

            self.node.get_logger().error(
                f'Failed to parse telemetry: {error}'
            )

    def send_start(self):

        if self.start_publisher is None:
            return

        msg = Empty()

        self.start_publisher.publish(msg)

        self.node.get_logger().info(
            'START command published'
        )

    def send_stop(self):

        if self.stop_publisher is None:
            return

        msg = Empty()

        self.stop_publisher.publish(msg)

        self.node.get_logger().info(
            'STOP command published'
        )

    def spin(self):

        if self.node is None:
            return

        try:

            rclpy.spin(self.node)

        except Exception as error:

            if self.node is not None:
                self.node.get_logger().error(
                    f'ROS spin error: {error}'
                )

    def shutdown(self):

        if self.node is not None:

            self.node.destroy_node()
            self.node = None

        if rclpy.ok():
            rclpy.shutdown()
