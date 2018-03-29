import numpy as np
import pandas as pd
import telepot
import urllib3
import os
import hashlib
import json
from time import time
from urllib.parse import urlparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from TOKEN import TOKEN

class MessageBot(object):
    def __init__(self):
        self.bot = telepot.Bot(TOKEN)
        if os.path.isfile('Data/user_list.csv'):
            print('User list exists')
            self.users = pd.read_csv('Data/user_list.csv')
        else:
            self.users = pd.DataFrame({'id':0,'name':0,'user_name':0},index=[0])
            #create csv
            self.users.to_csv('Data/user_list.csv')

        self._newuser_id = None

    def handle(self,msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        #print(content_type, chat_type, chat_id)
        if content_type == 'text':
             #bot.sendMessage(chat_id, msg['text'])
            #print(chat_id, msg['chat']['first_name'])
             #check if it is a new user
            self.new_user(content_type, chat_type, chat_id, msg)
            self.on_chat_message(content_type, chat_type, chat_id, msg)
            self.get_info(content_type, chat_type, chat_id, msg)
            self.get_users(content_type, chat_type, chat_id, msg)


    def write_users(self,user_list):
        with open("users.csv", 'w') as users_file:
            users_file.write("\n".join([str(uid) for uid in user_list]))

    def new_user(self,content_type, chat_type, chat_id, msg):
        greeter_dict = ['/start','/hallo']
        first_word = msg['text'].split(' ', 1)[0]
        if first_word in greeter_dict and self._newuser_id is None and chat_id not in self.users['id'].values:
            # user is not yet in user list!
            # 1st interaction with user
            greeter_msg = 'Welcome %s! You are new here. \n Chose a user name:' % msg['chat']['first_name']
            self.bot.sendMessage(chat_id,greeter_msg)
            self._newuser_id = chat_id
        elif first_word in greeter_dict and chat_id in self.users['id'].values:
            this_name = self.users.user_name.loc[self.users['id']==chat_id].values[0]
            message = 'You already have a user name, it is:\n %s' % this_name
            self.bot.sendMessage(chat_id,message)
        elif self._newuser_id == chat_id and chat_id not in self.users['id'].values:
            user_name = msg['text'].split(' ', 1)[0]
            if user_name not in self.users['user_name'].values:
                # all went ok, user name does not yet exist
                self._newuser_id = None
                message = 'Congrats, your user name is: %s \n Tell your friends!' % user_name
                message2 = 'To get more information how this works send: /info'
                self.bot.sendMessage(chat_id, message)
                self.bot.sendMessage(chat_id, message2)
                try:
                    self.users=pd.read_csv('Data/user_list.csv')
                except:
                    print('File does not exist')

                # update the user list
                new_user_dict = {'id':chat_id,'name':msg['chat']['first_name'],'user_name':user_name}
                self.users = self.users.append(new_user_dict,ignore_index=True)
                # write the user list
                self.users.to_csv('Data/user_list.csv')
            else:
                # user name already exists
                message = 'Sorry, your user name already exists.\nChoose a new one, please.'
                self.bot.sendMessage(chat_id, message)


    def on_chat_message(self, content_type, chat_type, chat_id, msg):
        # this is the main messages engine
        # the text is:
        text = msg['text']
        # store all the pending messages [id, text]
        # pending_text = []

        # sender user name
        this_sender = self.users.user_name.loc[self.users['id'] == chat_id].values[0]
        sender_says = 'From '+this_sender+': \n'

        # find the users the message is addressed to
        recipients = [t[1:] for t in text.split() if t.startswith('&')]

        for ix, t in enumerate(recipients):
            if str(t).endswith((',', '!', ':', '?', ';', '.')):
                recipients[ix] = t[:-1]

        if len(recipients) > 0:# and 'all' not in recipients:  # all is the key word to send to all users
            # loop over the recipients
            for name in recipients:
                # get the user id based on user name
                receiver_id = int(self.users.id.loc[self.users['user_name'] == name].values)
                # finally send the text to named recipients
                self.bot.sendMessage(receiver_id, sender_says+text)
                print(msg['chat']['first_name'],' sends to ',
                      self.users.user_name.loc[self.users['id'] == receiver_id].values[0])
                #print(receiver_id)
        else: #elif 'all' in recipients:
            # the message goes out to all users, except the sender
            for receiver_id in self.users.id.values:
                receiver_id = int(receiver_id)
                if receiver_id != chat_id:
                    # finally send the text to all recipients
                    self.bot.sendMessage(receiver_id, sender_says+text)

        #elif recipients == []:
        #    message = 'You did not specify a recipient. \n Include: &all \n if the message should go to all group members.'
        #    pending_text = [[chat_id], [text]]
        #    self.bot.message_loop(chat_id, message)


    def get_info(self, content_type, chat_type, chat_id, msg):
        # this will send the info message
        text = msg['text']
        if text == '/info':
            try:
                from info_text import info_text
                self.bot.sendMessage(chat_id, info_text)
            except:
                self.bot.sendMessage(chat_id, 'Sorry... no infos.')


    def get_users(self, content_type, chat_type, chat_id, msg):
        # this will send the user names
        text = msg['text']
        if text == '/getusers':
            user_list_array = self.users['user_name'].values
            user_list = ''
            for u in user_list_array:
                user_list=str(u)+'\n'+user_list
            #user_list.append([u for u in user_list_array])
            self.bot.sendMessage(chat_id, str(user_list))
