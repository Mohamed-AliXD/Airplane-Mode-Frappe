# Copyright (c) 2026, mohamedali456@gmail.com and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe import _
from frappe.model.document import Document


class ShopContract(Document):
    def validate(self):
        if self.expiry_date <= self.start_date:
            frappe.throw(_("Expiry Date must be after Start Date."))

    def on_update(self):
        active = self.status == "Active"
        frappe.db.set_value(
            "Shop",
            self.shop,
            {
                "status": "Occupied" if active else "Available",
                "tenant": self.tenant if active else None,
            },
        )

    def on_trash(self):
        frappe.db.set_value("Shop", self.shop, {"status": "Available", "tenant": None})
