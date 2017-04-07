import vk
import time
import re
import csv

SLEEP_TIME = 0.9
sleep_time = 0.9

session = vk.Session()
vk_api = vk.API(session)
wall = vk_api.wall.get(domain = 'velosipedization', count = 100)

#get all the posts from the wall

wall_posts = vk_api.wall.get(domain = 'velosipedization', count = 100, offset = 100)
wall_history = []
wall_len = wall_posts[0]
if wall_len > 100:
    resid = wall_len
    offset = 0
    while resid > 0:
        wall_history += vk_api.wall.get(owner_id = -26516961, count=100, offset=offset)
        resid -= 100
        offset += 100

#count text length of each post

k = 1
while k < len(wall_history):
    if type(wall_history[k]) == dict:
        new_post = wall_history[k]['text']
        new_post_words = re.sub("<br>", " ", new_post)
    # write as csv
    #with open('veloposts_length.csv', 'a', encoding='utf-8') as f:
    #	print(len(new_post_words.split(" ")), file = f)
    k += 1

#getting post ids

i = 1
post_id_list = []
for item in wall_history:
    while i < len(wall_history):
        if type(wall_history[i]) == dict:
            new_post_id = wall_history[i]['id']
        post_id_list.append(new_post_id)
        i += 1

#print(post_id_list[1])

#extracting post comments

m = 0
comment_history = []
while m < len(post_id_list):
    comment = vk_api.wall.getComments(owner_id=-26516961, post_id = post_id_list[m], count=100)
    comment_len = comment[0]
    if comment_len > 100:
        resid_com = comment_len
        offset_com = 0
        while resid_com > 0:
            comment_history += vk_api.wall.getComments(owner_id=-26516961, post_id = post_id_list[m], count=100, offset=offset_com)
            time.sleep(sleep_time)
            resid_com -= 100
            offset_com += 100
    else:
        comment_history += vk_api.wall.getComments(owner_id=-26516961, post_id = post_id_list[m], count=100)
        time.sleep(sleep_time)
    m += 1

#print(len(comment_history))

#extracting comment texts



n = 1
for item in comment_history:
    while n < len(comment_history):
        if type(comment_history[n]) == dict:
            comment_messages = comment_history[n]
            comment_text = comment_messages['text']
            comment_text_words = re.sub("<br>", " ", comment_text)
            user_id_comment = comment_messages['from_id']
            user_info = vk_api.users.get(user_ids=user_id_comment, fields='city')
            user_info.append("NA")
            if type(user_info[0]) == dict:
                user_city = user_info[0]['city']
                with open('comments_length.csv', 'a', encoding='utf-8') as csvfile:
                    fieldnames = ['post_id', 'comment_length', 'city']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow({'post_id': comment_history[n], 'comment_length' : len(comment_text_words), 'city' : user_city})
            else:
                with open('comments_length.csv', 'a', encoding='utf-8') as csvfile:
                    fieldnames = ['post_id', 'comment_length', 'city']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow({'post_id' : comment_history[n], 'comment_length': len(comment_text_words), 'city' : user_info[0]})
            n += 1
