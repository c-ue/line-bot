import datetime

inc = {
    "test1": {
        "acc": "aa@gmail.com",
        "pwd": "aa",
        "webdriver_path": "",
        "Line_Crx_Path": "",
        "user_data_dir": "./Default",
        "show_window": False,
        "layer": "Groups",
        "chat": "group name",
        "send": {"type": "text", "sticker_pkg": "", "content": "hello world"},
        "start_time": datetime.time(hour=0, minute=0, second=0),
        "stop_time": datetime.time(hour=0, minute=30, second=0)
    },
    "test2": {
        "acc": "aa@gmail.com",
        "pwd": "aa",
        "webdriver_path": "",
        "Line_Crx_Path": "",
        "user_data_dir": "./Default",
        "show_window": True,
        "layer": "Friends",
        "chat": "friend name",
        "send": {"type": "sticker", "sticker_pkg": "1", "content": "2"},
        "start_time": datetime.datetime.now().time(),
        "stop_time": (datetime.datetime.now() + datetime.timedelta(minutes=30)).time()
    },
}
