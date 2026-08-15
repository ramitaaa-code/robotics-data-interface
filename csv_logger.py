import csv
import os
from datetime import datetime


class CSVLogger:

    def __init__(self, filename="telemetry.csv"):

        self.filename = filename

        # Create the CSV file with a header if it doesn't exist
        if not os.path.exists(self.filename):

            with open(
                self.filename,
                "w",
                newline=""
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "timestamp",
                    "battery",
                    "velocity",
                    "running"
                ])

    def log_telemetry(
        self,
        battery,
        velocity,
        running
    ):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(
            self.filename,
            "a",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                timestamp,
                f"{battery:.2f}",
                f"{velocity:.2f}",
                running
            ])
