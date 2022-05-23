import os
import subprocess
import random
import json

import boto
from boto.s3.key import Key

AWS_ACCESS = "{{ aws_access }}"
AWS_SECRET = "{{ aws_secret }}"
AWS_HOST = "s3.eu-west-3.amazonaws.com"
AWS_BUCKET = "oxfam-mega-bouses"


def upload_file(file_path: str, remote_key: str):
    """Backup backup_file on third-party server."""
    connexion = boto.connect_s3(
        AWS_ACCESS,
        AWS_SECRET,
        host=AWS_HOST,
    )
    bucket = connexion.get_bucket(AWS_BUCKET)

    key = Key(bucket)
    key.key = remote_key
    key.set_contents_from_filename(file_path)


def handler(event, context):
    import time

    print("EVENT", event)
    print(
        "computed", event.get("requestContext", {}).get("http", {}).get("method", None)
    )

    if event.get("requestContext", {}).get("http", {}).get("method", None) == "OPTIONS":
        print("options", event)
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": {"status": "OK"},
        }

    start = time.time()
    body = json.loads(event["body"])
    print("BODY", body)

    with open("template.svg", "r") as fh:
        string_data = fh.read()

    print("opened", time.time() - start)

    replace_fields = {
        "[[username]]": body["user"]["name"],
        "[[userCowDung]]": body["user"]["cowDungImpact"],
        "[[billionnaireCowDung]]": body["billionaire"]["cowDungImpact"],
        "[[billionaire]]": body["billionaire"]["name"],
        "[[multiplier]]": body["multiplier"],
    }

    for to_replace, replace_with in replace_fields.items():
        string_data = string_data.replace(to_replace, str(replace_with))

    random_id = random.randint(0, 100000000)

    with open(f"/tmp/{random_id}.svg", "w") as fh:
        fh.write(string_data)

    print("data written", time.time() - start)

    subprocess.check_output(
        f'inkscape --export-width=800 --export-png="/tmp/{random_id}.png" /tmp/{random_id}.svg',
        shell=True,
    )

    print("inkscape done", time.time() - start)

    # upload the png to s3
    upload_file(f"/tmp/{random_id}.png", f"images/{random_id}.png")

    print("upload done", time.time() - start)

    # remove local files
    os.remove(f"/tmp/{random_id}.png")
    os.remove(f"/tmp/{random_id}.svg")

    print(
        "return",
        f"http://s3-eu-west-3.amazonaws.com/oxfam-mega-bouses/images/{random_id}.png",
        time.time() - start,
    )

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "status": "success",
                "image_url": f"http://s3-eu-west-3.amazonaws.com/oxfam-mega-bouses/images/{random_id}.png",
            }
        ),
    }
