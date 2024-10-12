import datetime
import os
from pathlib import Path
import hashlib
import json
from CTkMessagebox import CTkMessagebox


FOLDERPATH = Path(__file__).parent.parent.parent.resolve() / "src/resources/messages"
PATHTOCSVFOLDER= Path(__file__).parent.parent.resolve() / "resources/ListOfPeople"
MESSAGEJSONPATH = Path(__file__).parent.parent.resolve() / "resources/jsonMessages"

def addFile(oggetto, testo_base, persone):
    persone_list = [
        {"mail": mail, "TestoWatermark": watermark, "sha256": hashlib.sha256(watermark.encode('utf-8')).hexdigest()} for
        mail, watermark in persone.items()]

    messaggio = {
        "Oggetto": oggetto,
        "TestoBase": testo_base,
        "Persone": persone_list
    }
    timenow = (datetime.datetime.now()).strftime("%d-%m-%y %H.%M.%S")

    filename = oggetto + "(" + timenow + ")" + ".json"
    filePath = FOLDERPATH / filename

    with open(filePath, 'w', encoding='utf-8') as file:
        json.dump(messaggio, file, indent=4)


def generateCsv(textbox, name):
    name=name.replace(".csv", "")
    filename = name + ".csv"
    textbox=textbox.replace("\n", " ")
    textbox=textbox.replace("\t", " ")
    textbox=textbox.replace("Identifier", "")


    file = PATHTOCSVFOLDER / filename

    if file.is_file():
        os.remove(file)

    with open(file, "w") as f:
        f.write("Identifier\n")
        for mail in textbox.split():
            f.write(mail + "\n")
    CTkMessagebox(title="Success", message="File created successfully", sound=False, icon="check")
    return


def generateJson(obj, watermarkedDict):
    listapersone=[{"persona":person," watermarktext": wtext} for person,wtext in watermarkedDict.items()]

    with open(MESSAGEJSONPATH / f"{obj}.json", "w", encoding="utf-8") as f:
        json.dump(listapersone, f, indent=4)

