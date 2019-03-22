class Settings():
    def __init__(self):
        self.snake_speed = 8
        self.windows_width = 800
        self.windows_height = 600
        self.cell_size = 10
        self.map_width = int(self.windows_width / self.cell_size)
        self.map_height = int(self.windows_height / self.cell_size)
        # 颜色定义
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (230, 230, 230)
        self.dark_gray = (40, 40, 40)
        self.DARKGreen = (0, 155, 0)
        self.Green = (0, 255, 0)
        self.Red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.dark_blue = (0, 0, 139)
        # 游戏背景颜色
        self.BG_COLOR = self.white
        # 定义方向
        self.UP = 1
        self.DOWN = 2
        self.LEFT = 3
        self.RIGHT = 4
        # 贪吃蛇头部下标
        self.HEAD = 0
