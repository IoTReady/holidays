import requests
import os
import frappe
from datetime import datetime


def get_holidays(country_code: str, year: str, country=None):
    api_url = "https://api.api-ninjas.com/v1/holidays?country={}&year={}".format(
        country_code.lower(), year
    )
    api_key = os.environ["API_NINJAS_KEY"]
    response = requests.get(api_url, headers={"X-Api-Key": api_key})
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)
    # return response.json
    for holiday in response.json():
        # There are, sometimes, duplicates in the response
        try:
            store_holiday(holiday, country)
        except:
            pass
    frappe.db.commit()


def maybe_add_holiday_type(holiday_type: str):
    if not frappe.db.exists("Holiday Type", holiday_type):
        doc = frappe.new_doc("Holiday Type")
        doc.title = holiday_type
        doc.save()


def store_holiday(holiday: dict, country=None):
    """
    {
        'country': 'India',
        'iso': 'IN',
        'year': 2023,
        'date': '2023-03-08',
        'day': 'Wednesday',
        'name': 'Holi',
        'type': 'GAZETTED_HOLIDAY'
    }
    """
    holiday_type = holiday["type"].replace("_", " ").title()
    maybe_add_holiday_type(holiday_type)
    doc = frappe.new_doc("Country Holiday")
    if country:
        doc.country = country
    else:
        doc.country = holiday["country"]
    doc.year = holiday["year"]
    doc.date = datetime.strptime(holiday["date"], "%Y-%m-%d").date()
    doc.day = holiday["day"]
    doc.description = holiday["name"]
    doc.holiday_type = holiday_type
    doc.save()
