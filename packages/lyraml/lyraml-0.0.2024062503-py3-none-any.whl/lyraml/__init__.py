import requests
import inspect
import time
import json
from .utils.display_util import clear_line, green_check, red_check, reset_color
import time
from urllib.parse import parse_qs, quote
from .utils.source_code import get_source_code_hash, get_json_obj_hash
from .utils.constants import BASE_CLIENT_URL, PROJECT_BASE_URL, MODEL_BASE_URL, RUN_BASE_URL, DATASET_BASE_URL, JUDGE_BASE_URL, EVALUATION_BASE_URL
from .utils.file import upload_data, download_data, read_source_code_as_func


def print_error_message(code):
    try:
        print(error_code_message_map[code])
    except:
        print(error_code_message_map['unexpected_error'])

error_code_message_map = {
    'invalid_api_key': 'Invalid API Key. Please verify your API Key or generate a new one at https://lyra-ml.com Workspace Settings tab.',
    'exceed_storage_limit': '🚧 You\'ve reached your storage limit! To keep everything running smoothly, please visit our Pricing Page to explore upgrade options that suit your needs.',
    'unexpected_error': 'Oops! Something went wrong on our end. Please try again later. If the issue persists, feel free to contact our support team. We\’re here to help!'
}

class Lyra:
    def __init__(self, project_name, API_KEY):
        self.projectId = None
        self.error_code = None
        self.api_key = API_KEY
        self.judges = []
        response = requests.post(PROJECT_BASE_URL, json={'project_name': project_name}, headers={'Authorization': f'Bearer {API_KEY}'})
        if response.status_code == 201:
            body = json.loads(response.text)
            self.projectId = body["project"]["id"]
        else:
            body = json.loads(response.text)
            self.error_code = body["code"]
            print_error_message(self.error_code)


    def _download_dataset(self, dataset_tag):
        # Should get the download url and then download it here.
        response = requests.get(DATASET_BASE_URL + "/" + dataset_tag + "?projectId=" + self.projectId, headers={'Authorization': f'Bearer {self.api_key}'})
        if response.status_code != 200:
            raise ValueError("Failed to download dataset")

        dataset = json.loads(response.text)["dataset"]
        
        parsed_data = parse_qs(download_data(dataset["filename"], self.api_key))
        parsed_data['name'] = parsed_data['name'][0]
        return parsed_data

    def upload_dataset(self, dataset):
        dataset_hash = get_json_obj_hash(dataset.to_json())

        tag_response = requests.post(DATASET_BASE_URL + "/tag", json={
            'name': dataset.name,
            'hash': dataset_hash,
            'projectId': self.projectId,
        }, headers={'Authorization': f'Bearer {self.api_key}'})
        if tag_response.status_code != 200:
            raise ValueError("Failed to get dataset tag")

        tag = json.loads(tag_response.text)["tag"]
        dataset_filename = self.projectId + "_" + tag + ".txt"
        upload_data(dataset_filename, dataset.to_json(), self.api_key)

        dataset_response = requests.post(DATASET_BASE_URL, json={
            'filename': dataset_filename,
            'hash': dataset_hash,
            'name': dataset.name,
            'projectId': self.projectId,
            'tag': tag,
        }, headers={'Authorization': f'Bearer {self.api_key}'})

        if dataset_response.status_code != 200: 
            raise ValueError("Failed to post dataset tag: {tag}")
        return tag


    def add_judge(self, judge):
        scoring_source_code, judge_scoring_hash = get_source_code_hash(judge.scoring_rubric)
        passing_criteria_source_code, judge_passing_hash = get_source_code_hash(judge.passing_criteria)
        
        judge_tag_response = requests.post(JUDGE_BASE_URL + "/tag", json={
            'judge_passing_hash': judge_passing_hash,
            'judge_scoring_hash': judge_scoring_hash,
            'name': judge.name,
            'projectId': self.projectId,
        }, headers={'Authorization': f'Bearer {self.api_key}'})
        
        if judge_tag_response.status_code != 200:
            raise ValueError("Failed to get judge tag")

        judgeTag = json.loads(judge_tag_response.text)["judgeTag"]

        scoring_filename = self.projectId + "_" + judgeTag + "_scoring.txt"
        upload_data(scoring_filename, scoring_source_code, self.api_key)


        passing_filename = self.projectId + "_" + judgeTag + "_passing.txt"
        upload_data(passing_filename, passing_criteria_source_code, self.api_key)

        response = requests.post(JUDGE_BASE_URL, json={
            'judge': json.dumps(judge.to_json()),
            'passing_code_filename': passing_filename,
            'passing_hash': judge_passing_hash,
            'projectId': self.projectId,
            'scoring_code_filename': scoring_filename,
            'scoring_hash': judge_scoring_hash,
            # 'data_size': scoring_source_data_size + passing_data_size,
            'tag': judgeTag,
        }, headers={'Authorization': f'Bearer {self.api_key}'})

        if response.status_code == 201:
            body = json.loads(response.text)
            if body["isNew"]:
                print(f"✔ Judge {judgeTag} created.")
            else:
                print(f"✔ Judge {judgeTag} already exists.")
            
                for item in body["itemsUpdated"]:
                    print(f"✔ Judge {item['field']} field has been updated to: \"{item['value']}\"")
        
    def _get_judge_from_judge_tag(self, judge_tag):
        encoded_judge_tag = quote(judge_tag)
        judge_response = requests.get(JUDGE_BASE_URL + "/" + encoded_judge_tag + "/projects/" + self.projectId, headers={'Authorization': f'Bearer {self.api_key}'})
        if judge_response.status_code != 200:
            raise ValueError("Failed to get judge from judge tag")
        
        judge = json.loads(judge_response.text)["judge"]
        return judge


    def _get_scoring_rubric_func_from_judge(self, judge):
        scoring_source_code = download_data(judge["scoringCodeFilename"], self.api_key)
        return read_source_code_as_func(scoring_source_code, "scoring_rubric")


    def _get_passing_criteria_func_from_judge(self, judge):
        passing_source_code = download_data(judge["passingCodeFilename"], self.api_key)
        return read_source_code_as_func(passing_source_code, "passing_criteria")


    def evaluate_with(self, judge_tag):
        judge = self._get_judge_from_judge_tag(judge_tag)        

        def decorator(func):
            def wrapper(*args, **kwargs):
                dataset = self._download_dataset(judge["dataset_tag"])
                passed_cases = 0
                failed_cases = 0
                i = 0
                scores = []
                for row in dataset["data"]:
                    message = f"Evaluating {dataset['name']} {i}/{len(dataset['data'])}..."
                    print(f"\n{message}", end="", flush=True)
                    outputs = func(row)
                    scoring_rubric = self._get_scoring_rubric_func_from_judge(judge)
                    passing_criteria = self._get_passing_criteria_func_from_judge(judge)

                    score = scoring_rubric(outputs)
                    scores.append({
                        "output": outputs,
                        "score": score,
                    })
                    clear_line()
                    if passing_criteria(score):
                        passed_cases += 1
                        print(f"\r{green_check()} {dataset['name']}[{i}] score: {score} {reset_color()}", end="", flush=True)
                    else:
                        failed_cases += 1
                        print(f"\r{red_check()} {dataset['name']}[{i}] score: {score} {reset_color()}", end="", flush=True)
                    i += 1

                if failed_cases == 0:
                    print(f"\n{green_check()} All cases in dataset passed.")
                else:
                    print(f"\n\n{red_check()} {failed_cases} out of {len(dataset['data'])} failed")

                response = requests.post(EVALUATION_BASE_URL, json={
                    'scores': scores,
                    'judge_tag': judge["tag"],
                    'projectId': self.projectId,
                })

                if response.status_code != 201:
                    raise ValueError("Failed to create evaluation")
                
                return func(*args, **kwargs)
            return wrapper
        return decorator


    def trace(self, func):
        def wrapper(*args, **kwargs):
            if self.error_code:
                return

            params = inspect.signature(func).parameters
            source_code, hash_digest = get_source_code_hash(func)

            start = time.perf_counter()
            result = func(*args, **kwargs)
            latency = time.perf_counter() - start

            # This whole getting model tag and conditionally creation of model could be pulled out separately
            # Perhaps we can make it even more generic by doing the same for evaluations and datasets. 
            model_tag_response = requests.post(MODEL_BASE_URL + "/tag", json={
                'name': func.__name__,
                'hash': hash_digest,
                'projectId': self.projectId
            }, headers={'Authorization': f'Bearer {self.api_key}'})

            if model_tag_response.status_code != 200:
                raise ValueError("Failed to get the next run id")

            model_tag = json.loads(model_tag_response.text)["tag"]
            model_filename = self.projectId + "_" + model_tag + ".txt"
            upload_data(model_filename, source_code, self.api_key)


            param_keys = [key for key in params]
            formatted_args = []
            i = 0
            for arg in args:
                formatted_args.append({
                    'name': param_keys[i],
                    'value': arg,
                    'type': type(arg).__name__,
                })
                i += 1 
            
            formatted_outputs = [{
                'value': result,
                'type': type(result).__name__,
            }]
            
            model_response = requests.post(MODEL_BASE_URL, json={
                'inputs': [{'name': entry['name'], 'type': entry['type']} for entry in formatted_args],
                'modelTag': model_tag,
                'outputs': [{'type': entry['type']} for entry in formatted_outputs],
                'projectId': self.projectId,
            }, headers={'Authorization': f'Bearer {self.api_key}'})
 
            if model_response.status_code != 201:
                raise ValueError("Failed to create or fetch model with model tag: " + model_tag)

            run_creation_response = requests.post(RUN_BASE_URL, json={
                'inputs': formatted_args,
                'latency': latency,
                'modelTag': model_tag,
                'outputs': formatted_outputs,
                'projectId': self.projectId,
                # 'dataSize': data_size,
            }, headers={'Authorization': f'Bearer {self.api_key}'})

            body = json.loads(run_creation_response.text)
            if run_creation_response.status_code == 201:
                print("✨ View run " + body["run"]["id"] + " at " + BASE_CLIENT_URL + "/workspace/" + body["workspaceId"] + "/project/" + self.projectId)
                return result
            else:    
                self.error_code = body["code"]
                print_error_message(self.error_code)

        return wrapper