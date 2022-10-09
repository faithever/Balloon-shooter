import pygame

#initialize pygame and screen
pygame.init()

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

#background
background = pygame.image.load("./background.png")

#Stage
stage = pygame.image.load("./stage.png")
stage_rect = stage.get_rect()
stage_width = stage_rect.size[0]
stage_height = stage_rect.size[1]
stage_rect.left = 0
stage_rect.top = screen_height - stage_height 

#Player
player = pygame.image.load("./player.png")
player_rect = player.get_rect()
player_width = player_rect.size[0]
player_height = player_rect.size[1]
player_rect.left = screen_width / 2 - player_width / 2
player_rect.top = stage_rect.top - player_height
player_speed = 0.2
to_x = 0

# WEAPON
weapon_img = pygame.image.load("./weapon.png")
weapon_width = weapon_img.get_rect().size[0]
weapon_speed = 0.3

weapons = []

#load ball image
ball_images = [
   pygame.image.load("./ball1.png"),
   pygame.image.load("./ball2.png"),
   pygame.image.load("./ball3.png"),
   pygame.image.load("./ball4.png")]
ball_images_len = len(ball_images)
print("ball_images_len: {}".format(ball_images_len))

ball_speed_y = [-18, -15, -13, -11]

balls = []

#Running 
running = True

#Clock
clock = pygame.time.Clock()

#Program LEVEL
level = 0

#Text for Time
timeText = pygame.font.Font(None, 40)
startTime = pygame.time.get_ticks() 
elapseTime = 0

def create_ball1(direction = 1):
   print("Enter ceate_ball1")
   balls.append({
         "idx": 1,
         "to_x": 3 * direction,
         "to_y": -6,
         "pos_x": 50,
         "pos_y": 50,
         "init_spd_y": ball_speed_y[0]
   })

create_ball1()

while running:
   dt = clock.tick(30)
   curTime = pygame.time.get_ticks()
   elapseTime = int((curTime - startTime ) / 1000)
   playTimer = timeText.render(str(int(elapseTime)), True, (255,255,0))
   for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_LEFT:
            to_x -= player_speed
         elif event.key == pygame.K_RIGHT:
            to_x += player_speed
         elif event.key == pygame.K_ESCAPE:
            running = False
         elif event.key == pygame.K_SPACE:
            weapons.append([player_rect.left + (player_width / 2  - weapon_width / 2), player_rect.top])

      if event.type == pygame.KEYUP and not event.key is pygame.K_SPACE:
         to_x = 0

   # Player Calculating position
   player_rect.left += to_x * dt
   if player_rect.left < 0:
      player_rect.left = 0
   if player_rect.left > (screen_width - player_width):
      player_rect.left = screen_width - player_width 

   # Weapons position
   weapons = [ [w[0], w[1] - weapon_speed * dt]  for w in weapons ]
   weapons = [ [w[0], w[1] - weapon_speed * dt]  for w in weapons if w[1] > 0 ]

   # Ball position
   for ball_key, ball_value in enumerate(balls):
      ball_value["pos_x"] += ball_value["to_x"]
      ball_value["pos_y"] += ball_value["to_y"]
      ball_index = ball_value["idx"]
      ball_rect = ball_images[ball_index].get_rect()
      ball_width = ball_rect.size[0]
      ball_height = ball_rect.size[1]
      ball_rect.left = ball_value["pos_x"]
      ball_rect.top = ball_value["pos_y"]

      if ball_value["pos_x"] < 0 or ball_value["pos_x"] > screen_width - ball_width:
         ball_value["to_x"] = ball_value["to_x"] * -1
      if ball_value["pos_y"] > screen_height - stage_height - ball_height:
         ball_value["to_y"] = ball_value["init_spd_y"]
      else:
         ball_value["to_y"] += 0.5 

      # Check Collision
      for weapon_index, weapon in enumerate(weapons):
         weapon_rect = weapon_img.get_rect()
         weapon_rect.left = weapon[0]
         weapon_rect.top = weapon[1]
         if ball_rect.colliderect(weapon_rect):
            ball_value["idx"] += 1
            if ball_value["idx"] == ball_images_len:
               balls.pop(ball_key)
            else:
               balls.append({
                "idx": ball_value["idx"],
                "to_x": ball_value["to_x"] * -1,
                "to_y": ball_value["to_y"],
                "pos_x": ball_value["pos_x"],
                "pos_y": ball_value["pos_y"],
                "init_spd_y": ball_speed_y[ball_value["idx"]]})
            weapons.pop(weapon_index)
            break

      # check Collision with player
      if ball_rect.colliderect(player_rect):
         running = False

   # SCREEN BLIT
   screen.blit(background, (0,0))
   for weapon_x, weapon_y in weapons:
      screen.blit(weapon_img, (weapon_x, weapon_y))
   screen.blit(stage, (stage_rect.left, stage_rect.top))
   screen.blit(player, (player_rect.left, player_rect.top))
   screen.blit(playTimer, (10,10))

   if len(balls):
      for ball_value in balls:
         screen.blit(ball_images[ball_value["idx"]], (ball_value["pos_x"], ball_value["pos_y"]))
   else:
      if level == 0:
         create_ball1(-1)
         level += 1
      elif level == 1:
         create_ball1(1)
         create_ball1(-1)
         level += 1
   if level == 2:
      print("elapseTime {} and rest {}".format(elapseTime, int(elapseTime % 10)))
      if int(elapseTime % 10) == 0:
         create_ball1(1)
         level = 3
   elif level == 3:
      if len(balls) < 5:
         create_ball1(1)
         create_ball1(-1)
         level = 1


   #pygame displa update
   pygame.display.update()

#Destroy pygame
pygame.time.delay(2000)
pygame.quit()

