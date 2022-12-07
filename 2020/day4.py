import re

valid = 0
passport = {}

def checkPassport():
    global passport, valid
    if ("byr" in passport and "iyr" in passport and "eyr" in passport and
        "hgt" in passport and "hcl" in passport and "ecl" in passport and
        "pid" in passport):
        valid += 1
    passport = {}

YEAR = "^\d{4}$"
COLOR = "^#[a-f0-9]{6}$"
EYE_COLOR = "^(amb|blu|brn|gry|grn|hzl|oth)$"
PASSPORT_ID = "^\d{9}$"
HEIGHT = "^((\d{3})cm|(\d{2})in)$"

def validateField(key, value):
    global passport
    match key:
        case "byr":
            if re.match(YEAR, value) is not None and int(value) >= 1920 and int(value) <= 2002:
                passport[key] = value
        case "iyr":
            if re.match(YEAR, value) is not None and int(value) >= 2010 and int(value) <= 2020:
                passport[key] = value
        case "eyr":
            if re.match(YEAR, value) is not None and int(value) >= 2020 and int(value) <= 2030:
                passport[key] = value
        case "hgt":
            m = re.match(HEIGHT, value)
            if m is not None:
                if m.group(2) is not None:
                    h = int(m.group(2))
                    if h >= 150 and h <= 193:
                        passport[key] = value
                elif m.group(3) is not None:
                    h = int(m.group(3))
                    if h >= 59 and h <= 76:
                        passport[key] = value      
        case "hcl":
            if re.match(COLOR, value) is not None:
                passport[key] = value
        case "ecl":
            if re.match(EYE_COLOR, value) is not None:
                passport[key] = value
        case "pid":
            if re.match(PASSPORT_ID, value) is not None:
                passport[key] = value
    

with open("day4.txt", "r") as f:
    while True:
        line = f.readline()
        if len(line) == 0:
            checkPassport()
            break
        elif len(line.strip()) == 0:
            checkPassport()
        else:
            keyVals = line.strip().split(" ")
            for pair in keyVals:
                split = pair.split(":")
                validateField(split[0], split[1])

print(valid)
