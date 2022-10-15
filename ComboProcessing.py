import json

while True:
    msg = open("pipe2.txt", "r")
    if msg.read() == 'process':
        f = open("database.json", "r")
        combos = f.read()
        f.close()
        if combos:
            c = json.loads(combos)
            output = ''
            for key in c:
                combs = ''
                for act in c[key]:
                    combs += str(act) + ', '
                combs = combs[:-2]
                output += key + ': ' + combs + '\n'
            file = open("display.txt", "w")
            file.write(output)
            file.close()
            open('pipe2.txt', 'w').close()
