#!/usr/bin/env python3

import pandas as pd
import glob
import sqlite3

def main(d):
	db = sqlite3.connect(':memory:')
	for filename in glob.glob(d):
		df = pd.read_csv(filename, dtype=str)
		df['date'] = pd.to_datetime(df['公表_年月日'])
		df.to_sql('covid19', db, if_exists='append', index=None)
	df = pd.read_sql_query('SELECT date, count(date) FROM covid19 group by date;', db)
	db.close()
	df.to_csv("./tmp.csv", header=None, index=None)

if __name__ == '__main__':
	main('./*.csv')
