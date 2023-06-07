from flask import Flask, request, jsonify
import pandas as pd
from etl_processor import ETLProcessor
import asyncio

app = Flask(__name__)
etl_processor = ETLProcessor()


# Your API that can be called to trigger your ETL process
@app.route("/trigger_etl", methods=["GET"])
def trigger_etl():
    # Trigger your ETL process here
    result = asyncio.run(etl_processor.etl())
    return jsonify({"message": "ETL process started", "result": result}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
