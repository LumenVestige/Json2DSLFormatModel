def replace_last(source_string, old, new):
    parts = source_string.rsplit(old, 1)  # 从右侧分割一次
    return new.join(parts) if len(parts) > 1 else source_string  # 只有找到时才替换


def get_from_map(obj, key):
    for item_key in obj:
        if key == item_key:
            return obj[key]
    return ''
