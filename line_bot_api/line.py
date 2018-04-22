# TODO:
#   use beautifulsoup to faster
#   only use java to scroll to top or bottom not python loop
#   mix too scroll(left side and right side)
import time
import pathlib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class line:
    """Line chat bot api
        use to inital the line api.
        Line version 2.1.3.
        chrome-extension://mbopgmdnpcbohhpnfglgohlbhfongabi/
    """
    _item_ = None
    _str_ = None
    _engine_ = None
    _chat_list = None
    _current_chat = None
    _current_layer = None
    _msg_list = None
    _sticker_list = None
    _layer_list = None
    _default_implicitly_wait = 30
    _min_implicitly_wait = 3
    _network_delay = 0.05
    _try_times = 5

    def __str__(self):
        return self._str_

    def __get_item(self):
        return self._item_

    def __get_engine(self):
        return self._engine_

    def __get_chat_list(self):
        return self._chat_list

    def __get_current_chat(self):
        return self._current_chat

    def __get_msg_list(self):
        return self._msg_list

    def __get_sticker_list(self):
        return self._sticker_list

    def __get_layer_list(self):
        return self._layer_list

    def __get_current_layer(self):
        return self._current_layer

    def __get_network_delay(self):
        return self._network_delay

    def __get_try_times(self):
        return self._try_times

    def set_try_times(self, times):
        self._try_times = times
        return self._try_times

    def set_network_delay(self, seconds):
        self._network_delay = int(seconds)
        return self._network_delay

    def set_default_implicitly_wait(self, seconds):
        self._default_implicitly_wait = int(seconds)
        return self._default_implicitly_wait

    def set_min_implicitly_wait(self, seconds):
        self._min_implicitly_wait = int(seconds)
        return self._min_implicitly_wait

    def __init__(self, webdriver_path="", Line_Crx_Path="", user_data_dir="./Default", show_window=False):
        if webdriver_path == "":
            webdriver_path = str(pathlib.PurePath(__file__).with_name("chromedriver"))
        if Line_Crx_Path == "":
            Line_Crx_Path = str(pathlib.PurePath(__file__).with_name("LINE.crx"))
        user_data_dir = "user-data-dir=" + user_data_dir
        options = webdriver.ChromeOptions()
        options.add_extension(Line_Crx_Path)
        options.add_argument(user_data_dir)
        if not show_window:
            options.add_argument('headless')
        self.driver = webdriver.Chrome(executable_path=webdriver_path, chrome_options=options)
        self.driver.implicitly_wait(self._default_implicitly_wait)
        self.driver.get("chrome-extension://ophjlpahpchlmihnnnihgmmeilfjmjjc/index.html")
        self._engine_ = self.driver

    def login(self, username, password):
        input_username = self.driver.find_element_by_id("line_login_email")
        input_password = self.driver.find_element_by_id("line_login_pwd")
        input_username.clear()
        input_username.send_keys(username)
        input_password.send_keys(password)
        input_password.send_keys(Keys.ENTER)
        self.driver.implicitly_wait(self._min_implicitly_wait)
        code = self.driver.find_elements_by_xpath(
            "//div[@id = 'login_content']/div/section/div[@class = 'mdCMN01Code']")
        self.driver.implicitly_wait(self._default_implicitly_wait)
        if not self.is_login() and self._is_visible("login_incorrect"):
            return False, self.driver.find_element_by_id("login_incorrect").get_attribute("innerHTML")
        if len(code) == 0:
            return True, None
        return True, code[0].get_attribute("innerHTML")

    def _is_visible(self, eid):
        elem = self.driver.find_elements_by_id(eid)
        if len(elem) == 0:
            return False
        elem = elem[0]
        if "MdNonDisp" in elem.get_attribute("class"):
            return False
        return True

    def is_login(self):
        self.driver.implicitly_wait(self._min_implicitly_wait)
        ret = self._is_visible("login_content")
        self.driver.implicitly_wait(self._default_implicitly_wait)
        return not ret

    def close(self):
        self.driver.stop_client()
        return self.driver.quit()

    def _scroll_layer(self, category=_current_layer, mode="down"):
        if category == "Chats":
            category_elem_xpath = "//div[@id = '_chat_list_scroll']"
        elif category == "Friends":
            category_elem_xpath = "//div[@id = 'contact_mode_contact_list']"
        elif category == "Groups":
            category_elem_xpath = "//div[@id = 'wrap_group_list']/div[@class = 'MdScroll mdScroll01']"
        elif category == "AddFriends":
            category_elem_xpath = "//div[@id = 'wrap_recommend_list']/div[@class = 'MdScroll mdScroll01']"
        elif category == "Msg":
            category_elem_xpath = "//div[@id='_chat_message_area']"
        else:
            return False
        if mode == "up":
            mode_str = "0 - "
        elif mode == "down":
            mode_str = ""
        else:
            return False
        get_hight_js = \
            """function getElementByXpath(path) {
                    return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                }
                return getElementByXpath("%s").scrollHeight;""" % (category_elem_xpath)
        prev_hight = 0
        true_hight = self.driver.execute_script(get_hight_js)
        while prev_hight != true_hight:
            prev_hight = true_hight
            scroll_js = \
                """function getElementByXpath(path) {
                    return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                }
                getElementByXpath("%s").scrollBy(0, %sgetElementByXpath("%s").scrollHeight);""" % \
                (category_elem_xpath, mode_str, category_elem_xpath)
            self.driver.execute_script(scroll_js)
            time.sleep(self._network_delay)
            true_hight = self.driver.execute_script(get_hight_js)
        return True

    # TODO:
    #   tow layer find element too slow can fix by beautifulsoup
    #   line: 210 return left_side.get_attribute("innerHTML")

    def _get_chat_list(self, category=_current_layer):
        """
        Get left side slider content
        :param category: enum{Chats, Friends, Groups}
        :return: Success [(category_count,category_body), ...]
                 False   False
        """
        if category == "Chats":
            category_body_id = ["_chat_list_scroll"]
            category_count_elem = []
        elif category == "Friends":
            category_body_id = ["contact_wrap_new_friends", "contact_wrap_favorite_friends", "contact_wrap_friends"]
            category_count_elem = [(By.ID, "contact_friend_count"), (By.ID, "contact_friend_count"),
                                   (By.ID, "contact_friend_count")]
        elif category == "Groups":
            category_body_id = ["favoriteGroup", "invitedGroup", "joinedGroup"]
            category_count_elem = [(By.CLASS_NAME, "mdLFT04Ttl"), (By.CLASS_NAME, "mdLFT04Ttl"),
                                   (By.CLASS_NAME, "mdLFT04Ttl")]
        else:
            return False, None, None
        left_side = self.driver.find_element_by_id("leftSide")
        category_items = []
        for i in range(len(category_body_id)):
            category_elem = left_side.find_element_by_id(category_body_id[i])
            category_body_elem = category_elem.find_elements_by_tag_name("li")
            category_body = []
            for j in category_body_elem:
                category_body.append(j.get_attribute("title"))
            if len(category_count_elem) != 0:
                category_count = category_elem.find_elements(category_count_elem[i][0], category_count_elem[i][1])[0]. \
                    get_attribute("innerHTML")
                category_count = ''.join([i for i in category_count if i.isdigit()])
                if category_count == '':
                    category_count = '0'
                category_count = int(category_count)
            else:
                category_count = None
            category_items.append((category_count, category_body, category_body_elem))
        return category_items, left_side, None

    def _is_select_chat(self):
        time.sleep(self._network_delay)
        msg_layer = self.driver.find_elements_by_xpath(
            "//div[@id='_chat_message_area']//div[@id='_chat_room_msg_list']")
        if len(msg_layer) > 0:
            return True
        return False

    # TODO:
    #   use beautifulsoup to faster
    #   format the time to python datatime type
    #   get more information from msg layer
    def get_msg(self):
        msg_list = self.driver.find_elements_by_xpath(
            "//div[@id='_chat_message_area']//div[@id='_chat_room_msg_list']/div")
        msg = []
        date_time = None
        if len(msg_list) == 0:
            self._msg_list = msg
            return True
        for i in msg_list:
            if i.get_attribute("class") == "MdRGT10Notice mdRGT07Other mdRGT10Date":
                date_time = i.find_element_by_tag_name("time").get_attribute("innerHTML")
                continue
            elif i.get_attribute("class") != "MdRGT07Cont mdRGT07Other":
                continue
            speaker_l = i.find_elements_by_class_name("mdRGT07Ttl")
            speaker = None
            if len(speaker_l) == 1:
                speaker = speaker_l[0].get_attribute("innerHTML")
            msg_l = i.find_elements_by_class_name("mdRGT07MsgTextInner")
            msg_text = None
            if len(msg_l) == 1:
                msg_text = msg_l[0].get_attribute("innerHTML")
            img_l = i.find_elements_by_id("_chat_message_loading_area")
            img = None
            if len(img_l) == 1:
                img = img_l[0].find_elements_by_tag_name("img")[0].get_attribute("src")
            sticker_l = i.find_elements_by_css_selector(".mdRGT07Msg.mdRGT07Sticker")
            sticker = None
            if len(sticker_l) == 1:
                sticker = sticker_l[0].find_elements_by_tag_name("img")[0].get_attribute("src")
            time_l = i.find_elements_by_tag_name("time")
            time_m = None
            if len(time_l) == 1:
                if date_time is None:
                    return False
                time_m = date_time + ' ' + time_l[0].get_attribute("innerHTML")
            msg.append({'time': time_m, 'speaker': speaker, 'msg': msg_text, 'img': img, 'sticker': sticker})
            self._msg_list = msg
        return True

    def select_chat_layer(self, category):
        if category == "Chats":
            category_elem_xpath = "//li[@data-type = 'chats_list']/button"
        elif category == "Friends":
            category_elem_xpath = "//li[@data-type = 'friends_list']/button"
        elif category == "Groups":
            category_elem_xpath = "//li[@data-type = 'groups_list']/button"
        elif category == "AddFriends":
            category_elem_xpath = "//li[@data-type = 'addfriends']/button"
        else:
            return False
        self.driver.find_element_by_xpath(category_elem_xpath).click()
        self._current_layer = category
        if not self._scroll_layer(category=category, mode="down") or \
                not self._scroll_layer(category=category, mode="up"):
            return False
        self._chat_list, self._item_, self._str_ = self._get_chat_list(category=category)
        if self._chat_list is None:
            return False
        return True

    # TODO:
    #   self._sticker_list get sticker list
    def select_chat(self, chat_name, auto_get_msg=True):
        for i in self._chat_list:
            for j in range(len(i[1])):
                if i[1][j] == chat_name:
                    i[2][j].click()
                    self._item_ = self.driver.find_element_by_xpath("//div[@id='_chat_message_area']")
                    self._str_ = self._item_.get_attribute("innerHTML")
                    self._current_chat = chat_name
                    if auto_get_msg:
                        self._scroll_layer(category="Msg", mode="up")
                        return self.get_msg()
                    else:
                        return self._is_select_chat()
        return False

    # TODO:
    #   add send picture
    #   send sticker by a download sticker file (map disk file to driver file)
    def send_msg(self, content="2", data_sticker_pkg_id="1", type="sticker"):
        if type == "sticker":
            sticker_button = self.driver.find_element_by_xpath(
                "//div[@class = 'mdRGT06Btn']/button[@title = 'Stickers']")
            time.sleep(self._network_delay)
            sticker_button.click()
            j = self._try_times - 1
            while j > 0:
                time.sleep(self._network_delay)
                sticker_package_list = self.driver.find_elements_by_xpath(
                    "//ul[@id = '_chat_sticker_tab']/li/button/img")
                for i in sticker_package_list:
                    if data_sticker_pkg_id in i.get_attribute("data-sticker-pkg-id"):
                        j = -1
                        i.click()
                        break
                j -= 1
            if j == 0:
                return False
            j = self._try_times - 1
            while j > 0:
                time.sleep(self._network_delay)
                stickers = self.driver.find_elements_by_xpath("//ul[@id = '_chat_sticker_list']/li/img")
                if len(stickers) > int(content):
                    stickers[int(content) - 1].click()
                    time.sleep(self._network_delay)
                    return True
            return False
        elif type == "text":
            send_box = self.driver.find_element_by_id("_chat_room_input")
            send_box.send_keys(content)
            send_box.send_keys(Keys.ENTER)
            time.sleep(self._network_delay)
            return True
        return False
