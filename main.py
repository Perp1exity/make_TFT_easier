import get_list as glist
#import pop_up_window as pop
import pop_new as pop
import record_date as rdate


my_url = 'https://tactics.tools/zh/augments'  # 替换为你的目标网页

# 在程序开始调用make_cache_list(url, filename)，生成或更新cache_list，后续只读缓存
# 在程序开始时检查是否需要运行make_cache_list
if not rdate.has_run_today():
    print("这是今天第一次运行本程序，更新海克斯排名。")
    glist.make_cache_list(my_url)
    rdate.update_run_date()
else:
    print("今天已经运行过，跳过更新。")

# 创建图标和窗口
pop.create_icon_and_windows()
