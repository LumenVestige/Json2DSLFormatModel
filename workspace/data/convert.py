import json
import re
import string

from bs4 import BeautifulSoup, TemplateString

from utils.string_utils import replace_last, get_from_map
from utils.text_utils import text_is_empty

style_mapping = {
    'flex-direction': 'f_d',
    'flex-wrap': 'f_w',
    'align-items': 'a_i',
    'text-align': 't_a',
    'display': 'd',
    'justify-content': 'j_c',
    'border-radius': 'b_r',
    'flex': 'flex',
    'flex-grow': 'f_g',
    'flex-shrink': 'f_s',

}
style_mapping_reverse = {value: key for key, value in style_mapping.items()}


def get_support_compress_style_value(value: string):
    value = value.strip()
    if text_is_empty(value):
        return ''
    sub_values = value.split(';')
    res = ''
    for item in sub_values:
        sub_items = item.split(':')
        if len(sub_items) != 2:
            # print('1skip:' + item)
            continue
        sub_key = sub_items[0].strip()
        sub_value = sub_items[1].strip()
        c_sub_key = ""
        for key in style_mapping:
            if key == sub_key:
                c_sub_key = style_mapping[key]
        if text_is_empty(c_sub_key) is False:
            res += c_sub_key + ':' + sub_value + ';'
            continue
        print('skip:' + item)
    return res


extra_attrs_mapping = {
    'style': 's',
    'v-for': 'for',
    'v-if': 'if',
    'v-else-if': 'e_if',
    'v-else-else': 'else',
    'src': 'src',
    'href': 'l',
    'key': 'k'

}
extra_attrs_re_mapping = {value: key for key, value in extra_attrs_mapping.items()}


def get_support_compress_attr(key, value):
    key = key.strip().replace(':', '')
    try:
        value = value.strip()
        if key == 'style':
            style = get_support_compress_style_value(value)
            if len(style) == 0:
                print('skip style:' + key + ' ' + value)
                return ''
            return 's' + '=' + style
        c_sub_key = ''
        for temp in extra_attrs_mapping:
            if temp == key:
                c_sub_key = extra_attrs_mapping[key]
                break
        if text_is_empty(c_sub_key) is False:
            return c_sub_key + '=' + value
        print('==>skip attr:' + key + ' ' + value)
    except Exception as e:
        print(e)
        return ''
    return ''


def get_support_compress_attrs(attrs):
    if len(attrs) == 0:
        return ''
    res = ''

    for key in attrs:
        attr = get_support_compress_attr(key, attrs[key]).strip()
        if len(attrs) <= 1:
            continue
        if len(res) != 0 and (res.endswith('@') is False):
            res += '@'
        res += attr
    if res.endswith('@'):
        return replace_last(res, '@', '')
    else:
        return res


def d_compress_attrs(compress_attrs):
    if len(compress_attrs) == 0:
        return ''
    items = compress_attrs.split('@')
    att_str = ''
    for item in items:
        tmps = item.split('=')
        if len(tmps) != 2:
            continue
        attr_key = tmps[0]
        attr_value = tmps[1]
        d_attr_key = get_from_map(extra_attrs_re_mapping, attr_key)
        if d_attr_key == '':
            continue
        # style 类型
        if attr_key == 's':
            tmps = attr_value.split(';')
            s_res = ''
            for tmp in tmps:
                styles = tmp.split(':')
                if len(styles) != 2:
                    continue
                style_key = styles[0]
                style_value = styles[1]
                d_style = get_from_map(style_mapping_reverse, style_key)
                if d_style == '':
                    continue
                s_res += (d_style + ':' + style_value + ';')
            att_str += (d_attr_key + '=' + s_res)
        else:
            att_str += (d_attr_key + '=' + attr_value)
        att_str += '@'

    return att_str


def is_h_tag(tag):
    return tag == 'h1' or tag == 'h2' or tag == 'h3' or tag == 'h4' or tag == 'h5' or tag == 'h6'


def is_div_tag(tag):
    return tag == 'div' or tag == 'dl' or tag == 'dt' or tag == 'dd'


div_compress_tag = 'd'


# ud dsl 输出转码
def is_title(tag):
    return is_h_tag(tag)


def is_paragraph_tag(tag):
    return tag == 'p'


def is_block_tag(tag):
    return tag == 'block' or tag == 'span' or tag == 'audio' or tag == 'blockquote' or tag == 'article' or tag == 'section'


def is_flex(tag):
    return is_div_tag(tag)


