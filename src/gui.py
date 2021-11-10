from dearpygui import dearpygui as dpg

FONTFILE = "../fonts/NotoSansCJKjp-Medium.otf"

# dearpyGUIの座標系について
# windowの左上が(0, 0)
# x軸は右が正の方向
# y軸は下が正の方向
class ScoreView():

    TEXTURE_SIZE = {
    }
    def __init__(self):
        # ノーツのテクスチャ画像を初期化
        with dpg.texture_registry():
            # 1小節のノーツの個数

            # BMS_COUNT(1小節の分解能)
            self.BMS_COUNT = 9600
            # BMS_COUNT（1小節の分解能）に対する小節の倍率
            self.BAR_MAGNIFICATION = 300
            # 1小節のノーツの個数
            self.NOTES_NUM_PER_BAR = self.BMS_COUNT / self.BAR_MAGNIFICATION

            # スクラッチレーンの数
            self.SCRATCH_LANE_NUM = 1
            # 鍵盤のレーンの数
            self.LANE_NUM = 7

            width, height, channels, data = dpg.load_image("../images/scratch.png")
            self.TEXTURE_SIZE['scratch_tex'] = (width, height)
            # 1スクラッチレーンの横幅
            self.SCRATCH_LANE_WIDTH = width
            scratch_tex = dpg.add_static_texture(width, height, data, id='scratch_tex')
            width, height, channels, data = dpg.load_image("../images/white.png")
            # 1レーンの横幅
            self.LANE_WIDTH = width
            # 小節の横幅
            self.BAR_WIDTH = self.SCRATCH_LANE_NUM * self.SCRATCH_LANE_WIDTH + self.LANE_NUM * self.LANE_WIDTH
            # 小節の高さ
            self.BAR_HEIGHT = height*32
            self.TEXTURE_SIZE['white_tex'] = (width, height)
            white_tex = dpg.add_static_texture(width, height, data, id='white_tex')
            width, height, channels, data = dpg.load_image("../images/black.png")
            self.TEXTURE_SIZE['black_tex'] = (width, height)
            black_tex = dpg.add_static_texture(width, height, data, id='black_tex')
            # 4分小節線のピクセル幅
            self.BAR_1_4 = self.BAR_HEIGHT / 4
            # 16分小節線のピクセル幅
            self.BAR_1_16 = self.BAR_HEIGHT / 16

    def draw_tex(self, tex, x, y):
        """Summary line.
        テクスチャを描画します
        
        Args:
           tex(str): テクスチャの名前
           x: 左上のx座標
           y: 左上のy座標
        """
        dpg.draw_image(tex, pmin=(x, y), pmax=(x+self.TEXTURE_SIZE[tex][0], y+self.TEXTURE_SIZE[tex][1]))

    def draw_bar(self, x, y):
        """Summary line.
        左上の座標(x,y)を視点に、上方向（y軸負の方向）に小節を描画します

        Args:
            x: 左上のx座標
            y: 左上のy座標
        """
        c_x = x
        c_y = y+self.TEXTURE_SIZE['white_tex'][1]
        dpg.draw_line((c_x+self.BAR_WIDTH, c_y), (c_x+self.BAR_WIDTH, c_y-self.BAR_HEIGHT))
        # 縦棒を描画（スクラッチレーン）
        for c in range(self.SCRATCH_LANE_NUM):
            dpg.draw_line((c_x+self.SCRATCH_LANE_WIDTH*c, c_y), (c_x+self.SCRATCH_LANE_WIDTH*c, c_y-self.BAR_HEIGHT))
        c_x += self.SCRATCH_LANE_WIDTH
        # 縦棒を描画（鍵盤レーン）
        for c in range(self.LANE_NUM):
            dpg.draw_line((c_x+self.LANE_WIDTH*c, c_y), (c_x+self.LANE_WIDTH*c, c_y-self.BAR_HEIGHT))
        c_x = x
        c_y = y+self.TEXTURE_SIZE['white_tex'][1]
        # 16分線を描画
        for r in range(0, 16):
            dpg.draw_line((c_x, c_y-self.BAR_1_16*r), (c_x+self.BAR_WIDTH, c_y-self.BAR_1_16*r), color=(128,128,128))
        c_x = x
        c_y = y+self.TEXTURE_SIZE['white_tex'][1]
        # 4分線を描画
        for r in range(0, 4):
            dpg.draw_line((c_x, c_y-self.BAR_1_4*r), (c_x+self.BAR_WIDTH, c_y-self.BAR_1_4*r), color=(256,256,256))
        dpg.draw_line((c_x, c_y-self.BAR_HEIGHT), (c_x+self.BAR_WIDTH, c_y-self.BAR_HEIGHT), color=(256,256,256))

    def create_window(self):
        with dpg.font_registry():
            with dpg.font(FONTFILE, 20, default_font=True):
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Japanese)
        with dpg.window(label="Auto Clicker", width=1280, height=900) as window:
            # dpg.add_text('操作方法：\n座標追加：Space\n追加された最後の座標を削除：Delete\n追加された座標をクリック：c\nアプリ終了：Ctrl+Z')
            # 縦に3つの小節を描画
            for n in range(3, 0, -1):
                # 小節を描画
                x=0
                y=0+self.BAR_HEIGHT*n
                self.draw_bar(x, y)
                # ノーツの画像を配置
                self.draw_tex("scratch_tex", x, y)
                x += self.SCRATCH_LANE_WIDTH
                self.draw_tex("white_tex", x, y)
                x += self.LANE_WIDTH
                self.draw_tex("black_tex", x, y)
                x += self.LANE_WIDTH
                self.draw_tex("white_tex", x, y)
                x += self.LANE_WIDTH
                self.draw_tex("black_tex", x, y)
                x += self.LANE_WIDTH
                self.draw_tex("white_tex", x, y)
                x += self.LANE_WIDTH
                self.draw_tex("black_tex", x, y)
                x += self.LANE_WIDTH
                self.draw_tex("white_tex", x, y)
        viewport = dpg.create_viewport(title='Custom Title', width=1280, height=900)

        # ボタンを作る
        # button = dpg.add_button(label="Don't forget me!", parent=window)

        # ここからはおまじない程度に毎回実行する
        # dpg.setup_viewport()
        dpg.setup_dearpygui()
        dpg.show_viewport(viewport)
        dpg.start_dearpygui()
        # dpg.destroy_context()

if __name__=="__main__":
    view = ScoreView()
    view.create_window()