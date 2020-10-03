from datetime import datetime
from csv import reader

import pytz
import meter_usage_pb2
import meter_usage_pb2_grpc


class MeterUsage(meter_usage_pb2_grpc.MeterUsageServicer):
    def __init__(self, csv_file):
        self._csv_file = csv_file

    def ReadData(self, request, context):
        """
        Read the meter usage data from the CSV file and stream it to the client
        """
        with open(self._csv_file, 'r') as read_obj:
            meter_usage_csv = reader(read_obj)

            # Skip the CSV headers
            next(meter_usage_csv)

            # Stream the data points
            for meter_data in meter_usage_csv:
                # Calculate the timestamp and adjust the value data type, based on UTC
                row_timestamp = int(
                    pytz.timezone('UTC').localize(datetime.strptime(meter_data[0], '%Y-%m-%d %H:%M:%S')).timestamp()
                )
                row_value = float(meter_data[1])

                # Example of possible timestamp filtering, which isn't necessary currently
                # if (request.timestamp_from and row_timestamp < request.timestamp_from) \
                #         or (request.timestamp_to and row_timestamp > request.timestamp_to):
                #     continue

                yield meter_usage_pb2.MeterData(
                    timestamp=row_timestamp,
                    value=row_value
                )
