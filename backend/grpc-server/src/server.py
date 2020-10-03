from concurrent import futures
from meter_usage import MeterUsage

import grpc
import logging

import meter_usage_pb2_grpc

_logger = logging.getLogger(__name__)
_server_port = 9090
_csv_file = '../data/meterusage.csv'

def serve():
    # Initialize the gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    meter_usage_pb2_grpc.add_MeterUsageServicer_to_server(MeterUsage(_csv_file), server)
    server.add_insecure_port('[::]:%s' % _server_port)
    _logger.info("Starting gRPC server on port %s" % _server_port)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
