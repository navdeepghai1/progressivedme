'''
        Developer Navdeep
        Email navdeepghai1@gmail.com
'''
import frappe
import os
from os.path import exists, isfile, isdir, getsize

def process():
        HOME = "/home/progressivedme/progressivedme/sites/progressivedme.com/public/files"
        if not(exists(HOME)):
                print("path doesn't exists")
                return
        total_items = 1
        for item in frappe.db.sql(""" SELECT `tabItem`.name,
                    `tabItem`.temp_image, `tabItem`.image, `tabItem`.item_code,
                    `tabItem`.item_name FROM `tabItem`
                    """, as_dict=True):
            extn = "jpg"
            extn1 = "JPG"
            _file = "%s/%s.%s"%(HOME, item.get("name"), extn)
            _file1 = "%s/%s.%s"%(HOME, item.get("name"), extn1)
            flag = False
            temp = None
            if(isfile(_file)):
                    flag = True
                    temp = _file
            elif(isfile(_file1)):
                    temp = _file1
                    flag = True
            if not flag or not exists(temp):
                continue
            file_name = temp.split("/")[-1]
            name = file_name.replace(".jpg", "").replace(".JPG", "")
            file_url = "/files/%s"%(file_name)
            d = frappe.get_doc({
                "doctype": "File",
                "file_size": getsize(temp),
                "file_url": file_url,
                "attached_to_doctype": "Item",
                "attached_to_name": item.get("name"),
                "file_name": file_name,
                "folder": "Home/ItemImages",
                "thumbnail_url": file_url,
            })
            d.flags.ignore_folder_validate = True
            d.save()
            frappe.db.sql(""" UPDATE `tabItem` SET image = '%s' where name = '%s' """%(file_url, item.get("name")))
            print("saving file: %s "%(name))

