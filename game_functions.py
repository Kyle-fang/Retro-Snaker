import pygame
import sys
import random
import time

#游戏运行主体black
def running_game(screen,snake_speed_clock, ai_settings):
	startx = random.randint(3, ai_settings.map_width - 8) #开始位置
	starty = random.randint(3, ai_settings.map_height - 8)
	snake_coords = [{'x': startx, 'y': starty},  #初始贪吃蛇
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]

	direction = ai_settings.RIGHT   #  开始时向右移动
	music()
	food = get_random_location(ai_settings)     #实物随机位置
	#paused为暂停标志
	global paused
	paused = 1
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminate()
			elif event.type == pygame.KEYDOWN:
				if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != ai_settings.RIGHT:
					direction = ai_settings.LEFT
				elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != ai_settings.LEFT:
					direction = ai_settings.RIGHT
				elif (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != ai_settings.DOWN:
					direction = ai_settings.UP
				elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != ai_settings.UP:
					direction = ai_settings.DOWN
				elif event.key == pygame.K_SPACE:
					ai_settings.snake_speed=20
				elif event.key == pygame.K_p:
					paused = -paused
				elif event.key == pygame.K_ESCAPE:
					terminate()
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					ai_settings.snake_speed = 8

		if paused == 1:
			'''当paused=1时执行下面的代码，否则再次循环'''
			move_snake(direction, snake_coords, ai_settings) #移动蛇
			ret = snake_is_alive(snake_coords,ai_settings)
			if not ret:
				break #蛇跪了. 游戏结束
			snake_is_eat_food(snake_coords, food, ai_settings) #判断蛇是否吃到食物

			screen.fill(ai_settings.BG_COLOR)
			#draw_grid(screen)
			draw_snake(screen, snake_coords,ai_settings)
			draw_food(screen, food, ai_settings)
			draw_score(screen, (len(snake_coords) - 3)*10, ai_settings)		#蛇增加的长度乘10为获得的分数
			pygame.display.update()
			snake_speed_clock.tick(ai_settings.snake_speed) #控制fps
#将食物画出来
def draw_food(screen, food,ai_settings):
	x = food['x'] * ai_settings.cell_size
	y = food['y'] * ai_settings.cell_size
	foodRect = pygame.Rect(x, y, ai_settings.cell_size, ai_settings.cell_size)
	pygame.draw.rect(screen, ai_settings.Red, foodRect)
#将贪吃蛇画出来
def draw_snake(screen, snake_coords, ai_settings):
	for coord in snake_coords:
		x = coord['x'] * ai_settings.cell_size
		y = coord['y'] * ai_settings.cell_size
		wormSegmentRect = pygame.Rect(x, y, ai_settings.cell_size, ai_settings.cell_size)
		pygame.draw.rect(screen, ai_settings.black, wormSegmentRect)
		'''
		个性化：
		wormInnerSegmentRect = pygame.Rect(                #蛇身子里面的第二层亮绿色
			x + 4, y + 4, cell_size - 8, cell_size - 8)
		pygame.draw.rect(screen, blue, wormInnerSegmentRect)
		'''
#画网格(可选)
def draw_grid(screen, ai_settings):
	for x in range(0, ai_settings.windows_width, ai_settings.cell_size):  # draw 水平 lines
		pygame.draw.line(screen, ai_settings.dark_gray, (x, 0), (x, ai_settings.windows_height))
	for y in range(0, ai_settings.windows_height, ai_settings.cell_size):  # draw 垂直 lines
		pygame.draw.line(screen, ai_settings.dark_gray, (0, y), (ai_settings.windows_width, y))
#移动贪吃蛇
def move_snake(direction, snake_coords, ai_settings):
    if direction == ai_settings.UP:
        newHead = {'x': snake_coords[ai_settings.HEAD]['x'], 'y': snake_coords[ai_settings.HEAD]['y'] - 1}
    elif direction == ai_settings.DOWN:
        newHead = {'x': snake_coords[ai_settings.HEAD]['x'], 'y': snake_coords[ai_settings.HEAD]['y'] + 1}
    elif direction == ai_settings.LEFT:
        newHead = {'x': snake_coords[ai_settings.HEAD]['x'] - 1, 'y': snake_coords[ai_settings.HEAD]['y']}
    elif direction == ai_settings.RIGHT:
        newHead = {'x': snake_coords[ai_settings.HEAD]['x'] + 1, 'y': snake_coords[ai_settings.HEAD]['y']}

    snake_coords.insert(0, newHead)
#判断蛇死了没
def snake_is_alive(snake_coords, ai_settings):
	tag = True
	if snake_coords[ai_settings.HEAD]['x'] == -1 or snake_coords[ai_settings.HEAD]['x'] == ai_settings.map_width or\
            snake_coords[ai_settings.HEAD]['y'] == -1 or \
			snake_coords[ai_settings.HEAD]['y'] == ai_settings.map_height:
		tag = False # 蛇碰壁啦
	for snake_body in snake_coords[1:]:
		if snake_body['x'] == snake_coords[ai_settings.HEAD]['x'] and snake_body['y'] == snake_coords[ai_settings.HEAD]['y']:
			tag = False # 蛇碰到自己身体啦
	return tag
#判断贪吃蛇是否吃到食物
def snake_is_eat_food(snake_coords, food, ai_settings):  #如果是列表或字典，那么函数内修改参数内容，就会影响到函数体外的对象。
	if snake_coords[ai_settings.HEAD]['x'] == food['x'] and snake_coords[ai_settings.HEAD]['y'] == food['y']:
		food['x'] = random.randint(0, ai_settings.map_width - 1)
		food['y'] = random.randint(0, ai_settings.map_height - 1) # 食物位置重新设置
	else:
		del snake_coords[-1]  # 如果没有吃到实物, 就向前移动, 那么尾部一格删掉
#食物随机生成
def get_random_location(ai_settings):
	return {'x': random.randint(0, ai_settings.map_width - 1), 'y': random.randint(0, ai_settings.map_height - 1)}
# 背景音乐
def music():
	for m in range(1,2):
		file = r'music/'+str(m)+'.mp3'
		pygame.mixer.init()
		pygame.mixer.music.load(file)
		pygame.mixer.music.play(1,0.0)

#开始信息显示
def show_start_info(screen):
	font = pygame.font.Font('myfont.ttf', 40)
	tip = font.render('按任意键开始游戏~~~', True, (65, 105, 225))	#在屏幕中显示文字
	gamestart = pygame.image.load('gamestart.png')
	screen.blit(gamestart, (140, 30))
	screen.blit(tip, (240, 550))
	pygame.display.update()

	while True:  #键盘监听事件
		for event in pygame.event.get():  # event handling loop
			if event.type == pygame.QUIT:
				terminate()     #终止程序
			elif event.type == pygame.KEYDOWN:
				if (event.key == pygame.K_ESCAPE):  #终止程序
					terminate() #终止程序
				else:
					return #结束此函数, 开始游戏

#游戏结束信息显示
def show_gameover_info(screen):
	font = pygame.font.Font('myfont.ttf', 40)
	tip = font.render('按Q或者ESC退出游戏, 按任意键重新开始游戏~', True, (65, 105, 225))
	gamestart = pygame.image.load('gameover.png')
	screen.blit(gamestart, (60, 0))
	screen.blit(tip, (80, 300))
	pygame.display.update()

	while True:  #键盘监听事件
		for event in pygame.event.get():  # event handling loop
			if event.type == pygame.QUIT:
				terminate()     #终止程序
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:  #终止程序
					terminate() #终止程序
				else:
					return #结束此函数, 重新开始游戏

#画成绩
def draw_score(screen,score, ai_settings):
	font = pygame.font.Font('myfont.ttf', 30)
	scoreSurf = font.render('得分: %s' % score, True, ai_settings.Green)
	scoreRect = scoreSurf.get_rect()
	scoreRect.topleft = (ai_settings.windows_width - 120, 10)
	screen.blit(scoreSurf, scoreRect)
#程序终止
def terminate():
	pygame.quit()
	sys.exit()

