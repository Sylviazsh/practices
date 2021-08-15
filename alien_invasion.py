import sys
import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group


class Settings():
    """存储《外星人入侵》所有类的设置"""

    def __init__(self):
        """初始化游戏的设置"""
        self.screen_width = 1200  # 创建窗口
        self.screen_height = 800
        self.bg_color = (230, 230, 230)  # 背景色
        self.ship_speed_factor = 1.5
        # 子弹设置
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60


class Ship():
    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其初始值"""
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('ship.jpg')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # 将每艘新飞船放在屏幕底部
        self.rect.centerx = self.screen_rect.centerx
        self.center = float(self.rect.centerx)
        self.rect.bottom = self.screen_rect.bottom
        # 移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志调整飞船位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)


class Bullet(Sprite):
    """一个对飞船发射子弹进行管理的类"""

    def __init__(self, ai_settings, screen, ship):
        """在飞船所处位置创建一个子弹对象"""
        super(Bullet, self).__init__()
        self.screen = screen
        # 在（0，0）处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """向上移动子弹"""
        self.y -= self.speed_factor  # 更新表示子弹位置的小数值
        self.rect.y = self.y  # 更新表示子弹的rect位置

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        new_bullet = Bullet(ai_settings, screen, ship)  # 创建一颗子弹，并将其加入到编组bullets中
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, ship, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_screen(ai_settings, screen, ship, bullets):
    """更新屏幕上的图像，并切换到新屏幕"""
    screen.fill(ai_settings.bg_color)  # 每次循环时重绘屏幕
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    pygame.display.flip()  # 让最近绘制的屏幕可见


def run_game():
    pygame.init()  # 初始化游戏并创建一个屏幕对象
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invation')  # 设置标题
    ship = Ship(ai_settings, screen)  # 创建一个飞船
    bullets = Group()  # 创建一个用于储存子弹的编组

    while True:  # 开始游戏的主循环
        check_events(ai_settings, screen, ship, bullets)  # 监视键盘和鼠标事件
        ship.update()
        bullets.update()
        # 删除已消失的子弹
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
        # print(len(bullets))
        update_screen(ai_settings, screen, ship, bullets)  # 更新屏幕上的图像


run_game()
