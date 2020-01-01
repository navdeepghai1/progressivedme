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
		},{
			"fieldname": "drop_ship_legend",
			"fieldtype": "Select",
			"options": ["N", "O", "S"],
			"default": "N",
			"label": __("Drop Ship Legend"),
		},{
			"fieldname":"exclude_categories",
			"label": __("Exclude Categories"),
			"fieldtype": "MultiSelect",
			get_data: function() {
				var projects = frappe.query_report.get_filter_value("exclude_categories") || "";

				const values = projects.split(/\s*,\s*/).filter(d => d);
				const txt = projects.match(/[^,\s*]*$/)[0] || '';
				let data = [];

				frappe.call({
					type: "GET",
					method:'frappe.desk.search.search_link',
					async: false,
					no_spinner: true,
					args: {
						doctype: "Item Group",
						txt: txt,
						filters: {
							"name": ["not in", values]
						}
					},
					callback: function(r) {
						data = r.results;
					}
				});
				return data;
			},
			"default": "CBD Products, Custom Catalogue Program"
	
	}]
}
