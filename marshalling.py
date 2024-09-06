from datetime import datetime;

import rides_pb2 as pb

loc = pb.Location (
    lat=30.375320,
    lng=69.345116,
)
print('location')
print(loc)

print('enum: ride type')
print(pb.POOL) # 1
print(pb.REGULAR) # 0
print(pb.ride_type.Name(pb.POOL)) # POOL
print(pb.ride_type.Value('REGULAR')) # 0
print()


request = pb.StartRequest (
    car_id=95,
    driver_id='loid',
    passenger_ids=['P1','P2','P3'],
    type=pb.POOL, # over the bytes its going to be a single number ie 1
    location=loc,
)
print('request-1')
print(request.location.lat)
print(request)

# region setting time for request
time = datetime(2023,1,20,14,39,42) # this generated is not pythons date-time hence needs to be converted.
request.time.FromDatetime(time)
print('request-2 with time')
print(request)
print()
# endregion

time2 = request.time.ToDatetime()
print('time-2')
print(type(time2), time2) # <class 'datetime.datetime'> 2023-01-20 14:39:42
print()

# region Get Current Time
from google.protobuf.timestamp_pb2 import Timestamp
now = Timestamp()
now.GetCurrentTime()
print('current time')
print(now)
# endregion

# region Marshall
data = request.SerializeToString()
print('convert request to bytes')
print('type: ', type(data))
print('size: ', len(data))
print()
# endregion

# region json
# json is a very popular serialization format.
from google.protobuf.json_format import MessageToJson

dataJson = MessageToJson(request)
print('json serialization')
print(dataJson)
print()
# endregion

# region cmp sizes
print('encode size')
print('- json : ', len(dataJson))
print('- protobuf : ', len(data))
print()
# endregion

# region Unmarshall
request2 = pb.StartRequest ()
request2.ParseFromString(data)
print('un-marshall request')
print(request2)
# endregion
