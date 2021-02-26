import tkinter, tkinter.messagebox

# ワールド読込器
class Loader:
    def __init__(self, path: str):
        self.chips = dict() # チップ情報
        self.elems = list() # マップ全体の構造

        # マップの読み込み
        with open(path + '.pmap', mode='r', encoding='utf_16') as f:
            for line in f.readlines():
                # 1行分追加
                self.elems.append([])
                # 新しく追加した行をターゲットに設定。
                target = self.elems[-1]
                # ファイル内の文字を追加
                for c in line:
                    target.append(c)
                target.pop(-1)

        # csvの読み込み
        import csv
        with open(path + '.csv', mode='r', newline='', encoding='utf_16') as csvfile:
            cells = csv.reader(csvfile)
            for row in cells:
                self.chips[row[0]] = row[1]

        for key in self.chips.keys():
            # 最初のセルはスキップ
            if key == '要素':
                continue
            elif len(key) != 1:
                raise ValueError
            self.chips[key] = tkinter.PhotoImage(file=self.chips[key])

# パレットウィンドウ
class Palette(tkinter.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title('パレット')
        self.transient(master)
        self.__chips = dict()
        self.__elems = list()
        self.__canvas = tkinter.Canvas(self)
        self.__canvas.grid()

    def destroy(self):
        self.withdraw()

    def Load(self, loader: Loader):
        self.__chips = loader.chips
        self.__elems = loader.elems

        i = 1
        for key in self.__chips.keys():
            # 最初のセルを無視。
            if key == '要素':
                continue

            self.__canvas.create_image(i * 60, 60, image=self.__chips[key])
            i += 1