'''
	Developer Navdeep
	Email navdeepghai1@gmail.com
'''
import frappe
import click
from frappe.commands import pass_context

@click.command()
@click.argument("filename")
@pass_context
def read_data(context, filename):
	if(context.get("sites")):
		for site in context.get("sites") or []:
			if site == "progressivedme.com":
				frappe.init(site)
				frappe.connect()
	else:
		return
	from progressivedme.read_excel_data import read_csv_data
	update_subgroup(read_csv_data(context, filename))
	frappe.db.commit()
	# COMMIT THE CHANGES

def update_subgroup(data):
	for item in data:
		item_number = item.item_number
		minor_category = item.minor_category
		major_category = item.major_category
		if (item_number and minor_category and major_category
				and frappe.db.get_value("Item Group"), major_category):
			try:
				if(minor_category and not frappe.db.exists("Item Group", minor_category)):
			
					frappe.get_doc({
						"item_group_name": minor_category,
						"parent_item_group": major_category,
						"doctype": "Item Group",
					}).save(ignore_permissions=True)
				
				if(frappe.db.exists("Item Group", minor_category)):
					frappe.db.sql("UPDATE `tabItem Group` SET is_group=1 WHERE name = '%s' "%(major_category))
					frappe.db.sql(""" UPDATE `tabItem` SET item_group = '%s' WHERE name = '%s' 
							"""%(minor_category, item_number))
					print("Item: %s, Updated"%(item_number))

			except Exception as e:
				print("an error occurred while processing the item")
				print(e)	
		else:
			print("Missing Information for Item: %s"%(item_number))
			


commands = [read_data]
