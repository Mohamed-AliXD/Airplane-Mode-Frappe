# Copyright (c) 2026, mohamedali456@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder.functions import IfNull, Sum


def execute(filters=None):
    columns = get_columns()
    data = get_data()
    return columns, data, None, get_chart(data), get_summary(data)


def get_columns():
    return [
        {"label": _("Airline"), "fieldname": "airline", "fieldtype": "Link", "options": "Airline", "width": 220},
        {"label": _("Revenue"), "fieldname": "revenue", "fieldtype": "Currency", "width": 160},
    ]


def get_data():
    Airline = frappe.qb.DocType("Airline")
    Airplane = frappe.qb.DocType("Airplane")
    Flight = frappe.qb.DocType("Airplane Flight")
    Ticket = frappe.qb.DocType("Airplane Ticket")

    return (
        frappe.qb.from_(Airline)
        .left_join(Airplane).on(Airplane.airline == Airline.name)
        .left_join(Flight).on(Flight.airplane == Airplane.name)
        .left_join(Ticket).on((Ticket.flight == Flight.name) & (Ticket.docstatus == 1))
        .select(Airline.name.as_("airline"), IfNull(Sum(Ticket.total_amount), 0).as_("revenue"))
        .groupby(Airline.name)
        .run(as_dict=True)
    )


def get_chart(data):
    return {
        "data": {
            "labels": [d.airline for d in data],
            "datasets": [{"values": [d.revenue for d in data]}],
        },
        "type": "donut",
    }


def get_summary(data):
    total = sum(d.revenue for d in data)
    return [{"value": total, "label": _("Total Revenue"), "datatype": "Currency", "indicator": "Green"}]
