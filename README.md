# Robotics Data and Interface

A lightweight robotics dashboard built with **Python, PyQt5, and ROS 2**.

## Features

- Start / Stop simulated robot
- Live battery and velocity telemetry
- Robot status display
- Live telemetry graphs
- CSV telemetry logging
- ROS 2 communication in a background QThread

## Architecture

Mock ROS 2 Node → ROS Worker (QThread) → PyQt5 GUI → CSV Logger

The ROS 2 worker runs separately from the GUI so `rclpy.spin()` does not block the interface.

## ROS 2 Topics

- `/telemetry` — `std_msgs/msg/String` — Battery, velocity and robot status
- `/cmd_start` — `std_msgs/msg/Empty` — Start the simulated robot
- `/cmd_stop` — `std_msgs/msg/Empty` — Stop the simulated robot

Telemetry format:
`battery=98.50,velocity=1.25,running=True`

## Project Structure

- `dashboard.py` — PyQt5 dashboard
- `mock_ros2_node.py` — Simulated ROS 2 robot
- `ros_worker.py` — ROS 2 background worker
- `csv_logger.py` — Telemetry CSV logger
- `requirements.txt` — Project dependencies
- `README.md` — Project documentation
- `.gitignore` — Git ignore rules

## Requirements

- Ubuntu / WSL2
- ROS 2 Lyrical
- Python 3
- PyQt5
- pyqtgraph

## Installation

    source /opt/ros/lyrical/setup.bash
    sudo apt update
    sudo apt install python3-pyqt5 python3-pyqtgraph

## Run

Terminal 1:

    cd ~/robotics_data_interface
    source /opt/ros/lyrical/setup.bash
    python3 mock_ros2_node.py

Terminal 2:

    cd ~/robotics_data_interface
    source /opt/ros/lyrical/setup.bash
    python3 dashboard.py

## CSV Logging

Telemetry is automatically saved to `telemetry.csv` with:

`timestamp,battery,velocity,running`

## Validation

    python3 -m py_compile dashboard.py ros_worker.py mock_ros2_node.py csv_logger.py

Tested for ROS 2 communication, START / STOP control, telemetry updates, live graphs, battery drain and CSV logging.

## Author

**Ramita Gawade**  
Robotics & Automation Engineering

Built for the **Pace Robotics Technical Assessment**.
