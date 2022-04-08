import os
import requests
from datetime import datetime

today = datetime.now()
today_date = today.strftime("%A (%-m/%-d)")
today_time = today.strftime("%-I:%M %p")
print(today_time)
print(today_date)
print("")

SHEETY_ENDPOINT = os.environ["SHEETY_ENDPOINT"]

NUTRI_POST_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/nutrients"
NUTRI_APP_ID = os.environ['NUTRI_APP_ID']
NUTRI_API_KEY = os.environ['NUTRI_API_KEY']

headers = {
    "x-app-id": NUTRI_APP_ID,
    "x-app-key": NUTRI_API_KEY,
    "x-remote-user-id": "0",
}


def get_food():
    user_input = input("Write what you ate/drank: ")

    nutri_parameters = {
        "query": user_input,
        "timezone": os.environ["timezone"],
        # "aggregate": user_input
    }

    response = requests.post(NUTRI_POST_ENDPOINT, headers=headers, json=nutri_parameters)
    if response.status_code >= 400:
        print(response.status_code)
        print("\nPlease enter valid food or drinks. Be careful of spelling, weird symbols, or extra spaces")
        return get_food()
    else:
        print(f"Your entry '{user_input}' has been recorded and your Calorie Tracker updated")
        return response.json()["foods"]


nutritional_data_list = get_food()

for item in nutritional_data_list:
    sheety_add_row_parameters = {
        "food": {
            "date": today_date,
            "time": today_time,
            "food": item["food_name"],
            "quantity": item["serving_qty"],
            "unit": item["serving_unit"],
            "calories": item["nf_calories"],
            "sugar": item["nf_sugars"],
            "protein": item["nf_protein"],
        }
    }
    headers = {
                  "Authorization": os.environ['SHEETY_AUTH']
    }
    response = requests.post(url=SHEETY_ENDPOINT, json=sheety_add_row_parameters, headers=headers)
    response.raise_for_status()
