import random

import frappe


def execute():
    tickets = frappe.get_all(
        "Airplane Ticket",
        filters={"seat": ["is", "not set"]},
        pluck="name",
    )
    for name in tickets:
        seat = f"{random.randint(1, 99)}{random.choice('ABCDE')}"
        frappe.db.set_value("Airplane Ticket", name, "seat", seat)
