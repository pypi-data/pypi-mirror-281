import os
if __name__ == "__main__":
    import sys
    sys.path.append("/home/erwan/eve/test/asm/src")
import re

from asmat.analysis.parse_html import is_extension_instruction, instruction_categories
import asmat.const as const
import matplotlib.pyplot as plt



FUNCTION_PAGE_STYLE = """
<style>
    span:hover { cursor: default; opacity: 0.5; }
    body {margin: auto;max-width: 60%;padding-top: 1%;}
    h3 {margin: 4px;}
    .row {display: flex;}
    .column {flex: 50%;}
    pre code {background-color: #eee;border: 1px solid #999;display: block;padding: 20px;}
    td, th {border: 1px solid #DDD;padding: 4px;text-align: left;}
    tr:nth-child(even){background-color: #f2f2f2;}
</style><html><body><div class="row"><div class="column">"""

DOCUMENT_STYLE = """
<style>
    td, th {border: 1px solid #DDD;padding: 4px;text-align: left;}
    tr:hover {background-color: #D6EEEE;}
    table {border-collapse: collapse;width: 100%;text-align: center;margin-top: 10%;}
    body {margin: auto;max-width: 60%;padding-top: 1%;}
    #head {background-color: gainsboro;}
</style>
"""





def gen_pie_chart(path, proportion:list):
    fig, ax = plt.subplots()
    ax.pie(proportion, labels=['Control flow', 'Arithmetic/Logic', 'Data movement', 'Undefined'], autopct='%1.1f%%', shadow=True, startangle=90)
    plt.savefig(f'{const.root}/output/pages/{path}.jpg')
    plt.close(fig)


def data_assembly(instructions):
    colors = []
    ext = []
    nbExt = 0
    mem = 0

    cat0 = 0
    cat1 = 0
    cat2 = 0
    cat3 = 0

    for i in instructions:
        e = is_extension_instruction(i.split(' ')[0].upper())

        cat = instruction_categories(i.split(' ')[0].upper())
        cat0 += cat[0]
        cat1 += cat[1]
        cat2 += cat[2]
        cat3 += cat[3]

        if cat[0] == 1:
            colors.append((i, "Control flow", "blue"))
        elif cat[1] == 1:
            colors.append((i, "Arithmetic/Logic", " #e67e22"))
        elif cat[2] == 1:
            colors.append((i, "Data movement", "green"))
        else:
            colors.append((i, "Undefined", "red"))

        if e != None:
            if e not in ext:
                ext.append(e)
            nbExt += 1

        if re.match(".*0x[0-9a-f]+\(.*\).*", i):
            mem += 1

    if ext == []:
        ext = ['No extension used']

    result = {}
    result['cat0'] = cat0
    result['cat1'] = cat1
    result['cat2'] = cat2
    result['cat3'] = cat3
    result['ext'] = ext
    result['nbExt'] = nbExt
    result['mem'] = mem
    result['instr'] = colors

    return result


def generate_function_page(page_name:str, function:str, dataInstr:dict):

    if not os.path.exists(f"{const.root}/output/pages/{page_name}.html"):
        f = open(f"{const.root}/output/pages/{page_name}.html", 'x')
    else:
        f = open(f"{const.root}/output/pages/{page_name}.html", 'w')

    doc = FUNCTION_PAGE_STYLE
    doc += f"<h1>{function}</h1>"                        # Function name
    doc += f"<h3>Instructions: {len(dataInstr['instr'])}</h3>" # Number of instructions
    doc += f"<h3>Extension(s): {', '.join(dataInstr['ext'])}</h3>"               # List of extensions
    doc += f"<h3>Memory access: {dataInstr['mem']}</h3>"                # Number of memory access

    gen_pie_chart(page_name, [dataInstr['cat0'], dataInstr['cat1'], dataInstr['cat2'], dataInstr['cat3']])

    doc += f'<table style="border-collapse: collapse;border: 2px solid #eee; margin-top: 30px;max-width: 80%;min-width: 50%;">\
    <tr><th>Data movement</th><td>{dataInstr["cat2"]}</td></tr><tr><th>Logic/Arithmetic</th><td>{dataInstr["cat1"]}</td></tr><tr><th>Control flow</th><td>{dataInstr["cat0"]}</td>\
        </tr><tr><th>Undefined</th><td>{dataInstr["cat3"]}</td></tr></table></div>'
    doc += f'<div class="column"><img src="{page_name}.jpg" alt="" style="max-width: 100%;margin-top: 50px;"></div></div>'

    doc += f'<div><h2>Instructions</h2><pre><code style="max-height: 300px;overflow: scroll;">'

    for i in dataInstr['instr']:
        doc += f'<span style="background-color: {i[2]};" title="{i[1]}"> </span> {i[0]}\n'
    
    doc += "</code></pre></div></body></html>"

    f.write(doc)
    f.close()







def generate_index(functions):

    if not os.path.exists(f"{const.root}/output/index.html"):
        f = open(f"{const.root}/output/index.html", 'x')
    else:
        f = open(f"{const.root}/output/index.html", 'w')
    
    doc = "<html><body><table><h1>Assembly analysis</h1><tr id=\"head\"><th>Function</th>\
        <th>Instructions</th><th>Extensions</th></tr>"

    for i in functions:
        function_name = f"{i[0]}({', '.join(i[1])})"
        page_name = ''.join( map(lambda i : i if i.isalnum() else '_' , function_name) )

        dataInstr = data_assembly(i[2])

        doc += f'<tr><td><a href="pages/{page_name}.html">{function_name.replace("<", "&lt;").replace(">", "&gt;")}</a></td><td>{len(i[2])}</td><td>{", ".join(dataInstr["ext"])}</td></tr>'
        generate_function_page(page_name, function_name, dataInstr)

    doc += "</table></body></html>"

    f.write(DOCUMENT_STYLE + doc)
    f.close()





if __name__ == '__main__':
    print(''.join( map(lambda i : i if i.isalnum() else '_' , "res_defined_array(int*)")) )