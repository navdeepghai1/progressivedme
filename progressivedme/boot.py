'''
        Developer Navdeep
        Email navdeepghai1@gmail.com
'''

import frappe

def update_boot_context(context):
        
        context.update({
                "progressivedme": {
                }
        });



def get_all_sub_categories():
        categories = []

        for c in frappe.db.sql("""SELECT `tabItem`.item_group """):
                pass
