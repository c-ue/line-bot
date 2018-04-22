# Line bot api

###line(webdriver_path: str, Line_Crx_Path: str, user_data_dir: str, show_window: boolen)

init line object.

- webdriver_path: Path to the google chrome driver.
- Line_Crx_Path: Path to the Line chrome extension.
- user_data_dir: Path to save the chrome data.
- show_window: Run in background.

- Return
    - line object.

###login(username: str, password: str)

login line.

- username: Your account (e-mail) of the line.
- password: Your password of the account.

- Return
    - True, str: login success.
        - If str is None, success.
        - If str is code, need to verify login code.
    - False, str: login fail.
        - str is error message.

###is_login()

Check the login status.

- Return
       - True: Is still login.
       - False: Is nologin.
###close()

Release the line object.

###get_msg()

Get the message of the chat room.

- Return
    - True: Success.
        - See to lineobj._msg_list get {'time': str, 'speaker': str, 'msg': str, 'img': str, 'sticker': str}
    - False Fail.
    
###select_chat_layer(category: str)

Choice the type of the chat room.

- category: Type of the chat room. Enum{"Chats", "Friends", "Groups", "AddFriends"}

- Return
    - True: Success.
        - See self._chat_list to get (category_count: int of len, category_body: str of chat name, category_body_elem: element_obj of chat room)
    - False: Fail.

###select_chat(chat_name: str, auto_get_msg: boolen)

Choice the chat room.

- chat_name: The name of the chat room.
- auto_get_msg: Get the message of the chat.

- Return
    - True: Success.
    - False: Fail.
    - Msg: {'time': str, 'speaker': str, 'msg': str, 'img': str, 'sticker': str}.
    
###send_msg(content: str, data_sticker_pkg_id: str, type: str)

Send sticker or text message.

- content: The content of text message or the index of the stcker package. 
- data_sticker_pkg_id: The index of the package.
- type: The message type. Enum{"sticker", "text"}

- Return
    - True: Success.
    - False: Fail.

##END


