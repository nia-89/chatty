import time
from os import path
import glob
import re
import pandas
import numpy
import matplotlib.pyplot as plt
from PIL import Image
import json
import emoji
from wordcloud import WordCloud, STOPWORDS

def get_available_chats():
    return glob.glob("imports/*.txt")

def open_whatsapp_txt(filename):
    with open(filename, encoding="utf8") as chat:
        return chat.read()

def parse_whatsapp_txt(chat_text):
    parsed_text = []
    chat_line = chat_text.splitlines()
    for line in chat_line:
        #Android
        if re.search("^(0[1-9]|[1-2][0-9]|3[0-1])\/(0[1-9]|1[0-2])\/[0-9]{4},", line) and not re.search("Media omitted", line) and not re.search("live location", line):
                parsed_text_dictionary = {
                    "Date" : line[:10].replace(" ",""),
                    "User" : line.split(" ")[4].replace(":",""),
                    "Message" : line.split(": ")[-1]}
                parsed_text.append(parsed_text_dictionary)
        #iOS
        elif re.search("^\[([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}", line) and not re.search("Omitted media", line) and not re.search("live location", line):
                parsed_text_dictionary = {
                    "Date" : line[:11].replace(" ","").replace("[","").replace("]",""),
                    "User" : line.split(" ")[2].replace(":",""),
                    "Message" : line.split(": ")[-1]}
                parsed_text.append(parsed_text_dictionary)
    return parsed_text

def extract_emojis(parsed_whatsapp_text):
    emojis = []
    for line in parsed_whatsapp_text:
        if any(char in emoji.UNICODE_EMOJI for char in line['Message']):
            emojis.append(char)
    return emojis


def generate_data_frame(parsed_whatsapp_text):
    data_frame = pandas.DataFrame()
    for dictionary in parsed_whatsapp_text:
        data_frame = data_frame.append(dictionary, ignore_index=True)
    pandas.to_datetime(data_frame['Date'], dayfirst=True)
    return data_frame

def get_number_of_messages_by_user(data_frame):
    messages_by_user = data_frame['User'].value_counts()
    return messages_by_user

def get_number_of_messages_by_date(data_frame):
    messages_by_date = data_frame['Date'].value_counts().to_frame()
    return messages_by_date

def get_messages_over_time_by_user(data_frame):
    messages_over_time = data_frame
    messages_over_time['Date'] = pandas.to_datetime(data_frame['Date'], dayfirst=True, yearfirst=True)
    messages_over_time['Date'] = messages_over_time['Date'].dt.to_period('M')
    messages_over_time_grouped = messages_over_time.groupby('User')['Date'].value_counts(sort=False).unstack().fillna(0)
    return messages_over_time_grouped

def split_messages_into_words(data_frame):
    split_messages = data_frame["Message"].str.split()
    words = split_messages.explode("Message")
    return words

def generate_word_cloud(words, selected_mask=None):
    custom_stopwords = ['X','x','XXX','xxx','ok','OK'] + list(STOPWORDS)
    mask = numpy.array(Image.open(path.join('static/img/wordcloud_mask/', selected_mask + ".PNG")))
    wordcloud = WordCloud(
        width = 1000,
        height = 1000,
        background_color = 'rgba(255, 255, 255, 0)', mode='RGBA',
        mask=mask,
        stopwords = custom_stopwords).generate(str(words))
    word_cloud_url = 'img/wordcloud/wordcloud_' + time.strftime('%Y-%m-%d_%H%M%S') + '.png'
    wordcloud.to_file('static/' + word_cloud_url)
    return word_cloud_url

