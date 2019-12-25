# Copyright (c) 2013, Progressive DME and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import scrub, _
from frappe.utils import flt, cint, cstr, getdate, nowdate
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
				"body_html": item.extended_description if item.extended_description != "nan" else item.item_name,
				"vendor": item.vendor,
				"type": item.item_group,
				"variant_price": item_price,
				"list_price": item.list_price,
				"variant_taxable": "",
				"tags":" ".join([item.sub_item_group]),
				"variant_inventory_cost": item.standard_price,
				"image_src": "https://navdeepghai1.info%s"%(item.image) if item.image else "",
				"image_position": 1,
				"image_alt_text": item.item_name,
				"seo_title": item.item_name,
				"seo_description": item.extended_description,
				"published": item.published,
                                "variant_weight": item.item_weight,
                                "variant_weight_unit": "lb",
                                "published_scope": "Web",
                                "published_at": getdate(item.date_established).strftime("%Y-%m-%dT00:00:00-00:00")
			})

		return columns, data

	def get_items(self):
		conditions = ""
		limits = ""
		if self.filters.get("start") or self.filters.get("end"):
			limits += " LIMIT "
			if self.filters.get("start"):
				limits += " %s"%(self.filters.get("start"))
			if self.filters.get("start") and self.filters.get("end"):
				limits += ",%s"%(self.filters.get("end"))

		if self.filters.get("show_items_with_image"):
			conditions += " AND `tabItem`.image IS NOT NULL "
		else:
			conditions += " AND `tabItem`.image IS NULL "
		if self.filters.sub_item_group:
			conditions += " AND `tabItem`.item_group = '%s' "%(self.filters.sub_item_group)
		if self.filters.item_group and not self.filters.sub_item_group:
			conditions += """ AND `tabItem`.item_group IN (SELECT `tabItem Group`.name FROM `tabItem Group`
					WHERE `tabItem Group`.parent_item_group = '%s')"""%(self.filters.item_group)
		items = frappe._dict()
		for item in frappe.db.sql(""" SELECT `tabItem`.name,
				`tabItem`.item_name, `tabItem`.description, `tabItem`.extended_description,
				`tabItem`.vendor_number as vendor, `tabItem`.image,
				`tabItem Group`.parent_item_group AS item_group,
				`tabItem Group`.name as sub_item_group,
				'TRUE' AS published,
                                `tabItem`.item_weight,
				(SELECT `tabItem Price`.price_list_rate FROM `tabItem Price`
					WHERE `tabItem Price`.item_code = `tabItem`.name AND
						`tabItem Price`.price_list = '%s' LIMIT 1) AS list_price,
				(SELECT `tabItem Price`.price_list_rate FROM `tabItem Price`
					WHERE `tabItem Price`.item_code = `tabItem`.name AND
						`tabItem Price`.price_list = '%s' LIMIT 1) AS standard_price
				FROM
					`tabItem` INNER JOIN `tabItem Group`
				ON
					`tabItem`.item_group = `tabItem Group`.name
				WHERE
					`tabItem`.disabled = 0 %s
				ORDER BY
					`tabItem`.name, `tabItem Group`.parent_item_group %s
				"""%('List Price', 'Standard Price', conditions, limits), as_dict=True):
			items.setdefault(item.name, item)

		return items

	def get_columns(self):
		return [{
				"fieldname": "handle",
				"label": "Handle",
				"fieldtype": "Link",
                                "options": "Item",
				"width": 100,
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
				"fieldname": "tags",
				"fieldtype": "Data",
				"label": _("Tags"),
				"width": 150,
			},{
                                "fieldname": "template_suffix",
                                "fieldtype": "Data",
                                "label": "Template Suffix",
                                "width": 150
                        },{
                                "fieldname": "published_scope",
                                "fieldtype": "Data",
                                "label": "Published Scope",
                                "width": 150
                        },{
                                "fieldname": "published",
                                "fieldtype": "Data",
                                "label": "Published",
                                "width": 150,
                        },{
                                "fieldname": "published_at",
                                "fieldtype": "Data",
                                "label": "Published At",
                                "width": 150,
                        },{
                                "fieldname": "option1_name",
                                "fieldtype": "Data",
                                "label": "Option1 Name",
                                "width": 150
                        },{
                                "fieldname": "option1_value",
                                "fieldtype": "Data",
                                "label": "Option1 Value",
                                "width": 150
                        },{
                                "fieldname": "option2_name",
                                "fieldtype": "Data",
                                "label": "Option2 Name",
                                "width": 150
                        },{
                                "fieldname": "option2_value",
                                "fieldtype": "Data",
                                "label": "Option2 Value",
                                "width": 150
                        },{
                                "fieldname": "option3_name",
                                "fieldtype": "Data",
                                "label": "Option3 Name",
                                "width": 150
                        },{
                                "fieldname": "option3_value",
                                "fieldtype": "Data",
                                "label": "Option3 Value",
                                "width": 150
                        },{
                                "fieldname": "variant_sku",
                                "fieldtype": "Data",
                                "label": "Variant SKU",
                                "width": 150,
                        },{
                                "fieldname": "metafields_global_title_tag",
                                "fieldtype": "Data",
                                "label": "Metafields Global Title Tag",
                                "width": 250
                        },{
                                "fieldname": "metafields_global_description_tag",
                                "fieldtype": "Data",
                                "label": "Metafields Global Description Tag",
                                "width": 250
                        },{
                                "fieldname": "metafields_namespace",
                                "fieldtype": "Data",
                                "label": "Metafields Namespace",
                                "width": 150
                        },{
                                "fieldname": "metafield_key",
				"fieldtype": "Data",
				"label": "Metafield Key",
				"width": 120,
                        },{
				"fieldname": "metafield_value",
				"fieldtype": "Data",
				"label": "Metafield Value",
				"width": 120, 
                        },{
				"fieldname": "metafield_value_type",
				"fieldtype": "Data",
				"label": "Metafield Value Type",
				"width": 200,
                        },{
				"fieldname": "variant_grams",
				"fieldtype": "Data",
				"label": "Variant Grams",
				"width": 120,
			},{
				"fieldname": "variant_inventory_tracker",
				"fieldtype": "Data",
				"label": "Variant Inventory Tracker",
				"width": 200,
			},{
				"fieldname": "variant_inventory_qty",
				"fieldtype": "Data",
				"label": "Variant Inventory Qty",
				"width": 200
			},{
				"fieldname": "variant_inventory_policy",
				"fieldtype": "Data",
				"label": "Variant Inventory Policy",
				"width": 200,
			},{
				"fieldname": "variant_inventory_cost",
				"fieldtype": "Currency",
				"label": "Variant Inventory Cost",
				"width": 200,
			},{
				"fieldname": "variant_fulfillment_service",
				"fieldtype": "Data",
				"label": "Variant Fulfillment Service",
				"width": 200,
			},{
				"fieldname": "variant_price",
				"fieldtype": "Currency",
				"label": "Variant Price",
				"width": 120,
                        },{
				"fieldname": "variant_compare_at_price",
				"fieldtype": "Data",
				"label": "Variant Compare At Price",
				"width": 150,
                        },{
				"fieldname": "variant_require_shipping",
				"fieldtype": "Data",
				"label": "Variant Require Shipping",
				"width": 150, 
                        },{
				"fieldname": "variant_taxable",
				"fieldtype": "Data",
				"label": "Variant Taxable",
				"width": 120,
                        },{
				"fieldname": "variant_barcode",
				"fieldtype": "Data",
				"label": "Variant Barcode",
				"width": 120,
			},{
				"fieldname": "image_attachment",
				"fieldtype": "Data",
				"label": "Image Attachment",
				"width": 200,
			},{
				"fieldname": "image_src",
				"fieldtype": "Data",
				"label": "Image Src",
				"width": 200
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
				"fieldname": "variant_image",
				"fieldtype": "Data",
				"label": "Variant Image",
				"width": 200,
			},{
				"fieldname": "variant_weight",
				"fieldtype": "Float",
				"label": "Variant Weight",
				"width": 200,
                        },{
				"fieldname": "variant_weight_unit",
				"fieldtype": "Data",
				"label": "Variant Weight Unit",
				"width": 200,
                        },{
				"fieldname": "variant_tax_code",
				"fieldtype": "Data",
				"label": "Variant Tax Code",
				"width": 200,

		}]
