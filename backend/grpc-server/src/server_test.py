from concurrent import futures
from meter_usage import MeterUsage

import grpc
import unittest

import meter_usage_pb2
import meter_usage_pb2_grpc

class MeterUsageServerTest(unittest.TestCase):
    server_class = MeterUsage
    port = 50051
    csv_file = '../data/meterusage.csv'

    def setUp(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        meter_usage_pb2_grpc.add_MeterUsageServicer_to_server(MeterUsage(self.csv_file), self.server)
        self.server.add_insecure_port('[::]:%s' % self.port)
        self.server.start()

    def tearDown(self):
        self.server.stop(None)

    def get_server_responses(self):
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            meter_usage_readings = []
            stub = meter_usage_pb2_grpc.MeterUsageStub(channel)
            responses = stub.ReadData(meter_usage_pb2.ReadRequest())
            for response in responses:
                meter_usage_readings.append(response)
        return meter_usage_readings

    def test_server(self):
        meter_usage_readings = self.get_server_responses()
        # If the value of the given timestamp matches, it is very likely
        # that the dependent processes are functioning normally as well
        self.assertEqual([r for r in meter_usage_readings if r.timestamp == 1546398000][0].value, 58.68)

if __name__ == '__main__':
    unittest.main()