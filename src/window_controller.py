import tkinter as tk
from tkinter.constants import LEFT, TOP
from tkinter import filedialog
from tkinter import StringVar
from tkinter import ttk
from tkinter import constants
import os
import re
#

def input_text(frame_r: tk.Frame,
               label_text: str,
               text_width: int,
               initial: str = None,
               side_: constants = TOP,
               side_label: constants = LEFT,
               fmt: str = None):
    """テキストの入力ボックスを作成

    Args:
        frame_r (tkinter.Frame): 配置するフレーム
        label_text (str): ラベル
        text_width (int): 入力欄の幅
        initial (str, optional): 初期値. Defaults to None.
        side_ (tk.constants, optional): テキストボックス群の配置. Defaults to TOP.
        side_label (tk.contains, optional): ラベルとテキストボックスの位置関係. Defaults to LEFT.
        fmt (str): 正規表現. Default to None.
    Returns:
        tkinter.entry: テキストボックス
    """
    frame = tk.Frame(frame_r)
    frame.pack(side=side_)
    label = tk.Label(frame, text = label_text)
    label.pack(side=LEFT)
    if not fmt == None:
        def validate_input_header(val):
            """正規表現チェック

            Args:
                val (str)): 入力値
                fmt (str):正規表現

            Returns:
                bool: 正規表現にマッチしているか
            """
            if val == "":
                return True
            if re.fullmatch(fmt, val):
                return True
            return False
        validate = frame_r.register(validate_input_header)
        text = tk.Entry(frame, width = text_width,validate="key",validatecommand=(validate, "%P"))

    else:
        text = tk.Entry(frame, width = text_width)

    if initial != None:
        text.insert(tk.END,initial)
    label.pack(side=side_label)
    text.pack(side=side_label)
    return text

def input_path(frame_r: tk.Frame,
               label_text: str,
               width_input: int,
               file_or_dir: str = "file",
               initial: str = None,
               side_: constants = TOP):
    """ファイル（ディレクトリ）選択ボックスの配置

    Args:
        frame_r (tkinter.Frame): 配置するフレーム
        label_text (str): ラベル
        width_input (int): 入力欄の幅
        file_or_dir (str): "file" or "dir". Defaults to "file"
        initial (str, optional): 初期値. Defaults to None.
        side_ (tk.constants, optional): テキストボックス群の配置. Default to TOP.

    Returns:
        tkinter.Entry: パスの入力欄
    """
    frame = tk.Frame(frame_r)
    frame.pack(side=side_)
    label = tk.Label(frame, text = label_text)
    label.pack(side=LEFT)
    entry = StringVar()
    IFileEntry = ttk.Entry(frame, textvariable=entry, width=width_input)
    if initial != None:
        IFileEntry.insert(tk.END, initial)
    IFileEntry.pack(side=LEFT)
    if file_or_dir == "file":
        IFileButton = ttk.Button(frame, text="参照", command=lambda:_filedialog_clicked(entry))
    elif file_or_dir == "dir":
        IFileButton = ttk.Button(frame, text="参照", command=lambda:_dirdialog_clicked(entry))
    IFileButton.pack(side=LEFT)
    return entry

def label(frame_r: tk.Frame, text: str, side: constants = TOP):
    """ラベルを配置

    Args:
        frame_r (tk.Frame): 配置するフレーム
        text (str): ラベル本文
        side (tk.constants, optional): 配置の仕方. Defaults to TOP.
    """
    label = tk.Label(frame_r,text=text)
    label.pack(side=side)
    
def new_window(size: str,
               title: str = "window",
               resize: tuple = None,
               icon_file: str = None,
               topLevel: bool = False):
    """新規ウィンドウの作成

    Args:
        size (str): サイズ. "[width]x[height]"で入力
        title (str, optional): ウィンドウタイトル. Defaults to "window".
        resize (tuple, optional): ウィンドウのサイズ変更の可否。タプル型でTrue or Falseで設定(width, height). Defaults to None.
        icon_file (str, optional): ウィンドウのアイコンファイルのパス. Defaults to None.
        topLevel (bool, optional): ウィンドウをメインウィンドウに連動させるか. Defaults to False.

    Returns:
        tkinter.Tk: ウィンドウ
    """
    if topLevel:
        win = tk.Toplevel()
    else:
        win = tk.Tk()
    win.geometry(size)
    win.title(title)
    if not resize == None:
        win.resizable(width = resize[0], height = resize[1])
    if not icon_file == None:
        if os.path.isfile(icon_file):
            win.iconphoto(False, tk.PhotoImage(file = icon_file))
    return win

def scroll(frame_r: tk.Frame, widget: tk.Widget, vector: str = "Y", is_canvas: bool = False, region: list = None):
    """スクロールの作成

    Args:
        frame_r (tk.Frame): 配置フレーム
        widget (widget): 対象ウィジェット
        vector (int, optional): スクロール方向.y方向:"Y", x方向:"X". Defaults to "Y".
        is_canvas (bool, optional): canvasに配置するかどうか. Defaults to False.
        region (list), optional): canvasに配置する場合、スクロールサイズ. Defaults to None.
    """
    if vector == "X":
        scroll = tk.Scrollbar(frame_r,orient=tk.HORIZONTAL,command = widget.xview)
        widget.config(xscrollcommand = scroll.set)
    elif vector == "Y":
        scroll = tk.Scrollbar(frame_r,orient=tk.VERTICAL,command = widget.yview)
        widget.config(yscrollcommand = scroll.set)
    if is_canvas:
        widget.config(scrollregion=region)
    return scroll

def change_frame(frame):
    """画面遷移

    Args:
        frame (tk.Frame): 表示するフレーム
    """
    frame.tkraise()

