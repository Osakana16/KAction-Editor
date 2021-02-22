# KAction-Editor.py - 本プログラムのスタートアップ部
import tkinter, tkinter.messagebox, tkinter.filedialog
import worldeditor

# プログラム自身
class Program(tkinter.Tk):
    def __init__(self):
        super().__init__()

        # ウィンドウ設定
        self.title("KAction-Editor")
        self.geometry("640x480")
        self.palette = worldeditor.Palette(self)

        # リストボックスの設定
        # 読みこまれたワールド一覧
        self.world_list = tkinter.Listbox(master=self, selectmode='multiple')
        # ダブルクリックされたワールドを読みこむ。
        self.world_list.bind('<Double-Button-1>', lambda e: self.palette.Load(worldeditor.Loader(self.world_list.get('active').split('.')[0])))
        self.world_list.grid()

        # メニューの設定
        self.menubar = tkinter.Menu(self)

        # ファイル関連
        self.filemenu = tkinter.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='新規作成')
        self.filemenu.add_command(label='開く', command=self.OpenWorld)
        self.filemenu.add_command(label='終了', command=self.destroy)
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

    # マップを開く
    def OpenWorld(self):
        import os, glob
        folder_name = tkinter.filedialog.askdirectory(initialdir=os.path.abspath(os.path.dirname(__file__)))
        # フォルダーからファイル一覧を取得
        files = glob.glob(folder_name + '/*.pmap')
        for file in files:
            self.world_list.insert(0, file)

    # 終了処理
    def destroy(self):
        self.palette.quit()
        super().destroy()

program = Program()
program.Run()