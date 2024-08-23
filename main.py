import smtplib
import requests
from datetime import datetime
import time

MY_LAT = 51.507351 # Your latitude
MY_LONG = -0.127758 # Your longitude
USERNAME = "clarenceswag1@gmail.com"
PASSWORD = "Fill in"

# Your position is within +5 or -5 degrees of the ISS position.


# Check if our position is within +5 or -5 degrees of the ISS position
def proximity():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if abs(MY_LAT - iss_latitude) < 5 and abs(MY_LONG - iss_longitude) < 5:
        return True
    else:
        return False


# Check if time is 12 or later
def is_it_dark():
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
    time = datetime.now()

    if sunset <= time.hour <= sunrise:
        return True
    else:
        return False


while True:
    time.sleep(60)
    if proximity() and is_it_dark():
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=USERNAME, password=PASSWORD)
            connection.sendmail(from_addr=USERNAME,
                                to_addrs="clarenceogbuefi@gmail.com",
                                msg="Subject: LOOK UP!\n\nThe satelite is near you!")





# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.





