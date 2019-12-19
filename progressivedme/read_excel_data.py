'''
	Developer Navdeep
	Email navdeepghai1@gmail.com
'''

import frappe
from frappe.utils import flt, cstr, cint, getdate, nowdate
from frappe import (_, msgprint, throw, get_app_path,
		scrub)
import os
from os.path import exists, isdir, isfile
import pandas as pd

APP_NAME = "progressivedme"
DATA_FOLDER = "patches_data"
def read_csv_data(context, filename):
	app_path = get_app_path(APP_NAME)
	file_path = "/".join([app_path, DATA_FOLDER, filename])
	if not(exists(file_path)):
		print("File %s doesn't exists on path :%s "%(filename, file_path))
		return
	print(file_path)
	return read_data(pd.read_excel(file_path))

def read_data(pd_csv_object):	
	columns = get_columns(pd_csv_object)
	return map_columns_with_values(columns, pd_csv_object.values)

def map_columns_with_values(columns, values):
	data = []
	for val in values:
		temp = frappe._dict()
		for idx, col in enumerate(columns):
			temp[col] = val[idx]
		data.append(temp)
	return data
		
def get_columns(pd_csv_object):
	columns = []
	for column in pd_csv_object.columns:
		columns.append(scrub(column.replace(".", "").replace("-", "_").replace(" ", "_").replace("`", "")))
	return columns
		
		
	
