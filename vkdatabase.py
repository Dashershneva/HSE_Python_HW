import vk
import time
import sqlite3


session = vk.Session()
vk_api = vk.API(session)
wall = vk_api.wall.get(domain = 'velosipedization', count = 100)

#create mysql database

conn = sqlite3.connect('vkdatabase.db')
c = conn.cursor()
c.execute('''CREATE TABLE comments
             (iteration, comment_id, who_wrote, to_whom, date, text)''')
conn.commit()

query = ("INSERT INTO comments (iteration, comment_id, who_wrote, to_whom, date, text) " \
                " VALUES (?,?,?,?,?,?)")


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

time.sleep(15)

#getting post ids

i = 1
post_id_list = []
for item in wall_history:
    while i < len(wall_history):
        if type(wall_history[i]) == dict:
            new_post_id = wall_history[i]['id']
        post_id_list.append(new_post_id)
        print("i =", i)
        i += 1

#print(post_id_list[1])

time.sleep(20)

#extracting post comments

m = 0
comment_history = []
while m < len(post_id_list):
    if m  == 500 or m == 1000 or m == 2000:
        time.sleep(20)
    comment = vk_api.wall.getComments(owner_id=-26516961, post_id = post_id_list[m], count=100)
    comment_len = comment[0]
    if comment_len > 100:
        resid_com = comment_len
        offset_com = 0
        while resid_com > 0:
            comment_history += vk_api.wall.getComments(owner_id=-26516961, post_id = post_id_list[m], count=100, offset=offset_com)
            time.sleep(0.5)
            resid_com -= 100
            offset_com += 100
    else:
        comment_history += vk_api.wall.getComments(owner_id=-26516961, post_id = post_id_list[m], count=100)
        #time.sleep(0.5)
    print("m =", m)
    m += 1


time.sleep(10)

#getting comment info

n = 0
user_id_list = []
while n < len(comment_history):
    for item in comment_history:
        if type(comment_history[n]) == dict:
            com_cid = comment_history[n]['cid']
            com_from = comment_history[n]['from_id']
            text = comment_history[n]['text']
            user_id_list.append(comment_history[n]['from_id'])
            reply_key = 'reply_to_cid' in comment_history[n]
            if reply_key == True:
                reply_id = comment_history[n]['reply_to_cid']
            else:
                comment_history[n]['reply_to_cid'] = "none"
                reply_id = comment_history[n]['reply_to_cid']
            date_info = 'date' in comment_history[n]
            if date_info == True:
                date = time.ctime(comment_history[n]['date'])
            else:
                comment_history[n]['date'] = "none"
                date = comment_history[n]['date']
            data = [(n, com_cid, com_from, reply_id, date, text)]
            c.executemany(query, data)
            conn.commit()
            print(n, comment_history[n]['cid'], comment_history[n]['from_id'], reply_id, time.ctime(date))
            print ("n =", n)
        n += 1


time.sleep(15)
#getting user info

k = 0
user_info = []
for item in user_id_list:
    if k % 500 == 0:
        time.sleep(20)
    if user_id_list[k] > 0:
        user_info_item = vk_api.users.get(user_ids = user_id_list[k], fields =('bdate', 'city'))
        user_info.append(user_info_item[0])
        print("k = ", k)
    k += 1

#creating users table

time.sleep(15)

c.execute('''CREATE TABLE users
             (who_wrote, city, bdate)''')
conn.commit()

query_users = ("INSERT INTO users (who_wrote, city, bdate) " \
                " VALUES (?,?,?)")


time.sleep(20)

#selecting user info


t = 0
for item in user_info:
    if t == 1000 or t == 2000:
        time.sleep(15)
    uid = user_info[t]['uid']
    city = user_info[t]['city']
    bdate_key = 'bdate' in user_info[t]
    if bdate_key == True:
        user_bdate = user_info[t]['bdate']
    else:
        user_info[t]['bdate'] = 'unknown'
        user_bdate = user_info[t]['bdate']
    data_users = [(uid, city, user_bdate)]
    c.executemany(query_users, data_users)
    conn.commit()
    #print(user_info[t]['uid'], user_info[t]['city'], user_bdate)
    print("t =", t)
    t += 1

conn.close()