# ----------------- importing libraries -----------------
from tkinter import *
from random import randint
from math import sqrt
import time
# import threading
# import subprocess
# from winsound import *
import json

# ----------------- creating window -----------------
root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
centre_X = (screen_width / 2) - 400
centre_Y = (screen_height / 2) - 300
root.geometry('800x600+' + str(int(centre_X)) + '+' + str(int(centre_Y)))
root.resizable(False, False)
root.title('SPACE WAR')
root.iconbitmap('icon.ico')

# PlaySound('Arpeggiated-bassline.wav', SND_FILENAME | SND_LOOP | SND_ASYNC | SND_NOSTOP)
# Adding Running background image.
# backGroundImg = PhotoImage(file='space 3.png')

# ----------------- loading images -----------------
play_Img = PhotoImage(file='93868N2.png')
replay_Img = PhotoImage(file='Play_Again_logo_square.png')
home_Img = PhotoImage(file='download.png')
options_Img = PhotoImage(file='options.png')
leader_Img = PhotoImage(file='leaderboard.png')
leader_text_Img = PhotoImage(file='Leaderboard-Logo2 t.png')
control_Img = PhotoImage(file='control t.png')
credits_Img = PhotoImage(file='credits.png')
boss_Img = PhotoImage(file='boss.png')
final = PhotoImage(file='final 2.png')
select = PhotoImage(file='select.png')
running_background = PhotoImage(file='space 3 back.png')
back_1 = PhotoImage(file='back 1.png')
back_2 = PhotoImage(file='back 2.png')
back_3 = PhotoImage(file='back 3.png')
back = PhotoImage(file='back q.png')
tick = PhotoImage(file='select b.png')
b_bullet = PhotoImage(file='b 3.png')
save_Img = PhotoImage(file='save.png')
home_save_Img = PhotoImage(file='H_save.png')
cheat_Img = PhotoImage(file='cheat 1.png')
d_Img = [PhotoImage(file='back 1 d.png'), PhotoImage(file='back 2 d.png'), PhotoImage(file='back 3 d.png')]
instructions = "\n\tCONTROLS\t\n\nFunctions\t :\tKeys\n\nShooting\t  :\tSpace bar\n\nMovement\t:         Arrow Keys" \
               "\n\nPause\t:\tCrtl+a\n\nBoss Key\t:\tCrtl+z"
award = "\n\tCREDITS\t\n\n\n           AHMED KHAN"
cheats = "\n\tCHEAT CODES\n\n\t    'scoreup'\n\t   'powerup'\n\t'leavemealone'\n\t  'cosmicsave'\n\t 'chickenwar'\n" \
         "        'straighttothefinal'\n\n      ERASE:    Delete Key"
leader_d = {}
def_score = 0
over = False
load_d = {}
load_score = 0



