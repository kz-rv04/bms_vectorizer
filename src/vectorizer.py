import pandas as pd
import numpy as np

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import os
import sys
from pprint import pprint

import re
bms_pattern = re.compile(
    r".*HEADER FIELD(?P<header>.*)" +
    r"\*+.+MAIN DATA FIELD(?P<main>.*)",
    re.S
)

header_pattern = re.compile(
    r"#PLAYER\s+(?P<PLAYER>\d+)\n"+
    r"#GENRE\s+(?P<GENRE>.+)\n"+
    r"#TITLE\s+(?P<TITLE>.+)\n"+
    r"#ARTIST\s+(?P<ARTIST>.+)\n"+
    r"#BPM\s+(?P<BPM>\d+)\n"+
    r"#PLAYLEVEL\s+(?P<PLAYLEVEL>\d+)\n"+
    r"#RANK\s+(?P<RANK>\d+)\n"+
    r"#TOTAL\s+(?P<TOTAL>\d+)\n"+
    r"#STAGEFILE\s+(?P<STAGEFILE>.+)\n"
)

main_pattern = re.compile(
    r"#(?P<BARNUMBER>\d{3})"+
    r"(?P<CHANNEL>\d{2}):"+
    r"(?P<DATA>[0-9a-fA-F]+)"
)
# 1小節あたりの分解能（9600分音符まで表現可能）これをもとに譜面内の時間を求める
BMS_COUNT = 9600

def to_bms_time(row):
    note_resolution = len(row['DATA'])/2
    return [BMS_COUNT*(int(row['BARNUMBER'])-1)+int(BMS_COUNT/note_resolution)*n for n, note in enumerate(re.split(r"(..)", row['DATA'])[1::2]) if note!='00']

def load_bms(path):
    with open(path, mode="r") as f:
        s = f.read()
    match = bms_pattern.match(s)
    if match:
        match = match.groupdict()
        header = match.get("header").strip()
        main = match.get("main").strip()
    else:
        print(path, "not match")
    music_info = header_pattern.match(header).groupdict()
    pprint(music_info)
    df = pd.DataFrame.from_dict([main_pattern.match(line).groupdict() for line in main.split()], orient="columns").astype({"BARNUMBER": int, "CHANNEL": int})
    # http://www.charatsoft.com/develop/otogema/page/04bms/bms_struct.htm
    # 各チャネルに何部音符が入っているかをBMSカウント値（9600）を使って表現する
    # 例 #001(小節目)15（5鍵）:1700000000000018 len(16)/2=8分音符の場合 1拍目と8拍目（n拍目）に値が入っているので
    # [9600*1+9600/8*(1-1), 9600*1+9600/8*(8-1)] となる
    # つまり、9600*(BARNUMBER-1)+9600/(len(DATA)/2)*nが求める値
    print(df.head())
    df = df.query("10< CHANNEL < 20")
    df['bms_time'] = df.apply(lambda r: to_bms_time(r),axis=1)
    df_grouped = df.groupby('CHANNEL')
    for g in df_grouped:
        print(g)


def main():
    path = "../data/as_air_extreme.bme"
    load_bms(path=path)

if __name__=="__main__":
    main()