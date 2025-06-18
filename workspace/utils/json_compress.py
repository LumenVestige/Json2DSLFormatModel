import json


def replace_values(obj):
    # 判断类型是字典时遍历其键值对
    if isinstance(obj, dict):
        return {key: replace_values(value) for key, value in obj.items()}
    # 判断类型是列表时遍历其每一个元素
    elif isinstance(obj, list):
        return [replace_values(item) for item in obj]
    # 替换值为 "string_" 加上值的长度
    elif isinstance(obj, str):
        return f"s_{len(obj)}"
    # 如果是其他数据类型，直接转换为字符串并替换
    else:
        return f"s_{len(str(obj))}"


def compress_json(json_obj, mapping=True):
    if mapping:
        json_str = str(json.dumps(replace_values(json_obj), ensure_ascii=False, indent=0))
    else:
        json_str = str(json.dumps(json_obj, ensure_ascii=False, indent=0))

    json_lines = json_str.split("\n")
    compress_json_string = ""
    tmp = []

    for item in json_lines:
        strip_line = item.strip()
        is_need_skip_tag = True
        for char in item:
            if is_need_skip(char) is False:
                is_need_skip_tag = False
                break
        if is_need_skip_tag is True and len(tmp) > 0 and tmp[- 1]["compress_able"] is True:
            tmp[- 1]["line_br"] = False
        tmp.append({
            "line": strip_line,
            "line_br": True,
            "compress_able": is_need_skip_tag
        })
    for item in tmp:
        compress_json_string += item["line"]
        if item["line_br"]:
            compress_json_string += "\n"
    return compress_json_string


def is_need_skip(char):
    if char == '{' or char == '}' or char == '[' or char == ']' or char == ':' or char == ',':
        return True
    return False


def flatten_json(data, parent_key=''):
    if isinstance(data, dict):
        for key, value in data.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            flatten_json(value, new_key)  # 递归调用处理嵌套字典
    elif isinstance(data, list):
        for index, item in enumerate(data):
            new_key = f"{parent_key}"
            flatten_json(item, new_key)  # 递归调用处理嵌套列表
    else:
        # 非字典或列表的叶子节点打印路径和对应值
        print(f"{parent_key} = {data}")
