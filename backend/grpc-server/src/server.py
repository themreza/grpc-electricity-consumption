from concurrent import futures
from datetime import datetime

import grpc
import logging

from csv import reader

import meter_usage_pb2
import meter_usage_pb2_grpc

_logger = logging.getLogger(__name__)
_server_port = 9090


class MeterUsage(meter_usage_pb2_grpc.MeterUsageServicer):

    """ Read the meter usage data from the CSV file and stream it to the client """
    def ReadData(self, request, context):
        with open('../data/meterusage.csv', 'r') as read_obj:
            meter_usage_csv = reader(read_obj)
            next(meter_usage_csv) # Skip the CSV headers
            for meter_data in meter_usage_csv:
                _logger.warning(float(meter_data[1]))
                yield meter_usage_pb2.MeterData(
                    timestamp=int(datetime.strptime(meter_data[0], '%Y-%m-%d %H:%M:%S').timestamp()),
                    value=float(meter_data[1])
                )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    meter_usage_pb2_grpc.add_MeterUsageServicer_to_server(MeterUsage(), server)
    server.add_insecure_port('[::]:%s' % _server_port)
    _logger.info("Starting gRPC server on port %s" % _server_port)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
