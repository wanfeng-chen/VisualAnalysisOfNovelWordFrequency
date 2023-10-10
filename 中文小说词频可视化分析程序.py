from sys import maxsize
import tkinter
from tkinter import ttk
from tkinter import simpledialog
import tkinter.filedialog
import tkinter.messagebox
from tkinter import*
from tkinter.ttk import Notebook
import jieba
from jieba import analyse
from matplotlib import colors
import matplotlib.pyplot as plt
from numpy import array
from wordcloud import WordCloud
from PIL import Image
import wordcloud
from collections import Counter
import numpy as np
import collections
import jieba.posseg as psg
from itertools import combinations
import networkx as nx 
DATA = []
FILENANE = ''

FILENANER = ''
FILENANE_LIST =''


def openfile4():
    global  FILENANER

    FILENANER = tkinter.filedialog.askopenfilename( title='选取中文小说', filetypes=[('文本文件', '.txt')])

    if FILENANER=='':
        tkinter.messagebox.showinfo('操作提示','打开失败!')
    else:
        interface4.set(FILENANER)
        tkinter.messagebox.showinfo('操作提示','打开成功!')
    
    
def openfile_name4():

    global FILENANE_LIST

    FILENANE_LIST = tkinter.filedialog.askopenfilename( title='选取中文小说人名', filetypes=[('文本文件', '.txt')] )

    if FILENANE_LIST=='':
        tkinter.messagebox.showinfo('操作提示','打开失败!')
    else:
        interface5.set(FILENANE_LIST)
        tkinter.messagebox.showinfo('操作提示','打开成功!')


def get_count_result_list4():
    global FILENANER,FILENANE_LIST
    file = open(FILENANER,'r',encoding="UTF-8")
    file1 = open(FILENANE_LIST,'r',encoding="UTF-8")
    
    text = file.readlines()
    text_name = file1.read()

    name_list = text_name.split('\n')

    # print(name_list)

    relationlist=[]
    for lines in text:
        n=[]
        for i in name_list:
            for j in name_list[name_list.index(i)+1:]:
                if i in lines and j in lines and i!=j:
                    n.append(i)

        relationlist += combinations(sorted(set(n)),2)
    print(name_list)
    print(relationlist)
    relationDict=Counter(relationlist)
    return relationDict
    
def createRelationship():
    relationDict = get_count_result_list4()
    relationship_list = []

    plt.figure(' 人物关系图', figsize=(8, 6))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.text(-1.044, 0.87, '人物关系（线越短代表联系越紧密)',fontsize=12)  #-1，1字体位置
    relationship_list = []
    for item in relationDict.items():
        if item[1] >=20:
            relationship_list.append([item[0][0], item[0][1], str(item[1])])

    g = nx.Graph()
    g.add_weighted_edges_from(relationship_list)
    nx.draw(g, with_labels=True, font_size=12, node_size=1000, node_color='#9999FF')
    plt.show()

def stronger_createRelationship():
    relationship_dict=get_count_result_list4()
    relationship_dict_select = dict()
    for item in relationship_dict.items():
        if item[1] >= 20:
            relationship_dict_select[item[0]] = item[1]

    edgeWidth = []
    for i in relationship_dict_select.values():
        edgeWidth.append(i / 20)

    #图片比例尺，跟dpi合并计算后就是图片的分辨率
    plt.figure(' 增强人物关系图 ', figsize=(8, 6))
    g = nx.MultiGraph()
    g.add_edges_from(relationship_dict_select.keys())
    d = dict(g.degree)

    #nodelist节点名称，node_size节点大小，node_color 节点颜色，edge_color 线颜色，width宽度的值
    nx.draw_circular(g, nodelist=d.keys(), node_size=[v * 200 for v in d.values()], node_color='y', cmap=plt.cm.Paired, with_labels=True, edge_color=range(len(relationship_dict_select)), edge_cmap=plt.cm.Dark2, alpha=1.0, width=edgeWidth)

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.text(-1.044, 0.87, '线越宽代表联系越紧密\n点越大表示出现的次数越多',fontsize=12)  #-1，1字体位置
    plt.show()

