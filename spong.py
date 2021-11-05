import pygame as pg
import random as r
from time import sleep

#screen
scr_width = 800
scr_height = 800

class Player(pg.sprite.Sprite):
    def __init__(self, width, height, color, x, y):
        super().__init__()
        self.image = pg.Surface((width, height)) #has to be .image because of the Sprite-class
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_x = 0
        self.score = 0 
    
    def update(self):
        #using keystate instead of KEYDOWN event because of holding key down constantly
        self.vel_x = 0 #keeps player not moving
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            if self.rect.left >= 10:
                self.vel_x = -4.07
        if keystate[pg.K_RIGHT]:
            if self.rect.right <= scr_width - 10:
                self.vel_x = 4.07
        self.rect.x += self.vel_x #moves player * vel_x speed

class Player_two(pg.sprite.Sprite):
    def __init__(self, width, height, color, x, y):
        super().__init__()
        self.image = pg.Surface((width, height)) 
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_x = 0
        self.score = 0 
    
    def update(self):
        self.vel_x = 0 
        keystate = pg.key.get_pressed()
        if keystate[pg.K_a]:
            if self.rect.left >= 10:
                self.vel_x = -4.07
        if keystate[pg.K_d]:
            if self.rect.right <= scr_width - 10:
                self.vel_x = 4.07
        self.rect.x += self.vel_x 

