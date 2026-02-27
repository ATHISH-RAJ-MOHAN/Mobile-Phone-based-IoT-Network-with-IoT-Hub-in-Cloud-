import requests
import math
import time
import smtplib
from email.mime.text import MIMEText

# 1. THINGSBOARD SETTINGS
TB_URL = "http://54.193.225.222:8080"
JWT_TOKEN = ''
DEVICES = {
    "Athish": "d71d7990-135f-11f1-ab0c-751d37480f88",
    "Neil": "0f955150-1363-11f1-ab0c-751d37480f88",
    "Aadarsh": "3bfe2470-1362-11f1-ab0c-751d37480f88"
}

HEADERS = {
    "Content-Type": "application/json",
    "X-Authorization": f"Bearer {JWT_TOKEN}"
}

# 2. USC CAMPUS GEOFENCE SETTINGS
USC_LAT = 34.0206
USC_LON = -118.2854
RADIUS = 500   # meters

# 3. EMAIL SETTINGS
SEND_EMAIL = True

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "athishrajmohan3@gmail.com"
EMAIL_PASS = "klwb fqqc gbdc qmky"
EMAIL_TO = "athishrajmohan3@gmail.com"


def send_email_alert(device_name, dist, event_type):
    if event_type == "left":
        subject = f"{device_name} left USC campus"
        body = f"{device_name} is {dist:.2f} meters away from USC campus."
    else:
        subject = f"{device_name} entered USC campus"
        body = f"{device_name} is now inside the USC zone ({dist:.2f} m)."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, EMAIL_TO, msg.as_string())


# 4. HAVERSINE DISTANCE FUNCTION
def distance_m(lat1, lon1, lat2, lon2):
    R = 6371000
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dLon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c


# 5. CHECK ONE DEVICE
def check_device(device_name, device_id):
    url = f"{TB_URL}/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries"

    try:
        response = requests.get(url, headers=HEADERS).json()
        #print(response)
    except Exception as e:
        print(f"Error reading {device_name}: {e}")
        return

    if "lat" not in response or "lon" not in response:
        print(f"{device_name}: No GPS data yet.")
        return

    lat = float(response["lat"][0]["value"])
    lon = float(response["lon"][0]["value"])

    dist = distance_m(lat, lon, USC_LAT, USC_LON)

    global device_state

    current_state = "outside" if dist > RADIUS else "inside"
    previous_state = device_state[device_name]

    print(f"{device_name} is {current_state} USC zone ({dist:.2f} m)")

    # INSIDE → OUTSIDE
    if previous_state == "inside" and current_state == "outside":
        print(f"ALERT: {device_name} left USC zone!")
        if SEND_EMAIL:
            send_email_alert(device_name, dist, "left")

    # OUTSIDE → INSIDE
    if previous_state == "outside" and current_state == "inside":
        print(f"INFO: {device_name} entered USC zone!")
        if SEND_EMAIL:
            send_email_alert(device_name, dist, "entered")

    device_state[device_name] = current_state


# 6. MAIN LOOP
print("Starting USC Campus Alert System...\n")

device_state = {name: "unknown" for name in DEVICES}

while True:
    for name, dev_id in DEVICES.items():
        check_device(name, dev_id)

    print("----- Checking again in 10 seconds -----\n")
    time.sleep(10)