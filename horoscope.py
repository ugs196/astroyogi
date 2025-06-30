import requests

def fetch_horoscope(sign):
    url = f"https://horoscope-api-ortk.onrender.com/horoscope/today/{sign.lower()}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            horoscope = data.get('horoscope', 'No horoscope found.')
            date = data.get('date', 'N/A')
            return (
                f"🌟 *{sign.capitalize()} Horoscope - {date}*\n\n"
                f"{horoscope}"
            )
        else:
            return f"⚠️ Horoscope API error {response.status_code}: {response.text}"
    except Exception as e:
        return f"⚠️ Horoscope Exception: {str(e)}"
