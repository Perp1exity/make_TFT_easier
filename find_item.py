import get_list as glist


def find_item_in_list(cache_list, hex_name):
    """在缓存列表中查找包含指定名称的条目"""
    # 使用列表推导式筛选出包含 hex_name 的条目
    matching_item = [item for item in cache_list if hex_name in item]

    return matching_item


def print_item():
    my_url = 'https://tactics.tools/zh/augments'  # 替换为你的目标网页
    my_cache_list = glist.get_list()  # 得到缓存列表
    name_to_find = "咖啡甜心之徽"
    found_item = find_item_in_list(my_cache_list, name_to_find)

    print(found_item)
