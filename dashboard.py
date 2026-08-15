import sys
import time

from PyQt5.QtCore import QThread, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ros_worker import ROSWorker
from csv_logger import CSVLogger


class Dashboard(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Robotics Data Interface"
        )

        self.setMinimumSize(
            900,
            750
        )

        # -----------------------------
        # Telemetry data
        # -----------------------------

        self.time_data = []
        self.battery_data = []
        self.velocity_data = []

        self.start_time = time.time()

        # -----------------------------
        # CSV Logger
        # -----------------------------

        self.csv_logger = CSVLogger(
            "telemetry.csv"
        )

        # -----------------------------
        # Create GUI
        # -----------------------------

        self.create_ui()

        # -----------------------------
        # ROS worker
        # -----------------------------

        self.ros_thread = QThread()

        self.ros_worker = ROSWorker()

        self.ros_worker.moveToThread(
            self.ros_thread
        )

        self.ros_thread.started.connect(
            self.ros_worker.setup_ros
        )

        self.ros_thread.started.connect(
            self.ros_worker.spin
        )

        self.ros_worker.telemetry_received.connect(
            self.update_telemetry
        )

        self.ros_worker.connection_changed.connect(
            self.update_connection
        )

        self.start_button.clicked.connect(
            self.start_robot
        )

        self.stop_button.clicked.connect(
            self.stop_robot
        )

        self.ros_thread.start()

        # -----------------------------
        # Graph refresh timer
        # -----------------------------

        self.graph_timer = QTimer()

        self.graph_timer.timeout.connect(
            self.update_graphs
        )

        self.graph_timer.start(200)

    # =================================
    # GUI
    # =================================

    def create_ui(self):
        import pyqtgraph as pg

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        main_layout = QVBoxLayout()

        central_widget.setLayout(
            main_layout
        )

        # -----------------------------
        # Title
        # -----------------------------

        title = QLabel(
            "ROBOTICS DATA INTERFACE"
        )

        title.setStyleSheet(
            """
            font-size: 26px;
            font-weight: bold;
            """
        )

        main_layout.addWidget(title)

        # -----------------------------
        # Connection
        # -----------------------------

        self.connection_label = QLabel(
            "Connection: CONNECTING..."
        )

        self.connection_label.setStyleSheet(
            "font-size: 16px;"
        )

        main_layout.addWidget(
            self.connection_label
        )

        # -----------------------------
        # Robot status
        # -----------------------------

        self.robot_status_label = QLabel(
            "Robot Status: STOPPED"
        )

        self.robot_status_label.setStyleSheet(
            """
            font-size: 18px;
            font-weight: bold;
            """
        )

        main_layout.addWidget(
            self.robot_status_label
        )

        # -----------------------------
        # Telemetry cards
        # -----------------------------

        telemetry_layout = QHBoxLayout()

        # Battery
        battery_layout = QVBoxLayout()

        battery_title = QLabel(
            "BATTERY"
        )

        battery_title.setStyleSheet(
            """
            font-size: 14px;
            font-weight: bold;
            """
        )

        self.battery_label = QLabel(
            "0.00 %"
        )

        self.battery_label.setStyleSheet(
            "font-size: 28px;"
        )

        battery_layout.addWidget(
            battery_title
        )

        battery_layout.addWidget(
            self.battery_label
        )

        # Velocity
        velocity_layout = QVBoxLayout()

        velocity_title = QLabel(
            "VELOCITY"
        )

        velocity_title.setStyleSheet(
            """
            font-size: 14px;
            font-weight: bold;
            """
        )

        self.velocity_label = QLabel(
            "0.00 m/s"
        )

        self.velocity_label.setStyleSheet(
            "font-size: 28px;"
        )

        velocity_layout.addWidget(
            velocity_title
        )

        velocity_layout.addWidget(
            self.velocity_label
        )

        telemetry_layout.addLayout(
            battery_layout
        )

        telemetry_layout.addLayout(
            velocity_layout
        )

        main_layout.addLayout(
            telemetry_layout
        )

        # -----------------------------
        # Buttons
        # -----------------------------

        button_layout = QHBoxLayout()

        self.start_button = QPushButton(
            "START"
        )

        self.stop_button = QPushButton(
            "STOP"
        )

        self.start_button.setMinimumHeight(50)
        self.stop_button.setMinimumHeight(50)

        self.start_button.setStyleSheet(
            """
            QPushButton {
                font-size: 18px;
                font-weight: bold;
            }
            """
        )

        self.stop_button.setStyleSheet(
            """
            QPushButton {
                font-size: 18px;
                font-weight: bold;
            }
            """
        )

        button_layout.addWidget(
            self.start_button
        )

        button_layout.addWidget(
            self.stop_button
        )

        main_layout.addLayout(
            button_layout
        )

        # -----------------------------
        # Velocity graph
        # -----------------------------

        velocity_title = QLabel(
            "LIVE VELOCITY"
        )

        velocity_title.setStyleSheet(
            """
            font-size: 16px;
            font-weight: bold;
            """
        )

        main_layout.addWidget(
            velocity_title
        )

        self.velocity_plot = pg.PlotWidget()

        self.velocity_plot.setLabel(
            "left",
            "Velocity",
            units="m/s"
        )

        self.velocity_plot.setLabel(
            "bottom",
            "Time",
            units="s"
        )

        self.velocity_plot.showGrid(
            x=True,
            y=True
        )

        self.velocity_curve = (
            self.velocity_plot.plot()
        )

        main_layout.addWidget(
            self.velocity_plot
        )

        # -----------------------------
        # Battery graph
        # -----------------------------

        battery_graph_title = QLabel(
            "LIVE BATTERY"
        )

        battery_graph_title.setStyleSheet(
            """
            font-size: 16px;
            font-weight: bold;
            """
        )

        main_layout.addWidget(
            battery_graph_title
        )

        self.battery_plot = pg.PlotWidget()

        self.battery_plot.setLabel(
            "left",
            "Battery",
            units="%"
        )

        self.battery_plot.setLabel(
            "bottom",
            "Time",
            units="s"
        )

        self.battery_plot.showGrid(
            x=True,
            y=True
        )

        self.battery_curve = (
            self.battery_plot.plot()
        )

        main_layout.addWidget(
            self.battery_plot
        )

        # -----------------------------
        # Telemetry status
        # -----------------------------

        self.telemetry_label = QLabel(
            "Waiting for telemetry..."
        )

        main_layout.addWidget(
            self.telemetry_label
        )

    # =================================
    # START
    # =================================

    def start_robot(self):

        self.ros_worker.send_start()

        self.robot_status_label.setText(
            "Robot Status: START COMMAND SENT"
        )

    # =================================
    # STOP
    # =================================

    def stop_robot(self):

        self.ros_worker.send_stop()

        self.robot_status_label.setText(
            "Robot Status: STOP COMMAND SENT"
        )

    # =================================
    # Telemetry
    # =================================

    def update_telemetry(
        self,
        battery,
        velocity,
        running
    ):

        current_time = (
            time.time() - self.start_time
        )

        # Store graph data
        self.time_data.append(
            current_time
        )

        self.battery_data.append(
            battery
        )

        self.velocity_data.append(
            velocity
        )

        # -----------------------------
        # CSV logging
        # -----------------------------

        self.csv_logger.log_telemetry(
            battery,
            velocity,
            running
        )

        # Keep latest 100 samples
        max_points = 100

        if len(self.time_data) > max_points:

            self.time_data = (
                self.time_data[-max_points:]
            )

            self.battery_data = (
                self.battery_data[-max_points:]
            )

            self.velocity_data = (
                self.velocity_data[-max_points:]
            )

        # Update labels
        self.battery_label.setText(
            f"{battery:.2f} %"
        )

        self.velocity_label.setText(
            f"{velocity:.2f} m/s"
        )

        # Robot state
        if running:

            self.robot_status_label.setText(
                "Robot Status: RUNNING"
            )

        else:

            self.robot_status_label.setText(
                "Robot Status: STOPPED"
            )

        self.telemetry_label.setText(
            "Live telemetry received • Logging active"
        )

    # =================================
    # Graphs
    # =================================

    def update_graphs(self):

        if not self.time_data:
            return

        self.velocity_curve.setData(
            self.time_data,
            self.velocity_data
        )

        self.battery_curve.setData(
            self.time_data,
            self.battery_data
        )

    # =================================
    # Connection
    # =================================

    def update_connection(
        self,
        connected
    ):

        if connected:

            self.connection_label.setText(
                "Connection: CONNECTED"
            )

        else:

            self.connection_label.setText(
                "Connection: DISCONNECTED"
            )

    # =================================
    # Close
    # =================================

    def closeEvent(self, event):

        self.graph_timer.stop()

        try:

            self.ros_worker.shutdown()

            self.ros_thread.quit()

            self.ros_thread.wait(3000)

        except Exception:
            pass

        event.accept()


def main():

    app = QApplication(sys.argv)

    window = Dashboard()

    window.show()

    sys.exit(
        app.exec_()
    )


if __name__ == "__main__":
    main()
