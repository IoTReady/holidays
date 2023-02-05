import frappe
from datetime import datetime


@frappe.whitelist()
def holiday_type_query(doctype, txt, searchfield, start, page_len, filters):
    country = filters.get("country")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    if country and from_date and to_date:
        sql = "SELECT holiday_type, CONCAT(COUNT(date), ' Holidays') FROM `tabCountry Holiday` WHERE country=%s AND date >= %s AND date <= %s GROUP BY holiday_type"
        return frappe.db.sql(sql, (country, from_date, to_date))
    else:
        return frappe.get_all("Holiday Type", as_list=True)


@frappe.whitelist()
def get_holidays(country: str, holiday_type: str, from_date, to_date):
    return frappe.get_all(
        "Country Holiday",
        filters={
            "country": country,
            "holiday_type": holiday_type,
            "date": ["between", [from_date, to_date]],
        },
        fields=["date", "description"],
        order_by="date asc",
    )
