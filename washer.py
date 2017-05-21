import os.path
rootdir = 'G:/语料库/喵玉'

def delUseless(infile,outfile):
    infopen = open(infile,'r')
    lines = infopen.readlines()
    # 去除空行
    for i in range(len(lines)):
        line = lines[i]
        if not line.split():
            lines[i]=""

    #去除图片行
    for i in range(len(lines)):
        line = lines[i]
        if line.find(".jpg")!=-1 or line.find(".JPG") != -1 or line.find(".png")!=-1 or line.find(".PNG") != -1 or line.find(".gif") != -1 or line.find(".GIF") != -1 or line.find("下载附件")!=-1 or line.find("保存到相册")!=-1 or line.find("下载次数")!=-1 or line.find("上传")!=-1:
            lines[i]=""

    #去除压缩包
    for i in range(len(lines)):
        line = lines[i]
        if line.find(".rar") != -1 or line.find(".RAR") != -1:
            lines[i]=""

    #去除网页元素
    for i in range(len(lines)):
        line = lines[i]
        if line.find("$")!=-1:
            lines[i]=""

    #去除网址
    for i in range(len(lines)):
        line = lines[i]
        if line.find("http")!=-1:
            lines[i]=""

    for i in range(len(lines)):
        line = lines[i]
        if line.find("html") != -1:
            lines[i] = ""

    #去除旧版回复
    for i in range(len(lines)):
        line = lines[i]
        if line.find("回复")!=-1 or line.find("#")!=-1:
            lines[i]=""

    #去除replay行
    for i in range(len(lines)):
        line = lines[i]
        if line.find("replyreload")!=-1:
            lines[i]=""

    #去除nico视频标签
    for i in range(len(lines)):
        line = lines[i]
        jud=line.find("[nicovideo]")
        if jud!=-1:
            if jud==0:
                lines[i]=""
            else:
                lines[i]=line[:jud]+"\n"

    #自我介绍下移
    for i in range(len(lines)):
        line = lines[i]
        jud = line.find("【名称】")
        if jud != -1:
            if jud != 0:
                lines[i] = line[:jud]+"\n"
                lines.insert(i + 1, line[jud:])


    # 去除转义
    for i in range(len(lines)):
        line=lines[i]
        line=line.replace("&gt;","")
        line=line.replace("&lt;", "")
        line = line.replace(" ", "")
        line = line.replace("&quot;", "")
        line = line.replace("&amp;", "&")
        lines[i]=line

    #写入
    infopen.close()
    f = open(outfile, 'w')
    f.writelines(lines)
    f.close()

#遍历
if __name__=="__main__":
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    dir = "/washed/"
    if (not os.path.exists(rootdir+dir)):
        os.mkdir(rootdir+dir)
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        newpath = os.path.join(rootdir + dir, list[i])
        if os.path.isfile(path):
            delUseless(path, newpath[:-4]+"_washed.txt")