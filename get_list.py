import get_hex as ghex
import get_rank as grank
import os
import json


# 默认缓存列表文件名cache_list.json，在get_list(url, div_selector)中可修改


def save_cache_to_file(filename, cache_list):
    """将缓存列表保存到本地文件"""
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(cache_list, file, ensure_ascii=False, indent=4)


def load_cache_from_file(filename):
    """从本地文件加载缓存列表"""
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []


def make_cache_list(url):
    """生成缓存列表"""
    filename = 'cache_list.json'  # 使用变量来指定文件名
    hexes = ghex.get_hexes(url)
    ranks = grank.get_ranks_during_scroll(url)

    count_num = 0
    step = 3  # 每个 hex 后面跟随 3 个 rank
    output_list = []  # 初始化一个空列表来存储格式化的字符串

    # 遍历 hexes 列表中的每个 item
    for i, item in enumerate(hexes):
        # 从 ranks 列表中提取三个元素
        ranks_for_hex = ranks[i * step: (i + 1) * step]

        # 获取 ranks 的文本
        rank_texts = [rank.text for rank in ranks_for_hex]

        # 更新计数器
        count_num += 1

        # 格式化字符串
        formatted_output = f"{count_num}:{item.text} {'  '.join(rank_texts)}"
        # ' '.join(rank_texts): ' '，这是用来连接字符串的分隔符，空格在这个例子中用于分隔每个 rank_texts 元素。

        # 添加到 cache_list
        output_list.append(formatted_output)

    save_cache_to_file(filename, output_list)

    return output_list


def get_list():
    """获取列表，如果获取失败则使用缓存"""
    filename = 'cache_list.json'  # 使用变量来指定文件名

    # 我们只在软件运行时获取一遍最新数据，存入缓存，后续读取数据只读缓存数据，每次重新运行软件更新一次数据
    # try:
    #     # 尝试获取新列表
    #     return make_cache_list(url, filename)
    # except Exception as e:
    #     print(f"获取新列表失败: {e}")

    # 读取缓存列表
    return load_cache_from_file(filename)


def print_list():
    my_url = 'https://tactics.tools/zh/augments'  # 替换为你的目标网页
    make_cache_list(my_url)
    my_cache_list = get_list()  # 创建缓存列表
    # my_cache_list = load_cache_from_file('cache_list.json')  # 从缓存读

    # 打印 cache_list 内容
    for line in my_cache_list:
        print(line)


print_list()
