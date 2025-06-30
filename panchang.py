import requests
from datetime import datetime
from config import PROKERALA_CLIENT_ID, PROKERALA_CLIENT_SECRET

def get_access_token():
    url = "https://api.prokerala.com/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}

    try:
        response = requests.post(url, auth=(PROKERALA_CLIENT_ID, PROKERALA_CLIENT_SECRET), headers=headers, data=data)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print(f"❌ Token Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception getting token: {e}")
        return None

def get_first_name(lst, key):
    if not lst:
        return "❌ Not returned"
    try:
        return lst[0].get(key, "❌ Key missing")
    except Exception as e:
        return f"❌ Error: {e}"

def fetch_panchang_data(input_date_str):
    token = get_access_token()
    if not token:
        return "⚠️ Could not authenticate with Prokerala API."

    try:
        dt_obj = datetime.strptime(input_date_str, "%Y-%m-%d")
        iso_datetime = dt_obj.strftime("%Y-%m-%dT06:00:00+05:30")  # 6 AM IST

        url = "https://api.prokerala.com/v2/astrology/panchang"
        headers = {
            "Authorization": f"Bearer {token}"
        }

        params = {
            "datetime": iso_datetime,
            "coordinates": "22.57,88.36",  # Kolkata
            "ayanamsa": 1,
            "language": "en"
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json().get("data", {})
            # Uncomment to debug:
            # print("📦 RAW Panchang data:", data)

            tithi = get_first_name(data.get("tithi", []), "name")
            nakshatra = get_first_name(data.get("nakshatra", []), "name")
            yoga = get_first_name(data.get("yoga", []), "name")
            karana = get_first_name(data.get("karana", []), "name")

            return (
                f"📅 Tithi: {tithi}\n"
                f"🌠 Nakshatra: {nakshatra}\n"
                f"🪐 Yoga: {yoga}\n"
                f"🧩 Karana: {karana}"
            )
        else:
            return f"⚠️ API Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"⚠️ Exception fetching Panchang: {e}"
