from concurrent import futures
from datetime import datetime

import grpc
import logging

from csv import reader

import meter_usage_pb2
import meter_usage_pb2_grpc

_logger = logging.getLogger(__name__)
_server_port = 9090
_csv_file = '../data/meterusage.csv'

class MeterUsage(meter_usage_pb2_grpc.MeterUsageServicer):

    def ReadData(self, request, context):
        """
        Read the meter usage data from the CSV file and stream it to the client
        """
        with open(_csv_file, 'r') as read_obj:
            meter_usage_csv = reader(read_obj)

            # Skip the CSV headers
            next(meter_usage_csv)

            # Stream the data points
            for meter_data in meter_usage_csv:

                # Calculate the timestamp and adjust the value data type
                row_timestamp = int(datetime.strptime(meter_data[0], '%Y-%m-%d %H:%M:%S').timestamp())
                row_value = float(meter_data[1])

                # Example of possible timestamp filtering, which isn't necessary currently
                # if (request.timestamp_from and row_timestamp < request.timestamp_from) \
                #         or (request.timestamp_to and row_timestamp > request.timestamp_to):
                #     continue

                yield meter_usage_pb2.MeterData(
                    timestamp=row_timestamp,
                    value=row_value
                )


def serve():
    # Initialize the gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    meter_usage_pb2_grpc.add_MeterUsageServicer_to_server(MeterUsage(), server)
    server.add_insecure_port('[::]:%s' % _server_port)
    _logger.info("Starting gRPC server on port %s" % _server_port)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
