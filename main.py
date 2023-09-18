import pygame
import random
import csv

b = open('Files/coins.csv', 'r')  # read spreadsheet
reader = csv.reader(b)
bought = []  # array with the scores
for row in reader:  # appends the necessary columns
    bought.append(int(float((row[0]))))

pygame.mixer.init()
pygame.init()
width = 1300
height = 900
screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF)  # create screen
pygame.display.set_caption("Fish Eat Fish")
FPS = 60  # sets the fps
money = bought[0]  # retrieve money

# Uploads
menu_bg = pygame.image.load('Files/menu.png')
shop_bg = pygame.image.load('Files/shop.png')
check = pygame.image.load('Files/check.png')
check = pygame.transform.scale(check, (50, 50))
game_bg = pygame.image.load('Files/game.png')
win_bg = pygame.image.load('Files/win.png')
lose_bg = pygame.image.load('Files/lost.png')
font1 = pygame.font.SysFont('Files/Boulder', 50)
font2 = pygame.font.SysFont('Files/Boulder', 80)
pygame.mixer.music.load('Files/bg_music.wav')
pygame.mixer.music.play(-1)  # play music
pop = pygame.mixer.Sound('Files/pop.mp3')
ching = pygame.mixer.Sound('Files/ching.mp3')
characters = ['Files/1.png', 'Files/2.png', 'Files/3.png', 'Files/4.png', 'Files/5.png']

timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 3000)  # create two timed events

heart_event = pygame.USEREVENT + 1
pygame.time.set_timer(heart_event, 4000)

done = False
menu = True
game = False
CLOCK = pygame.time.Clock()  # for controlling the FPS
score = 50
lives = 30
change = False
victory = False
shop = False
player_speed = 5
speed = False
used = 0


class Bubble(pygame.sprite.Sprite):  # bubble object
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size = random.randrange(50, 80)  # random size
        self.image = pygame.image.load('Files/bubble.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 1300)  # random location
        self.rect.y = 1000
        self.speed = random.randrange(3, 10)

    def update(self):
        self.rect.y -= self.speed  # move the bubbles
        if self.rect.top < -50:  # regenerate bubbles
            self.rect.x = random.randrange(0, 1300)
            self.rect.y = 1000
            self.speed = random.randrange(3, 10)


class Player(pygame.sprite.Sprite):  # player class
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(characters[used]).convert_alpha()
        # Get the pixels
        self.size = score
        self.image = pygame.transform.scale(self.image, (self.size, self.size * 0.6))
        self.image_copy = self.image.copy()
        self.flipped = pygame.transform.flip(self.image_copy, True, False)  # create flipped image
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.centery = height / 2
        self.speedx = 0
        self.speedy = 0
        self.speed = player_speed  # set speed

    def get_size(self):  # get size
        return self.size

    def update(self):
        self.size = score  # change size
        self.speed = player_speed  # change speed
        self.image = pygame.transform.scale(self.image, (self.size, self.size * 0.6))
        if game:
            self.speedx = 0
            self.speedy = 0
            key = pygame.key.get_pressed()  # move fish
            if key[pygame.K_LEFT]:
                self.speedx = -self.speed
                self.image = self.image_copy
            if key[pygame.K_RIGHT]:
                self.speedx = self.speed
                self.image = self.flipped
            if key[pygame.K_UP]:
                self.speedy = -self.speed
            if key[pygame.K_DOWN]:
                self.speedy = self.speed
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.right > width:
                self.rect.right = width
            if self.rect.left < 0:
                self.rect.left = 0  # restrain fish
            if self.rect.bottom > height:
                self.rect.bottom = height
            if self.rect.top < 0:
                self.rect.top = 0
            global change
            if change:
                self.size = score  # update image
                self.image = pygame.image.load(characters[used]).convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.size, self.size * 0.6))
                self.image_copy = self.image.copy()
                self.flipped = pygame.transform.flip(self.image_copy, True, False)
                change = False


