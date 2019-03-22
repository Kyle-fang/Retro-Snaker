.pyimport pygame
from settings import Settings
import game_functions as gf

ai_settings = Settings()
def game():
	pygame.init()       # 模块初始化
	snake_speed_clock = pygame.time.Clock() # 创建Pygame时钟对象
	screen = pygame.display.set_mode((ai_settings.windows_width, ai_settings.windows_height)) #
	screen.fill(ai_settings.white)

	pygame.display.set_caption("贪吃蛇小游戏") #设置标题
	gf.show_start_info(screen)               #欢迎信息
	while True:
		gf.running_game(screen, snake_speed_clock, ai_settings)
		gf.show_gameover_info(screen)

game()
