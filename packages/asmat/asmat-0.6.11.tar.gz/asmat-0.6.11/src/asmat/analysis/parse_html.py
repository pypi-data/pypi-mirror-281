import urllib.request
from bs4 import BeautifulSoup
import os
import sqlite3



def load():
    if not os.path.exists("test/asm/src/analyze/source_html.txt"): 
        html = urllib.request.urlopen("https://shell-storm.org/x86doc/index.html").read()
        f = open("test/asm/src/analyze/source_html.txt", "x")
        f.write(str(html))
        f.close()
    else:
        html = open("test/asm/src/analyze/source_html.txt", "r").read()


    parser_html = BeautifulSoup(html, features="html.parser")

    assembly_instructions = []

    for i in parser_html.findAll('tr'):
        parser_html2 = BeautifulSoup(str(i), features="html.parser")
        td = parser_html2.findAll('td')

        if len(td) >= 4:
            l = [td[0].a.get_text(), td[1].get_text(), td[2].get_text(), td[3].get_text()]
        
            assembly_instructions.append(l)

    con = sqlite3.connect(f"{os.path.dirname(__file__)}/data.db")
    cur = con.cursor()
    res = cur.execute("DELETE FROM instructions")
    assert res.fetchone() == None

    cur.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name='instructions'")
    con.commit()

    cur.executemany("INSERT INTO instructions (instr_name, op_code, extension, description, instr_set) VALUES (?, ?, ?, ?, 'x86')", assembly_instructions)
    con.commit()


    res = cur.execute("SELECT DISTINCT instr_name FROM instructions WHERE extension != '' ORDER BY length(instr_name) DESC")
    print(len(res.fetchall()))

    res = cur.execute("SELECT DISTINCT instr_name FROM instructions ORDER BY length(instr_name) DESC")
    print(len(res.fetchall()))


    cur.close()
    con.close()


def is_extension_instruction(instr):
    con = sqlite3.connect(f"{os.path.dirname(__file__)}/data.db")
    cur = con.cursor()
    res = cur.execute("SELECT instr_name, extension FROM instructions WHERE extension != '' ORDER BY length(instr_name) DESC")

    for i in res:
        if i[0] == instr:
            return i[1]
    return None


def instruction_categories(instr):
    con = sqlite3.connect(f"{os.path.dirname(__file__)}/data.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT ctrl_flow, arith_logic, data_move FROM instructions WHERE instr_name='{instr}'")

    res = res.fetchone()
    if res is None:
        return (0, 0, 0, 1)
    if res[0] + res[1] + res[2] == 0:
        return (0, 0, 0, 1)
    else:
        return (res[0], res[1], res[2], 0)


if __name__ == '__main__':
    #load()
    #print(is_extension_instruction("movaps".upper()))
    print(instruction_categories("AAA"))
    pass

