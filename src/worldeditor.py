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
        self.bind('<ButtonPress-1>', self.__Select)
        self.transient(master)
        self.__chips = dict()
        self.__elems = list()
        self.__canvas = tkinter.Canvas(self)
        self.__canvas.grid()
        self.__selecting_elem = None

    def destroy(self):
        self.withdraw()

    def SelectingElem(self):
        return self.__selecting_elem

    def Load(self, loader: Loader):
        chips = loader.chips
        elems = loader.elems
        self.__elems = [[]]

        i = 0
        for key in chips.keys():
            # 最初のセルを無視。
            if key == '要素':
                continue

            self.__canvas.create_image(i * 60 + 60, 60, image=chips[key])
            self.__elems[i].append(chips[key])
            i += 1

class MapCanvas(tkinter.Canvas):
    def __init__(self, w, h, frame: tkinter.Frame, palette: Palette):
        super().__init__(frame, width=w, height=h)

        # スクロールバーの設定
        self.__scroll_bars = [tkinter.Scrollbar(frame, orient=tkinter.HORIZONTAL, command=self.xview), 
                              tkinter.Scrollbar(frame, orient=tkinter.VERTICAL, command=self.yview)]

        self.__scroll_bars[0].grid(row=1, column=0, sticky=tkinter.W + tkinter.E)
        self.__scroll_bars[1].grid(row=0, column=1, sticky=tkinter.S + tkinter.N)
        self.config(xscrollcommand=self.__scroll_bars[0].set, yscrollcommand=self.__scroll_bars[1].set)

        self.bind('<ButtonPress-1>')
        self.bind('<Motion>', self.__Draw)
        self.__elems = list()
        self.__chips = dict()
        self.__palette = palette

    # loaderから構造を参照する。
    def Load(self, loader):
        self.__elems = loader.elems
        self.__chips = loader.chips

        mx, my = (0, len(self.__elems))

        for y in range(my):
            temp = len(self.__elems[y])
            if temp > mx:
                mx = temp

        self.config(scrollregion=(0, -60, mx * 120, my * 120))

    def __Draw(self, event: tkinter.Event):
        if not self.__HasDrawingElems():
            return

        for y in range(len(self.__elems)):
            for x in range(len(self.__elems[y])):
                elem = self.__elems[y][x]
                if elem != ' ':
                    self.create_image(x * 120, y * 120, image=self.__chips[elem])

    def __HasDrawingElems(self) -> bool:
        return len(self.__elems) > 0