import os
import subprocess
import random
import json
from flask import Flask, request, Response, got_request_exception
from flask_cors import CORS, cross_origin
import requests
from createsend import Subscriber, List, BadRequest
import rollbar
import rollbar.contrib.flask
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

LIST_ID = os.getenv("campaign_monitor_list_id")
API_KEYS = os.getenv("campaign_monitor_api_keys")

@app.before_first_request
def init_rollbar():
    """init rollbar module"""
    rollbar.init(
        # access token
        "95cd402683da45329da08d8cd98487f6",
        # environment name
        "production",
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False,
    )

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)


@app.route("/subscribe", methods=["POST"])
@cross_origin()
def subscribe():
    data = request.json
    if any(key not in data for key in ["email", "name", "lastname"]):
        return Response(
            "Invalid information",
            status=400,
        )
    sub = Subscriber({"api_key": API_KEYS}, list_id=LIST_ID)
    custom_fields = [
        {"Key": "Quizz_PDG", "Value": "OUI"},
        {"Key": "PRENOM", "Value": data.get("name")},
    ]
    try:
        response = sub.add(
            LIST_ID, data.get("email"), data.get("lastname"), custom_fields, False, "yes"
        )
    except BadRequest as e:
        print(e)
        return Response(
                "Bad request",
                status=400,
            )

    return Response(
        data,
        status=201,
    )


@app.route("/", methods=["GET"])
def all():
    return Response("ok", status=201)

if __name__ == "__main__":
    app.run(debug=False)
