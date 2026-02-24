import os
import requests
from datetime import datetime
import smtplib

MY_LAT = 40.7128 
MY_LONG = 74.0060

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

def iss_within_range():
    #Your position is within +5 or -5 degrees of the ISS position.
    is_long =  MY_LONG - 5 <= iss_longitude <= MY_LONG + 5
    is_lan =  MY_LAT - 5 <= iss_latitude <= MY_LAT + 5
    if is_lan and is_long:
        print('Within latitude and longitude range, target is locked and awaiting for orders')
    elif is_lan:
        print('Within latitude range, standby for longitude confirmation')
    elif is_long:
        print('Within longitude range, waiting for target to approach latitude range')
    else:
        print('No eyes on target, we repeat, the target is not locked')
    return is_lan and is_long

if iss_within_range():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour
    is_dark = False
    if time_now <= sunrise or time_now >= sunset:
        print('It is dark')
        is_dark = True
    else:
        print('It is day')


my_email = os.environ.get('MY_EMAIL')
other_email = os.environ.get('OTHER_EMAIL')
password = os.environ.get('MY_PASSWORD')

with smtplib.SMTP(host='smtp.gmail.com', port=587) as connection:
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(from_addr=my_email, to_addrs=other_email,
                        msg=f'Subject:Look up Dumbass!\n\nISS has been spotted in your local area')
