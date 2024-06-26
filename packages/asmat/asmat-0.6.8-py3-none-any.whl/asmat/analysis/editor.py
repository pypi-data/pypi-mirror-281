import sqlite3
import datetime

def get_id():
    con = sqlite3.connect("test/asm/src/analyze/data.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT id FROM instructions WHERE edited='Never'")
    res = res.fetchone()
    if res != None:
        return int(res[0])
    else:
        return -1

id = get_id()
setId = False
iname = ""

while True:
    id = get_id()


    if id == -1:
        print("No row selected")
    else:
        con = sqlite3.connect("test/asm/src/analyze/data.db")
        cur = con.cursor()
        res = cur.execute(f"SELECT instr_name, id, description, extension FROM instructions WHERE id = {id}").fetchone()
        if res == None:
            id = -1
            print("Invalid id")
        else:
            iname = res[0]
            print(f"Instruction : {res[0]} (id {res[1]})\nExtension : {res[2]}\n{res[3]}")


    i = input(">>")
    if i == 'exit':
        break

    if 'id' in i:
        id = int(i.split(' ')[1])
        continue
    
    if i == 'pass':
        con = sqlite3.connect("test/asm/src/analyze/data.db")
        cur = con.cursor()
        cur.execute(f"UPDATE instructions SET edited='Pass' WHERE id={id} OR instr_name='{iname}';")
        con.commit()
        con.close()


    if 'set' in i:
        if id == -1:
            print("No data selected")
            continue
        else:
            s = i.split(' ')[1]
            if len(s) != 3 or s[0] != '0' and s[0] != '1' or s[1] != '0' and s[1] != '1' or s[2] != '0' and s[2] != '1':         
                print("Invalid set")
                continue
            con = sqlite3.connect("test/asm/src/analyze/data.db")
            cur = con.cursor()
            cur.execute(f"UPDATE instructions SET ctrl_flow = {s[0]}, arith_logic={s[1]}, data_move={s[2]}, edited='{str(datetime.datetime.now())}' WHERE id={id} OR instr_name='{iname}';")
            con.commit()
            con.close()
