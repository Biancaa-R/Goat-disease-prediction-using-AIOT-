# import requests
# import json
# r=requests.get("https://api.thingspeak.com/channels/2567333/feeds.json?api_key=T1YTUYGYW4TUOLM4&results=2")
# n=json.loads(r.text)

# for i in range(len(n["feeds"])):
#     list1=[n["feeds"][i]["entry_id"],n['feeds'][i]['field1'],n['feeds'][i]['field2'],n['feeds'][i]['field3'],n['feeds'][i]['created_at']]
#     print(list1)        

import requests
import json

posts = []
r = requests.get("https://api.thingspeak.com/channels/2567333/feeds.json?api_key=T1YTUYGYW4TUOLM4&results=2")
n = json.loads(r.text)

num = 0
for i in range(len(n["feeds"])):
    disease = []
    list1 = [n["feeds"][i]["entry_id"], n['feeds'][i]['field1'], n['feeds'][i]['field2'], n['feeds'][i]['field3'], n['feeds'][i]['created_at']]
    num += 1
    if num != 1:  # If it's not the first iteration
        if list1[1] == "1":
            disease.append("ppr")
        if list1[2] == "1":
            disease.append("anthrax")
        if list1[3] == "1":
            disease.append("tetanus")
        disease_str = ", ".join(disease) if disease else "none"
        dict1 = {
            "author": list1[0],
            "title": "disease detected on " + list1[4],
            "content": "The diseases detected is/are " + disease_str,
            "date": list1[4]
        }
        posts.append(dict1)


print(posts)

# posts=[]
# import requests
# import json
# r=requests.get("https://api.thingspeak.com/channels/2567333/feeds.json?api_key=T1YTUYGYW4TUOLM4&results=2")
# n=json.loads(r.text)
# num=0
# for i in range(len(n["feeds"])):
#     disease=[]
#     list1=[n["feeds"][i]["entry_id"],n['feeds'][i]['field1'],n['feeds'][i]['field2'],n['feeds'][i]['field3'],n['feeds'][i]['created_at']]
#     if num!=0:
#         num=num+1
#         for i in list1:
#             if i[1]=="1":
#                 disease.append("ppr")
#             if i[2]=="1":
#                 disease.apend("antharax")
#             if i[3]=="1":
#                 disease.append("tetanus")
#         dict1={"author":list1[0],"title":"disease detected on "+list1[4],"content":"The diseases detected is/ are "+ [j for j in disease],"date":list1[4] }
#         posts.insert(0,dict1)

# print(posts)    