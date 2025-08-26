"""
初始化程序。
"""

from config.constant import USER_SETTING_PATH

def store(action: str, username: str, password: str, channel: str) -> None:
    content = f'''"""
Some constants configured by the user themselves.
"""

# ACTION is the default behavior when running the program, which can be one of the following three:
# - "login"
# - "logout"
# - "shift"
ACTION = {action!r}

# USERNAME is the content filled in the "请输入用户名" box.
USERNAME = {username!r}

# PASSWORD is the content filled in the "请输入密码" box.
PASSWORD = {password!r}

# CHANNEL is the option to be selected on the "选择网络" panel, which can be one of the following four:
# - "校园网"
# - "中国移动"
# - "中国电信"
# - "中国联通"
CHANNEL = {channel!r}
'''
    with open(USER_SETTING_PATH, mode = "w", encoding = "utf-8") as file:
        file.write(content)


def initialize() -> None:
    print("初次见面，请先进行一些配置。\n")

    actions = {chr(ord("A") + i): value for (i, value) in enumerate(("登录", "登出", "转换"))}
    print('\t'.join(f'{choice}.{action}' for (choice, action) in actions.items()))
    action_choice = input("请选择进行的操作：")
    while action_choice.upper() not in actions:
        action_choice = input("输入有误，请重新选择操作：")
    action = actions[action_choice.upper()]
    print(f"您选择的操作是：{action}\n")
    action = {"登录": "login", "登出": "logout", "转换": "shift"}[action]

    username = input("请输入用户名：")
    while not username:
        username = input("用户名不能为空，请重新输入：")
    print(f"您的用户名是：{username}\n")

    password = input("请输入密码（明文显示，注意遮挡）：")
    while not password:
        password = input("密码不能为空，请重新输入：")
    print("")

    channels = {chr(ord("A") + i): value for (i, value) in enumerate(("校园网", "中国移动", "中国电信", "中国联通"))}
    print('\t'.join(f'{choice}.{channel.ljust(4)}' for (choice, channel) in channels.items()))
    channel_choice = input("请选择网络：")
    while channel_choice.upper() not in channels:
        channel_choice = input("输入有误，请重新选择网络：")
    channel = channels[channel_choice.upper()]
    print(f"您选择的网络是：{channel}\n")

    storages = {"Y": True, "N": False}
    storage_choice = input(f"是否存储本次配置（{'/'.join(storages)}）？")
    while storage_choice.upper() not in storages:
        storage_choice = input("输入有误，输入：")
    storage = storages[storage_choice.upper()]

    result = (action, username, password, channel)
    if storage:
        store(*result)

    return result


if __name__ == "__main__":
    initialize()
