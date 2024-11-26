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

def get_associated_runs(meshID: str, experiment_type: str | None) -> list[str]:
    query = {'mesh_id':meshID, "skip":0, "limit":2000} if meshID != "D006262" else {'mesh_id':meshID, "skip":0, "limit":5000} # D006262 is "Health"
    url = 'https://gmrepo.humangut.info/api/getAssociatedRunsByPhenotypeMeshIDLimit'
    try:
        api_response = requests.post(url, data=json.dumps(query))
    except requests.exceptions.RequestException as e:
        print(f"Error: Cannot connect to the API, error_msg: {e}")
        return []
    query_response = api_response.json()

    # run_id_list = [(run["run_id"], run["nr_reads_sequenced"]) for run in query_response]
    # scales = [30000, 300000, 3000000] # 10MB, 100MB, 1GB
    # scales = [30000, 40000, ..., 1000000]

    # scales = [i * 10000 for i in range(3, 101)]
    # for scale in scales:
    #     return_flag = False
    #     if meshID == "D003324" or meshID == "D060825":
    #         run_id_list = [(run["run_id"], run["nr_reads_sequenced"]) for run in query_response]
    #         return_flag = True
    #     else:
    #         run_id_list = [(run["run_id"], run["nr_reads_sequenced"]) for run in query_response if (run["nr_reads_sequenced"] != None and run["nr_reads_sequenced"] <= scale)]
    #         if len(run_id_list) > 100 or scale == 1000000:
    #             return_flag = True
    #     if return_flag:
    #         return run_id_list

    if experiment_type != None:
        if meshID in ["D006262", "D003924", "D011236", "D010300"]:
            scales = [i * 10000 for i in range(3, 101)] # at most 300MB
            for scale in scales:
                return_flag = False
                run_id_list = [(run["run_id"], run["nr_reads_sequenced"]) for run in query_response if (run["experiment_type"] == experiment_type and run["nr_reads_sequenced"] != None and run["nr_reads_sequenced"] <= scale)]
                if len(run_id_list) > 100 or scale == 1000000:
                    return_flag = True
                if return_flag:
                    return run_id_list
            # run_id_list = [(run["run_id"], run["nr_reads_sequenced"]) for run in query_response if run["experiment_type"] == experiment_type]
        else:
            run_id_list = [(run["run_id"], run["nr_reads_sequenced"]) for run in query_response if run["experiment_type"] == experiment_type]
    else:   
        run_id_list = [(run["run_id"], run["nr_reads_sequenced"]) for run in query_response]
    return run_id_list

if __name__ == "__main__":
    # experiment_type
    experiment_type = "Amplicon" # "Amplicon" or "Metagenomics"
    # 11 phenotypes
    # target_phenotype_list = ["Health", "Autism Spectrum Disorder", "Alzheimer Disease", "Attention Deficit Disorder with Hyperactivity", "Diabetes Mellitus, Type 2",
    #                     "Prediabetic State", "Cognitive Dysfunction", "Depression", "Coronary Artery Disease", "Parkinson Disease", "Kidney Diseases"]
    target_phenotype_list = ["Health", "Autism Spectrum Disorder", "Attention Deficit Disorder with Hyperactivity", "Diabetes Mellitus, Type 2", "Prediabetic State", "Parkinson Disease"]

    # Health: D006262
    # Autism Spectrum Disorder: D000067877 (V)
    # Attention Deficit Disorder with Hyperactivity: D001289 (V)
    # Diabetes Mellitus, Type 2: D003924
    # Prediabetic State: D011236
    # Parkinson Disease: D010300

    disease_runID_dict = dict()
    disease_to_meshID = get_diseases_to_meshID(target_phenotype_list)

    for key, value in tqdm(disease_to_meshID.items()):
        disease_run_ids = get_associated_runs(value, experiment_type)
        disease_runID_dict[key] = disease_run_ids
        print(f"Number of runs for {key}: {len(disease_runID_dict[key])}")
    
    # dict to json
    with open('disease_runID_ampn.json', 'w') as f:
        json.dump(disease_runID_dict, f, indent=4)