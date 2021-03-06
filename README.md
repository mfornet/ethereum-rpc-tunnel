# Tunnel to debug Ethereum-like RPC connections

## Usage

1. Clone the repository
2. Install dependencies:
   `python3 -m pip install --user -r requirements.txt`
3. Run:
   `python3 main.py`

This will open a (flask) server listening at `http://127.0.0.1:5432/`. Change your app endpoint to this address, and check the terminal to see all request and responses while the app is running.

## Use custom endpoint

By default it will use `http://mainnet.aurora.dev/` as the endpoint. If you want to change (for example to specify an API KEY), use environment variable `RPC`.
Environment variables can be stored in `.env` file, and they will be automatically loaded on startup.

## Store all request/response

All interaction between the tunnel and the endpoint can be saved in a MongoDB table for later inspection. Use it with:

```
docker run --name aurora-tunnel-db -d mongo:latest
export USE_MONGO_DB=1 # or save if in .env file
```

## Screenshot

![Screenshot](image/screenshot.png "Screenshot")
