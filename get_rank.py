from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re


def get_page_height(style_attr):
    # 从style属性中提取高度
    match = re.search(r'height:\s*(\d+)px', style_attr)
    if match:
        return int(match.group(1))
    return 0


def get_ranks_during_scroll(url):
    div_selector = '#tbl-body'  # 替换为你的目标div选择器

    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True)  # 使用headless=False可以看到浏览器窗口
        page = browser.new_page()

        # 访问目标网页
        page.goto(url)

        # 等待目标元素加载
        page.wait_for_selector(div_selector)

        # 获取目标div的style属性
        style_attr = page.evaluate(f'document.querySelector("{div_selector}").getAttribute("style")')
        # print(style_attr)

        # 从style属性中获取高度
        page_height = get_page_height(style_attr)
        # print(div_height)
        next_height = 0

        # 设置滚动步长与初始高度
        scroll_step = 460
        current_height = 0

        # 记录一个节点，此节点之前的海克斯style没“；”，之后的有
        note = 12

        all_rank = []

        while current_height < page_height:
            # 滚动页面
            page.evaluate(f'window.scrollTo(0, {current_height})')
            current_height += scroll_step

            # 等待一段时间，确保页面加载
            page.wait_for_timeout(1000)

            # 获取目标div的HTML内容
            content = page.inner_html(div_selector)
            # print(content)

            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(content, 'html.parser')

            while next_height < current_height and next_height < page_height:
                if note > 0:
                    # 定义要匹配的 style 属性值
                    style_value = (f"position:absolute;top:0;left:0;min-width:740px;width:100%;height:46px;transform"
                                   f":translateY({next_height}px)")
                    note -= 1
                else:
                    style_value = (f"position: absolute; top: 0px; left: 0px; min-width: 740px; width: 100%; height: "
                                   f"46px; transform: translateY({next_height}px);")

                # 使用正则表达式匹配 style 属性
                pattern = re.compile(re.escape(style_value))

                # 在content中查找所有含有 style 属性的元素：一行行排名数据
                rows_with_style = soup.find(style=pattern)

                ranks_in_row = rows_with_style.find_all('div', attrs={
                    'class': 'flex items-center justify-end px-[14px] css-1puwvti tbl-cell-right-border'})

                # 将获取的元素添加到列表中
                all_rank.extend(ranks_in_row)

                next_height += 46

        # 关闭浏览器
        browser.close()

        return all_rank


def print_rank(url):
    # 调用函数并打印结果
    ranks = get_ranks_during_scroll(url)

    # 初始化计数器
    count = 0
    num_hex = 0

    # 提取并打印每个元素中的文本
    for rank in ranks:
        # 打印元素的文本
        print(rank.text, end=' ')

        # 增加计数器
        count += 1

        # 每三个元素输出一个新行
        if count % 3 == 0:
            num_hex += 1
            print(num_hex, end=' ')
            print()  # 打印换行符

    # 如果元素总数不是3的倍数，最后一行也要换行
    if count % 3 != 0:
        print()


# 有可能会说加载失败，写程序的时候直接循环至成功
# 用缓存解决上述问题
