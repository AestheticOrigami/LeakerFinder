import hashlib
import json
import os
from pathlib import Path
import editdistance

FOLDERPATH = Path(__file__).parent.parent.resolve() / "resources/messages"


def find(text, filename=None):
    text = text.strip()
    hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
    if filename is not None:
        with open(filename, 'r', encoding='utf-8') as f:
            topscore=None
            finalperson=None
            data = json.load(f)
            for person in data["Persone"]:
                if person["sha256"] == hash:
                    return person, filename.stem
                else:
                    score = editdistance.eval(text, person["TestoWatermark"])
                    if topscore is None or score < topscore:
                        topscore = score
                        finalperson = person
            return finalperson, filename.stem
    else:
        filelist = os.listdir(FOLDERPATH)
        rightfile = None
        bestscore = None

        for file in filelist:
            filepath = FOLDERPATH / file

            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                score = editdistance.eval(text, data["TestoBase"])
                if bestscore is None or score < bestscore:
                    bestscore = score
                    rightfile = filepath

        return find(text,rightfile)