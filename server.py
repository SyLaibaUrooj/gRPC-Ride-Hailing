# This is going to be used to run the requests.
from concurrent.futures import ThreadPoolExecutor
# To generate new IDs. 
from uuid import uuid4
from time import perf_counter

import sys;
sys.path.append("/usr/local/lib/python3.10/site-packages/")

import grpc
# even though below shows error but error will not show up on console bcuz of added path in sys.
from grpc_reflection.v1alpha import reflection

import logging as log
log.basicConfig(level = log.INFO)

import rides_pb2 as pb
import rides_pb2_grpc as rpc
import validate

def new_ride_id():
    return uuid4().hex

# server side interceptor that is going to record how much time an operation took
# output: INFO:root:/Rides/Start took 0.000sec
class TimingInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        start = perf_counter()
        try:
            return continuation(handler_call_details)
        finally:
            duration = perf_counter() - start
            name = handler_call_details.method
            log.info('%s took %.3fsec', name, duration)

class Rides(rpc.RidesServicer): # This is called Rides from the RidesServicer that is defined by the generated grpc code.
    def Start(self, request, context): # override
        log.info('ride: %r', request)

        try:
            validate.start_request(request)
        except validate.Error as err:
            log.error('bad request: %s', err)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f'{err.field} is {err.reason}')
            raise err

        # TODO: Store ride in database
        ride_id = new_ride_id()
        return pb.StartResponse(id=ride_id)

    def Track(self, request_iterator, context):
        count = 0
        for request in request_iterator:
            # TODO: Store in database
            log.info('track: %s', request)
            count += 1

        return pb.TrackResponse(count=count)

# https [ openssl ]
# def load_credentials():
#     with open(config.cert_file, 'rb') as fp:
#         cert = fp.read()

#     with open(config.key_file, 'rb') as fp:
#         key = fp.read()

#     return grpc.ssl_server_credentials([(key, cert)])

 # below for the test_server.py
# def build_server(port):
#     server = grpc.server(ThreadPoolExecutor())
#     rpc.add_RidesServicer_to_server(Rides(), server)
#     names = (
#         pb.DESCRIPTOR.services_by_name['Rides'].full_name,
#         reflection.SERVICE_NAME,
#     )
#     reflection.enable_server_reflection(names, server)

#     addr = f'[::]:{port}'
#     server.add_insecure_port(addr)
#     return server

# Once the server ready, we can run it.
if __name__ == '__main__':
    import config

    # server = build_server(config.port) # for the test_server.py

    # generated generic grpc server.
    server = grpc.server(
        ThreadPoolExecutor(),
        interceptors=[TimingInterceptor()],
    )
    # register my server inside the grpc server.
    rpc.add_RidesServicer_to_server(Rides() , server)

    # we create below reflection so that client can query the server.
    names =  (
        pb.DESCRIPTOR.services_by_name['Rides'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(names,server)

    # define address.
    addr = f'[::]:{config.port}'

    # addr = f'[::]:{8888}'
    # Grpc uses HTTP/2, which is by default using HTTPS. We need to tell grpc to work with plain HTTP without TLS information.
    server.add_insecure_port(addr)

    # credentials = load_credentials()
    # server.add_secure_port(addr,credentials)
    server.start()

    log.info('server ready on %s', addr)
    server.wait_for_termination()
