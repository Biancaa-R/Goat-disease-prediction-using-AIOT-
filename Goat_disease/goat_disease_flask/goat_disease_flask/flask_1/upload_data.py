import requests
import json

detection={"ppr":"1","antharax":"0","tetanus":"0"}   
upload=False  
for i in detection.values():
    if i in ["1",]:
        upload=True
        break

if upload ==True  :  
    i=list(detection.values())
    requests.get('https://api.thingspeak.com/update?api_key=27KXSR99B65PCOMJ&field1=0&field1='+str(i[0])+'&field2='+str(i[1])+'&field3='+str(i[2]))
        
