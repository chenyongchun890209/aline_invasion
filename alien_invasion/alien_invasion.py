
import sys
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
import pygame


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源。"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        #创建用于存储子弹的编组
        self.bullets = pygame.sprite.Group()
        #创建用于存储外星人的编组
        self.aliens = pygame.sprite.Group()
        # 设置背景色
        self.bg_color = (230, 230, 230)

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            
            
            self._update_screen()

    def _update_bullets(self):

        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)
        #print(len(self.bullets)) 检查子弹是否被删除

    def _creat_fleet(self):
        """创建外星人群。"""
        #创建一个外星人并计算一行可容纳多少个外星人。
        #外星人的间距为外星人的宽度
        alien = Alien(self)
        alien_width = alien.rect.width
        availble_space_x = self.settings.screen_width - (2*alien_width)
        number_aliens_x = availble_space_x //(2*alien_width)
        #创建第一行外星人
        for alien_number in range(number_aliens_x):
            #创建一个外星人并将其加入当前行
            alien = Alien(self)
            alien.x = alien_width + 2*alien_width*alien_number
            alien.rect.x = alien.x
            self.aliens.add(self.alien)



    def _update_screen(self):
        # 每次循环时都重绘屏幕
        self.screen.fill(self.settings.bg_color)  # 类属性的使用？
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        #self.bullets.draw(self.screen)
        # 让最近绘制的屏幕可见。
        pygame.display.flip()

    def _check_events(self):
        # 监视键盘和鼠标事件。
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):

        if len(self.bullets) < self.settings.bullets_allowd:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)



if __name__ == '__main__':
    # 创建游戏实例并运行游戏。
    ai = AlienInvasion()
    ai.run_game()
