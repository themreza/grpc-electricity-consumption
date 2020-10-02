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
    """ Make a connection the gRPC server and receive the stream of data """
    def make_request(self):
        with grpc.insecure_channel('grpc-server:%s' % _grpc_port) as channel:
            stub = meter_usage_pb2_grpc.MeterUsageStub(channel)
            responses = stub.ReadData(
                meter_usage_pb2.ReadRequest(
                    timestamp_from=self.get_argument('timestamp_from', None),
                    timestamp_to=self.get_argument('timestamp_to', None),
                )
            )
            return responses

    def post(self):
        responses = self.make_request()
        if responses._state.code.name == 'OK':
            self.write({'data': responses})
        else:
            self.set_status(500)
            self.write({
                'error': responses._state.details,
                'debug': json.loads(responses._state.debug_error_string)
            })


class RootHandler(RequestHandler):
    def get(self):
        self.write({'message': 'gRPC Electricity Consumption Project API'})


def server_app():
    urls = [
        ("/", RootHandler),
        ("/meter-usage", MeterUsageHandler)
    ]
    return Application(urls)


if __name__ == '__main__':
    app = server_app()
    app.listen(_server_port)
    _logger.info("Starting HTTP server on port %s" % _server_port)
    IOLoop.instance().start()
