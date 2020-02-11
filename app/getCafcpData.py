import requests
import json
import re

# api
# url = 'https://cafcp.org/nocache/soss2-statusfile.json?_=1581271098841'
# url = 'https://cafcp.org/cafcp-station-details/15280'


## get station list
#url = 'https://cafcp.org/stationmap'
#response = requests.get(url).text
#
#res = re.search(r'\[\{"latitude".*?}]', response)
#stations = json.loads(res.group())
#
#with open('StationList.json', 'w') as f:
#    json.dump(stations, f)


# process stationInfo and get 
    
with open('StationList.json', 'r') as f:
    stations = json.load(f)    

stationInfo = {}
stationInfo['name'] = []
stationInfo['lat'] = []
stationInfo['lon'] = []
stationInfo['id'] = []

for s in stations:
    name = re.search(r'title:(.*?)]', s['opts']['title']).group(1)
    Id =  re.search(r'station:(.*?),', s['opts']['title']).group(1).strip()
    stationInfo['name'].append(name)
    stationInfo['id'].append(Id)
    stationInfo['lat'].append(s['latitude'])
    stationInfo['lon'].append(s['longitude'])

    
# Pull station detailed html
stationInfo['html'] = []
for Id in stationInfo['id']:
    print('processing '+Id+'...')
    res = json.loads(requests.get('https://cafcp.org/cafcp-station-details/'+Id, verify=False).text)
    stationInfo['html'].append(res['node_view'])
    
with open('StationInfo.json', 'w') as f:
    json.dump(stationInfo, f)