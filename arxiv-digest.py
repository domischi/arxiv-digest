#!/usr/bin/python3
import re
import sys
import os
import datetime
from settings import FOLLOWED_AUTHORS, SAVE_DIR

s = sys.stdin.read().replace("\r", "", int(1e6))
#with open('ar.txt', 'r') as f:
#    s=f.read()
#s=s.replace("\r", "", int(1e6))

out = ""

MATCHING_REGEX = "^arXiv:(?P<arxiv_id>\d\d\d\d\.\d\d\d\d\d).*?Title: (?P<title>.*?)\nAuthors: (?P<authors>.*?)\nCategories:"
DATE_REGEX = "received from  (?P<start_date_string>.*)  to  (?P<end_date_string>.*)"

matches = re.finditer(DATE_REGEX, s)
for m in matches:
    gd = m.groupdict()
    break
start_date = datetime.datetime.strptime(
    gd["start_date_string"], "%a %d %b %y %H:%M:%S %Z"
)
end_date = datetime.datetime.strptime(gd["end_date_string"], "%a %d %b %y %H:%M:%S %Z")
start_date = str(start_date.date())
end_date = str(end_date.date())


def print_group_dict(d, with_authors=False):
    d["title"] = d["title"].replace("\n", "", 10)
    d["authors"] = d["authors"].replace("\n", "", 10)
    ret = f"{d['arxiv_id']}: {d['title']} (https://arxiv.org/abs/{d['arxiv_id']})\n"
    if with_authors:
        ret += f"{d['authors']}\n"
    return ret


matches = re.finditer(MATCHING_REGEX, s, flags=re.DOTALL | re.MULTILINE)
for i,m in enumerate(matches):
    d = m.groupdict()
    out += print_group_dict(d)
    ## Add an empty line every 16 entries, just to make it more readable
    if (i+1)%16==0:
        out += '\n'

author_matches = 0
matches = re.finditer(MATCHING_REGEX, s, flags=re.DOTALL | re.MULTILINE)
out += "\n"
for m in matches:
    d = m.groupdict()
    for a in FOLLOWED_AUTHORS:
        if re.search(r"\b" + a + r"\b", d["authors"]):
            author_matches += 1
            out += "\n" + "*" * 50 + "\n" + f"{a} published something:\n"
            out += print_group_dict(d, with_authors=True)
            out += "\n" + "*" * 50 + "\n"
out += f"Today were {author_matches} author matches registered."
out += '\n'*5

os.makedirs(SAVE_DIR, exist_ok=True)
with open(f"{SAVE_DIR}/arxiv-digest-{end_date}.txt", "a") as f:
    f.write(out)
