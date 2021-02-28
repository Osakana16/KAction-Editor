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
        self.__selecting_elem = ' '

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
            self.__elems[i].append(key)
            i += 1

    def __Select(self, event: tkinter.Event):
        x, y = (event.x // 120, event.y // 120)
        try:
            self.__selecting_elem = self.__elems[y][x]
        except:
            print(self.__selecting_elem)

class MapCanvas(tkinter.Canvas):
    def __init__(self, w, h, frame: tkinter.Frame, palette: Palette):
        super().__init__(frame, width=w, height=h)

        # スクロールバーの設定
        self.__scroll_bars = [tkinter.Scrollbar(frame, orient=tkinter.HORIZONTAL, command=self.xview), 
                              tkinter.Scrollbar(frame, orient=tkinter.VERTICAL, command=self.yview)]

        self.__scroll_bars[0].grid(row=1, column=0, sticky=tkinter.W + tkinter.E)
        self.__scroll_bars[1].grid(row=0, column=1, sticky=tkinter.S + tkinter.N)
        self.config(xscrollcommand=self.__scroll_bars[0].set, yscrollcommand=self.__scroll_bars[1].set)

        self.bind('<ButtonPress-1>', self.__Pressed)
        self.bind('<Motion>', self.__Draw)
        self.__elems = list()
        self.__chips = dict()
        self.__palette = palette
        self.__width, self.__height = (0, 0)

    # loaderから構造を参照する。
    def Load(self, loader):
        self.__elems = loader.elems
        self.__chips = loader.chips

        mx, my = (0, len(self.__elems))

        for y in range(my):
            temp = len(self.__elems[y])
            if temp > mx:
                mx = temp

        self.__width, self.__height = (mx * 120, my * 120)
        self.config(scrollregion=(0, -60, self.__width, self.__height))

    def Save(self, filename: str):
        with open(filename, 'w', encoding='utf_16') as f:
            for sen in self.__elems:
                for ch in sen:
                    f.write(ch)
                f.write('\n')

    def __PutChip(self, x, y, ch):
        if y < 0 or x < 0:
            return
        
        must_loop = True
        while must_loop:
            try:
                self.__elems[y][x] = ch
                must_loop = False
            except IndexError:
                if len(self.__elems) <= y:
                    self.__elems.append([])
                elif len(self.__elems[y]) <= x:
                    self.__elems[y].append(' ')

    def __Pressed(self, event: tkinter.Event):
        print(self.winfo_width(), self.winfo_height())
        if not self.__HasDrawingElems():
            return

        mx = ((int(self.__scroll_bars[0].get()[1] * self.__width) - self.winfo_width()) + event.x)
        my = ((int(self.__scroll_bars[1].get()[1] * self.__height) - self.winfo_height()) + event.y)
        x, y = (mx // 120, my // 120)
        self.__PutChip(x, y, self.__palette.SelectingElem())

    def __Draw(self, event: tkinter.Event):
        self.create_rectangle(0, -60, self.__width, self.__height*2, fill='black')
        if not self.__HasDrawingElems():
            return

        for y in range(len(self.__elems)):
            for x in range(self.__width // 120):
                try:
                    elem = self.__elems[y][x]
                    if elem != ' ':
                        self.create_image(x * 120, y * 120, image=self.__chips[elem])
                except IndexError:
                    self.create_rectangle(x * 120 - 60, y * 120 - 60, x * 120 + 120 - 60, y * 120 + 120  - 60, fill='red')
                except KeyError:
                    print(elem)

    def __HasDrawingElems(self) -> bool:
        return len(self.__elems) > 0