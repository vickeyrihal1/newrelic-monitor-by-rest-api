#!env python

import urllib.request
import json

# ToDo: parse as argument
api_key = "NRAK-XXXXXXXXXXXXXXXXX"

api_v3_monitors = "https://synthetics.newrelic.com/synthetics/api/v3/monitors"
api_v2_alert_cond = "https://api.newrelic.com/v2/alerts_synthetics_conditions.json"

#uris = ["google.com"]

# Add headers
def request_header(nr_api, data=None, contentType="json", method=None) -> urllib.request:
    if method == "DELETE":
        req = urllib.request.Request(nr_api, method="DELETE")
    else:
        req = urllib.request.Request(nr_api, data=data)
    if contentType == "json":
        req.add_header('Content-Type', 'application/json')
    req.add_header('X-Api-Key', api_key)
    return(req)

# GET - Existing Monitor List 
def existing_monitors() -> dict:
    response = urllib.request.urlopen(request_header(api_v3_monitors))
    # decoded response in json
    decoded_response = json.loads(response.read().decode('utf-8'))
    #string output => decoded_response = response.read().decode('utf-8')
    return(decoded_response)

# GET - Extract Monitor Name and ID
def existing_monitors_metadata() -> dict:
    existing_monitor_name = {}
    for monitor in existing_monitors()["monitors"]:
        existing_monitor_name.update({monitor["name"]: monitor["id"]})
    return(existing_monitor_name)


# GET - Alert Conditions
def existing_alert_conditions(nr_api, data) -> dict:
    dataByte = urllib.parse.urlencode(data).encode("utf-8")
    #response = urllib.request.urlopen(request_header(nr_api, data=data_byte, content=None))
    response = urllib.request.urlopen(request_header(nr_api, contentType=None), data=dataByte)
    # decoded response in json
    decoded_response = json.loads(response.read().decode('utf-8'))
    #string output => decoded_response = response.read().decode('utf-8')
    return(decoded_response)

# POST add monitor
def add_synthetic_monitor(nr_api, monitor_uri):
    data = {
        "name" : monitor_uri, 
        "type" : "SIMPLE", 
        "uri": f"https://{monitor_uri}",
        "frequency" : 15, 
        "locations" : [ "AWS_US_EAST_1" ], 
        "status": "ENABLED",
        "options": {
            "verifySSL": "true"
        }
    }
    jsonbody = json.dumps(data)
    jsonbodybytes = jsonbody.encode('utf-8')
    # no response so just execute it
    urllib.request.urlopen(request_header(nr_api), jsonbodybytes)
    
# POST
def add_alert_condition(nr_api, monitor_uri, monitor_id) -> dict:
    data = {
    "synthetics_condition": {
        "name": monitor_uri,
        "monitor_id": monitor_id,
        "enabled": True
        }
    }
    jsonbody = json.dumps(data)
    jsonbodybytes = jsonbody.encode('utf-8')
    response = urllib.request.urlopen(request_header(nr_api), jsonbodybytes)

    # decoded response in json
    decoded_response = json.loads(response.read().decode('utf-8'))
    return(decoded_response)

# delete monitors by id
def del_monitors(monitor_id):
    nr_api = f"https://synthetics.newrelic.com/synthetics/api/v3/monitors/{monitor_id}"
    urllib.request.urlopen(request_header(nr_api, method = "DELETE"))

# delete monitors conditions by id
def del_alert_condition(condition_id):
    nr_api = f"https://api.newrelic.com/v2/alerts_synthetics_conditions/{condition_id}.json"
    urllib.request.urlopen(request_header(nr_api, method = "DELETE"))

# Existing alert condition against manually created policy - 3401443
def existing_alert_conditions_by_id(policy_id):
    existing_alert_conditions_by_id = existing_alert_conditions(api_v2_alert_cond, data=dict(policy_id=policy_id))
    api_v2_alert_cond_pol = f"https://api.newrelic.com/v2/alerts_synthetics_conditions/policies/{policy_id}.json"
    return(existing_alert_conditions_by_id, api_v2_alert_cond_pol)

# Create Synthetic monitors and alerts
def create_monitor_alerts(uris, existing_alert_conditions, api_v2_alert_cond_pol):
    ## Existing Monitors
    existing_monitors_name = existing_monitors_metadata()

    # name list in alert conditions
    existing_alert_conditions_name = []
    for name in existing_alert_conditions['synthetics_conditions']:
        existing_alert_conditions_name += [name["name"]]

    # Create Alerts and Alert Conditions
    for uri in uris:
        print("##############################")
        print(f"Processing monitor - {uri}")
        # WIP - add monitor
        if uri not in existing_monitors_name:
            response = add_synthetic_monitor(api_v3_monitors, uri)
            print(f"[Info] Synthetic monitor created -> {uri}.")
        else:
            print(f"[Warn] monitor already exists -> {uri}.")
        
        #Live - add condition
        if uri not in existing_alert_conditions_name:
            existing_monitors_name = existing_monitors_metadata()
            response = add_alert_condition(api_v2_alert_cond_pol,
                            uri,
                            existing_monitors_name[uri])
            print(f"Condition created -> {response}.")
