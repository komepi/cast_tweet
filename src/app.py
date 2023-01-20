#from komepiTkinter import k_tkinter as tkm
import tkinter as tk
from tkinter import ttk
import csv
from configparser import ConfigParser
import sys
from pathlib import Path
import time
from twitter import Twitter,OAuth
import datetime

import window_controller as tkm

exe_dir=Path(sys.argv[0]).parent
config_file=exe_dir.joinpath("config.ini")
def timestamp_file(time,stage):
    return exe_dir.parent.joinpath("timestamps").joinpath(str(time)+"_"+str(stage)+".txt")

def start_time(label):
    label.set("now recoding")
    global start
    start = time.time()

def post(tw,titles_,texts,url,time_list):
    title = titles_.get(titles_.curselection()[0])
    text=list()
    text.append(texts[0])##書き出し祭り
    text.append(title)#タイトル
    text.append(texts[1])#配信中です
    text.append(texts[2])#会場はこちら
    text.append(url)#url
    content = "\n".join(text)
    statusUpdate = tw.statuses.update(status=content)
    record_time(titles_,time_list)
    
def get_h_m_s(td):
    m, s = divmod(td.seconds, 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02}:{s:02}"

def record_time(lists,time_list):
    kind = lists.get(lists.curselection()[0])
    t = time.time()-start
    td = datetime.timedelta(seconds=t)
    time_list[kind] = get_h_m_s(td)
    
def end_broadcast(frame,time_list,time_,stage):
    times = list()
    for key, value in time_list.items():
        times.append(f"{value} {key}")
    with open(timestamp_file(time_,stage),"w",encoding="utf-8") as f:
        f.write("0:00:00 配信開始\n")
        f.write("\n".join(times))
    frame.destroy()
    
def set_titles(titles,path,stage):
    title_from_csv = list()
    with open(path,"r",newline="",encoding="utf-8") as f:
        reader = csv.reader(f)
        for line in reader:
            title_from_csv.append(stage+"-"+line[0]+":"+line[1])
    titles.delete(0,tk.END)
    titles.insert(0,*title_from_csv)
    
def read_config():
    config = dict()
    config_ini = ConfigParser()
    config_ini.read(config_file,encoding="utf-8")
    config_twitter=dict()
    for key in config_ini["TWITTER"]:
        config_twitter[key] = config_ini["TWITTER"][key]
    config["twitter"]=config_twitter
    config["others"] = config_ini["OTHERS"]["others"].split(",")
    texts=list()
    texts.append(config_ini["TWEET"]["tag"])
    texts.extend(config_ini["TWEET"]["main"].split(","))
    return config,texts

if __name__ == "__main__":
    timeList=dict()
    config,texts = read_config()
    twitter_auth = Twitter(auth = OAuth(*config["twitter"]))
    root = tkm.new_window("500x700","配信ツイートapp",resize=(False,False))
    
    stage_frame=tk.Frame(root)
    stage_frame.pack()
    time_box=tkm.input_text(stage_frame,"第",5,side_="left")
    tkm.label(stage_frame,"回",side="left")
    stage_box = tkm.input_text(stage_frame,"第",5,side_="left")
    tkm.label(stage_frame,"会場",side="left")
    
    file_frame=tk.Frame(root)
    file_frame.pack()
    path_box = tkm.input_path(file_frame,"タイトルリストファイル",30,"file",side_="left")
    ttk.Button(file_frame,text="セット",command=lambda:set_titles(titles,path_box.get(),stage_box.get())).pack(side="left")
    
    url_box = tkm.input_text(root,"YouTube URL",50)
    
    title_list=list()
    titles=tkm.listbox(root,title_list,text="第1会場",width=80,height=25)
    
    other=tkm.listbox(root,config["others"],height=len(config["others"]))
    buttons=tk.Frame(root)
    buttons.pack()
    ttk.Button(buttons,text="スタート",command=lambda:start_time(label_tx)).pack(side="left")
    ttk.Button(buttons,text="投稿",command=lambda:post(twitter_auth,titles,texts,url_box.get(),timeList)).pack(side="left")
    ttk.Button(buttons,text="NOW",command=lambda:record_time(other,timeList)).pack(side="left")
    ttk.Button(buttons,text="終了",command=lambda:end_broadcast(root,timeList,time_box.get(),stage_box.get())).pack(side="left")
    label_tx = tk.StringVar()
    now_recoding=tk.Label(root,textvariable=label_tx)
    now_recoding.pack()
    root.mainloop()