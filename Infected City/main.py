import pgzrun
import time
import random 

#system variables
WIDTH, HEIGHT, TITLE = 1000,800, "Infected City"

#defining variables to be used later
difficulty = 0
stage=0
lives = 0
livelist = []
previous_time= 0 
bullet_last_time = 0
hit_last_time = 0
game_complete_time= None
stats= {
    "score": 0,
    "time":0,
    "kills":0
}
old_stats= []
reader = open('store.txt', 'r')
for x in range(3):
    old_stats.append(int(reader.readline()))
reader.close()

#creating Actors
tank=Actor("tank")
tank.pos=(WIDTH/2, HEIGHT/2)
bullets=[]
start_button= Actor("start")
start_button.pos=(WIDTH/2, HEIGHT-300)
easy = Actor('easy')
hard= Actor('hard')
easy.pos = (WIDTH- 85, HEIGHT-90)
hard.pos = (WIDTH- 85, HEIGHT-30)
next_button = Actor("nextbutton")
next_button.pos= (WIDTH/2, HEIGHT-300)
game_over = Actor("gameover")
game_over.pos = (WIDTH/2, HEIGHT/3)
replay_button= Actor('playagain')
replay_button.pos = (WIDTH/2.2, HEIGHT-200)
walls = []

def initialiselives(list,lives):
    global livelist
    for x in range(lives):
        heart = Actor("heart")
        heart.pos = (x + 1) * 50, 50
        list.append(heart)
    livelist= list

def create_walls(stage):
    global walls
    walls = []
    if not stage:
        pass
    elif stage == 1:
        for x in range(3): 
            wall = Actor("wall")
            wall.pos = (x+1)*100-50,50
            walls.append(wall)
            
        for x in range(7,10):
            wall = Actor("wall")
            wall.pos = (x+1)*100-50,50
            walls.append(wall)
            
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
            
        for x in range(7,10):
            wall = Actor("wall")
            wall.pos = (x+1)*100-50,HEIGHT-50
            walls.append(wall)

    elif stage in [2,3]:
        for x in range(3): 
            wall = Actor("wall")
            wall.pos = (x+1)*100-50,50
            walls.append(wall)
            
        for x in range(7,10):
            wall = Actor("wall")
            wall.pos = (x+1)*100-50,50
            walls.append(wall)

        for y in range(2):
            wall=Actor("wall")
            wall.pos= 50, (y+1)*100-50
            walls.append(wall)

            wall=Actor("wall")
            wall.pos= WIDTH-50, (y+1)*100-50
            walls.append(wall)
        for y in range(6,7):
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
        for x in range(7,10):
            wall = Actor("wall")
            wall.pos = (x+1)*100-50,HEIGHT-50
            walls.append(wall)
    
