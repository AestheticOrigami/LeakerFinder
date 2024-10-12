import json
from pathlib import Path
from argon2 import PasswordHasher

SECRET_FILE = Path(__file__).parent.parent.resolve() / "secret.json"


def loginCheck(passwordbox):
    pswPlain = passwordbox.get()
    ph = PasswordHasher()
    file = SECRET_FILE
    with open(file) as f:
        data = json.load(f)
    psw_hash = data["password"]
    try:
        ph.verify(psw_hash, pswPlain)
        return True
    except:
        return False

def getinfo(name):
    with open(SECRET_FILE) as f:
        data = json.load(f)
        if  isinstance(data[name],(int, float)):
            return data[name]
        else:
            return data[name].replace(" ", "")

def changePassword(newpassword):
    try:
        ph = PasswordHasher()
        psw_hash = ph.hash(newpassword)

        with open(SECRET_FILE) as f:
            data = json.load(f)
        data["password"] = psw_hash
        with open(SECRET_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except:
        return False


def changeAPIChatGpt(newkey):
    try:
        with open(SECRET_FILE, "r") as f:
            data = json.load(f)
        data["apiKeyChatgpt"] = newkey
        with open(SECRET_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except:
        return False


def changeMail(newmail):
    try:
        with open(SECRET_FILE, "r") as f:
            data = json.load(f)
        data["mailSender"] = newmail
        with open(SECRET_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except:
        return False


def changeMailPsw(newpsw):
    try:
        with open(SECRET_FILE, "r") as f:
            data = json.load(f)
        data["mailPassword"] = newpsw
        with open(SECRET_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except:
        return False


def resetToken():
    try:
        with open(SECRET_FILE, "r") as f:
            data = json.load(f)
        data["tokenUsed"] = 0
        with open(SECRET_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except:
        return False


def changeGptModel(var):
    try:
        with open(SECRET_FILE, "r") as f:
            data = json.load(f)
        data["gptModel"] = var
        with open(SECRET_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except:
        return False

def updateTokenCounter(x):
    try:
        with open(SECRET_FILE, "r") as f:
            data = json.load(f)
        data["tokenUsed"] += x
        with open(SECRET_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except:
        return False