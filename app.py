from flask import Flask, render_template, request, Response
app = Flask(__name__)

from bot import init_message, normal_message
import json

ARGS = ""

@app.route('/')
def hello_world():  # put application's code here
    global ARGS
    ARGS = ""
    print(ARGS)
    return render_template("base.html")

@app.route('/message', methods=["POST"])
def receive_message():
    global ARGS
    data = request.get_json()
    message = (data['message'])
    properties = ""
    if ARGS == "":
        cust_response, properties, json_arguments = normal_message(message, ARGS)
    else:
        cust_response, properties, json_arguments = normal_message(message, ARGS)
    properties = json.dumps(properties)
    print(properties)
    if properties != "":
        properties = [{'name': item['address']['street'], 'id': item['_id']} for item in json.loads(properties)]
    ARGS = json_arguments
    print(json_arguments)
    response_json = {"message1": cust_response,
                      "message2": properties,
                    "message3": json_arguments}
    print(ARGS)
    return Response(json.dumps(response_json), status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run()
    