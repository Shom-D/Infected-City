import pgzrun
import time

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

#prevtime=0

def initialiselives(list):
    for x in range(lives):
        heart = Actor("heart")
        heart.pos = (x + 1) * 50, 50
        list.append(heart)
        print(f"Heart {x + 1} created at {heart.pos}")
    return list


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
        

def movementcheck(player):
    global walls
    for wall in walls:
        if player.colliderect(wall):
                return True  
    return False  


def update():
        global bullets
        
        if keyboard.w and 150<tank.y:
            tank.angle=0
            if movementcheck(tank):
                tank.y+= 3
            else:
                tank.y-=3

        if keyboard.s and tank.y<HEIGHT-150:
            tank.angle=180
            if movementcheck(tank):
                tank.y-=3
            else:
                tank.y+=3

        if keyboard.d and tank.x<WIDTH-150:
            tank.angle=270
            
            if movementcheck(tank):
                tank.x-=3
            else:
                tank.x+=3

        if keyboard.a and 150<tank.x:
            tank.angle=90
            if movementcheck(tank):
                tank.x+=3
            else:
                tank.x-=3
            
        if keyboard.space:
            bullet=Actor("bulletgreen2")
            bullet.pos=tank.pos
            bullet.angle=tank.angle
            bullets.append(bullet)
            
        for bullet in bullets:
            if bullet.collidelist(walls)!=-1:
                bullets.remove(bullet)
            if bullet.angle==90:
                bullet.x-=7
            elif bullet.angle == 180:
                bullet.y+=7
            elif bullet.angle == 270:
                bullet.x+=7
            elif bullet.angle == 0:
                bullet.y-=7


    
def on_mouse_down(pos):
    global stage,livelist,walls
    if not stage:
        if startbutton.collidepoint(pos):
            stage+=1
            livelist = initialiselives([])
            createwalls(stage)
    

def draw():
    global stage,livelist,walls,bullets
    screen.clear()
    if not stage:
        screen.blit("titlescreen", (0, 0))
        screen.draw.text("Infected City", (WIDTH/5, HEIGHT/5), color = (255,255,255), fontsize=150)
        startbutton.draw()


    elif stage in [1,2,3]:
        
        tank.draw()
        
        for wall in walls:
            wall.draw()
        for heart in livelist:
            heart.draw() 
            #print(f"Drawing heart at {heart.pos}")
        for bullet in bullets:
            bullet.draw()
    


pgzrun.go()