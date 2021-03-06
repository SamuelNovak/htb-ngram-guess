import re
import json
from requests import request


regex = re.compile(b"var data = (.*);")

def remove_tag(s):
    return " ".join([w.split("_")[0] if "_" in w else w for w in s.split(" ")])

def load_ngram_data(expr:str, year:int):
    req = request("GET", "https://books.google.com/ngrams/graph?content={}&year_start={}&year_end={}&corpus=15&smoothing=0".format(expr.replace(" ", "+"), year, year+1))
    if req.ok:
        raw = req.content
        data = json.loads(re.findall(regex, raw)[0].decode("utf-8"))
        return [(remove_tag(i["ngram"]), i["timeseries"][0]) for i in data if "*" not in i["ngram"]]
    else:
        return None