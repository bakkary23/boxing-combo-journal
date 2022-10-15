import json


def add_to_database(cs, c):
    cs["Combo " + str(len(cs) + 1)] = c


combos = {}
while True:
    fileObject = open("pipe.json", "r")
    jsonContent = fileObject.read()
    fileObject.close()
    msg = open("pipe2.txt", "r")
    if msg.read() == '-1':
        combos = {}
        msg.close()
        open('pipe2.txt', 'w').close()
    if jsonContent:
        combo = json.loads(jsonContent)
        add_to_database(combos, combo['1'])
        open('pipe.json', 'w').close()
        json_s = json.dumps(combos)
        json_f = open("database.json", "w")
        json_f.write(json_s)
        json_f.close()
