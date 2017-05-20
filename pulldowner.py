import requests
import re
import os

#在这里输入你要爬的帖子数，大于0，但不要大于总帖子数。。。
TNUM=100

s = requests.Session()

NYASAMA_HEADERS = {
                'Host': 'bbs.nyasama.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/50.0.2661.102 Safari/537.36'
            }

PATH='corpus/'

NYASAMA_URL = 'http://bbs.nyasama.com/forum.php?mod=viewthread&tid='
NYASAMA_PAGE = '&page='

#爬取
def PullDown(tid):
    pdata=""
    if isValid(tid):
        page=int(getPageNum(tid))
        for i in range(1,page+1):
            data=s.get(NYASAMA_URL + str(tid) + NYASAMA_PAGE + str(i), headers=NYASAMA_HEADERS).content.decode('gbk')
            data=data.replace("\r\n","")
            data=data.replace("&nbsp;","")
            wdata=washData(data)
            wdata=wdata[0:-1]
            pdata+=wdata
        return pdata
    else:
        return ""

#判断帖子是否存在
def isValid(tid):
    r = s.get(NYASAMA_URL + str(tid), headers=NYASAMA_HEADERS)
    if r.ok:
        data = r.content.decode('gbk')
        if "alert_error" in data:
            print("z")
            return False
        else:
            return True

#获取帖子页数
def getPageNum(tid):
    print(tid)
    r = s.get(NYASAMA_URL + str(tid), headers=NYASAMA_HEADERS)
    if r.ok:
        data = r.content.decode('gbk')
        list = re.compile('span title="共 (.*?) 页')
        page = re.findall(list, data)
        if len(page)==0:
            return "1"
        else:
            return page[0]

#数据过滤
def washData(rawdata):
    list = re.compile('postmessage_[0-9]*">(.*?)</td')
    speak=re.findall(list, rawdata)
    data="";
    for s in speak:
        data+=filterData(s)
    return data

#单个数据清洗
def filterData(rawdata):
    st=0;
    le=len(rawdata)
    data=""
    en=rawdata.find("<",st,le)
    while en!=-1:
        if en!=st:
            data += rawdata[st:en]
            data += "\n"
        st = rawdata.find(">", en, le) + 1
        en = rawdata.find("<", st, le)
    if st!=le:
        data+=rawdata[st:le]
        data += "\n"
    return data

#创建路径
def makeDir():
    dir = "corpus/"
    if(not os.path.exists(dir)):
        os.mkdir(dir)

#写入文件
def writeFile(data,num):
    open(PATH+str(5000*num-4999)+"~"+str(5000*num)+".txt", 'wb').write(data)

if __name__=="__main__":
    if TNUM>0 and str(TNUM).isdigit():
        makeDir()
        turn=int((TNUM-1)/5000)
        for i in range(turn):
            alldata=""
            for j in range(5000*i+1,5000*i+5001):
                alldata+=PullDown(j)
            writeFile(alldata.encode("gbk"),i+1)
        extradata=""
        for k in range(5000 * turn + 1, TNUM+1):
            extradata += PullDown(k)
        writeFile(extradata.encode("gbk"),turn+1)
