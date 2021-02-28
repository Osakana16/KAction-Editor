# KAction-Editor.py - 本プログラムのスタートアップ部
import tkinter, tkinter.messagebox, tkinter.filedialog
import worldeditor

# プログラム自身
class Program(tkinter.Tk):
    Length = (1280, 720)
    def __init__(self):
        super().__init__()

        # ウィンドウ設定
        self.title("KAction-Editor")
        self.geometry(f"{Program.Length[0]}x{Program.Length[1]}")
        self.palette = worldeditor.Palette(self)

        self.menulist_frame = tkinter.Frame(self, width=Program.Length[0] // 2, height=Program.Length[1], borderwidth=3, relief='groove')
        self.canvas_frame = tkinter.Frame(self, width=Program.Length[0] // 2, height=Program.Length[1], borderwidth=3, relief='groove')

        # リストボックスの設定
        # 読みこまれたワールド一覧
        self.world_list = tkinter.Listbox(self.menulist_frame, selectmode='multiple')
        # ダブルクリックされたワールドを読みこむ。
        self.world_list.bind('<Double-Button-1>', self.LoadWorld)
        self.world_list.grid(row=1)
        label = tkinter.Label(self.menulist_frame, text='マップリスト')
        label.grid(row=0)

        self.canvas = worldeditor.MapCanvas(Program.Length[0] // 2, Program.Length[1] - 25, self.canvas_frame, self.palette)
        self.canvas.grid(row=0, column=0, sticky=tkinter.N + tkinter.S)

        self.canvas_frame.grid(row=0, column=0, sticky=tkinter.N + tkinter.S + tkinter.W + tkinter.E)
        self.menulist_frame.grid(row=0, column=2, sticky=tkinter.N)

        # メニューの設定
        self.menubar = tkinter.Menu(self)

        # ファイル関連
        self.filemenu = tkinter.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='新規作成')
        self.filemenu.add_command(label='開く', command=self.OpenWorld)
        self.filemenu.add_command(label='保存', command=self.Save)
        self.menubar.add_cascade(label='ファイル', menu=self.filemenu)

        # ツール
        self.toolmenu = tkinter.Menu(self.menubar, tearoff=0)
        self.toolmenu.add_command(label='パレット', command=self.palette.deiconify)
        self.menubar.add_cascade(label='ツール', menu=self.toolmenu)

        # ヘルプ関連
        import webbrowser
        self.helpmenu = tkinter.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label='マニュアル')
        self.helpmenu.add_command(label='GitHubのページ', command=lambda: webbrowser.open('https://github.com/Osakana16/KAction-Editor'))
        self.menubar.add_cascade(label='ヘルプ', menu=self.helpmenu)

        self.config(menu=self.menubar)
        self.is_first_launch = False    # 初めて起動したかどうか。

    # メインループ
    def Run(self):
        self.mainloop()

    # ディレクトリ内のマップを開く
    def OpenWorld(self):
        import os, glob
        folder_name = tkinter.filedialog.askdirectory(initialdir=os.path.abspath(os.path.dirname(__file__)))
        # フォルダーからファイル一覧を取得
        files = glob.glob(folder_name + '/*.pmap')
        for file in files:
            self.world_list.insert(0, file)

    def Save(self):
        self.canvas.Save(self.world_list.get('active'))

    # 開いたマップを読み込む。
    def LoadWorld(self, event):
        loader = worldeditor.Loader(self.world_list.get('active').split('.')[0])
        self.canvas.Load(loader)
        self.palette.Load(loader)

    # 終了処理
    def destroy(self):
        self.palette.quit()
        super().destroy()

program = Program()
program.Run()