# ----------------- Class to run the game -----------------
class Play:
    def __init__(self):
        self.canvas = Canvas(width=800, height=600, highlightthickness=0)
        self.canvas.pack()
        self.characterImg = PhotoImage(file="spaceship (1).png")
        self.bulletsImg = PhotoImage(file="bullets.png")
        self.missile_Img = PhotoImage(file='missile t.png')
        self.asteroid_Img = PhotoImage(file="asteroid s.png")
        self.canvas.create_image(0, 0, image=running_background, anchor=NW)
        self.home_button = Button(self.canvas, image=home_Img, borderwidth=0, highlightthickness=0, width=50,
                                  height=50, command=self.main_menu, activebackground='black', relief=FLAT)
        self.home_button.place(x=748, y=2)
        self.save_button = Button(self.canvas, image=home_save_Img, borderwidth=0, highlightthickness=0, width=50,
                                  height=50, command=self.save, activebackground='black', relief=FLAT)
        self.save_button.place(x=748, y=52)
        self.c = ["white", "#fefefe", "#fdfdfd"]
        # for placing stars in background
        # for i in range(500):
        #    x = randint(1, 800)
        #    y = randint(1, 600)
        #    size = randint(2, 3)
        #    f = randint(0, 2)
        #    xy = (x, y, x + size, y + size)
        #    temp_star = self.canvas.create_rectangle(xy)
        #    self.canvas.itemconfig(temp_star, fill=self.c[f])
        self.canvas.bind_all('<Key>', self.key_pressed)
        self.canvas.bind_all('<KeyRelease>', self.key_release)
        self.canvas.bind_all('<Control-a>', self.pause_f)
        self.canvas.bind_all('<Control-z>', self.boss)
        self.score = load_score
        self.score_text = self.canvas.create_text(100, 20, text="Score: " + str(self.score), font='algerian 30',
                                                  fill='#a300fe')
        self.FPS = 1000 // 25
        self.characterX = 360
        self.characterY = 480
        self.enemy_speed = 13
        self.num_of_enemies = 8
        self.character_speed = 25
        self.bullet_speed = 30
        self.asteroid_speed = 2
        self.X_limit, self.Y_limit = 768, 568
        self.D1 = 1
        self.bulletX = self.characterX
        self.bulletY = self.characterY
        self.asteroid_x, self.asteroid_y = randint(0, 720), 0
        self.enemy_aura = self.bullet_aura = 32
        self.character_aura = 64
        self.asteroid_aura = 175
        self.boss_x, self.boss_y = 390, 0
        self.boss_bullet_x, self.boss_bullet_y = [], []
        self.boss_bullet = []
        self.num_of_boss_bullets = 8
        self.boss_bullet_speed = 14
        self.boss_health = 30
        self.count = 3
        self.cheat_code = ""
        self.start_time = time.time()
        self.score_check = self.score
        self.loaded = True
        self.fire = False
        self.right, self.left = False, False
        self.up, self.down = False, False
        self.game_over = False
        self.pause = False
        self.boss_on = False
        self.power = False
        self.final_stage = False
        self.win = False
        self.save_on = False
        self.cheat_on = False
        self.chicken_on = False

        self.enemy_f()
        self.character_f()
        self.character_movement()
        self.enemy_movement()
        self.canvas.after(20000, self.asteroid_f)
        self.canvas.after(20099, self.asteroid_movement)
        self.collision()

    # ----------------- function to generate enemy images -----------------
    def enemy_f(self):
        self.enemy_img1 = []
        self.enemy_img2 = []
        self.enemy_img3 = []
        self.chicken_img = []
        self.enemy_x = []
        self.enemy_y = []
        self.app = []
        for i in range(self.num_of_enemies):
            self.enemy_img1.append(PhotoImage(file="ufo 1.png"))
            self.enemy_img2.append(PhotoImage(file="ufo 2 w.png"))
            self.enemy_img3.append(PhotoImage(file="ufo 3 w.png"))
            self.chicken_img.append(PhotoImage(file='Militarychicken 1.png'))
            if self.D1 == 1:
                self.enemy_x.append(randint(0, 768))
                self.enemy_y.append(0)
            if self.D1 == 2:
                self.enemy_x.append(0)
                self.enemy_y.append(randint(0, 568))
            self.app.append(
                self.canvas.create_image(self.enemy_x[i], self.enemy_y[i], image=self.enemy_img1[i], anchor=NW))

    # ----------------- function to move enemies -----------------
    def enemy_movement(self):
        self.check_time = time.time()
        if (abs(self.start_time - self.check_time) >= 60) and (abs(self.score - self.score_check)) <= 10:
            self.enemy_speed += 1
            self.score_check = self.score
            self.start_time = time.time()
        if not self.chicken_on:
            if 0 <= self.score < 30:
                self.enemy_images = self.enemy_img1
                self.safe_distance = 35
            if 30 <= self.score < 50:
                self.enemy_speed = 12
                self.enemy_images = self.enemy_img2
                self.safe_distance = 65
                self.enemy_aura = 64
                self.X_limit, self.Y_limit = 736, 536
            if self.score >= 50:
                self.enemy_speed = 11
                self.enemy_images = self.enemy_img3
                self.safe_distance = 130
                self.enemy_aura = 100
                self.X_limit, self.Y_limit = 700, 500
        else:
            self.enemy_speed = 11
            self.enemy_images = self.chicken_img
            self.safe_distance = 85
            self.enemy_aura = 80
            self.X_limit, self.Y_limit = 720, 520

        for j in range(self.num_of_enemies):
            if self.D1 == 1 and not self.pause:
                self.canvas.move(self.app[j], 0, self.enemy_speed)
                self.enemy_y[j] += self.enemy_speed
                if self.enemy_y[j] >= self.Y_limit:
                    self.canvas.delete(self.app[j])
                    self.enemy_x[j] = randint(0, self.X_limit)
                    self.enemy_y[j] = 0
                    self.app[j] = self.canvas.create_image(self.enemy_x[j], self.enemy_y[j], image=self.enemy_images[j],
                                                           anchor=NW)
            if self.D1 == 2 and not self.pause:
                self.canvas.move(self.app[j], self.enemy_speed, 0)
                self.enemy_x[j] += self.enemy_speed
                if self.enemy_x[j] >= self.X_limit:
                    self.enemy_y[j] = randint(0, self.Y_limit)
                    self.enemy_x[j] = 0
                    self.canvas.delete(self.app[j])
                    self.app[j] = self.canvas.create_image(self.enemy_x[j], self.enemy_y[j], image=self.enemy_images[j],
                                                           anchor=NW)
            if self.D1 == 3 and not self.pause:
                self.canvas.move(self.app[j], - self.enemy_speed, 0)
                self.enemy_x[j] -= self.enemy_speed
                if self.enemy_x[j] <= 0:
                    self.enemy_y[j] = randint(0, self.Y_limit)
                    self.enemy_x[j] = self.X_limit
                    self.canvas.delete(self.app[j])
                    self.app[j] = self.canvas.create_image(self.enemy_x[j], self.enemy_y[j], image=self.enemy_images[j],
                                                           anchor=NW)
        self.over_f()
        if not self.game_over and not self.final_stage:
            self.canvas.after(self.FPS, self.enemy_movement)

    # ----------------- function to generate character image -----------------
    def character_f(self):
        if not self.game_over:
            self.character = self.canvas.create_image(self.characterX, self.characterY, image=self.characterImg,
                                                      anchor=NW)
            self.over_f()

    # ----------------- function to move character -----------------
    def character_movement(self):
        if not self.pause:
            self.old_x, self.old_y = self.characterX, self.characterY
            if self.left:
                self.characterX -= self.character_speed
                if self.characterX <= 0:
                    self.characterX += self.character_speed
            elif self.right:
                self.characterX += self.character_speed
                if self.characterX >= 736:
                    self.characterX -= self.character_speed
            elif self.up:
                self.characterY -= self.character_speed
                if self.characterY <= 0:
                    self.characterY += self.character_speed
            elif self.down:
                self.characterY += self.character_speed
                if self.characterY >= 536:
                    self.characterY -= self.character_speed
            if (abs(self.old_x - self.characterX) >= self.character_speed or abs(
                    self.old_y - self.characterY) >= self.character_speed):
                self.canvas.delete(self.character)
                self.character_f()
        self.canvas.after(self.FPS, self.character_movement)

    # ----------------- function to generate bullet image -----------------
    def bullet_f(self):
        if not self.pause:
            if not self.power:
                self.bullet = self.canvas.create_image(self.bulletX + 16, self.bulletY + 10,
                                                       image=self.bulletsImg, anchor=NW)
            else:
                self.bullet = self.canvas.create_image(self.bulletX, self.bulletY, image=self.missile_Img,
                                                       anchor=NW)

            if not self.final_stage:
                self.collision()
            else:
                self.boss_collision()

    # ----------------- function to move bullet -----------------
    def bullet_movement(self):
        if not self.game_over:
            if self.fire:
                try:
                    self.canvas.delete(self.bullet)
                except:
                    pass
                self.bullet_f()
                self.bulletY -= self.bullet_speed
                if self.bulletY > 0:
                    self.canvas.after(self.FPS, self.bullet_movement)
                else:
                    self.canvas.delete(self.bullet)
                    self.fire = False
                    self.loaded = True

    # ----------------- function to generate asteroid image -----------------
    def asteroid_f(self):
        if not self.game_over and not self.final_stage:
            if not self.boss_on:
                self.asteroid = self.canvas.create_image(self.asteroid_x, self.asteroid_y, image=self.asteroid_Img,
                                                         anchor=NW)
                self.asteroid_collision()
            else:
                self.canvas.after(self.FPS, self.asteroid_f)

    # ----------------- function to move asteroid -----------------
    def asteroid_movement(self):
        if not self.pause and not self.game_over and not self.final_stage:
            self.canvas.delete(self.asteroid)
            self.asteroid_y += self.asteroid_speed
            if self.asteroid_y >= 600:
                self.asteroid_x, self.asteroid_y = randint(0, 720), 0
                self.canvas.after(10000, self.asteroid_movement)
            else:
                self.asteroid_f()
                self.canvas.after(self.FPS, self.asteroid_movement)
        else:
            self.canvas.after(self.FPS, self.asteroid_movement)

    # ----------------- function to detect collision with asteroid -----------------
    def asteroid_collision(self):
        if ((self.asteroid_x <= self.characterX <= self.asteroid_x + self.asteroid_aura) and (
                self.asteroid_y <= self.characterY <= self.asteroid_y + self.asteroid_aura)) or (
                (self.asteroid_x <= self.characterX + self.character_aura <= self.asteroid_x + self.asteroid_aura) and (
                self.asteroid_y <= self.characterY + self.character_aura <= self.asteroid_y + self.asteroid_aura)):
            self.show_over()
        for b in range(self.num_of_enemies):
            if ((self.asteroid_x <= self.enemy_x[b] <= self.asteroid_x + self.asteroid_aura) and (
                    self.asteroid_y <= self.enemy_y[b] <= self.asteroid_y + self.asteroid_aura)) or (
                    (self.asteroid_x <= self.enemy_x[b] + self.enemy_aura <= self.asteroid_x + self.asteroid_aura) and (
                    self.asteroid_y <= self.enemy_y[b] + self.enemy_aura <= self.asteroid_y + self.asteroid_aura)):
                self.canvas.delete(self.app[b])
                self.enemy_x[b], self.enemy_y[b] = randint(0, self.X_limit), 0
                self.app[b] = self.canvas.create_image(self.enemy_x[b], self.enemy_y[b], image=self.enemy_images[b],
                                                       anchor=NW)
        if ((self.asteroid_x <= self.bulletX <= self.asteroid_x + self.asteroid_aura) and (
                self.asteroid_y <= self.bulletY <= self.asteroid_y + self.asteroid_aura)) or (
                (self.asteroid_x <= self.bulletX + self.bullet_aura <= self.asteroid_x + self.asteroid_aura) and (
                self.asteroid_y <= self.bulletY + self.bullet_aura <= self.asteroid_y + self.asteroid_aura)):

            if not self.power:
                self.canvas.delete(self.bullet)
                self.fire = False
                self.loaded = True
            else:
                self.asteroid_y = 600
                self.canvas.delete(self.bullet)
                self.fire = False
                self.loaded = True
                # PlaySound('Explosion+7.wav', SND_ASYNC)

    # ----------------- function to be called when any keyboard key is pressed -----------------
    def key_pressed(self, event):
        global load_d
        if self.cheat_on:
            self.cheat_on = False
            self.canvas.delete(self.cheat_text)
        self.cheat_code += event.char
        if event.keysym == 'Left':
            self.left = True
            self.cheat_code = ""
        if event.keysym == 'Right':
            self.right = True
            self.cheat_code = ""
        if event.keysym == 'Up':
            self.up = True
            self.cheat_code = ""
        if event.keysym == 'Down':
            self.down = True
            self.cheat_code = ""
        if event.keysym == 'Delete':
            self.cheat_code = ""
        if event.keysym == "Return" and self.save_on:
            print(1)
            try:
                with open('load.txt', 'r') as file:
                    for line in file:
                        pass
                load_d = json.loads(line)
            except:
                pass
            load_d[self.save_entry.get()] = self.score
            with open('load.txt', 'a+') as file:
                file.write(json.dumps(load_d))
                file.write('\n')
            self.save_entry.place_forget()
            self.save_on = False
            self.save_button.place(x=748, y=52)
            self.pause = False

        # ----------------- adding some cheat codes -----------------
        if self.cheat_code == "scoreup":
            self.cheat_on = True
            self.cheat_text = self.canvas.create_text(400, 300, text="Cheat code activated",
                                                      font='times 40', fill='red')
            self.cheat_code = ""
            self.score += 10
            self.canvas.delete(self.score_text)
            self.score_text = self.canvas.create_text(100, 20, text="Score: " + str(self.score),
                                                      font='algerian 30', fill='#a300fe')
            self.canvas.after(500, lambda: self.key_pressed(event))
        if self.cheat_code == "leavemealone":
            self.cheat_on = True
            self.cheat_text = self.canvas.create_text(400, 300, text="Cheat code activated",
                                                      font='times 40', fill='red')
            self.cheat_code = ""
            for z in range(self.num_of_enemies):
                self.canvas.delete(self.app[z])
                self.enemy_x[z] = randint(0, self.X_limit)
                self.enemy_y[z] = 0
                self.app[z] = self.canvas.create_image(self.enemy_x[z], self.enemy_y[z], image=self.enemy_images[z],
                                                       anchor=NW)
            self.canvas.after(500, lambda: self.key_pressed(event))
        if self.cheat_code == "cosmicsave":
            self.cheat_on = True
            self.cheat_text = self.canvas.create_text(400, 300, text="Cheat code activated",
                                                      font='times 40', fill='red')
            self.cheat_code = ""
            self.asteroid_y = 600
            self.canvas.after(500, lambda: self.key_pressed(event))
        if self.cheat_code == "powerup":
            self.cheat_on = True
            self.cheat_text = self.canvas.create_text(400, 300, text="Cheat code activated",
                                                      font='times 40', fill='red')
            self.cheat_code = ""
            if not self.power:
                self.power = True
                self.bullet_aura += 100
            else:
                self.power = False
                self.bullet_aura -= 100
            self.canvas.after(500, lambda: self.key_pressed(event))
        if self.cheat_code == "straighttothefinal":
            self.cheat_on = True
            self.cheat_text = self.canvas.create_text(400, 300, text="Cheat code activated",
                                                      font='times 40', fill='red')
            self.cheat_code = ""
            self.final_stage_f()
            self.canvas.after(500, lambda: self.key_pressed(event))
        if self.cheat_code == "chickenwar":
            self.cheat_on = True
            self.cheat_text = self.canvas.create_text(400, 300, text="Cheat code activated",
                                                      font='times 40', fill='red')
            self.cheat_code = ""
            if not self.chicken_on:
                self.chicken_on = True
            else:
                self.chicken_on = False
            self.canvas.after(500, lambda: self.key_pressed(event))

        if event.keysym == 'space' and self.loaded:
            # PlaySound('laser.wav', SND_ASYNC)
            self.cheat_code = ""
            self.loaded = False
            self.fire = True
            self.bulletX, self.bulletY = self.characterX, self.characterY
            self.bullet_movement()

    # ----------------- function to be called when any keyboard key is released -----------------
    def key_release(self, event):
        if event.keysym == 'Left':
            self.left = False
        if event.keysym == 'Right':
            self.right = False
        if event.keysym == 'Up':
            self.up = False
        if event.keysym == 'Down':
            self.down = False

    # ----------------- function to create a final level -----------------
    def final_stage_f(self):
        self.final_stage = True
        try:
            for g in self.app:
                self.canvas.delete(g)
            self.canvas.delete(self.asteroid)
        except:
            pass
        self.boss_spaceship = self.canvas.create_image(self.boss_x, self.boss_y, image=final)
        self.canvas.delete(self.score_text)
        self.boss_health_text = self.canvas.create_text(400, 20, text="Health: " + str(self.boss_health),
                                                        font='algerian 30', fill='#a300fe')
        self.boss_arrival()

    # ----------------- function to generate boss-spaceship image -----------------
    def boss_arrival(self):
        if self.boss_y < 110:
            self.canvas.move(self.boss_spaceship, 0, 2)
            self.boss_y += 2
            self.canvas.after(self.FPS, self.boss_arrival)
        else:
            if not self.pause:
                for e in range(self.num_of_boss_bullets):
                    self.boss_bullet_x.append(randint(0, 800))
                    self.boss_bullet_y.append(150)
                    self.boss_bullet.append(self.canvas.create_image(self.boss_bullet_x[e], self.boss_bullet_y[e],
                                                                     image=b_bullet))
                self.boss_fire()
            else:
                self.canvas.after(self.FPS, self.boss_arrival)

    # ----------------- function to control boss-spaceship's bullets -----------------
    def boss_fire(self):
        if not self.pause and not self.game_over:
            for y in range(self.num_of_boss_bullets):
                self.canvas.move(self.boss_bullet[y], 0, self.boss_bullet_speed)
                self.boss_bullet_y[y] += self.boss_bullet_speed
                if self.boss_bullet_y[y] >= 600:
                    self.canvas.delete(self.boss_bullet[y])
                    self.boss_bullet_x[y], self.boss_bullet_y[y] = randint(0, 768), 150
                    self.boss_bullet[y] = self.canvas.create_image(self.boss_bullet_x[y], self.boss_bullet_y[y],
                                                                   image=b_bullet)
            self.collision()
            self.canvas.after(self.FPS, self.boss_fire)
        else:
            self.canvas.after(self.FPS, self.boss_fire)

    # ----------------- function to detect collision with boss-spaceship -----------------
    def boss_collision(self):
        if ((self.boss_x - 390 <= self.bulletX <= self.boss_x - 392 + 742) and (
                self.boss_y - 110 <= self.bulletY <= self.boss_y - 110 + 135)) or (
                (self.boss_x - 390 <= self.bulletX + self.bullet_aura <= self.boss_x - 392 + 742) and (
                self.boss_y - 110 <= self.bulletY + self.bullet_aura <= self.boss_y - 110 + 135)):
            if not self.power:
                self.boss_health -= 1
            else:
                self.boss_health -= 5
            self.canvas.delete(self.bullet)
            self.fire = False
            self.loaded = True
            self.canvas.itemconfigure(self.boss_health_text, text="Health: " + str(self.boss_health))
            if self.boss_health <= 0:
                self.win = True
                self.score += 20
                self.show_over()

    # ----------------- function to pause the game -----------------
    def pause_f(self, event):
        self.cheat_code = ""
        if not self.pause:
            self.pause = True
        elif self.pause and not self.boss_on:
            self.unpause_timer()

    # ----------------- function to resume the game -----------------
    def unpause_timer(self):
        try:
            self.canvas.delete(self.unpause_text)
        except:
            pass
        self.unpause_text = self.canvas.create_text(400, 200, text=str(self.count), font='century 100', fill='red')
        if type(self.count) == int:
            self.count -= 1
        else:
            self.count = -1
        if self.count >= -1:
            if self.count == 0:
                self.count = "GO"
            self.canvas.after(1000, self.unpause_timer)
        else:
            self.canvas.delete(self.unpause_text)
            self.count = 3
            self.pause = False

    # ----------------- function to create boss-key -----------------
    def boss(self, event):
        if not self.boss_on:
            self.boss_on = True
            self.pause = True
            self.home_button.place_forget()
            self.save_button.place_forget()
            self.b_img = self.canvas.create_image(0, 0, image=boss_Img, anchor=NW)
        else:
            self.canvas.delete(self.b_img)
            self.home_button.place(x=748, y=2)
            self.save_button.place(x=748, y=52)
            self.boss_on = False
            self.unpause_timer()

    # ----------------- function to detect collision between enemies and character's bullet -----------------
    def collision(self):
        if not self.game_over and not self.final_stage:
            if self.fire:
                for h in range(self.num_of_enemies):
                    # if ((self.enemy_x[h] <= self.bulletX <= self.enemy_x[h] + self.enemy_aura) and (
                    #        self.enemy_y[h] <= self.bulletY <= self.enemy_y[h] + self.enemy_aura)) or (
                    #        (self.enemy_x[h] <= self.bulletX + self.bullet_aura <= self.enemy_x[h] + self.enemy_aura)
                    #        and (self.enemy_y[h] <= self.bulletY + self.bullet_aura <= self.enemy_y[h]
                    #             + self.enemy_aura)):
                    if sqrt(((self.enemy_x[h] - self.bulletX) ** 2) + (
                            (self.enemy_y[h] - self.bulletY) ** 2)) < self.safe_distance:
                        # print(self.enemy_x[h],self.enemy_y[h],self.enemy_x[h]+32,self.enemy_y[h]+32)
                        # print(self.canvas.bbox(self.bullet))
                        # print(self.canvas.bbox(self.app[h]))
                        # PlaySound('Explosion+7.wav', SND_ASYNC)
                        self.canvas.delete(self.app[h])
                        self.enemy_x[h], self.enemy_y[h] = randint(0, self.X_limit), 0
                        self.app[h] = self.canvas.create_image(self.enemy_x[h], self.enemy_y[h],
                                                               image=self.enemy_images[h], anchor=NW)
                        self.canvas.delete(self.bullet)
                        self.fire = False
                        self.loaded = True
                        self.score += 1
                        self.canvas.itemconfigure(self.score_text, text="Score: " + str(self.score))
                        if self.score >= 10:
                            self.D1 = randint(1, 3)
                        if self.score >= 70:
                            self.final_stage_f()
        else:
            for o in range(self.num_of_boss_bullets):
                if ((self.characterX <= self.boss_bullet_x[o] <= self.characterX + self.character_aura) and (
                        self.characterY <= self.boss_bullet_y[o] <= self.characterY + self.character_aura)) or (
                        (self.characterX <= self.boss_bullet_x[o] + 27 <= self.characterX + self.character_aura)
                        and (self.characterY <= self.boss_bullet_y[o] + 27 <= self.characterY + self.character_aura)):
                    self.show_over()

    # ----------------- function to detect collision between character and enemies -----------------
    def over_f(self):
        for g in range(self.num_of_enemies):
            if self.score < 30:
                self.over_check = ((self.characterX <= self.enemy_x[g] <= self.characterX + self.character_aura)
                                   and (self.characterY <= self.enemy_y[g] <= self.characterY +
                                        self.character_aura)) or ((self.characterX <= self.enemy_x[g] +
                                                                   self.enemy_aura <= self.characterX
                                                                   + self.character_aura) and (
                                                                          self.characterY <= self.enemy_y[g]
                                                                          + self.enemy_aura <= self.characterY
                                                                          + self.character_aura))
            else:
                self.over_check = ((self.enemy_x[g] <= self.characterX <= self.enemy_x[g] + self.enemy_aura) and (
                        self.enemy_y[g] <= self.characterY <= self.enemy_y[g] + self.enemy_aura)) or (
                                          (self.enemy_x[g] <= self.characterX + self.character_aura <=
                                           self.enemy_x[g] + self.enemy_aura) and (
                                                  self.enemy_y[g] <= self.characterY
                                                  + self.character_aura <= self.enemy_y[g] + self.enemy_aura))
            if self.over_check:
                # PlaySound('Explosion+7.wav', SND_ASYNC)
                self.show_over()

        if self.final_stage:
            if ((self.boss_x - 390 <= self.characterX <= self.boss_x - 392 + 742)
                and (self.boss_y - 110 <= self.characterY <= self.boss_y - 110 + 135)) or (
                    (self.boss_x - 390 <= self.characterX + self.character_aura
                     <= self.boss_x - 392 + 742)
                    and (self.boss_y - 110 <= self.characterY
                         + self.character_aura <= self.boss_y - 110 + 135)):
                self.show_over()

    # ----------------- function to over the game -----------------
    def show_over(self):
        global def_score
        global over
        self.canvas.delete("all")
        self.save_button.place_forget()
        self.canvas.create_image(0, 0, image=running_background, anchor=NW)
        self.game_over = True
        self.replay()
        def_score = self.score
        over = True

    # ----------------- function to restart the game -----------------
    def restart(self):
        self.canvas.pack_forget()
        Play()

    # ----------------- function to return to the main menu -----------------
    def main_menu(self):
        self.game_over = True
        self.canvas.pack_forget()
        m.display()

    # ----------------- function to save the game -----------------
    def save(self):
        self.save_on = True
        self.save_button.place_forget()
        self.save_entry = Entry(self.canvas, insertwidth=1, font='Algerian 20', fg='#9c00ff', highlightthickness=0,
                                selectbackground="#a200fc", highlightcolor=None, bg='#eaf0fa')
        self.save_entry.place(x=240, y=220)
        self.save_entry.insert(0, "Save as: ")
        self.pause = True

    # ----------------- function to show replay screen -----------------
    def replay(self):
        if not self.win:
            self.over_text = self.canvas.create_text(400, 170, text="Game over !",
                                                     font='algerian 60', fill='red')
        else:
            self.over_text = self.canvas.create_text(400, 170, text="You Win !",
                                                     font='algerian 60', fill='red')
        self.final_score = self.canvas.create_text(390, 270, text="Score: " + str(self.score),
                                                   font='algerian 40', fill='#a300fe')
        self.button1 = Button(self.canvas, image=replay_Img, borderwidth=0, highlightthickness=0, width=250, height=100,
                              command=self.restart, activebackground='black', relief=FLAT)
        self.button1.place(x=260, y=360)


