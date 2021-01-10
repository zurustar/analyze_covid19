#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import glob
import sys
import os
import datetime

def main(d, outputcsvfile, outputimgfile):
    srclabel = '公表_年月日'
    df = pd.DataFrame()
    for filename in glob.glob(d + os.sep + "*.csv"):
        if filename != d + os.sep + outputcsvfile:
            tmp = pd.read_csv(filename, dtype=str).fillna(0)
            if df.empty:
                df = tmp
            else:
                df = pd.concat([df, tmp])
    s = pd.to_datetime(df[srclabel]).value_counts()
    df = pd.DataFrame(s)
    df = df.rename(columns={srclabel: 'positive'})
    df['date'] = df.index
    mindate = min(df.index)-datetime.timedelta(days=7)
    maxdate = max(df.index)
    dates = pd.date_range(start=mindate, end=maxdate, freq='D')
    df2 = pd.DataFrame({'date': dates})
    df = pd.merge(df2, df, how='left').fillna(0)
    df['7days_mean'] = df['positive'].rolling(7).mean().fillna(0)
    df.to_csv(d + os.sep + outputcsvfile)
    #
    fig = plt.figure(dpi=100, figsize=(16, 9))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(df['date'], df['positive'], color='blue')
    ax.plot(df['date'], df['7days_mean'], color='red')
    plt.savefig(d + os.sep + outputimgfile)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
