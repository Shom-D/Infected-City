import pgzrun
import time
import random

#system variables
WIDTH, HEIGHT, TITLE = 1000,800, ""

#defining variables to be used later
score = 0

reader = open("store.txt", 'r')
highscore = reader.readline()
old_times=[]
for line in reader:
    old_times.append(line)
reader.close()
for x in range(len(old_times)):
    old_times[x]=int(old_times[x])
print(old_times)
difficulty=0
stage=0
lives = 5 if difficulty==0 else 3
livelist = []
previous_time= 0 
bullet_last_time = 0
hit_last_time = 0


#creating Actors
tank=Actor("tank")
tank.pos=(WIDTH/2, HEIGHT/2)
enemy1 = Actor("slime")
bullets=[]
#enemy2 = 
#enemy3 =
startbutton= Actor("start")
startbutton.pos=(WIDTH/2, HEIGHT-300)
walls = []

def initialiselives(list,lives):
    global livelist
    for x in range(lives):
        heart = Actor("heart")
        heart.pos = (x + 1) * 50, 50
        list.append(heart)
    livelist= list
        #print(f"Heart {x + 1} created at {heart.pos}")



def createwalls(stage):
    global walls
    if not stage:
        pass
    elif stage == 1:
        for x in range(3): 
            wall = Actor("wall")
            wall.pos = (x+1)*100-50,50
            walls.append(wall)
            print(f"Wall created at {wall.pos}")
        for x in range(7,10):
            wall = Actor("wall")
            wall.pos = (x+1)*100-50,50
            walls.append(wall)
            print(f"Wall created at {wall.pos}")
        for y in range(7):
            wall=Actor("wall")
            wall.pos= 50, (y+1)*100-50
            walls.append(wall)

            wall=Actor("wall")
            wall.pos= WIDTH-50, (y+1)*100-50
            walls.append(wall)
        for x in range(3): 
            wall = Actor("wall")
            wall.pos = (x+1)*100-50,HEIGHT-50
            walls.append(wall)
            print(f"Wall created at {wall.pos}")
        for x in range(7,10):
            wall = Actor("wall")
            wall.pos = (x+1)*100-50,HEIGHT-50
            walls.append(wall)


    #  elif stage ==         
        
def create_enemies(stage):
    global enemy_attributes
    enemy_attributes = [[],[],[]]
    if stage == 1:
        for x in range(0,20):
            enemy = Actor("slime")
            spawn = random.randint(1,2)
            enemy.x = random.randint(350,650)
            if spawn == 1:
                enemy.y = 50
            else:
                enemy.y = HEIGHT - 50
            enemy_attributes[0].append(enemy)
            enemy_attributes[1].append(spawn)
            enemy_attributes[2].append(False)


def update():
        global bullets, previous_time,bullet_last_time, enemy_attributes, stage,lives, livelist, hit_last_time

        current_time = time.time()
        delta_time = current_time-previous_time
        previous_time = current_time
        speed = 200
        original_pos= (tank.x,tank.y)
        
        if keyboard.w and 150<tank.y:
            tank.angle=0
            tank.y-=speed *delta_time

        if keyboard.s and tank.y<HEIGHT-150:
            tank.angle=180
            
            tank.y+=speed *delta_time

        if keyboard.d and tank.x<WIDTH-150:
            tank.angle=270
            tank.x+=speed *delta_time

        if keyboard.a and 150<tank.x:
            tank.angle=90
            
            tank.x-=speed *delta_time

        if tank.collidelist(walls) != -1:
            tank.pos= original_pos
            
        if keyboard.space:
            if current_time - bullet_last_time > 0.5:

                bullet=Actor("bulletgreen2")
                bullet.pos=tank.pos
                bullet.angle=tank.angle
                bullets.append(bullet)
                bullet_last_time= time.time()
            
        for bullet in bullets:
            if bullet.collidelist(walls)!=-1 or not (0<bullet.x<WIDTH) or not (0<bullet.y<HEIGHT):
                bullets.remove(bullet)
            if bullet.angle==90:
                bullet.x-=7
            elif bullet.angle == 180:
                bullet.y+=7
            elif bullet.angle == 270:
                bullet.x+=7
            elif bullet.angle == 0:
                bullet.y-=7

        if stage:
            for counter in range(len(enemy_attributes[0])):

                if enemy_attributes[1][counter] == 1:
                    enemy_attributes[0][counter].y = enemy_attributes[0][counter].y +1

                elif enemy_attributes[1][counter] == 2:
                    enemy_attributes[0][counter].y = enemy_attributes[0][counter].y -1
        
            if tank.collidelist(enemy_attributes[0]) != -1 and current_time-hit_last_time >3:
                print("Collision")
                lives -= 1
                initialiselives([],lives)
                hit_last_time = time.time()

    
def on_mouse_down(pos):
    global stage,livelist,walls,start_time,lives
    if not stage:
        if startbutton.collidepoint(pos):
            stage+=1
            initialiselives([],lives)

            createwalls(stage)
            create_enemies(stage)
            start_time= time.time()

def gameOver(message, time, ):
    screen.clear
    

def draw():
    global stage,livelist,walls,bullets, enemy_attributes,start_time,lives
    screen.clear()
    if not stage:
        screen.blit("titlescreen", (0, 0))
        screen.draw.text("Infected City", (WIDTH/5, HEIGHT/5), color = (255,255,255), fontsize=150)
        startbutton.draw()


    elif stage in [1,2,3]:
        tank.draw()
        
        for wall in walls:
            wall.draw()
        if len(livelist)==0:
            gameOver("You died", )
        else:
            for heart in livelist:
                heart.draw() 
                #print(f"Drawing heart at {heart.pos}")
        for bullet in bullets:
            bullet.draw()
        for x in range(len(enemy_attributes[0])):
            if time.time()-start_time > x:
                enemy_attributes[0][x].draw()
            if WIDTH<enemy_attributes[0][x].x or 0 > enemy_attributes[0][x].x:
                enemy_attributes[0][x].remove()

    


pgzrun.go()