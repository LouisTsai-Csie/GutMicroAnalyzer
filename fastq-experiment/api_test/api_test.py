import json
import requests
## -- get all phenotypes  --
url = 'https://gmrepo.humangut.info/api/get_all_phenotypes'
res = requests.post(url, data={})
res_json_phenotypes = res.json().get('phenotypes')
with open('all_disease_example.json', 'w') as f:
    json.dump(res_json_phenotypes, f, indent=4)

## -- get all associted runs --
## use skip = 0, limit = 100 to retrieve the first 100 runs, then
##     skip = 100, limit = 100 to retrieve the next 100 runs ....
query = {'mesh_id':"D006262", "skip":0, "limit":2000} 
url = 'https://gmrepo.humangut.info/api/getAssociatedRunsByPhenotypeMeshIDLimit'
res = requests.post(url, data=json.dumps(query))
res_json = res.json()
with open('single_disease_example.json', 'w') as f:
    json.dump(res_json, f, indent=4)