def is_img_tag(tag):
    return tag == 'img'


def is_video_tag(tag):
    return tag == 'video'


def is_media_tag(tag):
    return tag == 'source'


def is_text(tag):
    return tag == 'pre' or tag == 'textarea' or tag == 'label' or tag == 'code'


def is_bold_text(tag):
    return tag == 'strong' or tag == 'b' or tag == 'em'


def is_small_text(tag):
    return tag == 'small'


def is_italic_text(tag):
    return tag == 'i'


def is_link_tag(tag):
    return tag == 'a'


def is_list(tag):
    return tag == 'ul' or tag == 'ol'


def is_list_item(tag):
    return tag == 'li'


def is_address(tag):
    return tag == 'address'


tag_mapping = {
    "img": "im",
    "span": "sp",
    "p": "p",
    "strong": "st",
    "video": "v",
    "a": "a",
    "ul": "ul",
    "ol": "ol",
    "li": "li",
    "pre": "pr",
    "small": "small",
    "audio": "au",
    "textarea": "tt",
    "label": "la",
    "i": "i",
    "b": "b",
    "blockquote": "bq",
    "article": "at",
    "source": "sr",
    "code": "code",
    "em": "em",
    "address": "ad",
    "section": "se"
}

tag_mapping_reverse = {value: key for key, value in tag_mapping.items()}
tag_mapping_reverse['d'] = 'div'


# not_support_tags = set()
def get_support_compress_tag(tag):
    if text_is_empty(tag):
        return ''
    tag = tag.strip()
    if is_h_tag(tag):
        return tag
    if is_div_tag(tag):
        return div_compress_tag
    for key in tag_mapping:
        if key == tag:
            return tag_mapping[tag]
    if hasattr(tag_mapping, tag):
        return tag_mapping[tag]
    # print('=============not support tag===>:' + tag)
    # not_support_tags.add(tag)
    return ''


def get_text(text):
    if text_is_empty(text):
        return ''
    matches = re.findall(r"{{.*?}}", text)
    if len(matches) > 0:
        return matches[0].replace(' ', '')
    else:
        return ''


def is_container_compress_tag(compress_tag):
    return compress_tag == 'd' or compress_tag == 'p' or compress_tag == 'sp'


def depth_first_traversal(node):
    root_node = {}
    tag = get_support_compress_tag(node.name)
    if len(tag) == 0:
        return root_node
    root_node['t'] = tag
    attrs = get_support_compress_attrs(node.attrs)
    if len(attrs) > 0:
        root_node['a'] = attrs
    elif is_div_tag(node.name) is True:
        root_node['a'] = 's=d:block'

    text = node.string
    if text_is_empty(text) is True:
        text_contents = [str(child) for child in node.contents if isinstance(child, TemplateString)]
        text = ''.join(text_contents)

    value = get_text(text)
    if len(value) > 0:
        root_node['v'] = value
    children = []
    for child in node.children:
        if child.name:
            tmp = depth_first_traversal(child)
            if len(tmp) > 0:
                children.append(tmp)
    if len(children) > 0:
        root_node["c"] = children
    # check node is valid
    if len(root_node) == 1:
        return {}
    # print(len(root_node), root_node)
    if set(root_node.keys()) == {'t', 'a'} and (
            root_node['a'] == 's=d:block' or is_container_compress_tag(root_node['t'])):
        return {}
    return root_node


def d_compress_traverse_json(obj):
    node = {}
    if isinstance(obj, dict):
        # 如果是字典，遍历所有键值对
        for key, value in obj.items():
            if key == 't':
                if is_h_tag(value):
                    tag = value
                else:
                    tag = get_from_map(tag_mapping_reverse, value)
                if len(tag) == 0:
                    continue
                node[key] = tag
                continue
            if key == 'a':
                node[key] = d_compress_attrs(value)
                continue
            if key == 'v':
                node[key] = value
                continue
            if key == 'c':
                node[key] = d_compress_traverse_json(value)
                continue
            node['node'] = d_compress_traverse_json(value)
            # raise Exception("unknown key", key)
        if get_from_map(node, 'node') != '':
            return node['node']
        return node
    elif isinstance(obj, list):
        array = []
        for item in obj:
            array.append(d_compress_traverse_json(item))
        return array
    else:
        return obj


