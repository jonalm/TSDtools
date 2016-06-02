from __future__ import print_function
import pandas as pd
import numpy as np
from os.path import join as joinpath
from os.path import dirname

TSDINFOFILE = "/tsd/p33/data/durable/LRP Genetics Database/LRP_GENETICS-25.04.16-I_deCODE_clean.txt"    
MOCKINFOFILE = joinpath(dirname(__file__), "../mockdata/info")

def getcontrolID(fin):
    cols = ["PN", "Diagnose"]
    df = pd.read_csv(fin, sep="\t", usecols=cols)

    # capitalize all entries
    for col in cols:
        df[col] = map(lambda x: str(x).upper(), df[col])

    for nantag in ["___NA___", "UNKNOWN", "OTHER", "?", "??","ANNET", "0"]:
        df = df.replace(nantag, "NaN")

    for controltag in ["KONTROLL", "NORMAL CONTROL"]:
        df = df.replace(controltag, "CON")

    return set(df.loc[df["Diagnose"] == "CON"]["PN"])

if __name__=="__main__":
    control = getcontrolID(TSDINFOFILE)
    with open("controls", "w") as fout:
        for c in control:
            print(c, file=fout)
