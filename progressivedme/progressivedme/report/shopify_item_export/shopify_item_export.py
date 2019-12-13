# Copyright (c) 2013, Progressive DME and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import scrub
from frappe.utils import flt, cint, cstr
import math

def execute(filters=None):
        return ShopifyItemExport(filters).run()

class ShopifyItemExport(object):
        
        def __init__(self, filters):
                self.filters = frappe._dict(filters or {})

        def run(self):
                columns = self.get_columns()
                data = []
                items = self.get_items()
                for key in sorted(items.keys()):
                        item = items[key]
                        item_price = (math.trunc(item.list_price)-1) + 0.99
                        data.append({
                                "handle": item.name,
                                "title": item.item_name,
                                "body_html": item.extended_description,
                                "vendor": item.vendor,
                                "type": item.item_group,
                                "variant_price": item_price,
                                "list_price": item.list_price,
                                "variant_taxable": "",
                                "standard_price": item.standard_price,
                                "option1_value": "%s - Height: %s x Width: %s "%(item.item_name, item.product_height, item.product_width), 
                                "image_src": "https://navdeepghai1.info%s"%(item.image) if item.image else "",
                                "image_position": 1,
                                "image_alt_text": item.item_name,
                                "seo_title": item.item_name,
                                "seo_description": item.extended_description,
                        })

                return columns, data

        def get_items(self):
                conditions = ""
                if self.filters.get("show_items_with_image"):
                        conditions += " AND `tabItem`.image IS NOT NULL "
                items = frappe._dict()
                for item in frappe.db.sql(""" SELECT `tabItem`.name, `tabItem`.item_group,
                            `tabItem`.item_name, `tabItem`.description, `tabItem`.extended_description,
                            `tabItem`.vendor_number as vendor, `tabItem`.image
                            FROM
                                    `tabItem`
                            WHERE
                                    `tabItem`.disabled = 0 %s 
                            """%(conditions), as_dict=True):
                        items.setdefault(item.name, item)

                self.update_price_list_for_items("Standard Price", items)
                self.update_price_list_for_items("List Price", items)
                return items

        def update_price_list_for_items(self, price_list, items):
                fieldname = scrub(price_list)
                for item_price in frappe.db.sql(""" SELECT `tabItem Price`.price_list_rate,
                            `tabItem Price`.item_code
                            FROM `tabItem Price` WHERE price_list = '%s' """%(price_list), as_dict=True):
                        if item_price.item_code in items:
                                items[item_price.item_code][fieldname] = item_price.get("price_list_rate")

        def get_columns(self):
                return [{
                            "fieldname": "handle",
                            "label": "Handle",
                            "fieldtype": "Data",
                            "width": 200,
                        },{
                            "fieldname": "title",
                            "label": "Title",
                            "fieldtype": "Data",
                            "width": 200,
                        },{
                            "fieldname": "body_html",
                            "fieldtype": "Data",
                            "label": "Body (HTML)",
                            "width": 200,
                        },{
                            "fieldname": "vendor",
                            "fieldtype": "Data",
                            "label": "Vendor",
                            "width": 100
                        },{
                            "fieldtype": "Data",
                            "fieldname": "type",
                            "label": "Type",
                            "width": 150,
                        },{
                            "fieldname": "variant_price",
                            "fieldtype": "Float",
                            "label": "Variant Price",
                            "width": 120,
                        },{
                            "fieldname": "list_price",
                            "fieldtype": "Float",
                            "label": "List Price",
                            "width": 120,
                        },{
                            "fieldname": "standard_price",
                            "fieldtype": "Float",
                            "label": "Standard Price",
                            "width": 100,
                        },{
                            "fieldname": "option1_value",
                            "fieldtype": "Data",
                            "label": "Option1 Value",
                            "width": 120,

                        },{
                            "fieldname": "image_src",
                            "fieldtype": "Data",
                            "label": "Image Src",
                            "width": 200,
                        },{
                            "fieldname": "variant_taxable",
                            "fieldtype": "Data",
                            "label": "Variant Taxable",
                            "width": 80
                        },{
                            "fieldname": "image_position",
                            "fieldtype": "Int",
                            "label": "Image Position",
                            "width": 70,
                        },{
                            "fieldname": "image_alt_text",
                            "fieldtype": "Data",
                            "label": "Image Alt Text",
                            "width": 200,
                        },{
                            "fieldname": "seo_title",
                            "fieldtype": "Data",
                            "label": "SEO Title",
                            "width": 200,
                        },{
                            "fieldname": "seo_description",
                            "fieldtype": "Data",
                            "label": "SEO Description",
                            "width": 200
                }]