def load_Relationship():
    fn = tkinter.filedialog.asksaveasfilename(title='保存文件', filetypes=[('csv源文件', '.csv')])
    if fn == '': 
        return
    else:
        fn = fn + '.csv'
    relationship_dict = get_count_result_list4()
    with open(fn, 'w', encoding='UTF-8-sig') as f:
        for item in relationship_dict.items():
            f.write(item[0][0] + "," + item[0][1] + "," + str(item[1]) + "\r\n")



def get_count_result_list(filename):
    file = open(filename,'r',encoding="UTF-8")
    text = file.read()
    result= jieba.lcut(text)
    result_count = collections.Counter(result)
    result_dict =  dict(result_count)
    result_sort_list = list(result_dict.items())
    result_sort_list.sort(key=lambda  X:X[1],reverse=True)
    result = []

    stop_file = open('stopwords_zh.txt',encoding="UTF-8")
    stop_text = stop_file.read()
    stop_words = stop_text.split("\n")

    for word in result_sort_list:
        if word[0] not in stop_words:
            result.append(word)

    del result[0]
    del result[0]
    return result

def draw_bar(data):
    listX = []
    listY = []

    for item in data[0:10]:
        listX.append(item[0])
        listY.append(item[1])

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.bar(listX, listY, color='#FF0000', width=0.5)   
    plt.show()

def draw_pie(data):
    listX = []
    listY = []

    for item in data[0:10]:
        listX.append(item[0])
        listY.append(item[1])
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.pie(x=listY, labels=listX)
    plt.show()

def draw_wordcloud(filename):   
    file = open(filename,'r',encoding="UTF-8")
    text = file.read()
    file.close()
    result = jieba.lcut(text)

    result_count = collections.Counter(result)
    result_dict =  dict(result_count)
    result_sort_list = list(result_dict.items())
    result_sort_list.sort(key=lambda  X:X[1],reverse=True)
    result = []

    stop_file = open('stopwords_zh.txt',encoding="UTF-8")
    stop_text = stop_file.read()
    stop_words = stop_text.split("\n")

    for word in result_sort_list:
        if word[0] not in stop_words:
            result.append(word)

    del result[0]
    del result[0]
    listX = []
    for item in result:
        listX.append(item[0])
    data = " ".join(listX)
    img = Image.open('alice_color.png')
    img = np.array(img)

    ciyun = wordcloud.WordCloud(background_color='white', mask=img,font_path="simhei.ttf",random_state=10).generate(data)
    plt.imshow(ciyun)
    plt.axis('off')
    plt.show()

def openfile():
    global DATA, FILENANE

    FILENANE = tkinter.filedialog.askopenfilename( title='都好好的', filetypes=[('文本文件', '.txt')] )

    if FILENANE=='':
        tkinter.messagebox.showinfo('操作提示','打开失败!')
    else:
        interface3.set(FILENANE)
        tkinter.messagebox.showinfo('操作提示','打开成功!')
    DATA = get_count_result_list(FILENANE)
    
def fenci():
    result = text1.get("1.0","end")
    result = jieba.lcut(result)

    stop_file = open('stopwords_zh.txt',encoding="UTF-8")
    stop_text = stop_file.read()
    stop_words = stop_text.split("\n")
    result_text = []

    for word in result:
        if word[0] not in stop_words:
            result_text.append(word)    
        
    for word in result_text:
        text2.insert("insert",word+" ")
    
