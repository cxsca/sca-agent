import requests
import sys

route_to_test = "http://localhost/identity/.well-known/openid-configuration"

try:
    r = requests.get(route_to_test)
    if r.status_code != 200:
        sys.exit("Agent is down. Please check if agent can successfully startup.\n"
                 f"Details : {route_to_test} ({r.status_code} - {r.reason})")
except(Exception):
    sys.exit("Network Error. Something went wrong accessing the network")
