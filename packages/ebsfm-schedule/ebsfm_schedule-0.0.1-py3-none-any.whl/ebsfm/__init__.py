from datetime import datetime

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


def schedule(channel, date=""):
    """
    EBS FM, EBS 외국어전문 방송의 편성표를 가져옵니다.
    :param channel: RADIO - EBS FM 채널, IRADIO - EBS 외국어전문 방송
    :param date: yyyyMMdd 형식의 편성표를 가져올 기준일, 생략시 오늘
    :return: DataFrame
    """
    response = requests.get(f"https://www.ebs.co.kr/schedule?channelCd={channel}&onor={channel}&date={date}")
    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.find("ul", "main_timeline").select("li")

    def parse_item(item):
        time = item.find("span", "").text.strip()
        title = item.find("strong").text.strip()
        desc = item.find("span", "txt_cnt").text.strip()
        return {"time": time, "title": title, "desc": desc}

    date = datetime.now().strftime("%Y%m%d") if date == "" else date

    def set_datetime(row):
        time = row["time"]
        if int(time[:2]) > 23:
            time = '0' + str(int(time[:2]) - 24) + time[2:]
            row["dt"] = datetime.strptime(date + " " + time, "%Y%m%d %H:%M")
            row["dt"] = row["dt"] + pd.DateOffset(days=1)
        else:
            row["dt"] = datetime.strptime(date + " " + time, "%Y%m%d %H:%M")

        return row

    dict_list = [parse_item(item) for item in items]
    df = pd.DataFrame(dict_list)

    df = df.apply(set_datetime, axis=1)

    df["end"] = df["dt"].shift(-1)

    df = df[df["title"].str[:2] != "정파"]
    df = df[df["title"] != "라디오 캠페인"]

    df["end"] = df["end"].fillna(df["time"])

    df["duration(s)"] = ((pd.to_datetime(df["end"]) - pd.to_datetime(df["dt"])) / np.timedelta64(1, 's')).astype("int")
    df["date"] = df["dt"].dt.date
    df = df[["date", "time", "duration(s)", "title", "desc", "dt"]]
    return df
