# Robotics Data and Interface

A lightweight desktop robotics dashboard built using **Python, PyQt5, and ROS 2**.

The application connects a PyQt5 desktop interface to a simulated ROS 2 robot, allowing the user to:

- Start and stop the simulated robot
- Monitor live battery and velocity telemetry
- View telemetry values in real time
- Visualize telemetry using live plots
- Log timestamped telemetry data to a CSV file
- Keep ROS 2 communication running in a background thread without blocking the GUI

## System Architecture

The implementation follows the architecture specified in the assessment.

                 MOCK ROS 2 NODE
                       |
              /telemetry topic
                       |
                       v
              +------------------+
              |    ROS WORKER    |
              |   QThread        |
              |   rclpy.spin()   |
              +--------+---------+
                       |
                  Qt Signals
                       |
                       v
              +------------------+
              |   PYQT5 GUI      |
              |                  |
              |  START / STOP    |
              |  Connection      |
              |  Battery         |
              |  Velocity        |
              |  Live Graphs     |
              +--------+---------+
                       |
                       v
                CSV LOGGER
                       |
                       v
                telemetry.csv
ROS 2 Interfaces
Topic   	Message Type    	Direction	Purpose
/telemetry	std_msgs/msg/String	Robot → GUI	Publishes battery, velocity and running state
/cmd_start	std_msgs/msg/Empty	GUI → Robot	Starts the simulated robot
/cmd_stop	std_msgs/msg/Empty	GUI → Robot	Stops the simulated robot

Telemetry is published in the following format:

battery=98.50,velocity=1.25,running=True

The ROS worker parses the telemetry message and sends the values to the PyQt5 interface using Qt signals.

Project Structure
robotics_data_interface/
├── dashboard.py
├── mock_ros2_node.py
├── ros_worker.py
├── csv_logger.py
├── requirements.txt
├── README.md
└── .gitignore
File Description
mock_ros2_node.py

Simulates the robot.

Publishes battery and velocity telemetry
Publishes the robot running state
Listens for /cmd_start
Listens for /cmd_stop
Simulates battery drain while running
Simulates changing velocity
ros_worker.py

Provides the ROS 2 interface for the PyQt application.

Runs ROS 2 communication in a background QThread
Uses rclpy.spin()
Subscribes to /telemetry
Publishes /cmd_start
Publishes /cmd_stop
Sends telemetry to the GUI using Qt signals
dashboard.py

Provides the desktop interface.

Displays ROS connection status
Displays battery level
Displays velocity
Displays robot running state
Provides START and STOP controls
Displays live battery and velocity plots
Sends received telemetry to the CSV logger
csv_logger.py

Handles telemetry logging.

Each telemetry sample is saved with:

timestamp,battery,velocity,running
Requirements
Ubuntu Linux
ROS 2
Python 3
PyQt5
pyqtgraph

The project was developed and tested using Ubuntu through WSL2 with ROS 2 Lyrical.

Installation
1. Source ROS 2
Open an Ubuntu terminal and run:source /opt/ros/lyrical/setup.bash

2. Install Python dependencies
From the project directory:
sudo apt update
sudo apt install python3-pyqt5 python3-pyqtgraph

3. Verify the environment
python3 -c "import rclpy; print('rclpy OK')"
python3 -c "import PyQt5; print('PyQt5 OK')"
python3 -c "import pyqtgraph; print('pyqtgraph OK')"
Running the Application

The application requires the mock ROS 2 node and the PyQt5 dashboard to run.

Terminal 1 — Start the mock robot
cd ~/robotics_data_interface
source /opt/ros/lyrical/setup.bash
python3 mock_ros2_node.py

The node will begin publishing telemetry.

Terminal 2 — Start the dashboard
cd ~/robotics_data_interface
source /opt/ros/lyrical/setup.bash
python3 dashboard.py

The PyQt5 dashboard will open.

Using the Dashboard
START

Clicking START publishes a command to:

/cmd_start

The simulated robot then:

Changes to the RUNNING state
Generates non-zero velocity
Slowly decreases battery level
Publishes updated telemetry
STOP

Clicking STOP publishes a command to:

/cmd_stop

The simulated robot then:

Changes to the STOPPED state
Sets velocity to 0.00 m/s
Stops battery drain
Live Visualization

The dashboard displays two live plots:

Velocity vs Time
Battery vs Time

The plots update as telemetry is received from the ROS 2 mock robot.

CSV Logging

Telemetry is automatically logged to:

telemetry.csv

The file contains:

timestamp,battery,velocity,running

Example:

timestamp,battery,velocity,running
2026-08-15 16:32:47,100.00,0.00,False
2026-08-15 16:32:48,99.98,1.25,True
2026-08-15 16:32:48,99.96,1.36,True

The CSV file is generated at runtime and is excluded from Git using .gitignore.

Threading Model

The GUI runs in the main Qt thread.

ROS 2 communication runs inside a separate QThread.

This prevents the ROS 2 spin loop from blocking the PyQt5 interface.

The communication flow is:

ROS 2 telemetry
      |
      v
ROSWorker
      |
      | Qt Signal
      v
PyQt5 Main Thread
      |
      +----> Dashboard values
      |
      +----> Live graphs
      |
      +----> CSV logger

Commands travel in the opposite direction:

START / STOP button
        |
        v
    ROS Worker
        |
        v
ROS 2 command topic
        |
        v
   Mock Robot
Assessment Requirements Covered
 Mock ROS 2 node
 Simulated battery telemetry
 Simulated velocity telemetry
 /cmd_start command
 /cmd_stop command
 PyQt5 desktop interface
 Background ROS worker
 Connection status
 Live battery and velocity metrics
 START / STOP controls
 Live telemetry plots
 Timestamped CSV logging
Demo

The demonstration shows:

Application running on Ubuntu
START button controlling the simulated robot
Live battery and velocity updates
Live telemetry plots
STOP button returning velocity to zero
Generated CSV telemetry log
Author

Robotics & Automation Engineering

Built as part of the Pace Robotics technical assessment.
