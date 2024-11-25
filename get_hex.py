from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def get_hexes(url):
    # 使用 Playwright 的上下文管理器启动浏览器
    with sync_playwright() as p:
        # 启动 Firefox 浏览器
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()

        # 设置自定义的请求头，默认已经模拟浏览器了，可以不用手动设置
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"
        })

        # 打开目标网页
        page.goto(url)

        # 等待页面加载完成
        page.wait_for_timeout(5000)  # 等待5秒以确保所有内容加载完成

        # 获取页面内容
        content = page.content()

        # 关闭浏览器
        browser.close()

        # 用 BeautifulSoup 解析页面内容
        soup = BeautifulSoup(content, 'html.parser')

        # 返回所有的海克斯
        all_hex = soup.find_all('div', attrs={'class': 'pl-[6px] font-roboto font-normal truncate'})

        return all_hex


def print_hex(url):
    hexes = get_hexes(url)

    count_hex = 0

    for hex in hexes:
        print(hex.text, end=' ')
        count_hex += 1
        print(count_hex, end=' ')
        print()
