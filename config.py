from os import environ
# from pathlib import Path

# here = Path(__file__).absolute().parent

port = int(environ.get('PORT', 8888))
host = environ.get('HOST', 'localhost')

# cert_file = environ.get('CERT_FILE', here / 'cert.pem')
# key_file = environ.get('KEY_FILE', here / 'key.pem')
