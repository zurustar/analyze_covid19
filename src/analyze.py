#!/usr/bin/env python3

import sys
import os
import glob
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

d = sys.argv[1]
outputcsvfile = d + os.sep + sys.argv[2]
outputimgfile = d + os.sep + sys.argv[3]

# ファイルから読み込む。globを使うとワイルドカードで指定できる
df = pd.DataFrame()
for filename in glob.glob(d + os.sep + '*.csv'):
    if filename != outputcsvfile:
        df = pd.read_csv(filename, dtype=str)
# 文字列型になっている日付情報を日付型に変換
df['date'] = pd.to_datetime(df['公表_年月日'])
# 日付情報以外は不要なので絞り込む。二重の[]でカラムを抽出できる
df = df[['date']]
# インデックスが消えているので再構築。これをやらないとこの後のgroupby(〜).count()が想定通りにならない
df = df.reset_index()
# 陽性者数を算出(元データは1陽性者につき1レコードになっている)
df = df.groupby('date').count()
# このあとのmergeのためにインデックスになっている日付情報を普通の列にする
df = df.reset_index()
# indexという名前の列が陽性者数になっているので列名変更
df = df.rename(columns={'index': 'positive'})
# 日の数を数えたためゼロ人の日のデータがない状態になっているので、日付のリストを作ってJOINする
days = pd.date_range(start=df['date'].min()-datetime.timedelta(days=7),end=df['date'].max())
days = pd.DataFrame({'date': days})
df = pd.merge(days, df, how='left').fillna(0)
# 7日平均を追加
df['7days_mean'] = df['positive'].rolling(7).mean().fillna(0)
# CSVとして保存
df.to_csv(outputcsvfile)
# グラフの準備
fig = plt.figure(dpi=80, figsize=(16, 9))
ax = fig.add_subplot(1, 1, 1)
# 陽性者数のプロット
ax.plot(df['date'], df['positive'], color='blue', label='positive', linewidth=2)
# 七日間平均のプロット
ax.plot(df['date'], df['7days_mean'], color='red', label='7days-mean', linewidth=3, linestyle='-.')
# X方向の範囲指定
ax.set_xlim(df['date'].min(), df['date'].max())
# Y方向の範囲指定
ax.set_ylim(0, df['positive'].max()*1.1)
# X軸のラベルの設定
ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=None, interval=7, tz=None))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
ax.tick_params(axis='x', rotation=90)
# グリッド線表示
ax.grid()
# 判例表示
ax.legend(loc='upper left')
# 保存
plt.savefig(outputimgfile)
