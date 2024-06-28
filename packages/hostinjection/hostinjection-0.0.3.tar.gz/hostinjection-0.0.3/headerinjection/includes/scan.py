import requests
from headerinjection.includes import sms
from headerinjection.includes import write

header = {"Host": "evil.com"}

def cvescan(url,output):
    try:
        req = requests.get(url,headers=header,timeout=5)
        responce = req.url
        if "evil.com" in responce:
            print(f"\nits vuln: {url}")
            if True:
                sms.whatsapp(url)
            if output is not None:
                write.write(output,str(url+"\n"))
        else:
            print(f"its not vuln: {url}\n")
    except requests.exceptions.RequestException as e:
        print("invalid url")