def convert_tree_2_ui_dsl(d_compress_tree):
    node = {'type': '',
            'for': {},
            'if': {},
            'else-if': {},
            'else': {},
            'props': {}}
    obj = d_compress_tree
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == 't':
                tag = value
                key = 'type'
                if is_title(tag):
                    node[key] = 'title'
                    continue
                if is_paragraph_tag(tag):
                    node[key] = 'paragraph'
                    continue

                if is_block_tag(tag):
                    node[key] = 'block'
                    continue

                if is_flex(tag):
                    node[key] = 'flex'
                    continue

                if is_img_tag(tag):
                    node[key] = 'img'
                    continue

                if is_video_tag(tag):
                    node[key] = 'video'
                    continue

                if is_media_tag(tag):
                    node[key] = 'media'
                    continue

                if is_text(tag):
                    node[key] = 'text'
                    continue

                if is_bold_text(tag):
                    node[key] = 'bold_text'
                    continue

                if is_small_text(tag):
                    node[key] = 'small_text'
                    continue

                if is_italic_text(tag):
                    node[key] = 'italic_text'
                    continue

                if is_link_tag(tag):
                    node[key] = 'link'
                    continue

                if is_list(tag):
                    node[key] = 'list'
                    continue

                if is_list_item(tag):
                    node[key] = 'li_item'
                    continue

                if is_address(tag):
                    node[key] = 'address'
                    continue
                continue
            if key == 'a':
                if len(value) == 0:
                    continue
                items = value.split('@')
                for item in items:
                    tmps = item.split('=')
                    if len(tmps) != 2:
                        continue
                    attr_key = tmps[0]
                    attr_value = tmps[1]
                    if attr_key == '':
                        continue
                    # style 类型
                    if attr_key == 'style':
                        tmps = attr_value.split(';')
                        s_res = ''
                        for tmp in tmps:
                            styles = tmp.split(':')
                            if len(styles) != 2:
                                continue

                            style_key = styles[0]
                            style_value = styles[1]
                            if text_is_empty(style_key) or text_is_empty(style_value):
                                continue
                            if style_key == 'display' and style_value == 'block':
                                node['type'] = 'block'
                                continue
                            if style_key.startswith('flex'):
                                node['props'][style_key] = style_value
                                node['type'] = 'flex'
                                continue
                            if style_key == 'justify-content':
                                node['props']['flex-' + style_key] = style_value
                                node['type'] = 'flex'
                                continue
                            if style_key == 'align-items':
                                node['props']['flex-' + style_key] = style_value
                                node['type'] = 'flex'
                                continue
                            if style_key == 'border-radius':
                                if node['type'] == 'flex' or node['type'] == 'block':
                                    node['type'] = 'card'
                                    node['props'][style_key] = style_value
                                if node['type'] == 'img':
                                    node['type'] = 'radian_img'
                                    node['props'][style_key] = style_value
                                continue

                    if attr_key == 'v-for':
                        node['for'] = attr_value
                        continue
                    # if attr_key == 'key':
                    #     node['props'][attr_key] = attr_value
                    if attr_key == 'v-if':
                        node['if'] = attr_value
                        continue
                    if attr_key == 'v-else-if':
                        node['else-if'] = attr_value
                        continue
                    if attr_key == 'v-else-else':
                        node['else'] = attr_value
                        continue
                    if attr_key == 'src' or attr_key == 'href':
                        if attr_value.startswith('url_request-'):
                            node['props'][attr_key] = attr_value.replace('url_request-', 'https://')
                        else:
                            if 'image' in attr_value.lower():
                                node['type'] = 'img'
                                node['props']['src'] = '{{' + attr_value + '}}'
                            else:
                                node['props'][attr_key] = '{{' + attr_value + '}}'

                        continue
                # node[key] = create_ui_dsl(value)
                continue
            if key == 'v':
                node['props']['content'] = value
                continue
            if key == 'c':
                node['children'] = convert_tree_2_ui_dsl(value)
                continue
            # raise Exception("unknown key", key)

        if node['type'] == 'block' and get_from_map(node['props'], 'content') != '' and get_from_map(node,
                                                                                                     'children') == '':
            node['type'] = 'text'

        if len(node['for']) == 0:
            del node['for']
        if len(node['else-if']) == 0:
            del node['else-if']
        if len(node['if']) == 0:
            del node['if']
        if len(node['else']) == 0:
            del node['else']
        if len(node['props']) == 0:
            del node['props']

        return node
    elif isinstance(obj, list):
        array = []
        for item in obj:
            array.append(convert_tree_2_ui_dsl(item))
        return array
    else:
        return obj
