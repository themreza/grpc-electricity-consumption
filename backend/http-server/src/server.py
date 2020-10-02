from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop

import grpc
import logging
import json

import meter_usage_pb2
import meter_usage_pb2_grpc

_logger = logging.getLogger(__name__)
_server_port = 8080
_grpc_port = 9090


class MeterUsageHandler(RequestHandler):
    def make_request(self):
        """
        Make a connection the gRPC server and receive the stream of data
        """
        with grpc.insecure_channel('grpc-server:%s' % _grpc_port) as channel:
            # Subscribe to the channel and read the messages
            stub = meter_usage_pb2_grpc.MeterUsageStub(channel)
            meter_usage_readings = []
            responses = stub.ReadData(meter_usage_pb2.ReadRequest())
            # Convert data from type MeterData into a simple dictionary to be JSON-encoded
            for response in responses:
                meter_usage_readings.append({
                    'timestamp': response.timestamp,
                    'value': response.value
                })
            return meter_usage_readings

    def get(self):
        try:
            responses = self.make_request()
            self.write({
                'data': responses
            })
        except grpc._channel._MultiThreadedRendezvous as err:
            # Catch any errors that may happen during the gRPC stream
            self.set_status(500)
            self.write({
                'error': err._state.details,
                'debug': json.loads(err._state.debug_error_string)
            })

class RootHandler(RequestHandler):
    def get(self):
        self.write({'message': 'gRPC Electricity Consumption Project API'})


def server_app():
    # API routes
    urls = [
        ("/", RootHandler),
        ("/meter-usage", MeterUsageHandler)
    ]
    return Application(urls)


if __name__ == '__main__':
    # Initialize the HTTP server
    app = server_app()
    app.listen(_server_port)
    _logger.info("Starting HTTP server on port %s" % _server_port)
    IOLoop.instance().start()
