# Copyright (c) 2026, mohamedali456@gmail.com and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document


class Shop(Document):
    def before_validate(self):
        if not self.rent_amount:
            self.rent_amount = frappe.db.get_single_value(
                "Shop Settings", "default_rent_amount"
            )
