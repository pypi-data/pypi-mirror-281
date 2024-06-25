import requests
import httpx
import asyncio
import inspect
import time
import json
import hashlib
from .utils.display_util import clear_line, green_check, red_check, reset_color
import time
from urllib.parse import parse_qs, quote
from .utils.source_code import get_source_code_hash, get_json_obj_hash
from .utils.constants import BASE_URL, BASE_CLIENT_URL, PROJECT_BASE_URL, RUN_BASE_URL, DATASET_BASE_URL, JUDGE_BASE_URL, EVALUATION_BASE_URL
from .utils.file import upload_data, download_data, read_source_code_as_func


async def post_data(url, json_data):
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=json_data)
        return response


async def get_data(url):
    async with httpx.AsyncClient() as client: 
        response = await client.get(url)
        return response

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
        self.judges = []
        response = requests.post(PROJECT_BASE_URL, json={'project_name': project_name, 'api_key': API_KEY})
        if response.status_code == 201:
            body = json.loads(response.text)
            self.projectId = body["project"]["id"]
        else:
            body = json.loads(response.text)
            self.error_code = body["code"]
            print_error_message(self.error_code)

    def _download_dataset(self, dataset_tag):
        # Should get the download url and then download it here.
        response = requests.get(DATASET_BASE_URL + "/" + dataset_tag)
        if response.status_code != 200:
            raise ValueError("Failed to download dataset")
        
        dataset = json.loads(response.text)["dataset"]
        
        parsed_data = parse_qs(download_data(dataset["filename"]))
        parsed_data['name'] = parsed_data['name'][0]
        return parsed_data

    def upload_dataset(self, dataset):
        dataset_hash = get_json_obj_hash(dataset.to_json())

        tag_response = requests.post(DATASET_BASE_URL + "/tag", json={
            'name': dataset.name,
            'hash': dataset_hash,
            'projectId': self.projectId,
        })
        if tag_response.status_code != 200:
            raise ValueError("Failed to get dataset tag")

        tag = json.loads(tag_response.text)["tag"]
        dataset_filename = self.projectId + "_" + tag + ".txt"
        upload_data(dataset_filename, dataset.to_json())

        dataset_response = requests.post(DATASET_BASE_URL, json={
            'filename': dataset_filename,
            'hash': dataset_hash,
            'name': dataset.name,
            'projectId': self.projectId,
            'tag': tag,
        })

        if dataset_response.status_code != 200: 
            raise ValueError("Failed to post dataset tag: {tag}")
        return tag


    def add_judge(self, judge):
        # Grab the source code and hash of scoring_rubric and passing_criteria
        scoring_source_code, judge_scoring_hash = get_source_code_hash(judge.scoring_rubric)
        passing_criteria_source_code, judge_passing_hash = get_source_code_hash(judge.passing_criteria)
        
        judge_tag_response = requests.post(JUDGE_BASE_URL + "/tag", json={
            'judge_passing_hash': judge_passing_hash,
            'judge_scoring_hash': judge_scoring_hash,
            'name': judge.name,
            'projectId': self.projectId,
        })
        
        if judge_tag_response.status_code != 200:
            raise ValueError("Failed to get judge tag")

        judgeTag = json.loads(judge_tag_response.text)["judgeTag"]

        scoring_filename = self.projectId + "_" + judgeTag + "_scoring.txt"
        upload_data(scoring_filename, scoring_source_code)


        passing_filename = self.projectId + "_" + judgeTag + "_passing.txt"
        upload_data(passing_filename, passing_criteria_source_code)

        response = requests.post(JUDGE_BASE_URL, json={
            'judge': json.dumps(judge.to_json()),
            'passing_code_filename': passing_filename,
            'passing_hash': judge_passing_hash,
            'projectId': self.projectId,
            'scoring_code_filename': scoring_filename,
            'scoring_hash': judge_scoring_hash,
            # 'data_size': scoring_source_data_size + passing_data_size,
            'tag': judgeTag,
        })

        if response.status_code == 201:
            body = json.loads(response.text)
            print("!!body: ", body)
            if body["isNew"]:
                print(f"✔ Judge {judgeTag} created.")
            else:
                print(f"✔ Judge {judgeTag} already exists.")
            
                for item in body["itemsUpdated"]:
                    print(f"✔ Judge {item['field']} field has been updated to: \"{item['value']}\"")
        
    def _get_judge_from_judge_tag(self, judge_tag):
        encoded_judge_tag = quote(judge_tag)
        judge_response = requests.get(JUDGE_BASE_URL + "/" + encoded_judge_tag + "/projects/" + self.projectId)
        if judge_response.status_code != 200:
            raise ValueError("Failed to get judge from judge tag")
        
        judge = json.loads(judge_response.text)["judge"]
        return judge

    def _get_scoring_rubric_func_from_judge(self, judge):
        scoring_source_code = download_data(judge["scoringCodeFilename"])
        return read_source_code_as_func(scoring_source_code, "scoring_rubric")


    def _get_passing_criteria_func_from_judge(self, judge):
        passing_source_code = download_data(judge["passingCodeFilename"])
        return read_source_code_as_func(passing_source_code, "passing_criteria")

    def evaluate_with(self, judge_tag):
        judge = self._get_judge_from_judge_tag(judge_tag)        

        def decorator(func):
            def wrapper(*args, **kwargs):
                dataset = self._download_dataset(judge["dataset_tag"])
                print("!!!dataset here: ", dataset)
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

                # Should this just be converted to using requests. import requests? 
                response = asyncio.run(post_data(EVALUATION_BASE_URL, json_data={
                    'scores': scores,
                    'judge_tag': judge["tag"],
                    'projectId': self.projectId,
                }))
                return func(*args, **kwargs)
            return wrapper
        return decorator


    # TODO: Modularize this
    def trace(self, func):
        def wrapper(*args, **kwargs):
            if self.error_code:
                return
            # print("args: ", args)
            # print("type(args[0]): ", type(args[0]))
            # print("kwargs: ", kwargs)
            params = inspect.signature(func).parameters
            # print("params: ", params)
            source_code = inspect.getsource(func)
            hasher = hashlib.sha256()
            hasher.update(source_code.encode('utf-8'))
            hash_digest = hasher.hexdigest()
            # print(f"Hash: {hash_digest}")

            start = time.perf_counter()
            result = func(*args, **kwargs)
            latency = time.perf_counter() - start

            # Save the source code to a file
            public_url, data_size = upload_text_to_firebase(source_code, hash_digest + '_code-snippet.txt')

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
            
            formatted_outputs = {
                'value': result,
                'type': type(result).__name__,
            }

            response = asyncio.run(post_data(RUN_BASE_URL, json_data={
                'codeSnippetUrl': public_url,
                'latency': latency,
                'projectId': self.projectId,
                'funcName': func.__name__,
                'codeHash': hash_digest,
                'inputs': formatted_args,
                'outputs': formatted_outputs,
                'dataSize': data_size,
            }))

            body = json.loads(response.text)
            if response.status_code == 201:
                print("✨ View run " + body["run"]["id"] + " at " + BASE_CLIENT_URL + "/workspace/" + body["workspaceId"] + "/project/" + self.projectId)
                return result
            else:    
                self.error_code = body["code"]
                print_error_message(self.error_code)

        return wrapper