class Fish(pygame.sprite.Sprite):  # enemy fish class
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        x = random.randint(1, 4)  # random image
        if x == 1:
            self.image = pygame.image.load('Files/fish1.png').convert_alpha()
        elif x == 2:
            self.image = pygame.image.load('Files/fish2.png').convert_alpha()
        elif x == 3:
            self.image = pygame.image.load('Files/fish3.png').convert_alpha()
        elif x == 4:
            self.image = pygame.image.load('Files/fish4.png').convert_alpha()
        self.size = random.randrange(score - 30, score + 150, 10)
        speed = 2  # sets basic speed
        for i in range(50, 250, 75):  # increase speed
            if score > i:
                speed = speed + 1
        self.speed = random.randint(speed, speed + 1)
        self.image = pygame.transform.scale(self.image, (self.size, self.size * 0.6))
        self.image_copy = self.image.copy()
        self.flipped = pygame.transform.flip(self.image_copy, True, False)
        self.rect = self.image.get_rect()
        self.rect.y = random.randint(0, 800)  # random location
        self.direction = random.randint(1, 2)
        if self.direction == 1:
            self.rect.x = 1400
        elif self.direction == 2:
            self.rect.x = -200

    def update(self):
        if game:
            if self.direction == 1:
                self.image = self.image_copy
                self.rect.x -= self.speed
                if self.rect.right < -100:
                    Fish.kill(self)  # destroy fish when they reach the end
                    f = Fish()
                    fish.add(f)
            elif self.direction == 2:
                self.image = self.flipped
                self.rect.x += self.speed
                if self.rect.left > 1400:
                    Fish.kill(self)
                    f = Fish()
                    fish.add(f)

    def get_size(self):
        return self.size  # return size


def draw_health(surf, x, y, z):  # draw health bar
    if z < 0:
        z = 0
    bar_length = 300
    bar_height = 40
    fill = (z/30) * bar_length
    outline_rect = pygame.Rect(x - 1, y - 1, bar_length + 2, bar_height + 5)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, (105, 180, 129), fill_rect)
    pygame.draw.rect(surf, (0, 43, 93), outline_rect, 5, 7)


class Coin(pygame.sprite.Sprite):  # create coin class
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Files/coin.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(100, 1200)
        self.rect.y = random.randrange(100, 800)


class Heart(pygame.sprite.Sprite):  # create heart class
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Files/heart.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(100, 1200)
        self.rect.y = random.randrange(100, 800)


bubble = pygame.sprite.Group()  # create sprite groups
fish = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
coin = pygame.sprite.Group()
heart = pygame.sprite.Group()

for i in range(8):  # create bubbles
    b = Bubble()
    bubble.add(b)

for i in range(8):  # create enemy fish
    f = Fish()
    fish.add(f)
    all_sprites.add(f)

m = Coin()  # create hearts and coins
coin.add(m)
h = Heart()
heart.add(h)

