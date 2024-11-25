import tkinter as tk
from tkinter import PhotoImage
import identify_hex as ihex


def create_icon_and_windows():
    scaling_factor = 0.8  # 125% 缩放因子
    root = tk.Tk()

    # 设置任务栏图标
    try:
        icon = PhotoImage(file="icon.png")  # 确保有一个图像文件名为 icon.png
        root.iconphoto(False, icon)
    except tk.TclError:
        print("无法加载图标文件，请检查文件路径和格式。")
        return

    root.title("Hex Viewer")  # 设置窗口标题
    root.geometry("1x1")  # 设置一个不可见的小窗口用于任务栏图标
    root.withdraw()  # 隐藏主窗口

    # 创建图标窗口
    icon_window = tk.Toplevel(root)
    icon_width = int(95 * scaling_factor)
    icon_height = int(95 * scaling_factor)
    icon_x = int(1319 * scaling_factor)
    icon_y = int(0 * scaling_factor)
    icon_window.geometry(f"{icon_width}x{icon_height}+{icon_x}+{icon_y}")
    icon_window.attributes("-topmost", True)  # 确保窗口总在最上层
    icon_window.overrideredirect(True)  # 去掉顶部栏

    # 加载图标
    try:
        icon_label_image = PhotoImage(file="icon.png")  # 确保有一个图像文件名为 icon.png
    except tk.TclError:
        print("无法加载图标文件，请检查文件路径和格式。")
        return

    icon_label = tk.Label(icon_window, image=icon_label_image, bg='#f0f0f0', relief="raised")
    icon_label.image = icon_label_image
    icon_label.pack(fill='both', expand=True)

    # 创建三个消息窗口
    message1 = ihex.identify_hexes(1)
    message2 = ihex.identify_hexes(2)
    message3 = ihex.identify_hexes(3)
    windows_labels = create_message_windows(root, scaling_factor, message1, message2, message3)

    def toggle_windows(event):
        if any(win.state() == 'normal' for win, _ in windows_labels):
            # 如果有窗口是正常显示的，则隐藏所有窗口
            for win, _ in windows_labels:
                win.withdraw()
            update_messages(windows_labels)  # 更新
        else:
            # 如果所有窗口都是隐藏状态，则恢复所有窗口
            for win, _ in windows_labels:
                win.deiconify()

    # 绑定点击事件
    icon_label.bind("<Button-1>", toggle_windows)

    # 确保图标窗口显示在最上层
    icon_window.lift()

    root.deiconify()  # 显示主窗口以使其在任务栏显示图标
    root.mainloop()


def create_message_windows(root, scaling_factor, message1, message2, message3):
    messages = [message1, message2, message3]
    positions = [(415, 210), (820, 210), (1225, 210)]
    windows_labels = []

    for message, position in zip(messages, positions):
        win = tk.Toplevel(root)
        win_x = int(position[0] * scaling_factor)
        win_y = int(position[1] * scaling_factor)
        win.geometry(f"+{win_x}+{win_y}")
        win.attributes("-topmost", True)  # 始终在最上层
        win.overrideredirect(True)  # 去掉顶部栏

        try:
            # 将 message 列表中的内容合并为带换行的字符串
            message_text = "\n".join(message)
        except (TypeError, AttributeError):
            message_text = "未识别到海克斯"

        # 创建标签并添加到窗口中
        label = tk.Label(win, text=message_text, padx=10, pady=10, bg='#f0f0f0', wraplength=250)
        label.pack(expand=True, fill='both')

        win.withdraw()  # 初始时隐藏消息窗口
        windows_labels.append((win, label))

    return windows_labels


def update_messages(windows_labels):
    messages = [ihex.identify_hexes(1), ihex.identify_hexes(2), ihex.identify_hexes(3)]

    for (win, label), message in zip(windows_labels, messages):
        try:
            # 将 message 列表中的内容合并为带换行的字符串
            message_text = "\n".join(message)
        except (TypeError, AttributeError):
            message_text = "更新失败"

        # 更新标签内容
        label.config(text=message_text)
