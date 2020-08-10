#!/usr/bin/env python3

import pandas as pd
import glob
import sqlite3
import sys
import os
from datetime import date

def main(d):
	output_filename = d + os.sep + "result.csv"
	db = sqlite3.connect(':memory:')
	#db = sqlite3.connect(d + os.sep + "debug.db")
	df = None
	for filename in glob.glob(d + os.sep + "*.csv"):
		if filename == output_filename:
			continue
		print("loading", filename)
		tmp = pd.read_csv(filename, dtype=str)
		tmp['date'] = pd.to_datetime(tmp['公表_年月日'])
		tmp = tmp.loc[:,['date']]
		if df == None:
			df = tmp
		else:
			df = pd.concat([df, tmp], axis=0)
	df = df.assign(counter=1)
	dt = pd.date_range('2020-01-01', date.today(),  freq='D')
	dt = dt.to_frame(index=False, name="date").assign(counter=0)
	df = pd.concat([df, dt], axis=0)
	df.to_sql('covid19', db, if_exists='append', index=None)
	df = pd.read_sql_query('SELECT date, SUM(counter) AS counter FROM covid19 group by date;', db)
	df.to_csv(output_filename)
	db.close()

if __name__ == '__main__':
	main(sys.argv[1])