while not done:
    CLOCK.tick(FPS)  # sets frame rate
    mouse = pygame.mouse.get_pos()  # gets position from mouse
    for event in pygame.event.get():  # User did something
        if event.type == timer_event:  # adds a coin every 3 seconds
            if game:
                coin.empty()  # destroys previous coins
                coin = pygame.sprite.Group()
                x = random.randint(1, 4)
                if x == 1:
                    m = Coin()  # creates new coin object
                    coin.add(m)

        if event.type == heart_event:  # adds a heart every 3 seconds
            if game:
                heart.empty()  # destroys previous hearts
                heart = pygame.sprite.Group()
                x = random.randint(1, 4)
                if x == 1:
                    m = Heart()  # creates new heart object
                    heart.add(m)

        if event.type == pygame.QUIT:  # If user clicked close
            bought[0] = money
            f = open('Files/coins.csv', 'wt', newline='')  # saves high scores into the spreadsheet
            f.truncate()  # delete previous information
            writer = csv.writer(f)
            for i in range(0, len(bought)):
                writer.writerow([str(bought[i])])
            done = True  # Flag that we are done so we exit this loop
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:  # if mouse is pressed down
            if shop:
                if (80 <= mouse[0] <= 320) and (435 <= mouse[1] <= 510):
                    used = 0  # first fish
                if not speed:
                    if (690 <= mouse[0] <= 925) and (780 <= mouse[1] <= 850):
                        speed = True  # buy speed boost
                        player_speed = 7
                        money = money - 10
                for i in range(1, 4):  # choose other fish
                    if (375 + 305*(i-1) <= mouse[0] <= 625 + 305*(i-1)) and (435 <= mouse[1] <= 510):
                        if money >= 20 + (i-1) * 20:  # subtract money
                            if bought[i] == 0:
                                bought[i] = 1
                                money = money - 20 + (i-1) * 20
                            elif bought[i] == 1:  # change selected fish
                                used = i

                if (375 <= mouse[0] <= 625) and (770 <= mouse[1] <= 830):  # choose last fish
                    if money >= 90:
                        if bought[4] == 0:
                            bought[4] = 1
                            money = money - 90
                        elif bought[i] == 1:
                            used = 4
            if menu:
                if (674 <= mouse[0] <= 1020) and (350 <= mouse[1] <= 445):  # play button
                    menu = False
                    shop = True
                    screen.blit(game_bg, (0, 0))
                    pygame.mixer.Sound.play(pop)
            if shop:
                if (990 <= mouse[0] <= 1250) and (754 <= mouse[1] <= 850):  # play button
                    shop = False
                    game = True
                    pygame.mixer.Sound.play(pop)
                    player = Player()
                    all_sprites.add(player)
                    score = player.get_size()
            if victory:
                if (480 <= mouse[0] <= 820) and (550 <= mouse[1] <= 650):  # play again button
                    pygame.mixer.Sound.play(pop)
                    # reset variables
                    score = 50
                    victory = False
                    menu = True
                    fish.empty()
                    all_sprites.empty()
                    all_sprites = pygame.sprite.Group()
                    fish = pygame.sprite.Group()
                    player_speed = 5
                    for i in range(8):
                        f = Fish()
                        fish.add(f)
                        all_sprites.add(f)
                    lives = 30
                    player.kill()
    if shop:
        screen.blit(shop_bg, (0, 0))  # display images
        buy_text = font1.render("Buy", True, (56, 98, 125))
        use_text = font1.render("Use", True, (64, 148, 69))
        bought_text = font1.render("Used", True, (64, 148, 69))
        coin_text = font2.render(str(money), True, (56, 98, 125))
        screen.blit(coin_text, (1090, 645))  # writes the texts
        screen.blit(use_text, (160, 457))  # writes the texts
        for i in range(1, 4):
            if bought[i] == 0:
                screen.blit(buy_text, (160 + i*304, 457))  # writes the texts
            else:
                screen.blit(use_text, (160 + i*304, 457))  # writes the texts
        if bought[4] == 0:
            screen.blit(buy_text, (160 + 304, 795))  # writes the texts
        else:
            screen.blit(use_text, (160 + 304, 795))  # writes the texts
        if not speed:
            screen.blit(buy_text, (160 + 2*304, 795))  # writes the texts
        else:
            screen.blit(bought_text, (155 + 2*304, 795))  # writes the texts

        for i in range(0, 4):
            if used == i:
                screen.blit(check, (303*i + 280, 370))  # writes the texts
        if used == 4:
            screen.blit(check, (303 + 280, 710))  # writes the texts

    if menu:
        screen.blit(menu_bg, (0, 0))  # display background
    if game:
        if lives <= 0:  # detect game over
            game = False
            victory = True
        if score == 300:  # detect victory
            game = False
            victory = True
            money = money + 40
        screen.blit(game_bg, (0, 0))
        draw_health(screen, 920, 40, lives)
        # update sprites
        all_sprites.update()
        fish.update()
        fish.draw(screen)
        all_sprites.draw(screen)
        coin.update()
        coin.draw(screen)
        heart.update()
        heart.draw(screen)
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(80, 35, 250, 60))
        pygame.draw.rect(screen, (0, 43, 93), pygame.Rect(79, 33, 255, 66), 5, 7)
        display_score = score - 50
        score_text = font1.render("Score: " + str(display_score), True, (0, 43, 93))
        screen.blit(score_text, (100, 50))  # writes the texts

        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(400, 35, 250, 60))
        pygame.draw.rect(screen, (0, 43, 93), pygame.Rect(399, 33, 255, 66), 5, 7)
        score_text = font1.render("Coins: " + str(money), True, (0, 43, 93))
        screen.blit(score_text, (420, 50))  # writes the texts
        # detect hits
        hits = pygame.sprite.spritecollide(player, coin, True)  # hit money
        for hits in hits:
            money = money + 1
            pygame.mixer.Sound.play(ching)
        hits = pygame.sprite.spritecollide(player, heart, True)  # hit heart
        for hits in hits:
            if lives < 30:
                lives = lives + 4  # increase health
            if lives > 30:
                lives = 30
            pygame.mixer.Sound.play(pop)
        for f in fish:
            hits = pygame.sprite.collide_rect(player, f)  # hit fish
            if hits:
                x = f.get_size()  #get size of fish
                y = 5
                for i in range(50, 400, 40):
                    if x > i:
                        y = y + 5
                if player.get_size() >= x:
                    score = score + y  # increase score
                    f.kill()
                    f = Fish()  # create new fish
                    fish.add(f)
                    all_sprites.add(f)
                    change = True
                    pygame.mixer.Sound.play(pop)
                if player.get_size() < x:
                    lives = lives - 1
                    change = True
    if victory:
        if lives <= 0:
            screen.blit(lose_bg, (0, 0))  # display background
        else:
            screen.blit(win_bg, (0, 0))  # writes the texts
    bubble.update()
    bubble.draw(screen)

    pygame.display.flip()  # updates the scenes

raise SystemExit
