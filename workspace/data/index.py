import json
import os

from bs4 import BeautifulSoup

from data.convert import depth_first_traversal, d_compress_traverse_json, convert_tree_2_ui_dsl
from half_json.core import JSONFixer

jsonFixer = JSONFixer()


def create_dsl(file_path):
    print('dsl parser:' + file_path)
    with open(file_path, "r", encoding="utf-8") as vue_file:
        text = vue_file.read()
    soup = BeautifulSoup(text, 'html.parser')
    root_node = soup.find('div')
    # print(file_path)
    # print(not_support_tags)
    return depth_first_traversal(root_node)


def d_compress_tree(compress_json_str):
    try:
        json_obj = json.loads(compress_json_str)
        return d_compress_traverse_json(json_obj)
    except Exception as e:
        print(e, "json parse error,try fix: ")
        res = jsonFixer.fix(compress_json_str)
        if res.success:
            print('fix success')
            compress_json_str = res.line
            return d_compress_traverse_json(json.loads(compress_json_str))
        else:
            print('fix fail')
            raise Exception("json parse error")


def create_ui_dsl(d_compress_tree_obj):
    return convert_tree_2_ui_dsl(d_compress_tree_obj)


def get_random_jsons():
    with open(f'{os.path.dirname(__file__)}/random_json/random_data.json', "r", encoding="utf-8") as r_file:
        json_str = r_file.read()
    return json.loads(json_str)
