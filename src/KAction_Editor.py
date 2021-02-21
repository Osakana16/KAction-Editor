# KAction-Editor.py - 本プログラムのスタートアップ部
import tkinter, tkinter.messagebox

# プログラム自身
class Program(tkinter.Tk):
    def __init__(self):
        super().__init__()

        # ウィンドウ設定
        self.title("KAction-Editor")
        self.geometry("640x480")

        # メニューの設定
        self.menubar = tkinter.Menu(self)
        # ファイル関連
        self.filemenu = tkinter.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='新規作成')
        self.filemenu.add_command(label='開く')
        self.filemenu.add_command(label='終了', command=self.OnQuit)
        self.menubar.add_cascade(label='ファイル', menu=self.filemenu)

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

    # 終了処理
    def OnQuit(self):
        quit()

program = Program()
program.Run()