from twilio.rest import Client
from headerinjection.includes import scan

account_sid = 'ur sid'
auth_token = 'ur token'

def whatsapp(url):
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body= "Title: Host Header Injection \n" + "URL: " + url + '\n bug found',
            to='whatsapp:+917395967819'
)
    except:
        print("unable to send message")


