# Copyright (c) 2026, mohamedali456@gmail.com and contributors
# For license information, please see license.txt

# import frappe


import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
    def on_submit(self):
        self.db_set("status", "Completed")

    def on_change(self):
        if self.has_value_changed("gate_number"):
            frappe.enqueue(
                "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_ticket_gates",
                flight=self.name,
                gate_number=self.gate_number,
                queue="short",
                enqueue_after_commit=True,
            )


def update_ticket_gates(flight, gate_number):
    tickets = frappe.get_all("Airplane Ticket", filters={"flight": flight}, pluck="name")
    for name in tickets:
        frappe.db.set_value("Airplane Ticket", name, "gate_number", gate_number)
