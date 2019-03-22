import sys

import pygame

from bullet import Bullet

from alien import Alien

from time import sleep


def check_keydown_events(event,ai_settings,screen, ship, bullets):
    '''响应按下'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_q:
        sys.exit()
    #当飞船移动时也能发射子弹
    if event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def check_events(ai_settings,screen,ship, bullets):
    '''响应鼠标键盘事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)

def update_screen(ai_settings, screen, stats, ship, bullets, aliens, play_button):
    # 每次循环时都会重绘屏幕
    # 调用方法screen_fill()——用背景色填充屏幕
    screen.fill(ai_settings.screen_bg_color)
    #在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    #aline.blitme()

    #如果游戏处于非活动状态，就绘制play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings, screen, ship, aliens, bullets):
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #print(len(bullets))  # 显示当前在屏幕上有多少个子弹，从而核实子弹确实被删除了
    check_bullet_alien_collide(ai_settings, screen, ship, aliens, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullet_num:
        # 创建一颗子弹，并将其加入到编组bullets中
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_bullet_alien_collide(ai_settings, screen, ship, aliens, bullets):
    '''检查是否有子弹击中了外星人
        如果有，就删除相应的外星人和子弹
        遍历编组bullets中所有子弹，再遍历编组aliens中的每个外星人。
        每当子弹与外星人重叠时，groupcllid()就在它返回的字典中添加一个键值对。
        两个实参True告诉pygame删除发生碰撞的子弹和外星人
    '''

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        # 删除现有所有子弹
        bullets.empty()
        # 当前外星人群消灭干净后，将会立刻出现一个新的外星人群
        create_fleet(ai_settings, screen, ship, aliens)

def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_heigth - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
    '''计算屏幕可以容纳多少行外星人'''
    #以外星人的高度来记长，减去飞船的高度和空出的外星人与飞船间的距离
    available_space_y = (ai_settings.screen_heigth - (10*alien_height) - ship_height)
    number_rows = int(available_space_y/(2*alien_height))       #number_rows为外星人的行数
    return number_rows

def crate_aline(ai_settings, screen, aliens, alien_number, rows_number):
    # 创建一个外星人并将其加入当前行
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height*rows_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    '''创建一个外星人群'''
    #创建一个外星人，并计算一行可容纳多少个外星人'''
    #外星人的间距为外星人的宽度'''
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width )
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    #穿件外星人群
    for row_number in range(number_rows):
        #创建一个外星人
        for alien_number in range(number_aliens_x):
            crate_aline(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    '''当外星人到达屏幕边缘时的应对措施'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    '''将整群外星人下移，并改变他们的方向'''
    for alien in aliens.sprites():
        alien.rect.y +=ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    '''响应被外星人撞到的飞船'''
    if stats.ships_left > 0:
        # 将ship_left减1
        stats.ships_left -= 1

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕地端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        #暂停
        sleep(0.5)
    else:
        stats.game_active = False

def check_aliens_bottom(ai_setting, stats, screen, ship, aliens, bullets):
    '''检查是否有外星人到达了屏幕底部'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞到一样处理
            ship_hit(ai_setting, stats, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    '''检查是否有外星人位于屏幕边缘，并更新外星人的位置'''
    check_fleet_edges(ai_settings, aliens)
    #更新外星人群中所有外星人的位置'''
    aliens.update()
    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    #检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
