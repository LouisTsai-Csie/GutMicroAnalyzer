import json
import requests
from tqdm import tqdm
def get_diseases_to_meshID(phenotypes_list: list[str]) -> dict[str, str]:
    ## -- get all phenotypes  --
    url = 'https://gmrepo.humangut.info/api/get_all_phenotypes'
    try:
        api_response = requests.post(url, data={})
    except requests.exceptions.RequestException as e:
        print(f"Error: Cannot connect to the API, error_msg: {e}")
        return {}
    phenotype_response = api_response.json().get('phenotypes')

    disease_to_meshID = dict()
    for phenotype in tqdm(phenotype_response):
        if phenotype["term"] in phenotypes_list:
            disease_to_meshID[phenotype["term"]] = phenotype["disease"]
    return disease_to_meshID

def get_associated_runs(meshID: str) -> list[str]:
    query = {'mesh_id':meshID, "skip":0, "limit":2000} if meshID != "D006262" else {'mesh_id':meshID, "skip":0, "limit":5000} # D006262 is "Health"
    url = 'https://gmrepo.humangut.info/api/getAssociatedRunsByPhenotypeMeshIDLimit'
    try:
        api_response = requests.post(url, data=json.dumps(query))
    except requests.exceptions.RequestException as e:
        print(f"Error: Cannot connect to the API, error_msg: {e}")
        return []
    query_response = api_response.json()
    run_id_list = [run["run_id"] for run in query_response]
    # print(f"Number of runs for {meshID}: {len(run_id_list)}")
    return run_id_list

if __name__ == "__main__":
    # 11 phenotypes
    target_phenotype_list = ["Health", "Autism Spectrum Disorder", "Alzheimer Disease", "Attention Deficit Disorder with Hyperactivity", "Diabetes Mellitus, Type 2",
                        "Prediabetic State", "Cognitive Dysfunction", "Depression", "Coronary Artery Disease", "Parkinson Disease", "Kidney Diseases"]
    
    disease_runID_dict = dict()
    disease_to_meshID = get_diseases_to_meshID(target_phenotype_list)

    for key, value in tqdm(disease_to_meshID.items()):
        disease_run_ids = get_associated_runs(value)
        disease_runID_dict[key] = disease_run_ids
    
    # dict to json
    with open('disease_runID.json', 'w') as f:
        json.dump(disease_runID_dict, f, indent=4)