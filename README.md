# gRPC-Ride-Hailing
This repository contains a ride-hailing service implementation using gRPC, inspired by the LinkedIn Learning course gRPC in Python. The project demonstrates how to build and deploy a ride-hailing application with gRPC for efficient, high-performance communication between services.

LinkedIn Learning : https://www.linkedin.com/learning/grpc-in-python/why-grpc?autoplay=true&amp;u=2323090

falcon learning session
presenter: SYEDA LAIBA UROOJ
DATE: 24TH JAN 2023

1) create rides.proto
> protoc --python_out=. rides.proto
produces 'rides_pb2.py'

2) create marshalling.py
run without debugging

3) create gen.sh
After writing the service for the server, we run this shell script. 
Since, the command is a bit long, I wrote it in the sh file.
> ./gen.sh
produces two files 'rides_pb2.py' &  'rides_pb2_grpc.py'
'rides_pb2_grpc.py' is human-readable & will be implemented by me.

4) create requirements.txt & create_env.py
Standing in create_env.py do run without debugging to install necessary dependencies.

5) create server.py
Implement 'rides_pb2_grpc.py' & start the server here.
run without debugging

6) grpc_url
> grpcurl --version
After adding reflection in server.py
> grpcurl -plaintext localhost:8888 list [ make sure server is running]
> grpcurl -plaintext localhost:8888 list Rides [ outputs the methods in Rides ]
> grpcurl -plaintext localhost:8888 describe .Rides.Start
> grpcurl -plaintext localhost:8888 describe .StartRequest

7) add json file data
// -d = data , @ =  @ sign, meaning read it from the standard output
> grpcurl  -plaintext -d @ localhost:8888 Rides.Start < request.json
Remove driver-id in json file & hit again.

8) create client.py
run without debugging
INFO:root:connected to localhost:8888

9) export PROCESS_SPAWN_TIMEOUT=30

10) 
run without debugging - server
run without debugging - client

11) generate keys using OpenSSL
./gen-key.sh
output: key.pem , cert.pem
run server
grpcurl  -insecure -d @ localhost:8888 Rides.Start < request.json [ produces expected output ]
[ insecure because these are self-signed certificates. ]
code commented in server.py since running client.py gives errors [ connection lost ]

12) testing
> python -m pytest -v
