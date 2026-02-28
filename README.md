# **USC Campus Geofence Alert System**

A real‑time geolocation monitoring system built using **ThingsBoard**, **OwnTracks**, and a custom **Python geofence engine**.  
The program tracks multiple mobile devices, computes their distance from USC, and sends **email alerts** when users **enter** or **leave** the campus geofence.

---

## **Features**

- Real‑time GPS tracking for multiple devices  
- Haversine‑based distance calculation  
- 500m USC campus geofence  
- State‑based alerts (no repeated emails)  
- Email notifications for:
  - **Entering USC**
  - **Leaving USC**
- Robust telemetry fetching with error handling  
- Works with OwnTracks (HTTP mode)

---

## **System Architecture**

```
OwnTracks App (Phone)
        ↓
ThingsBoard Telemetry API
        ↓
Python Geofence Script
        ↓
Email Alerts (SMTP)
```

---

## **Requirements**

- Python 3.8+
- ThingsBoard instance (cloud or local)
- OwnTracks installed on each phone
- Gmail App Password (for SMTP email)
- Device tokens for each phone

Install dependencies:

```bash
pip install requests
```

---

## **How It Works**

### 1. **OwnTracks → ThingsBoard**
Each phone publishes GPS coordinates (`lat`, `lon`) to ThingsBoard using:

```
POST /api/v1/<DEVICE_TOKEN>/telemetry
```

### 2. **Python Script → ThingsBoard API**
The script polls telemetry every 10 seconds:

```
/api/plugins/telemetry/DEVICE/<device_id>/values/timeseries
```

### 3. **Geofence Logic**
- Computes distance from USC using the Haversine formula  
- Determines whether the device is **inside** or **outside**  
- Tracks previous state to avoid duplicate alerts  

### 4. **Email Alerts**
Sends one‑time notifications when:

- `inside → outside` → **Left USC**
- `outside → inside` → **Entered USC**

---

## **Configuration**

Update these fields in the script:

```python
TB_URL = "http://<your-thingsboard-ip>:8080"
JWT_TOKEN = "<your-jwt-token>"

DEVICES = {
    "name1": "<device-id1>",
    "name2": "<device-id2>",
    "name3": "<device-id3>"
}

EMAIL_USER = "your_email@gmail.com"
EMAIL_PASS = "your_app_password" 
EMAIL_TO = "your_email@gmail.com"
```
#### **Note:** "your_app_password" needs to be generated from the link https://myaccount.google.com/security. You will get the app_password after you enable the 2-Factor Authentication and refresh the page. Use emails ending with "gmail.com".
---

## **Running the Program**

```bash
python main.py
```

Expected output:

```
name1 is inside USC zone (132.45 m)
name2 is outside USC zone (1240.22 m)
INFO: name1 entered USC zone!
ALERT: name2 left USC zone!
```

---

## **Email Alert Examples**

**Subject:** name1 left USC campus  
**Body:** name1 is xxx meters away from USC campus.

**Subject:** Neil entered USC campus  
**Body:** Neil is now inside the USC zone (xxx m).

---

## **Project Structure**

```
.
├── main.py     # Main Python script
├── README.md             # Project documentation
└── requirements.txt      # Dependencies (optional)
```

---

