# Copyright (c) 2026, mohamedali456@gmail.com and contributors
# For license information, please see license.txt

# import frappe

import random

import frappe
from frappe import _
from frappe.model.document import Document


class AirplaneTicket(Document):
    def before_insert(self):
        self.validate_capacity()
        self.seat = f"{random.randint(1, 99)}{random.choice('ABCDE')}"

    def validate(self):
        self.remove_duplicate_add_ons()
        self.calculate_total()

    def before_submit(self):
        if self.status != "Boarded":
            frappe.throw(_("You can only submit a ticket when its status is Boarded."))

    def validate_capacity(self):
        airplane = frappe.db.get_value("Airplane Flight", self.flight, "airplane")
        capacity = frappe.db.get_value("Airplane", airplane, "capacity") or 0
        booked = frappe.db.count(
            "Airplane Ticket",
            {"flight": self.flight, "docstatus": ["!=", 2]},
        )
        if booked >= capacity:
            frappe.throw(_("This flight is full. Capacity is {0} seats.").format(capacity))

    def remove_duplicate_add_ons(self):
        seen, unique = set(), []
        for row in self.add_ons:
            if row.item not in seen:
                seen.add(row.item)
                unique.append(row)
        self.set("add_ons", unique)
        for i, row in enumerate(self.add_ons, start=1):
            row.idx = i

    def calculate_total(self):
        self.total_amount = (self.flight_price or 0) + sum(
            (row.amount or 0) for row in self.add_ons
        )
