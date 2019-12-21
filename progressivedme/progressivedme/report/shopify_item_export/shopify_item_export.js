// Copyright (c) 2016, Progressive DME and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Shopify Item Export"] = {
	"filters": [{
			"fieldname": "show_items_with_image",
			"fieldtype": "Check",
			"label": __("Show Items With Image"),
			"default": true,
		},{
			"fieldname": "item_group",
			"fieldtype": "Link",
			"options": "Item Group",
			"label": __("Item Category(Major Category)"),
			"get_query": function(){
				return{
					"filters":{
						"is_group": 1
					}
				}
			}
		},{
			"fieldname": "sub_item_group",
			"fieldtype": "Link",
			"options": "Item Group",
			"label": __("Sub Item Group(Minor Category)"),
			"get_query": function(){
				let parent_item_group = cur_page.page.page.fields_dict.item_group.get_value();
				let filters = {
					"is_group": 0
				};
				if(parent_item_group){
					$.extend(filters, {
						"parent_item_group": parent_item_group
					});
					return {
						"filters": filters
					}
				}
			}
		},{
			"fieldname": "start",
			"fieldtype": "Int",
			"label": __("Start"),
		},{
			"fieldname": "end",
			"fieldtype": "Int",
			"label": __("End"),
	}]
}
