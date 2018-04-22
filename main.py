from account_inc import inc
import line_bot_api
import sys
import datetime
import atexit


def main(argv):
    line_app = line_bot_api.line(webdriver_path=inc[argv]["webdriver_path"],
                                 Line_Crx_Path=inc[argv]["Line_Crx_Path"],
                                 user_data_dir=inc[argv]["user_data_dir"],
                                 show_window=inc[argv]["show_window"])
    atexit.register(line_app.close)
    print("start to login")
    ret, msg = line_app.login(username=inc[argv]["acc"], password=inc[argv]["pwd"])
    if not ret:
        # TODO:
        #   login error process
        return False, "login error"
    if msg is not None:
        # TODO:
        #   login code process
        return False, msg
    print("start to select_chat_layer")
    if not line_app.select_chat_layer(inc[argv]["layer"]):
        # TODO:
        #   not exist layer type process
        return False, "not exist layer"
    print("start to select_chat")
    if not line_app.select_chat(chat_name=inc[argv]["chat"], auto_get_msg=False):
        # TODO:
        #   not exist chat name process
        return False, "not exist chat"
    print("start to is_occur_time")
    line_app.set_network_delay(1)
    if is_occur_time(argv):
        i = 0
        while not line_app.send_msg(content=inc[argv]["send"]["content"],
                                    data_sticker_pkg_id=inc[argv]["send"]["sticker_pkg"],
                                    type=inc[argv]["send"]["type"]):
            print("is_occur_time worse %d times." % i + 1)
            if i == 3:
                return False, "Send msg error"
            i += 1
        print("start to stop")
    else:
        return False, "Not match the occur condition"
    return True, None


# check the occur condition.
def is_occur_time(argv):
    return inc[argv]["start_time"] < datetime.datetime.now().time() < inc[argv]["stop_time"]


if __name__ == "__main__":
    start = datetime.datetime.now().timestamp()
    for i in sys.argv[1:]:
        try:
            ret, msg = main(i)
            if not ret:
                print(msg)
        except KeyboardInterrupt:
            # TODO:
            #   unknown error process
            print("When doing %s happened unknow error." % i)
        print("cost [%s]:" % i, datetime.datetime.now().timestamp() - start)
