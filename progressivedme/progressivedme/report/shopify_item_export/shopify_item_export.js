// Copyright (c) 2016, Progressive DME and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Shopify Item Export"] = {
	"filters": [{
			"fieldname": "show_items_with_image",
			"fieldtype": "Check",
			"label": "Show Items With Image",
			"default": true,
		},{
			"fieldname": "item_group",
			"fieldtype": "Link",
			"options": "Item Group",
			"label": "Item Category",
	}]
}
