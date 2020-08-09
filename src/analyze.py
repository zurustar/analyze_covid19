#!/usr/bin/env python3

import pandas as pd
import glob
import sqlite3
import sys
import os

def main(d):
	output_filename = d + os.sep + "result.csv"
	db = sqlite3.connect(':memory:')
	for filename in glob.glob(d + os.sep + "*.csv"):
		if filename == output_filename:
			continue
		print("loading", filename)
		tmp = pd.read_csv(filename, dtype=str)
		tmp['date'] = pd.to_datetime(tmp['公表_年月日'])
		tmp.to_sql('covid19', db, if_exists='append', index=None)
	df = pd.read_sql_query('SELECT date, count(date) FROM covid19 group by date;', db)
	df.to_csv(output_filename)
	db.close()

if __name__ == '__main__':
	main(sys.argv[1])
