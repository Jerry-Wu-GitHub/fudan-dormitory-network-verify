import os
import sys

from src.install_prerequsites import install_prerequsites
install_prerequsites()

if not (os.path.isdir("./config") and os.path.isfile("./config/constant.py")):
    print("未找到 ./config/constants.py 文件，请重新下载！")
    input("【按下「回车键」退出】")

from config.constant import USER_SETTING_PATH

args = sys.argv
if len(args) < 5:
    if not os.path.isfile(USER_SETTING_PATH):
        from src.initialize import initialize
        args += initialize()[len(args) - 1:]
    else:
        import importlib.util
        from pathlib import Path

        def load_module_from_path(module_name: str, file_path: str):
            file_path = Path(file_path).resolve()
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        
        user_settings = load_module_from_path("user_settings", USER_SETTING_PATH)
        if len(args) < 2:
            args.append(user_settings.ACTION)
        if len(args) < 3:
            args.append(user_settings.USERNAME)
        if len(args) < 4:
            args.append(user_settings.PASSWORD)
        if len(args) < 5:
            args.append(user_settings.CHANNEL)

from src.account import Account, ChannelError, LoginError


def main(*args) -> None:
    action = args[0]
    if not (action in ("login", "logout", "shift")):
        print(f'The first parameter should be "login", "logout", "shift" or "auto", but got {action!r}')

    account = Account(args[1], args[2], args[3])
    action = {
        "off": "login",
        "on": "logout"
    }[account.user_online_state] if (action == "shift") else action

    try:
        {
            "login": account.login,
            "logout": account.logout,
        }[action]()
    except (ChannelError, LoginError) as error:
        print(error)


try:
    main(*args[1:])
except Exception as error:
    print(f"Unknown error occurred during runtime: {error.__class__.__name__}: {str(error)}")
    input("Please provide timely feedback to the developer 24300240141@m.fudan.edu.cn . Thank you! Press the 'Enter' key to exit")
