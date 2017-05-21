import json
import random
import os.path

#填入清洗后的语料库路径
rootdir = 'G:/语料库/喵玉/washed'

conv=[]

data = {1:16, 2:8, 3:4, 4:2, 5:1}

#带权重随机对应语句数
def randombyValue():
    all_data = []
    for v, w in data.items():
        temp = []
        for i in range(w):
            temp.append(v)
        all_data.extend(temp)

    n = random.randint(0, len(all_data) - 1)
    return all_data[n]

def formatConv(infile):
    infopen = open(infile,'r')
    lines = infopen.readlines()
    le=len(lines)
    i=0
    while i<le:
        num=randombyValue()
        if i+num>=le:
            num=le-i-1
        elif i+num==le-2:
            num+=1
        tmp = []
        for j in range(num + 1):
            tmp.append(lines[i + j][:-1])
        i += num
        i+=1
        conv.append(tmp)

def formatJson(outfile):
    jdata = json.dumps({'conversations': conv}, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
    f = open(outfile, 'w')
    f.write(jdata)
    f.close()

if __name__=="__main__":
    list = os.listdir(rootdir)
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        formatConv(path)
    formatJson(rootdir+"/dialog.json")