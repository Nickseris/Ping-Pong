from pygame import *
from random import randint

font.init()

# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed_x, player_speed_y):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)

        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speedx = player_speed_x
        self.speedy = player_speed_y

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

 # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


    def update(self):
        global run

        # рандомное направлние мяча при запуске игры
        if number == 1:
            self.rect.x += self.speedx
            self.rect.y += self.speedy
        else:
            self.rect.x -= self.speedx
            self.rect.y -= self.speedy
        # отскок от мяча
        if self.rect.colliderect(racket1.rect) or self.rect.colliderect(racket2.rect):
            self.speedx *= -1
        
        if self.rect.y >= win_height or self.rect.y <= 0:
            self.speedy *= -1
        # проигрыш
        if self.rect.x < 100 or self.rect.x > win_width-145:
            self.speedx=0
            self.speedy=0
            racket1.speedx=0
            racket1.speedy=0
            racket2.speedx=0
            racket2.speedy=0
            window.blit(lose, (215, win_height/2))
            

# класс главного игрока
class Player(GameSprite):
    # метод для управления спрайтов стрелками клавиатуры
    def update1(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.top > 0:
            self.rect.y -= self.speedy
        if keys[K_s] and self.rect.bottom < win_height:
            self.rect.y += self.speedy

    def update2(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.top > 0:
            self.rect.y -= self.speedy
        if keys[K_DOWN] and self.rect.bottom < win_height:
            self.rect.y += self.speedy

    # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

# рандомное направлние мяча
number = randint(0,1)

# Создаем окошко
win_width = 700
win_height = 500
clock = time.Clock()
icon = image.load('tenis_ball.png')
display.set_caption("Ping-Pong")
display.set_icon(icon)
window = display.set_mode((win_width, win_height))


# создаем ракетки
racket1 = Player('racket.png', 100, win_height/2, 45, 110, 0, 15)
racket2 = Player('racket.png', win_width-145, win_height/2, 45, 110, 0, 15)
ball = GameSprite('tenis_ball.png', win_width/2, win_height/2, 50, 50, 3, 3)


# текст
font = font.SysFont(None, 70)
lose = font.render("You lose ;(", True, (139, 0, 0))


# Основной цикл игры:
run = True # флаг сбрасывается кнопкой закрытия окна

while run:

    # событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
    
# сама игра: действия спрайтов, проверка правил игры, перерисовка
    # обновляем фон
    window.fill((110,213,200))

    # передвижение ракеток
    racket1.update1()
    racket2.update2()
    ball.update()
    # обновление персонажей
    ball.reset()
    racket1.reset()
    racket2.reset()  

    # FPS
    display.update()
    clock.tick(60)