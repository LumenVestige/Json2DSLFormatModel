import os
import time

import torch

import json

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from data.index import d_compress_tree, create_ui_dsl
from utils.common_utils import get_cost_time
from utils.json_compress import compress_json
from utils.string_utils import get_from_map

os.environ["TOKENIZERS_PARALLELISM"] = "false"
device = "cuda" if torch.cuda.is_available() else "cpu"
print('device:', device)
token = "100861991jksdhdfsh_sju445jhdfsjd_009skdj--yyusd"
ws_token = "jkasdhjkahdjkahsjk"
dsl_path = "/dsl_wwqqok_0093/llsdjkj_0092/ggg"

model_service_local_host = "http://127.0.1.1:9791"
model_service_host = ""
model_monitor_host = ""


class DSLModel:
    def __init__(self, tokenizer, model):
        self.tokenizer = tokenizer
        self.model = model

    def get_model_result(self, json_data):
        time1 = time.time()
        prompt = create_prompt(json_data)
        input_ids = self.tokenizer.encode(prompt, return_tensors='pt',
                                          padding='max_length',
                                          max_length=1024,
                                          truncation=True).to(device)
        print("===========================================")
        with torch.no_grad():
            outputs = self.model.generate(input_ids, max_length=2048)
            outputs_token_len = len(outputs[0])
        output = self.tokenizer.decode(outputs[0], skip_special_tokens=True).replace('ui dsl:', '')
        output_len = len(output)
        cost_time = get_cost_time(time1)
        try:
            result = json.loads(output)
            return {"isJson": True, "costTime": cost_time, "len": output_len, "token_len": outputs_token_len,
                    "result": json.dumps(result, ensure_ascii=False)}
        except:
            return {"isJson": False, "costTime": cost_time, "len": output_len, "token_len": outputs_token_len,
                    "result": output}

    def get_result(self, json_data):
        module_result = self.get_model_result(json_data)
        compress_json_str = module_result['result']
        print('compress_json_str:', compress_json_str)
        d_res = d_compress_tree(compress_json_str)
        dsl = create_ui_dsl(d_res)
        root_children = get_from_map(dsl, 'children')
        if root_children != '' and len(root_children) == 1:
            return {"dsl": root_children[0]}
        return {"dsl": dsl}


def create_prompt(json_str):
    try:
        json_obj = json.loads(json_str)
        compress_json_str = compress_json(json_obj)
        prompt = 'convert to ui dsl from json data:\n' + compress_json_str
        # print(len(prompt), prompt)
        return prompt
    except Exception as e:
        print(e, json_str)
        return ''


def create_eval_model(checkpoint) -> DSLModel:
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint).to(device)
    # 设置模型为评估模式
    model.eval()
    return DSLModel(tokenizer, model)


def create_reasoning_eval_model() -> DSLModel:
    return create_eval_model(f'{os.path.dirname(__file__)}/model')



def get_server_config():
    return {"token": token, "dslPath": dsl_path}


def create_model_server_request(json_data):
    # return {"url": f"http://{bridge_host}:9791" + dsl_path,
    #         "form": {"data": json_data, "__key": token}}
    # return {"url": f"{model_service_host}" + dsl_path,
    #         "form": {"data": json_data, "__key": token}}
    return create_model_local_server_request(json_data)


def create_model_local_server_request(json_data):
    # return {"url": f"http://{bridge_host}:9791" + dsl_path,
    #         "form": {"data": json_data, "__key": token}}
    return {"url": f"{model_service_local_host}" + dsl_path,
            "form": {"data": json_data, "__key": token}}