def listbox(frame_r: tk.Frame,
            lists: list,
            text: str = None,
            side: constants = TOP,
            width: int = 30,
            height: int = 6):
    """リストボックスを作成
    listbox.curselection()で現在選択しているインデックスを取得
    listbox.get(xx)でそのテキストを取得
    Args:
        frame_r (tk.Frame): 配置したフレーム
        lists (list): 項目
        text_ (str, optional): 何のリストか示すテキスト. Defaults to None.
        side_ (tk.contains, optional): どこに配置するか. Defaults to TOP.
        width_ (int, optional): 幅. Defaults to 30.
        height_ (int, optional): 表示する項目数. Defaults to 6.

    Returns:
        tk.Listbox: 作成したリストボックス
    """
    var = tk.StringVar(value = lists)
    frame = tk.Frame(frame_r)
    frame.pack(side = side)
    if not text == None:
        label = tk.Label(frame, text = text)
        label.pack()
    listbox = tk.Listbox(frame, listvariable=var,width = width,height = height)
    listbox.pack(side="left")
    if len(lists) > height:
        scrollbar = ttk.Scrollbar(frame, orient = "vertical", command=listbox.yview)
        listbox["yscrollcommand"] = scrollbar.set
        scrollbar.pack(side="right",fill="both")

    return listbox

def table(frame_r, header, lists, widths, side_=TOP, is_scroll = False):
    """テーブルを作成する

    Args:
        frame_r (tk.Frame): 配置したいフレーム
        header (list): 項目名のリスト
        lists (list): 挿入するデータのリスト。項目数が複数の場合、listsのそれぞれの要素はlistもしくはtupleとなる.

        widths (list): それぞれの項目の幅
        side_ (tk.contains, optional): どこに配置するか. Defaults to TOP.
        is_scroll (bool, optional): スクロールは必要か. Defaults to False.

    Returns:
        tk.Treeview: テーブル
    """
    tree_frame = tk.Frame(frame_r)
    tree_frame.pack(side=side_)
    tree = ttk.Treeview(tree_frame)
    tree["column"] = tuple([i for i in range(1, len(header)+1)])
    tree["show"] = "headings"

    for i in tree["column"]:
        tree.column(int(i), width = widths[int(i)-1])
    for i in range(1, len(header) + 1):
        tree.heading(i, text=header[i-1])
    
    for l in lists:
        tree.insert("", "end", values=tuple(l))
    
    if is_scroll:
        vbar = scroll(tree_frame, tree)
        tree.pack(side="left")
        vbar.pack(side="left",fill=tk.Y)
    else:
        tree.pack()
    
    return tree


# ファイル指定の関数
def _filedialog_clicked(entry):
    fTyp = [("", "*")]
    iFile = os.path.abspath(os.path.dirname(__file__))
    iFilePath = filedialog.askopenfilename(filetype = fTyp, initialdir = iFile)
    entry.set(iFilePath)

# フォルダ指定の関数
def _dirdialog_clicked(entry):
    iDir = os.path.abspath(os.path.dirname(__file__))
    iDirPath = filedialog.askdirectory(initialdir = iDir)
    entry.set(iDirPath)

class TreeView():
    
    def __init__(self,
                 frame: tk.Frame,
                 header: list,
                 widths: list,
                 height: int,
                 is_scroll: bool,
                 is_headings: bool):
        """TreeViewを初期化

        Args:
            frame (tk.Frame): 配置したいフレーム
            header (list): 項目名のリスト
            widths (list): それぞれの項目の幅
            height (int): 表示する行数
            is_scroll (bool): スクロールバーの有無
            is_headings (bool): 開くやつか否か
        """
        self.is_headings = is_headings
        self.is_scroll = is_scroll
        tree_frame = tk.Frame(frame)
        
        tree = ttk.Treeview(tree_frame)
        if is_headings:
            num_column = len(header)+1
            tree["show"] = "headings"
        else:
            num_column = len(header)
        tree["column"] = tuple([i for i in range(1,num_column)])
        tree["height"] = height
        
        if is_headings:
            for i in tree["column"]:
                tree.column(int(i),width = widths[int(i)-1])
            for i in range(1,num_column):
                tree.heading(i,text=header[i-1])
        else:
            tree.column("#0",width=widths[0])
            for i in tree["column"]:
                tree.column(int(i),width=widths[int(i)])
            tree.heading("#0",text=header[0])
            for i in range(1,num_column):
                tree.heading(i,text=header[i])
        tree.pack()
        self.tree_frame = tree_frame
        self.tree = tree
    
    def insert_data(self,datas: list or tuple, parent: str = None, is_open: bool = False):
        """Treeviewにデータを挿入する

        Args:
            datas (list or tuple): 挿入するデータ
            parent (str, optional): 親要素. Defaults to None.
            is_open (bool, optional): 開くか否か. Defaults to False.

        Returns:
            str: 行の要素
        """
        if parent == None:
            p = ""
        else:
            p = parent
        if self.is_headings:
            iid = self.tree.insert(
                p,
                tk.END,
                value=tuple(datas)
            )
        else:
            iid = self.tree.insert(
                p,
                tk.END,
                text = datas[0],
                value=tuple(datas[1:]),
                open=is_open
            )
        return iid
    
    def plot(self, frame_side: constants = TOP):
        """Treeviewの配置

        Args:
            frame_side (tk.constans): 配置箇所
        """
        self.tree_frame.pack(side=frame_side)
        if self.is_scroll:
            self.tree.pack(side="left")
            scroll = tk.Scrollbar(self.tree_frame,orient=tk.VERTICAL,command=self.tree.yview)
            scroll.pack(side="left",fill="y")
            self.tree["yscrollcommand"] = scroll.set
        else:
            self.tree.pack()
            