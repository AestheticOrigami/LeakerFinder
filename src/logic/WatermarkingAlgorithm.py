from pathlib import Path
import pandas as pd
import re
from CTkMessagebox import CTkMessagebox
from openai import OpenAI
import random
from src.logic.Security import getinfo, updateTokenCounter

FOLDERPATH = Path(__file__).parent.parent.resolve() / "resources/ListOfPeople"
SY2VA = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
         'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

ZEROWIDTHCHAR = [
    '\u034F',
    '\u00AD',
    '\u180C',
    '\u180D',
    '\u180E',
    '\u200B',
    '\u200C',
    '\u200E',
    '\u200F'
]


def sanitize(text):
    text = text.replace("  ", " ")

    text = text.strip()

    return text


def newLineWatermark(text, ppl):
    binarray = []
    dictionary = {}
    watermarkspot = 0
    token = "$$$"

    text = re.sub(r'(\w)?\$\$\$(\w)?', lambda m: (m.group(1) or '') + ' $$$ ' + (m.group(2) or ''), text)

    text = sanitize(text)

    csvlist = fileLoader(ppl)
    npeople = len(csvlist)
    textarray = text.split(" ")

    for tk in textarray:
        if tk == token:
            watermarkspot += 1

    nofbit = len(bin(npeople)) - 2

    while len(binarray) < npeople:
        num = bin(len(binarray))
        num = num[2:]
        num = num.zfill(nofbit)
        binarray.append(num)
    combination = pow(2, watermarkspot)
    if npeople > combination:

        CTkMessagebox(title="Error", message="There are not enough spot for watermark", sound=True)
        return

    else:
        for i in range(npeople):
            arraytext = text.split(" ")
            binary = binarray[i]
            binary.split()

            for j in range(len(arraytext) - 1):
                if len(binary) == 0:
                    break
                if j >= len(arraytext):
                    break
                if arraytext[j] == token:
                    if binary[-1] == "1":
                        arraytext[j] = "\n"
                        binary = binary[:-1]
                    else:
                        arraytext.remove(arraytext[j])
                        binary = binary[:-1]
            wtext = ""
            for j in range(len(arraytext)):
                if arraytext[j] == "/n":
                    wtext += arraytext[j]
                else:
                    wtext += arraytext[j] + " "
            wtext=wtext.replace("$$$","")
            dictionary.update({csvlist.loc[i, "Identifier"]: wtext})

    return dictionary


def hiddenWatermark(text, people):
    csv = fileLoader(people)
    csvlist = csv["Identifier"].tolist()
    token = "(*)"
    dictionary = {}
    nppl = len(csvlist)


    text = sanitize(text)
    arraytext = text.split()
    find = False
    index = 0
    for i in range(len(arraytext)):
        if token in arraytext[i]:
            find = True
            index = i
            break
    if find:

        arraytext[index] = arraytext[index].replace(token, "")
    else:

        index = random.randint(0, len(arraytext) - 1)

    for i in range(nppl):
        watermarkedarraytext = arraytext.copy()
        wordtowatermark = watermarkedarraytext[index]
        splittedword = list(wordtowatermark)

        base = fromdexto(i)
        valbase = list(base)
        for j in valbase:
            finalval = todex(j)
            splittedword.insert(0, ZEROWIDTHCHAR[finalval - 1])
        watermarkedarraytext[index] = "".join(splittedword)
        dictionary.update({csvlist[i]: " ".join(watermarkedarraytext)})
    return dictionary


def contentBasedWatermark(text, ppl):
    client = OpenAI(api_key=getinfo("apiKeyChatgpt"))
    model = getinfo("gptModel")
    dictionary = {}
    text = sanitize(text)
    csv = fileLoader(ppl)
    csvlist = csv["Identifier"].tolist()
    npeople = len(csvlist)
    try:
        chat = client.chat.completions.create(
            model=model,
            temperature=0.2,
            frequency_penalty=0.1,
            max_completion_tokens=npeople*10,
            messages=[
                {"role": "system",
                 "content": "Act like a very accurate native speaker dictionary robot"},
                {
                "role": "user",
                "content": f"give me back a list of exactly {npeople} synonyms consistent with the context of the sentence in which they are found. The format should be: 'base word || synonymous'. No introductory or final sentences. Text: {text}"
                }
            ]
        )

    except Exception as e:
        CTkMessagebox(title="Error", message="API Problems, check the credit or the apikey", sound=True, icon="cancel")
        return
    content = chat.choices[0].message.content


    base = []
    synonyms = []

    for line in content.split("\n"):
        clear_line = line.strip()
        linearr = clear_line.split(" ")
        str_base = ""
        str_syn = ""
        tokenfound = False
        for i in range(len(linearr)):
            if linearr[i] == "||" or tokenfound:
                if linearr[i] == "||":
                    tokenfound = True
                    continue
                str_syn += linearr[i] + " "
                continue
            str_base += linearr[i] + " "
        base.append(str_base.strip())
        synonyms.append(str_syn.strip())


    for i in range(npeople - 1):
        replace_regex = re.compile(re.escape(base[i]), re.IGNORECASE)
        wtext = replace_regex.sub(synonyms[i], text)
        dictionary.update({csvlist[i]: wtext})

    updateTokenCounter(chat.usage.total_tokens)

    return dictionary


def fileLoader(ppl):
    try:
        folderpath = FOLDERPATH / ppl
        csvlist = pd.read_csv(folderpath)
        return csvlist

    except:
        CTkMessagebox(title="Error", message="File not found", sound=True)
        return pd.DataFrame()



def fromdexto(number):
    number_of_char = len(ZEROWIDTHCHAR)
    final_string = ""
    while True:
        if number < number_of_char:
            final_string += SY2VA[number]
            break
        else:
            final_string += SY2VA[number % number_of_char]
            number = number // number_of_char

    return final_string


def todex(value):
    number_of_char = len(ZEROWIDTHCHAR)
    final_number = 0
    newvalue = value[0]
    for i in range(len(newvalue)):
        final_number += SY2VA.index(newvalue[int(i)]) * (number_of_char ** i)
    return final_number