def create_enemies(stage):
    global enemy_attributes
    enemy_attributes = {
        "enemies":[],
        "spawn":[],
        "drawn": [],
        "health":[],
        "speed":[]
        }
    number_of_enemies = stage*10+10*difficulty
    if stage == 1:
        for x in range(number_of_enemies):
            enemy = Actor("slime")
            spawn = random.randint(1,2)
            enemy.x = random.randint(350,650)
            speed= 1.5
            if spawn == 1:
                enemy.y = 50
            else:
                enemy.y = HEIGHT - 50
            enemy_attributes["enemies"].append(enemy)
            enemy_attributes["spawn"].append(spawn)
            enemy_attributes["health"].append(1)
            enemy_attributes["drawn"].append(False)
            enemy_attributes["speed"].append(speed)

    elif stage == 2:
        for x in range(number_of_enemies):
            health = random.randint(1,2)
            if health == 1:
                enemy = Actor("slime")
                speed = 1.5
            else:
                enemy = Actor("insect")
                speed = 2.25
            spawn = random.randint(1,4)
            if spawn == 1:
                enemy.pos = (random.randint(350,650),50)
            elif spawn == 2:
                enemy.pos = (random.randint(350,650),HEIGHT-50)
            elif spawn == 3:
                enemy.pos = (50, random.randint(250,550))
            elif spawn ==4:
                enemy.pos = (WIDTH-50, random.randint(250,550))

            enemy_attributes["enemies"].append(enemy)
            enemy_attributes["spawn"].append(spawn)
            enemy_attributes["health"].append(health)
            enemy_attributes["drawn"].append(False)
            enemy_attributes["speed"].append(speed)

    elif stage == 3:
        for x in range(number_of_enemies):
            health = random.randint(1,4)
            if health == 1:
                enemy = Actor("slime")
                speed = 1.5
            elif health== 2:
                enemy = Actor("insect")
                speed = 2.25
            elif health > 2:
                health=4
                enemy= Actor("brute")
                speed = 0.75
            spawn = random.randint(1,4)
            if spawn == 1:
                enemy.pos = (random.randint(350,650),50)
            elif spawn == 2:
                enemy.pos = (random.randint(350,650),HEIGHT-50)
            elif spawn == 3:
                enemy.pos = (50, random.randint(250,550))
            elif spawn ==4:
                enemy.pos = (WIDTH-50, random.randint(250,550))

            enemy_attributes["enemies"].append(enemy)
            enemy_attributes["spawn"].append(spawn)
            enemy_attributes["health"].append(health)
            enemy_attributes["drawn"].append(False)
            enemy_attributes["speed"].append(speed)
    
def update():
        global bullets, previous_time,bullet_last_time, enemy_attributes, stage,lives, livelist, hit_last_time,stats

        current_time = time.time()
        delta_time = current_time-previous_time
        previous_time = current_time
        speed = 200
        original_pos= (tank.x,tank.y)
        reload_time = 0.2+ difficulty*0.15
        cooldown = 3 - difficulty*2
        
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
            if current_time - bullet_last_time > reload_time:

                bullet=Actor("bullet")
                bullet.pos=tank.pos
                bullet.angle=tank.angle
                bullets.append(bullet)
                bullet_last_time= time.time()
            
        for bullet in bullets:
            if bullet.collidelist(walls)!=-1 or not (0<bullet.x<WIDTH) or not (0<bullet.y<HEIGHT):
                bullets.remove(bullet)
                continue
            if bullet.angle==90:
                bullet.x-=7
            elif bullet.angle == 180:
                bullet.y+=7
            elif bullet.angle == 270:
                bullet.x+=7
            elif bullet.angle == 0:
                bullet.y-=7

            for x in range (len(enemy_attributes["enemies"])):
                if bullet.colliderect(enemy_attributes["enemies"][x]):
                    bullets.remove(bullet)
                    if enemy_attributes["health"][x]==1:
                         stats["kills"]+=1
                    enemy_attributes["health"][x]-=1
                    stats["score"] +=1
                    break

        if stage:
            for index, enemy in enumerate(enemy_attributes["enemies"]):
                enemy_speed= enemy_attributes["speed"][index]

                if enemy_attributes["spawn"][index] == 1 and enemy_attributes["drawn"][index]:
                    enemy.y +=  enemy_speed

                elif enemy_attributes["spawn"][index] == 2 and enemy_attributes["drawn"][index]:
                    enemy.y -= enemy_speed

                elif enemy_attributes["spawn"][index] == 3 and enemy_attributes["drawn"][index]:
                    enemy.x += enemy_speed
                    
                elif enemy_attributes["spawn"][index] == 4 and enemy_attributes["drawn"][index]:
                    enemy.x -=enemy_speed
                
                if enemy_attributes["health"][index]<=0:
                    enemy.pos =(0,0)
                    
            if tank.collidelist(enemy_attributes["enemies"]) != -1 and current_time-hit_last_time >cooldown:
                lives -= 1
                initialiselives([],lives)
                hit_last_time = time.time()
    