def fenci1():
    comment = text3.get("1.0","end")

    comment = comment.replace('、', '')
    comment = comment.replace('，', '。')
    comment = comment.replace('《', '。')
    comment = comment.replace('》', '。')
    comment = comment.replace('～', '')
    comment = comment.replace('…', '')
    comment = comment.replace('\r', '')
    comment = comment.replace('\t', ' ')
    comment = comment.replace('\f', ' ')
    comment = comment.replace('/', '')
    comment = comment.replace('、', ' ')
    comment = comment.replace('/', '')
    comment = comment.replace('。', '')
    comment = comment.replace('（', '')
    comment = comment.replace('）', '')
    comment = comment.replace('_', '')
    comment = comment.replace('?', ' ')
    comment = comment.replace('？', ' ')
    comment = comment.replace('“', '')
    comment = comment.replace('”', '')
    comment = comment.replace('：', '')

    result = list(psg.cut(comment))
    peo_name = []
    pla_name = []
    org_name = []

    for item in range(0,len(result)):
        print(result[item].word,result[item].flag)
        if result[item].flag== "nr":
            peo_name.append(result[item].word)
        elif result[item].flag == "ns":
            pla_name.append(result[item].word)
        elif result[item].flag == "nt":
            org_name.append(result[item].word)
        elif result[item].flag == "nz":
            org_name.append(result[item].word)
        elif result[item].flag == "nl":
            org_name.append(result[item].word)
        elif result[item].flag == "ng":
            org_name.append(result[item].word)
        else:
            continue
    
    peo_name1 = '  '.join(peo_name)
    pla_name2 = '  '.join(pla_name)
    org_name3 = '  '.join(org_name)

    text4.insert("insert","人名:"+peo_name1+"\n")
    text4.insert("insert","地名:"+pla_name2+"\n")
    text4.insert("insert","组织名:"+org_name3+"\n")
    


def zhongwenyanshi():#中文分词演示
    notebook.hide(1)
    notebook.hide(2)
    notebook.hide(3)
    notebook.select(0)
    labe1 = tkinter.Label(face1,text="源\n文\n本")
    text1 = tkinter.Text(face1,width=60,height=7)
    labe2 = tkinter.Label(face1,text="分\n词\n结\n果")
    text2 = tkinter.Text(face1,width=60,height=7)
    button = tkinter.Button(face1, text='开始分词', width=62, height=1,command=fenci)

    labe1.place(x=10,y=10)
    text1.place(x=35,y=10)
    labe2.place(x=10,y=120)
    text2.place(x=35,y=120)
    button.place(x=12,y=220)
    
def zhongwenmimingshibieyanshi():#命名实体识别演示
    face2 = tkinter.Frame(bg="blue")
    notebook.hide(0)
    notebook.hide(2)
    notebook.hide(3)
    notebook.select(1)
    labe1 = tkinter.Label(face2,text="源\n文\n本")
    text3 = tkinter.Text(face2,width=60,height=7)
    labe2 = tkinter.Label(face2,text="分\n词\n结\n果")
    text4 = tkinter.Text(face2,width=60,height=7)
    button = tkinter.Button(face2, text='开始分词', width=62, height=1,command=fenci1)

    labe1.place(x=10,y=10)
    text1.place(x=35,y=10)
    labe2.place(x=10,y=120)
    text2.place(x=35,y=120)
    button.place(x=12,y=220)

def cipinfenxi():#词频分析演示
    notebook.hide(0)
    notebook.hide(1)
    notebook.hide(3)
    notebook.select(2)

    Label1 = Label(face3,text="文件名:",width=8,height=1)
    entry1 = Entry(face3,width=49,textvariable=interface3)
    button1 = Button(face3,text="打开小说",width=60,height=1,command=openfile)
    button2 = Button(face3,text="画柱状图",width=60,height=1,command=lambda:draw_bar(DATA))
    button3 = Button(face3,text="画饼形图",width=60,height=1,command=lambda:draw_pie(DATA))
    button4 = Button(face3,text="画词云图",width=60,height=1,command=lambda: draw_wordcloud(FILENANE))

    Label1.place(x=20,y=20)
    entry1.place(x=100,y=20)
    button1.place(x=20,y=70)
    button2.place(x=20,y=120)
    button3.place(x=20,y=170)
    button4.place(x=20,y=220)

