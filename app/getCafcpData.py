import requests
import json
import re


# url = 'https://cafcp.org/nocache/soss2-statusfile.json?_=1581271098841'
# url = 'https://cafcp.org/cafcp-station-details/15280'

# response = json.loads(requests.get(url).text)

url = 'https://cafcp.org/stationmap'
response = requests.get(url).text

# response = r'\n haha [{"latitude"@$$@$@$@$@]sadfs]df'
res = re.search(r'\[\{"latitude".*?}]', response)
stations = json.loads(res.group())

with open('StationList.json', 'w') as f:
    json.dump(stations, f)




# print(response[-1000:])
# print(response['node_view'])