def on_mouse_down(pos):
    global stage,livelist,walls,start_time,lives, enemy_attributes,level_start_time, difficulty
    if not stage:
        if easy.collidepoint(pos):
            difficulty = 0
        if hard.collidepoint(pos):
            difficulty = 1
        if start_button.collidepoint(pos):
            stage+=1
            lives = 5 if difficulty==0 else 3
            initialiselives([],lives)
            create_walls(stage)
            create_enemies(stage)
            start_time= time.time()
            level_start_time=time.time()
    elif stage in [1,2,3] and len(livelist):
        if all_defeated(enemy_attributes["health"]):
            if next_button.collidepoint(pos):
                stage+=1
                create_enemies(stage)
                create_walls(stage)
                level_start_time=time.time()
    else:
        if replay_button.collidepoint(pos):
            stage = 0

def write_to_file(filename, stats):
    open(filename, 'w').close()
    writer = open(filename, 'a')
    for x in stats:
        writer.write(str(x)+'\n')
    writer.close()

def gameFinished(status, old_stats):
    screen.clear()
    screen.fill((0,0,0))
    message = Actor(status)
    message.pos = (WIDTH/2, HEIGHT/3)
    message.draw()
    replay_button.draw()
    counter = 0
    new_stats = []
    for key in stats:
        height = HEIGHT-400+counter*50
        width = WIDTH/2.5
        screen.draw.text(f"{key}: {stats[key]}", (width, height))
        if key == 'time':
            if status== 'gameover':
                new_stats.append(old_stats[counter])
            elif stats[key]<old_stats[counter]:
                screen.draw.text(f"New Best {key}!", (width + 150, height))
                new_stats.append(stats[key])
            else:
                new_stats.append(old_stats[counter])
        else:
            if stats[key]>old_stats[counter]:
                screen.draw.text(f"New Best {key}!", (width + 150, height))
                new_stats.append(stats[key])
            else:
                new_stats.append(old_stats[counter])
        counter+=1
    write_to_file("store.txt", new_stats)

def all_defeated(list):
    return all(health == 0 for health in list)

def draw_list(list):
    for item in list:
        item.draw()

def draw():

    global stage,livelist,walls,bullets, enemy_attributes,start_time,lives,game_complete_time,level_start_time, stats, old_stats
    screen.clear()
    if not stage:
        screen.blit("titlescreen", (0, 0))
        screen.draw.text("Infected City", (WIDTH/5, HEIGHT/5), color = (255,255,255), fontsize=150)
        rect = Rect((WIDTH-180, HEIGHT-120),(180, 120))
        screen.draw.filled_rect(rect, (0,0,0))
        easy.draw()
        hard.draw()
        start_button.draw()
        for key in stats:
            stats[key]=0
        if difficulty:
            screen.draw.text("Hard Mode Selected", (WIDTH/2.5, HEIGHT-150), color = (255,255,255))
        else:
            screen.draw.text("Easy Mode Selected", (WIDTH/2.5, HEIGHT-150), color = (255,255,255))

    elif stage in [1,2,3]:
        if len(livelist):
            screen.fill((25,25,25),)
            tank.draw()
            draw_list(walls)
            draw_list(livelist)
            draw_list(bullets)

            screen.draw.text(f"Score: {stats['score']}", (WIDTH-160, 20), color = (255,255,255), fontsize = 45)

            for x in range(len(enemy_attributes["enemies"])):
                if time.time()-level_start_time > x and enemy_attributes["health"][x]>0:
                    enemy_attributes["enemies"][x].draw()
                    enemy_attributes["drawn"][x]= True
                if not (0<enemy_attributes["enemies"][x].x<WIDTH) or not (0<enemy_attributes["enemies"][x].y<HEIGHT):
                    enemy_attributes["health"][x] = 0
                    continue
                if not len(enemy_attributes["enemies"]):
                    stage+=1
            if all_defeated(enemy_attributes["health"]):
                next_button.draw()

        else:
            if not stats["time"]:
                stats["time"]= int(time.time()-start_time)

            gameFinished('gameover', old_stats)

    else: 
        if not stats["time"]:
            stats["time"]= int(time.time()-start_time)
        gameFinished('win', old_stats)
            
pgzrun.go()