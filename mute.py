import requests
import time

mute_list = {}
mute_count = {}
mute_timer = {}


# restrict method
def restrict_user(chat_id, user_id, can_send_messages=None, can_send_media_messages=None,
                  can_send_other_messages=None, until_date=None):
    params = {'chat_id': chat_id,
              'user_id': user_id,
              'until_date': until_date,
              'can_send_messages': can_send_messages,
              'can_send_media_messages': can_send_media_messages,
              'can_send_other_messages': can_send_other_messages}
    return requests.get('restrictChatMember', params)


# return current unix time + 3 min
def timer():
    t = time.gmtime()[:]
    suspend_time = time.mktime(t[:4] + (t[4]+3,) + t[5:])
    return suspend_time


# checker
def checker(message, mute_list):
    if 'mute' in message['text'].lower():
        muter = message['from']['id']
        if message['reply_to_message']['from']['id']:
            mute_id = message['reply_to_message']['from']['id']
            chat_id = message['chat']['id']
            return gen(mute_list, mute_id, muter, chat_id)


# delete method
def del_message(chat_id, message_id):
    params = {'chat_id': chat_id,
              'message_id': message_id}
    return requests.get('deleteMessage', params)


# mute list redactor
def gen(mute_list, mute_id, muter, chat_id):
    if mute_id in mute_list:
        if muter in mute_list[mute_id]:
            print('Already in list')
        else:
            mute_list[mute_id].append(muter)
            if len(mute_list[mute_id]) == 3:
                restrict_user(chat_id, mute_id, timer(), False, False, False)
            else:
                print(mute_list, str(3 - len(mute_list[mute_id])) + ' left')
    else:
        mute_list[mute_id] = [muter]
        return mute_list