# ----------------- Class for main menu -----------------
class Main_screen:
    def __init__(self):
        self.update = False
        self.entry_on = False

    # ----------------- function to display main screen -----------------
    def display(self):
        global leader_d
        self.on = False
        self.canvas1 = Canvas(width=800, height=600, highlightthickness=0)
        self.canvas1.pack()
        self.canvas1.create_image(0, 0, image=running_background, anchor=NW)
        self.canvas1.create_text(400, 100, text='Space War', font='algerian 80', fill='red')
        # creating play button
        self.start_button = Button(self.canvas1, image=play_Img, borderwidth=0, width=150, height=80,
                                   command=self.start)
        self.start_button.place(x=310, y=380)
        self.options_button = Button(self.canvas1, image=options_Img, borderwidth=0, highlightthickness=0, width=80,
                                     command=self.options, height=80, activebackground='black', relief=FLAT)
        self.options_button.place(x=718, y=2)
        self.entry_button = Button(self.canvas1, text="Enter your name", font='algerian 20', borderwidth=0, relief=FLAT,
                                   highlightthickness=0, command=self.show_entry, activebackground='#eaf0fa',
                                   width=19, fg='#9c00ff', bg='#eaf0fa', activeforeground='#9c00ff')
        self.entry_button.place(x=240, y=220)
        self.background_button = Button(self.canvas1, image=select, borderwidth=0, width=200, height=80, bg='#060d1d',
                                        highlightthickness=0, command=self.background,
                                        activebackground='#060d1d')
        self.background_button.place(x=290, y=500)

    # ----------------- function to start the game -----------------
    def start(self):
        self.canvas1.pack_forget()
        Play()

    # ----------------- function to display the name entry window -----------------
    def show_entry(self):
        if not self.entry_on:
            self.entry_on = True
            self.entry_button.place_forget()
            self.entry = Entry(self.canvas1, insertwidth=1, font='Algerian 20', fg='#9c00ff', highlightthickness=0,
                               selectbackground="#a200fc", highlightcolor=None, bg='#eaf0fa')
            self.entry.place(x=240, y=220)
            self.entry.insert(0, "Hey enter your name: ")
            self.canvas1.bind_all('<Return>', self.welcome)

    # ----------------- function to display the welcome text -----------------
    def welcome(self, e):
        global xscore
        global over
        self.update = True
        try:
            self.entry.place_forget()
            self.entry_on = False
            self.entry_button.place(x=240, y=220)
            self.canvas1.delete(self.name_text)
            self.name_text = self.canvas1.create_text(410, 310, text="welcome " + str(self.entry.get()),
                                                      font='algerian 24', fill='#FF33FF')
        except:
            self.name_text = self.canvas1.create_text(410, 310, text="welcome " + str(self.entry.get()),
                                                      font='algerian 24',
                                                      fill='#FF33FF')
        self.name = self.entry.get()

    # ----------------- function to display change the background screen -----------------
    def background(self):
        self.start_button.place_forget()
        self.options_button.place_forget()
        if not self.entry_on:
            self.entry_button.place_forget()
            if self.update:
                self.canvas1.delete(self.name_text)
        else:
            self.entry.place_forget()
        self.background_button.place_forget()
        if self.on:
            self.options()
        self.b = IntVar()
        x = 30
        for i in range(3):
            Radiobutton(self.canvas1, image=d_Img[i], variable=self.b, value=i, highlightthickness=0,
                        borderwidth=0).place(x=x, y=200)
            x += 250
        self.background_button = Button(self.canvas1, image=tick, borderwidth=0, width=200, height=64, bg='#060d1d',
                                        highlightthickness=0, command=lambda: self.change_background(True),
                                        activebackground='#060d1d')
        self.background_button.place(x=500, y=500)
        self.background_button = Button(self.canvas1, image=back, borderwidth=0, width=120, height=70, bg='#060d1d',
                                        highlightthickness=0, command=lambda: self.change_background(False),
                                        activebackground='#060d1d')
        self.background_button.place(x=100, y=500)

    # ----------------- function to change the background screen -----------------
    def change_background(self, do):
        global running_background
        if do:
            self.selection = self.b.get()
            if self.selection == 0:
                running_background = back_1
            elif self.selection == 1:
                running_background = back_2
            elif self.selection == 2:
                running_background = back_3
        self.canvas1.pack_forget()
        self.display()

    # def _on_mousewheel(self, event):
    # self.canvas1.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def cheat_board(self):
        if not self.cheat_board_on:
            self.cheat_board_on = True
            self.cheat_text = Text(self.canvas1, height=12, width=25, font='century 20', bg='#7067d8',
                                   borderwidth=0, highlightthickness=3, highlightbackground='black', tabs=90,
                                   highlightcolor='black', selectbackground='#7067d8', selectforeground='black')
            self.cheat_text.insert(END, cheats)
            self.cheat_text.config(state='disabled')
            self.cheat_text.place(x=200, y=100)
            if self.leader_on:
                self.leader_frame.place_forget()
                self.leader_on = False
            if self.credit_on:
                self.credit_text.place_forget()
                self.credit_on = False
            if self.load_on:
                self.load_frame.place_forget()
                self.load_on = False
            if self.control_on:
                self.control_text.place_forget()
                self.control_on = False
        else:
            self.cheat_text.place_forget()
            self.cheat_board_on = False

    # ----------------- function to load the saved games -----------------
    def load_game(self):
        if not self.load_on:
            global load_d
            self.load_on = True
            self.load_frame = Frame(self.canvas1, bg='#7067d8')
            self.load_frame.place(x=200, y=100)
            self.load_canvas = Canvas(self.load_frame, height=400, bg='#7067d8', highlightthickness=0)
            self.load_canvas.pack(side=LEFT, fill=BOTH, expand=1)
            self.my_scrollbar = Scrollbar(self.load_frame, orient=VERTICAL, command=self.load_canvas.yview)
            self.my_scrollbar.pack(side=RIGHT, fill=Y)
            self.load_canvas.configure(yscrollcommand=self.my_scrollbar.set)
            self.load_canvas.bind('<Configure>',
                                  lambda e: self.load_canvas.configure(scrollregion=self.load_canvas.bbox("all")))
            self.second_frame = Frame(self.load_canvas, bg='#7067d8')
            self.load_window = self.load_canvas.create_window(0, 0, window=self.second_frame, anchor="nw")
            self.d = IntVar()
            try:
                with open('load.txt', 'r') as file:
                    for line in file:
                        pass
                load_d = json.loads(line)
                for i in load_d:
                    Radiobutton(self.second_frame, text=i, variable=self.d, value=load_d[i], relief=RAISED,
                                font='century 18', indicatoron=1, width=25, highlightcolor='black', borderwidth=1,
                                height=3, bg='#7067d8', command=self.save_score, activebackground='#7067d8').pack()
            except:
                pass

            if self.leader_on:
                self.leader_frame.place_forget()
                self.leader_on = False
            if self.control_on:
                self.control_text.place_forget()
                self.control_on = False
            if self.credit_on:
                self.credit_text.place_forget()
                self.credit_on = False
            if self.cheat_board_on:
                self.cheat_text.place_forget()
                self.cheat_board_on = False
        else:
            self.load_frame.place_forget()
            self.load_on = False

    # ----------------- function to save the loaded score -----------------
    def save_score(self):
        global load_score
        load_score = self.d.get()
        self.load_game()

    # ----------------- function to display leaderboard -----------------
    def leader_board(self):
        if not self.leader_on:
            global def_score
            global leader_d
            global over
            if self.update and over:
                leader_d[self.name] = def_score
            self.leader_on = True
            self.leader_frame = Frame(self.canvas1)
            self.leader_scrollbar = Scrollbar(self.leader_frame, orient=VERTICAL, highlightthickness=0)
            self.leader_text = Text(self.leader_frame, height=12, width=25, font='century 20', bg='#7067d8',
                                    borderwidth=0, highlightthickness=3, yscrollcommand=self.leader_scrollbar.set,
                                    highlightbackground='black', highlightcolor='black', selectbackground='#7067d8',
                                    selectforeground='black')
            self.leader_text.image_create(END, image=leader_text_Img)
            self.leader_scrollbar.config(command=self.leader_text.yview)
            self.leader_scrollbar.pack(side=RIGHT, fill=Y)
            self.leader_text.config(state=DISABLED)
            self.leader_text.pack()
            self.leader_frame.place(x=200, y=100)

            leader_d = dict(sorted(leader_d.items(), key=lambda item: item[1], reverse=True))
            with open('file.txt', 'a+') as file:
                if len(leader_d) != 0:
                    file.write(json.dumps(leader_d))
                    file.write('\n')

            with open('file.txt', 'r') as file:
                for line in file:
                    pass
            try:
                leader_d = json.loads(line)
                self.leader_text.config(state=NORMAL)
                for y in leader_d:
                    self.leader_text.insert(END, str(y) + '\t:\t' + str(leader_d[y]) + '\n')
                self.leader_text.config(state=DISABLED)
            except:
                pass
            if self.control_on:
                self.control_text.place_forget()
                self.control_on = False
            if self.credit_on:
                self.credit_text.place_forget()
                self.credit_on = False
            if self.load_on:
                self.load_frame.place_forget()
                self.load_on = False
            if self.cheat_board_on:
                self.cheat_text.place_forget()
                self.cheat_board_on = False
        else:
            self.leader_frame.place_forget()
            self.leader_on = False

    # ----------------- function to display controls -----------------
    def controls(self):
        if not self.control_on:
            self.control_on = True
            self.control_text = Text(self.canvas1, height=12, width=25, font='century 20', bg='#7067d8',
                                     borderwidth=0, highlightthickness=3, highlightbackground='black',
                                     highlightcolor='black', selectbackground='#7067d8', selectforeground='black')
            self.control_text.insert(END, instructions)
            self.control_text.config(state='disabled')
            self.control_text.place(x=200, y=100)
            if self.leader_on:
                self.leader_frame.place_forget()
                self.leader_on = False
            if self.credit_on:
                self.credit_text.place_forget()
                self.credit_on = False
            if self.load_on:
                self.load_frame.place_forget()
                self.load_on = False
            if self.cheat_board_on:
                self.cheat_text.place_forget()
                self.cheat_board_on = False
        else:
            self.control_text.place_forget()
            self.control_on = False

    # ----------------- function to display credits -----------------
    def credits(self):
        if not self.credit_on:
            self.credit_on = True
            self.credit_text = Text(self.canvas1, height=12, width=25, font='century 20', bg='#7067d8',
                                    borderwidth=0, highlightthickness=3, highlightbackground='black',
                                    highlightcolor='black', selectbackground='#7067d8', selectforeground='black')
            self.credit_text.insert(END, award)
            self.credit_text.config(state='disabled')
            self.credit_text.place(x=200, y=100)
            if self.leader_on:
                self.leader_frame.place_forget()
                self.leader_on = False
            if self.control_on:
                self.control_text.place_forget()
                self.control_on = False
            if self.load_on:
                self.load_frame.place_forget()
                self.load_on = False
            if self.cheat_board_on:
                self.cheat_text.place_forget()
                self.cheat_board_on = False
        else:
            self.credit_text.place_forget()
            self.credit_on = False

    # ----------------- function to create options button -----------------
    def options(self):
        if not self.on:
            self.load_on = False
            self.credit_on = False
            self.control_on = False
            self.leader_on = False
            self.cheat_board_on = False
            self.leader = Button(self.canvas1, height=100, width=195, image=leader_Img, highlightthickness=0,
                                 borderwidth=0, command=self.leader_board)
            self.leader.place(x=600, y=179)
            # self.canvas1.bind_all("<MouseWheel>", self._on_mousewheel)
            self.control = Button(self.canvas1, height=100, width=195, image=control_Img, highlightthickness=0,
                                  borderwidth=0, command=self.controls)
            self.control.place(x=600, y=299)
            self.credit = Button(self.canvas1, height=100, width=195, image=credits_Img, highlightthickness=0,
                                 borderwidth=0, command=self.credits)
            self.credit.place(x=600, y=419)
            self.load = Button(self.canvas1, height=100, width=195, image=save_Img, highlightthickness=0,
                               borderwidth=0, command=self.load_game)
            self.load.place(x=10, y=190)
            self.cheat = Button(self.canvas1, height=100, width=195, image=cheat_Img, highlightthickness=0,
                                borderwidth=0, command=self.cheat_board)
            self.cheat.place(x=10, y=310)
            self.on = True
        else:
            self.leader.place_forget()
            self.control.place_forget()
            self.credit.place_forget()
            self.load.place_forget()
            self.cheat.place_forget()
            self.on = False
            if self.leader_on:
                self.leader_frame.place_forget()
                self.leader_on = False
            if self.control_on:
                self.control_text.place_forget()
                self.control_on = False
            if self.credit_on:
                self.credit_text.place_forget()
                self.credit_on = False
            if self.load_on:
                self.load_frame.place_forget()
                self.load_on = False
            if self.cheat_board_on:
                self.cheat_text.place_forget()
                self.cheat_board_on = False


m = Main_screen()
m.display()
mainloop()

