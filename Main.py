import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import webbrowser

root = tk.Tk()
title = tk.StringVar(root,"GSC Collection (by Kerwin)") #字串變數

def Get_Info():
    target = r"https://www.goodsmile.info/zh/products/search?utf8=%E2%9C%93&search%5Bquery%5D=Hololive&search%5Badult%5D=1&commit=%E6%AA%A2%E7%B4%A2#searchResults"

    result=requests.get(target)
    soup = BeautifulSoup(result.text, 'html.parser')
    divs = soup.find_all('div', 'hitBox')
    l = []
    str_ = ""

    for div in divs: 
        img = div.a.img.attrs['data-original'].split("/")[6]
        time = img[:4] + "/"+img[4:6]+"/"+img[6:]
        link = div.a.attrs['href']
        name = div.a.span.span.text.replace(" ","")
        l.append([time,name,link])
    l.sort(key = lambda a : a[0])
    return l
    
def Crawler():
    Load_Scene = tk.Toplevel()
    Load_Scene.title("抓取結果")
    Load_Scene.geometry("600x500")
    # Load_Scene.iconbitmap("LOGO.ico")
    Load_Scene.grab_set() # lock on new scene
    tree=ttk.Treeview(Load_Scene,columns=("0","1","2","3"),show="headings")
    tree.heading("0",text="人物")
    tree.heading("1",text="時間")
    tree.heading("2",text="種類")
    tree.heading("3",text="URL")
    info = Get_Info()
    for item in info:
        time = item[0]
        if "figma" in item[1]: 
            name =  item[1].split("figma")[1]
            type_ = "figma"
        elif "POPUPPARADE" in item[1]:
            name =  item[1].split("POPUPPARADE")[1]
            type_ = "POP UP PARADE"
        elif "黏土人" in item[1]:
            name =  item[1].split("黏土人")[1]
            type_ = "黏土人"
        else:
            name =  item[1]
            type_ = "PVC"
        tree.insert("","end",values=[name,time,type_,item[2]])
    tree.pack()
    def tree_double(event):
        curItem = tree.focus()
        url = tree.item(curItem)["values"][3]
        webbrowser.open_new(url)
    tree.bind("<Double-Button-1>",tree_double)

# print(root.winfo_screenwidth()) # 輸出螢幕寬度
# print(root.winfo_screenheight()) # 輸出螢幕高度
w=720  # width
h=480  # height
x=00  # 與視窗左上x的距離
y=100  # 與視窗左上y的距離
root.geometry('{}x{}+{}+{}'.format(w,h,x,y))
root.title(title.get())
root.configure(bg="#7AFEC6")
# root.iconbitmap('LOGO.ico')


# L1=tk.Label(root,text='I am Label',bg='#DDA0DD',fg="#8B008B",font=("'microsoft yahei",18,"bold"))
# title
topic = tk.Label(root,text='GSC Collection',
    font=("'microsoft yahei",18,"bold"),cursor='draped_box',padx=15,pady=20)

button_Go = tk.Button(root,text="抓取",activebackground='#BE77FF',
    relief="ridge",state=tk.NORMAL,cursor='target',command=Crawler)


topic.pack()
button_Go.pack()
root.mainloop()
