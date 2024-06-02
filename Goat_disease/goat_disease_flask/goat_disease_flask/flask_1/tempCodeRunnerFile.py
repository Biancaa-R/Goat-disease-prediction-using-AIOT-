import requests
import json
r=requests.get("https://api.thingspeak.com/channels/2567333/feeds.json?api_key=T1YTUYGYW4TUOLM4&results=2")
n=json.loads(r.text)

for i in range(len(n["feeds"])):
    list1=[n["feeds"][i]["entry_id"],n['feeds'][i]['field1'],n['feeds'][i]['field2'],n['feeds'][i]['field3'],n['feeds'][i]['created_at']]
    print(list1)        
            