def renwuguanxiyanshi():#人物关系分析演示
    notebook.hide(0)
    notebook.hide(1)
    notebook.hide(2)
    notebook.select(3)
    
    label1 = tkinter.Label(face4, text='小说文件名：', width=10, height=1)
    entry1 = tkinter.Entry(face4, width=49, textvariable=interface4)
    label2 = tkinter.Label(face4,text='人物名文件：',width=10,height=1)
    entry2 = tkinter.Entry(face4,width=49,textvariable=interface5)
    button1 = tkinter.Button(face4, text='打开小说文件', width=60, height=1, command=openfile4, background='yellow')
    button5 = tkinter.Button(face4,text='打开人名文件',width=60,height=1,command=openfile_name4,background='lightblue')
    button2 = tkinter.Button(face4, text='生成标准人物人物关系图', width=60, height=1,command=createRelationship)
    button3 = tkinter.Button(face4, text='生成增强人物关系图', width=60, height=1,command=stronger_createRelationship)
    button4 = tkinter.Button(face4, text='导出人物关系关系数据', width=60, height=1,command=load_Relationship)

    label1.place(x=20, y=5)
    entry1.place(x=100, y=5)
    label2.place(x=20,y=30)
    entry2.place(x=100,y=30)
    button1.place(x=20, y=60)
    button5.place(x=20,y=100)
    button2.place(x=20, y=140)
    button3.place(x=20, y=180)
    button4.place(x=20, y=220)



win = tkinter.Tk()
win.geometry('470x295')
win.title("中文文本词频可视化分析软件")
win['background']='blue'

Label1 = Label(win,text="222222",width=8,height=1)
Label1.place(x=300,y=200)


menber = tkinter.Menu(master=win)#创建主菜单栏对象


menu1 = tkinter.Menu(menber,tearoff=0)#创建主菜单栏选项
menber.add_command(label="中文分词演示",command=zhongwenyanshi)

menu2 = tkinter.Menu(menber,tearoff=0)
menber.add_command(label="命名实体识别演示",command=zhongwenmimingshibieyanshi)

menu3 = tkinter.Menu(menber,tearoff=0)
menber.add_command(label="词频分析演示",command=cipinfenxi)

menu4 = tkinter.Menu(menber,tearoff=0)
menber.add_command(label="人物关系分析演示",command=renwuguanxiyanshi)

menu5 = tkinter.Menu(menber,tearoff=0)
menber.add_command(label="退出",command=win.quit)

win["menu"] = menber

notebook = ttk.Notebook()
face1 = tkinter.Frame(bg="lightblue")
face2 = tkinter.Frame(bg="lightyellow")
face3 = tkinter.Frame(bg="pink")
face4 = tkinter.Frame(bg="red")
notebook.add(face1,text="中文分词演示")
notebook.add(face2,text="命名实体识别演示")
notebook.add(face3,text="词频分析")
notebook.add(face4,text="人物关系分析演示")
notebook.pack(padx=10, pady=5, fill=tkinter.BOTH, expand=True)

path = StringVar()
#--------------------------------------------------------------------------
labe1 = tkinter.Label(face1,text="源\n文\n本")
text1 = tkinter.Text(face1,width=60,height=7)
labe2 = tkinter.Label(face1,text="分\n词\n结\n果")
text2 = tkinter.Text(face1,width=60,height=7)
button = tkinter.Button(face1, text='开始分词', width=62, height=1,command=fenci)

labe1.place(x=10,y=10)
text1.place(x=35,y=10)
labe2.place(x=10,y=120)
text2.place(x=35,y=120)
button.place(x=12,y=220)
#-------------------------------------------------------------------------
labe1 = tkinter.Label(face2,text="源\n文\n本")
text3 = tkinter.Text(face2,width=60,height=7)
labe2 = tkinter.Label(face2,text="分\n词\n结\n果")
text4 = tkinter.Text(face2,width=60,height=7)
button = tkinter.Button(face2, text='开始分词', width=62, height=1,command=fenci1)

labe1.place(x=10,y=10)
text3.place(x=35,y=10)
labe2.place(x=10,y=120)
text4.place(x=35,y=120)
button.place(x=12,y=220)
#--------------------------------------------------------------------------
interface3 = tkinter.StringVar(face3)
interface4 = tkinter.StringVar(face4)
interface5 = tkinter.StringVar(face4)
notebook.hide(1)
notebook.hide(2)
notebook.hide(3)
notebook.select(0)
#--------------------------------------------------------------------------
win.mainloop()