class AI(pg.sprite.Sprite):
    def __init__(self, width, height, color, x, y):
        super().__init__()
        self.image = pg.Surface((width, height)) 
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_x = 0
        self.score = 0 
        
    def update(self):
        self.vel_x = 0 
        
        #The AI
        ball_center = (Peli.ball.rect.left + Peli.ball.rect.right) // 2
        AI_center = (self.rect.left + self.rect.right) // 2
        paddle_left = self.rect.left + Peli.ball.rect.width
        paddle_right = self.rect.right - Peli.ball.rect.width
        ball_y = Peli.ball.rect.top
        AI_y = self.rect.bottom
        walls_left = self.rect.left >= 10
        walls_right = self.rect.right <= scr_width - 10
        p1_vel_x = Peli.p1.vel_x

        if Peli.ball.vel_y < 0: #moving towards the AI player
            #chase the ball and add wall constraints
            #hit with sides to increase speed
            if ball_center > paddle_right and abs(ball_y - AI_y) > 10 and walls_right:
                self.vel_x = 4
            if ball_center < paddle_left and abs(ball_y - AI_y) > 10 and walls_left:
                self.vel_x = -4
        else:
            #return to center (width // 2 < ball pos > width // 4 and player is not moving)
            if abs(AI_center - ball_center) > scr_width // 4 and abs(AI_center - ball_center) < scr_width // 2 or ball_y > scr_height // 3 and ball_y < scr_height // 2 and p1_vel_x == 0:
                if AI_center < (scr_width // 2) - 2:
                    self.vel_x = 2.85
                elif AI_center > (scr_width // 2) + 2:
                    self.vel_x = -2.85
            #follow the ball
            if ball_y > scr_height // 2 and p1_vel_x != 0:
                if ball_center > AI_center and abs(ball_y - AI_y) > 10 and walls_right:
                    self.vel_x = 2.85
                if ball_center < AI_center and abs(ball_y - AI_y) > 10 and walls_left:
                    self.vel_x = -2.85
            
        self.rect.x += self.vel_x #moves player * vel_x speed
    
class Ball(pg.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pg.image.load('data/ball.png').convert_alpha() 
        self.image = pg.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_x = 4.3
        self.vel_y = 4.85
    
    #less speed
    def dec_speed(self):
        if abs(self.vel_y) > 4.85:
            self.vel_y = self.vel_y * 0.85
    
    #more speed
    def add_speed(self):
        #limit speed
        if abs(self.vel_y * 1.15) < 15:
            self.vel_y = self.vel_y * 1.15 

    def respawn(self, direction = 4.85):
        #angle
        self.vel_x = r.choice([4, -4])
        self.vel_y = direction

        self.rect.x = r.choice([Peli.spawn_left, Peli.spawn_right])
        self.rect.y = scr_height // 2

    def update(self):
      
        #constraints (bouncing off the walls)
        if self.rect.left <= 0 and self.vel_x < 0 or self.rect.right >= scr_width and self.vel_x > 0:
            sound = pg.mixer.Sound('data/hit.wav')
            sound.play()
            self.vel_x = -self.vel_x

        collision_p1 = self.rect.bottom >= Peli.p1.rect.top and self.rect.left > Peli.p1.rect.left - 20 and self.rect.right < Peli.p1.rect.right + 20
        if Peli.two_players:
            collision_p2 = self.rect.top <= Peli.p2.rect.bottom and self.rect.left > Peli.p2.rect.left and self.rect.right - self.rect.width < Peli.p2.rect.right
        else:
            collision_AI = self.rect.top <= Peli.AI.rect.bottom and self.rect.left > Peli.AI.rect.left and self.rect.right - self.rect.width < Peli.AI.rect.right

        if collision_p1:
            sound = pg.mixer.Sound('data/hit.wav')
            sound.play()
            ball_center = (self.rect.left + self.rect.right) // 2
            p1_center = (Peli.p1.rect.left + Peli.p1.rect.right) // 2
            p1_middle_paddle = ball_center > p1_center - (self.rect.width // 2) and ball_center < p1_center + (self.rect.width // 2)
            
            #move back the ball a little to prevent bugs with collision detection
            self.rect.y -= abs(self.vel_y)

            if p1_middle_paddle:
                self.vel_x = 0
                self.dec_speed()       
            elif self.rect.right < p1_center:
                self.vel_x = -4
                self.add_speed()
            elif self.rect.left > p1_center:
                self.vel_x = 4
                self.add_speed()
            
            #make sure ball doesnt bounce if it's gone too far below paddle
            if self.rect.bottom - 10 < Peli.p1.rect.top:
                self.vel_y = -self.vel_y
        
        if Peli.two_players:
            if collision_p2:
                sound = pg.mixer.Sound('data/hit.wav')
                sound.play()            
                ball_center = (self.rect.left + self.rect.right) // 2
                p2_center = (Peli.p2.rect.left + Peli.p2.rect.right) // 2
                p2_middle_paddle = ball_center > p2_center - (self.rect.width // 2) and ball_center < p2_center + (self.rect.width // 2)
                
                self.rect.y += abs(self.vel_y)

                if p2_middle_paddle:
                    self.vel_x = 0
                    self.dec_speed()       
                elif self.rect.right < p2_center:
                    self.vel_x = -4
                    self.add_speed()
                elif self.rect.left > p2_center:
                    self.vel_x = 4
                    self.add_speed()
                
                if self.rect.top + 10 > Peli.p2.rect.top:
                    self.vel_y = -self.vel_y
        else:                    
            if collision_AI:
                sound = pg.mixer.Sound('data/hit.wav')
                sound.play()            
                ball_center = (self.rect.left + self.rect.right) // 2
                AI_center = (Peli.AI.rect.left + Peli.AI.rect.right) // 2
                AI_middle_paddle = ball_center > AI_center - (self.rect.width // 2) and ball_center < AI_center + (self.rect.width // 2)

                self.rect.y += abs(self.vel_y)

                if AI_middle_paddle:
                    self.vel_x = 0
                    self.dec_speed()       
                elif self.rect.right < AI_center:
                    self.vel_x = -4
                    self.add_speed()
                elif self.rect.left > AI_center:
                    self.vel_x = 4
                    self.add_speed()
                
                if self.rect.top + 10 > Peli.AI.rect.top:
                    self.vel_y = -self.vel_y
                        
        #movement
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

class Ohjelma:
    '''Pelaaja ohjaa mailaa ja pelin tarkoituksena on lyödä pallo maaliin. Maali on aukko mailan vastakkaisessa seinässä. Pelaaja saa pisteen, jos osuu maaliin. 
    Tietokone saa pisteen, jos pallo osuu pelaajan puoleiseen seinään. Peli loppuu 11 pisteeseen.'''''
    def __init__(self):
        pg.mixer.pre_init(buffer=1024)
        pg.init()
        pg.font.init()

        #screen
        self.scr = pg.display.set_mode((scr_width, scr_height))
        pg.display.set_caption("Spong")
        icon = pg.image.load('data/spong.ico')
        pg.display.set_icon(icon)
        #convert images for faster loading
        self.bg1 = pg.image.load('data/tausta.png').convert()
        self.bg2 = pg.image.load('data/space1.jpeg').convert()
        self.bg3 = pg.image.load('data/space2.jpg').convert()
        self.bg4 = pg.image.load('data/space3.jpg').convert()
        self.bg5 = pg.image.load('data/space4.jpg').convert()
        self.bg6 = pg.image.load('data/space5.jpg').convert()
        self.bg7 = pg.image.load('data/space6.jpg').convert()
        self.bg8 = pg.image.load('data/space7.jpg').convert()
        self.bg9 = pg.image.load('data/space8.jpg').convert()
        self.bg0 = pg.image.load('data/space9.jpg').convert()
        #transform background to set screen size
        self.bg1 = pg.transform.scale(self.bg1, (scr_width, scr_height))
        self.bg2 = pg.transform.scale(self.bg2, (scr_width, scr_height))
        self.bg3 = pg.transform.scale(self.bg3, (scr_width, scr_height))
        self.bg4 = pg.transform.scale(self.bg4, (scr_width, scr_height))
        self.bg5 = pg.transform.scale(self.bg5, (scr_width, scr_height))
        self.bg6 = pg.transform.scale(self.bg6, (scr_width, scr_height))
        self.bg7 = pg.transform.scale(self.bg7, (scr_width, scr_height))
        self.bg8 = pg.transform.scale(self.bg8, (scr_width, scr_height))
        self.bg9 = pg.transform.scale(self.bg9, (scr_width, scr_height))
        self.bg0 = pg.transform.scale(self.bg0, (scr_width, scr_height))
        #starting background
        self.bg = self.bg1
        
        #Sprite groups: (GroupSingle() could also be used to hold a single sprite)
        self.color_grey = (128, 128, 128)

        #Players
        self.p1 = Player(150, 25, (255,255,255), scr_width / 2, scr_height - 25)    
        self.p1_group = pg.sprite.Group()
        self.p1_group.add(self.p1)
        self.p2 = Player_two(150, 25, (255,255,255), scr_width / 2, 25)   
        self.p2_group = pg.sprite.Group()
        self.p2_group.add(self.p2)
        self.two_players = False
        
        #The AI
        self.AI = AI(150, 25, (255,255,255), scr_width / 2, 25)    
        self.AI_group = pg.sprite.Group()
        self.AI_group.add(self.AI)

        #The Ball
        self.spawn_left = r.randrange(60, scr_width // 2)
        self.spawn_right = r.randrange(scr_width // 2, scr_width - 60)
        self.ball = Ball(25, r.choice([self.spawn_left, self.spawn_right]), scr_height / 2)
        self.ball_group = pg.sprite.Group()
        self.ball_group.add(self.ball)
 
        #text
        self.font = pg.font.SysFont("Terminal", 26)
        self.font_menu = pg.font.SysFont("Terminal", 60)
        self.end_font = pg.font.SysFont("Terminal", 80)
        self.end_font_small = pg.font.SysFont("Terminal", 30)

        #player names
        self.name_font = pg.font.SysFont("Terminal", 18)
        self.p1_n = "P1"
        self.p2_n = "P2"
        self.AI_n = "CPU"
        self.p1_name = self.name_font.render(self.p1_n, True, (255, 255, 255))
        self.p2_name = self.name_font.render(self.p2_n, True, (255, 255, 255))
        self.AI_name = self.name_font.render(self.AI_n, True, (255, 255, 255))
        self.p1_name_l = self.name_font.size(self.p1_n)[0] // 2
        self.p2_name_l = self.name_font.size(self.p2_n)[0] // 2
        self.AI_name_l = self.name_font.size(self.AI_n)[0] // 2

        #clock
        self.clock = pg.time.Clock()
        self.fps = 60

        #game over
        self.end = False
        self.game_over = False
        self.text_color = (255, 107, 0)
        self.txt_GO = "GAME OVER"
        self.txt_ESC = "F2 - RESTART"
        self.txt_F2 = "ESC - QUIT"
        self.txt_end = self.end_font.render(self.txt_GO, True, self.text_color)
        self.txt_end2 = self.end_font_small.render(self.txt_ESC, True, self.text_color)
        self.txt_end3 = self.end_font_small.render(self.txt_F2, True, self.text_color)
        self.txt_end_l = self.end_font.size(self.txt_GO)[0] // 2
        self.txt_end2_l = self.end_font_small.size(self.txt_ESC)[0] // 2
        self.txt_end3_l = self.end_font_small.size(self.txt_F2)[0] // 2

        #menu
        self.play = False
        self.selected = 1

        #background music
        pg.mixer.music.load('data/menu.wav')
        pg.mixer.music.play(-1, 0.0)
    
    def main_loop(self):
        while True:
            self.update()

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    exit()
                
                #theme selection
                if event.key == pg.K_1:
                    self.bg = self.bg1
                if event.key == pg.K_2:
                    self.bg = self.bg2
                if event.key == pg.K_3:
                    self.bg = self.bg3
                if event.key == pg.K_4:
                    self.bg = self.bg4
                if event.key == pg.K_5:
                    self.bg = self.bg5
                if event.key == pg.K_6:
                    self.bg = self.bg6
                if event.key == pg.K_7:
                    self.bg = self.bg7
                if event.key == pg.K_8:
                    self.bg = self.bg8
                if event.key == pg.K_9:
                    self.bg = self.bg9
                if event.key == pg.K_0:
                    self.bg = self.bg0

                if self.play:
                    if event.key == pg.K_F2:
                        self.restart()
                    if event.key == pg.K_F3:
                        self.play = False #back to menu
                else:
                    #game menu
                    if self.selected == 1:
                        if event.key == pg.K_DOWN:
                            self.selected = 2
                        if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                            self.play = True
                            pg.mixer.music.stop()

                    if self.selected == 2:
                        if event.key == pg.K_UP:
                            self.selected = 1
                        if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                            self.play = True
                            self.two_players = True
                            pg.mixer.music.stop()
                        
        #take note of the drawing order - the ones below will be drawn on top of others
        self.scr.blit(self.bg, (0, 0))  
        self.p1_group.draw(self.scr)
        if self.two_players:
            self.p2_group.draw(self.scr)
        else: 
            self.AI_group.draw(self.scr)
        if self.play and not self.game_over:
            self.ball_group.draw(self.scr)   

        #menu screen
        if not self.play:
            text1 = f"{self.p1_n} vs {self.AI_n}"
            text2 = f"{self.p1_n} vs {self.p2_n}"
            text1_l = self.font_menu.size(text1)[0] // 2
            text2_l = self.font_menu.size(text2)[0] // 2

            if self.selected == 1:
                self.txt_start = self.font_menu.render(text1, True, self.text_color)
                self.txt_start_2 = self.font_menu.render(text2, True, self.color_grey)
            elif self.selected == 2:
                self.txt_start = self.font_menu.render(text1, True, self.color_grey)
                self.txt_start_2 = self.font_menu.render(text2, True, self.text_color)
            
            self.scr.blit(self.txt_start, (scr_width / 2 - text1_l, scr_height / 2 - 40))
            self.scr.blit(self.txt_start_2, (scr_width / 2 - text2_l, scr_height / 2 + 10))
            
        else:  
            #game is running
            self.p1.update()
            if self.two_players:
                self.p2.update()
            else:
                self.AI.update()
            self.ball.update()
            
            self.is_goal()

        #keeping scoretext updated inside loop 
        self.txt1 = self.font.render(f"{self.p1_n}: {self.p1.score}", True, (255, 255, 255))
        self.txt2 = self.font.render(f"{self.p2_n}: {self.p2.score}", True, (255, 255, 255))
        self.txt3 = self.font.render(f"{self.AI_n}: {self.AI.score}", True, (255, 255, 255))
        
        #draw player names and scoretext
        offset = 50
        self.scr.blit(self.p1_name, (self.p1.rect.center[0] - self.p1_name_l, self.p1.rect.center[1] - offset))
        self.scr.blit(self.txt1, (40 + self.p1_name_l * 2, 40))
        if self.selected == 2:
            self.scr.blit(self.p2_name, (self.p2.rect.center[0] - self.p2_name_l, self.p2.rect.center[1] + offset))
            self.scr.blit(self.txt2, (scr_width - 95 - self.p2_name_l * 2, 40))
        else:
            self.scr.blit(self.AI_name, (self.AI.rect.center[0] - self.AI_name_l, self.AI.rect.center[1] + offset))
            self.scr.blit(self.txt3, (scr_width - 95 - self.AI_name_l * 2, 40))

        if not self.game_over:
            pg.display.flip()
        
        else:
            self.ball.rect.center = (scr_width //2, scr_height // 2)
            self.ball.vel_y = 0
            self.ball_vel_x = 0
        
        if self.end:
            self.game_over = True

        self.clock.tick(self.fps)

    def is_goal(self):
        goal = False
        #scoring
        if self.ball.rect.y < 0:
            sound = pg.mixer.Sound('data/p1_scores.wav')
            sound.play()
            self.p1.score +=1
            #set ball direction towards who made last goal
            self.ball_dy = 4.85
            goal = True

        elif self.ball.rect.y > scr_height:
            sound = pg.mixer.Sound('data/AI_scores.wav')
            sound.play()
            if self.two_players:
                self.p2.score += 1
            else:
                self.AI.score += 1
            self.ball_dy = -4.85
            goal = True
            
        if goal:
            self.ball.respawn(self.ball_dy)
              
            #game end
            max_goals = 11
            if self.p1.score >= max_goals or self.AI.score >= max_goals or self.p2.score >= max_goals:
                self.scr.blit(self.txt_end, (scr_width // 2 - self.txt_end_l, scr_height // 2 - 40))
                self.scr.blit(self.txt_end2, (scr_width // 2 - self.txt_end2_l, scr_height // 2 + 30))
                self.scr.blit(self.txt_end3, (scr_width // 2 - self.txt_end3_l, scr_height // 2 + 60))
                self.end = True
                sleep(2.5) #wait for sound effects to stop
                if self.AI.score >= max_goals or self.p2.score >= max_goals:
                    sound = pg.mixer.Sound('data/game_over.wav')
                else:
                    sound = pg.mixer.Sound('data/fanfare.wav')

                sound.play()

    def restart(self):
        self.end = False
        self.game_over = False
        self.p1.score = 0
        self.p1.rect.center = (scr_width / 2, scr_height - 25)
        if self.two_players:
            self.p2.score = 0
            self.p2.rect.center = (scr_width / 2, 25)
        else:
            self.AI.score = 0
            self.AI.rect.center = (scr_width / 2, 25)
        self.ball.respawn()

Peli = Ohjelma()
Peli.main_loop()
