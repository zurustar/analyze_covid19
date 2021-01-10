# analyze_covid19

東京都が公開している新型コロナウイルス感染者数を記したcsvファイルをちょこっと加工してexcelで感染者数の推移を示すグラフを作成しやすくするだけのツール。

## 使い方

srcディレクトリ内に分析対象のcsvファイルを置いてから、
docker-compose up
を実行するとsrcディレクトリ内に出力されるresult.csvというファイルをExcelで読み込んでグラフを描くなどすることを想定。

今日時点では以下のURLに対象となるファイルがおいてあった。
https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients.csv

