#!/usr/bin/env python
# -*-coding:utf-8-*-
# File Name     : parse.py
# Description   :
# Author        :
# Creation Date : 2019-03-26
# Last Modified : 2019年03月26日 星期二 17时04分03秒
# Created By    : lsl
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号


def main():
    df = pd.read_csv("./roommate.csv")
    df["性别"] = df["性别"].map(lambda x: x.strip())
    df = pd.read_csv("./roommate.csv")
    df["性别"] = df["性别"].map(lambda x: x.strip())
    df = df[(df["性别"] == "man") | (df["性别"] == "woman")]
    df["性别"].value_counts().plot.pie()
    plt.show()
    df[(df["职业"] != "…") & (df["职业"] != "...") & (df["职业"] != "未知")][
        "职业"
    ].value_counts().head(10).plot.pie()
    plt.show()


if __name__ == "__main__":
    main()
