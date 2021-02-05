import requests

routes_to_check = ["http://scan-runner/health",
                   "http://source-resolver/health"]

for route in routes_to_check:
    r = requests.get(route)
    obj = r.json()
    print(route + " : " + str(obj))