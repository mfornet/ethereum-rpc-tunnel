try:
    import json
    import multiprocessing as mp
    import os
    import time

    import dotenv
    import requests
    from flask import Flask, request

    from color import Print

except ModuleNotFoundError:
    print("""
    Install dependencies:

    python3 -m pip install --user -r requirements.txt
    """)
    exit(1)

dotenv.load_dotenv()


if os.getenv('USE_MONGO_DB'):
    from pymongo import MongoClient
    client = MongoClient('mongodb://localhost:27017')
    table = client.tunnel_rpc['aurora_mainnet']
else:
    print("""
    Queries are not saved. To save them in a Mongo database use:

    docker run --name aurora-tunnel-db -d mongo:latest
    export USE_MONGO_DB=1 # or save if in .env file
    """)

    class Table:
        def insert_one(self, *args, **kwargs): ...
    table = Table()


PORT = 5432
TARGET = os.getenv('RPC') or 'http://mainnet.aurora.dev/'

app = Flask(__name__)

headers = {
    'Content-Type': 'application/json; charset=utf-8',
}

INDEX = mp.Value('i', 0)


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'HEAD'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'HEAD'])
def index(path):
    with INDEX.get_lock():
        index = INDEX.value
        INDEX.value += 1

    if request.method == 'POST':
        rpc_request = request.data.decode()

        while True:
            Print.green(index, 'request:', rpc_request)
            res = requests.request(
                "POST", TARGET, headers=headers, data=rpc_request)

            if res.status_code != 200:
                Print.red(index, 'code:', res.status_code)
                Print.red(index, 'Sleeping')
                time.sleep(1.5)
            else:
                Print.cyan(index, 'code:', res.status_code)
                break

        rpc_response = res.content.decode()

        try:
            rpc_request_json = json.loads(rpc_request)
        except json.decoder.JSONDecodeError:
            rpc_request_json = None

        rpc_response = res.content.decode()

        try:
            rpc_response_json = json.loads(rpc_response)
        except json.decoder.JSONDecodeError:
            rpc_response_json = None

        if rpc_response_json is None or 'error' in rpc_response_json:
            Print.red(index, 'response', rpc_response)
        else:
            Print.blue(index, 'response', rpc_response)

        table.insert_one({
            'request_raw': rpc_request,
            'request_json': rpc_request_json,
            'response_raw': rpc_response,
            'response_json': rpc_response_json
        })

        return res.content


if __name__ == '__main__':
    app.run(port=PORT)
