import json

def make_json(search='', customResponse='', intent='', workflow='', response=[], questions=[]):
    x = {
        "search":search, "customResponse":customResponse, "intent":intent, "workflow":workflow, "response":response, "questions":questions
    }
    return json.dumps(x)

