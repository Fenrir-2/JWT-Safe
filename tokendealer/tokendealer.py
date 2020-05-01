import time, zmq, jwt, json, random, string, atexit
from datetime import datetime, timedelta
from Cryptodome.PublicKey import RSA


def close_connections(ctx:zmq.Context):
    """
    Function used when stopping the tokendealer
    """
    ctx.destroy()
    if ctx.closed :
        print("Connection successfully closed.")
        exit()
    else :
        exit(-1)

def generate_keypair() -> (bytes,bytes):
    """
    Function used to generate the RSA keypair for jwt encryption
    """
    keypair = RSA.generate(2048)
    priv = keypair.export_key()
    pub = keypair.publickey().export_key()
    return pub, priv


if __name__ == "__main__":

    # dict holding tokens
    tokens = {}

    # generating the RSA keypair to encrypt/decrypt jwt
    pubkey,privkey = generate_keypair()

    # creating the context and the socket 
    context = zmq.Context()
    sock = context.socket(zmq.REP)
    sock.bind("tcp://0.0.0.0:7000")

    # setting a function as exit function (when stopping docker-compose)
    atexit.register(close_connections,context)

    # main loop
    while True:
        print("Beginning reception...")
        # json received through the socket
        api_call = sock.recv_json()

        # login method for the creation of the token
        if 'login' in api_call:
            enc_jwt = jwt.encode({'login':api_call['login'], 'timestamp': datetime.now().__str__()},privkey, algorithm='RS256')
            token = enc_jwt.decode('utf-8')
            tokens[api_call['login']] = token
            sock.send_json({'token':token})
        # verify method : decoding the token, testing if the token generation is less or equal than 1 hour
        elif 'verify' in api_call:
            try:
                decoded = jwt.decode(api_call['verify'],pubkey,algorithm='RS256')

                if decoded['login'] in tokens and tokens[decoded['login']] == api_call['verify']:
                    timestamp = datetime.strptime(decoded['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
                    if datetime.now() - timestamp <= timedelta(hours = 1):
                        sock.send_json({'valid': True})
                    else :
                        tokens.pop(decoded['login'])
                        sock.send_json({'valid': False})
                else :
                    sock.send_json({'valid': False})
            except jwt.exceptions.DecodeError as error:
                sock.send_json({'valid': False})
        # delete method : decoding the token, deleting it if really present in tokens list
        elif 'delete' in api_call:
            try:
                decoded = jwt.decode(api_call['delete'],pubkey,algorithm='RS256')

                if decoded['login'] in tokens and tokens[decoded['login']] == api_call['delete']:
                    timestamp = datetime.strptime(decoded['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
                    tokens.pop(decoded['login'])
                    sock.send_json({'deleted': True})
                else :
                    sock.send_json({'deleted': False})
            except jwt.exceptions.DecodeError as error:
                sock.send_json({'deleted': False})
