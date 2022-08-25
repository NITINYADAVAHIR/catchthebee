import random
import pygame

#initialize pygame
pygame.init()

#game constants
GAME_FOLDER = 'D:/python project/game dev/art_of_game_development/game_2/'
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 700

FPS = 60
TWO_SECONDS = FPS * 2
CLOUD_VELOCITY = 1
BEE_VELOCITY = 10
FLAP_RATE = 4
BOUNCE_GAP = 20
BEE_COUNT = 3

#create the window
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#know the sys fonts
#print(pygame.font.get_fonts())

#load the game font
game_font = pygame.font.SysFont(name='segoescript', size= 40, bold= True, italic= False )

#Using the game_font generate some texts
game_lose_text = game_font.render('Game Over, you LOSE!!!', True, (255,0,0))
game_win_text = game_font.render('Game Over, you WIN!!!', True, (255,0,0))

game_over_text = game_win_text
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

game_restart_text = game_font.render('Press q to quit, r to restart the game!!!', True, (0,0,255))
game_restart_text_rect = game_restart_text.get_rect()
game_restart_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2+60)



#window background
background_image = pygame.image.load(GAME_FOLDER + 'cafe.jpg')
background_image_rect = background_image.get_rect()
background_image_rect.topleft = (0,0)

#spray_can and spray_can pressed
spray_can = []
spray_can_pressed = []
for i in range(6):
    spray_can.append( pygame.image.load(GAME_FOLDER + 'spray_can_' + str(i) + '.png'))
    spray_can_pressed.append( pygame.image.load(GAME_FOLDER + 'spray_can_pressed_' + str(i) + '.png'))

my_can = spray_can[0]
my_can_rect = my_can.get_rect()
my_can_rect.center = WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 100


#spray_cloud
spray_cloud = []
for i in range(10):
    spray_cloud.append(pygame.image.load(GAME_FOLDER + 'spray_cloud_' + str(i) + '.png'))

current_cloud = spray_cloud[0]
current_cloud_rect = current_cloud.get_rect()


#bee
bees = {
    (-1,0) : [pygame.image.load(GAME_FOLDER + 'bee_0_left.png'), pygame.image.load(GAME_FOLDER + 'bee_1_left.png')],
    (-1,1) : [pygame.image.load(GAME_FOLDER + 'bee_0_bottomleft.png'), pygame.image.load(GAME_FOLDER + 'bee_1_bottomleft.png')],
    (-1,-1) : [pygame.image.load(GAME_FOLDER + 'bee_0_topleft.png'), pygame.image.load(GAME_FOLDER + 'bee_1_topleft.png')],
    (1,0): [pygame.image.load(GAME_FOLDER + 'bee_0_right.png'), pygame.image.load(GAME_FOLDER + 'bee_1_right.png')],
    (1,1) : [pygame.image.load(GAME_FOLDER + 'bee_0_bottomright.png'), pygame.image.load(GAME_FOLDER + 'bee_1_bottomright.png')],
    (1,-1) : [pygame.image.load(GAME_FOLDER + 'bee_0_topright.png'), pygame.image.load(GAME_FOLDER + 'bee_1_topright.png')]
}
movements = list(bees.keys())
print(movements)
movement = random.choice(movements)

bee = bees[movement][0]
bee_rect = bee.get_rect()
bee_rect.left= random.randint(0, WINDOW_WIDTH)
bee_rect.top= random.randint(0, WINDOW_HEIGHT)
bee_delay = TWO_SECONDS + TWO_SECONDS

dead_bees = []
current_bee_index = 0
#setup
pygame.mouse.set_visible(False)

#sound setup
bee_buzz = pygame.mixer.Sound(GAME_FOLDER + 'bee_buzzing.mp3')
# bee_buzz.set_volume(0.1)
is_buzzing = False

#game_values
my_can_level = 0
cloud_level =0
sprayed = 0
flap = FLAP_RATE
bee_alive = True
game_status = 1
#clock for moderating the loop iterations
clock = pygame.time.Clock()

#main game loop
running = True
while running:
    #blit the background image
    display_surface.blit(background_image, background_image_rect)

    #set my_can to the position of mouse
    my_can_rect.topleft = pygame.mouse.get_pos()

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.MOUSEBUTTONDOWN and game_status == 1:
            if ev.button == 1:
                if my_can_level < len(spray_can)-1:
                    my_can_level+=1
                    cloud_level = 0
                    my_can = spray_can_pressed[my_can_level]
                    current_cloud = spray_cloud[cloud_level]
                    current_cloud_rect.top = my_can_rect.top - 20
                    current_cloud_rect.right = my_can_rect.left
                    sprayed = TWO_SECONDS
                elif my_can_level == len(spray_can)-1:
                    game_status = 0 # loss
                    game_over_text = game_lose_text

        elif ev.type == pygame.MOUSEBUTTONUP :
            my_can = spray_can[my_can_level]
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_q:
                running = False
            elif ev.key == pygame.K_r:
                my_can_level = 0
                my_can = spray_can[my_can_level]
                cloud_level = 0
                sprayed = 0
                flap = FLAP_RATE
                bee_alive = True
                game_status = 1
                bee_delay = TWO_SECONDS + TWO_SECONDS
                bee_buzz.stop()
                is_buzzing = False
                dead_bees.clear()

    # animate the bee
    if game_status != 2:
        if flap:
            if bee_alive:
                bee_rect.left += movement[0] * BEE_VELOCITY
                bee_rect.top += movement[1] * BEE_VELOCITY
            flap-=1
        else:
            if bee == bees[movement][0]:
                bee = bees[movement][1]
            else:
                bee = bees[movement][0]
            flap = FLAP_RATE

        if bee_alive:
            # change the direction
            if bee_rect.left <= BOUNCE_GAP:
                movement = random.choice([(1, 0), (1, -1), (1, 1)])
                bee = bees[movement][0]
            elif bee_rect.right >= WINDOW_WIDTH - BOUNCE_GAP:
                movement = random.choice([(-1, 0), (-1, -1), (-1, 1)])
                bee = bees[movement][0]
            elif bee_rect.top <= BOUNCE_GAP:
                movement = random.choice([(-1, 0), (-1, 1), (1, 0), (1, 1)])
                bee = bees[movement][0]
            elif bee_rect.bottom >= WINDOW_HEIGHT - BOUNCE_GAP:
                movement = random.choice([(-1, 0), (-1, -1), (1, 0), (1, -1)])
                bee = bees[movement][0]
        else:
            #fall
            if bee_rect.bottom < WINDOW_HEIGHT:
                bee_rect.bottom+= 2
            else:
                #copy the dead bee
                temp = []
                temp.append(bee.copy())
                temp.append(bee_rect.copy())
                dead_bees.append(temp)

                current_bee_index +=1
                if current_bee_index < BEE_COUNT:
                    #next bee to come
                    bee_delay = TWO_SECONDS + TWO_SECONDS
                    bees[movement][0] = pygame.transform.rotate(bees[movement][0], 180)
                    bees[movement][1] = pygame.transform.rotate(bees[movement][1], 180)
                    movement = random.choice(movements)
                    bee = bees[movement][0]
                    flap = FLAP_RATE
                    bee_alive = True
                    is_buzzing = False

                else:
                    game_status = 2 #game over
                    game_over_text = game_win_text
                    print('Game Over')
        #blit the can and the bee
        display_surface.blit(my_can, my_can_rect)

        if bee_delay > 0:
            bee_delay -=1
        else:
            if not is_buzzing:
                bee_buzz.play(-1)
                is_buzzing= True
            display_surface.blit(bee, bee_rect)



        if sprayed:
            current_cloud_rect.left -= CLOUD_VELOCITY
            if current_cloud_rect.colliderect(bee_rect):
                if bee_alive and cloud_level < 7 :
                    bees[movement][0] = pygame.transform.rotate(bees[movement][0], 180)
                    bees[movement][1] = pygame.transform.rotate(bees[movement][1], 180)
                    bee_alive = False
                    bee_buzz.stop()


            display_surface.blit(current_cloud, current_cloud_rect)
            sprayed -= 1

            if sprayed % 12 == 0 and sprayed:
                cloud_level += 1
                current_cloud = spray_cloud[cloud_level]

    if game_status != 1:
        display_surface.blit(game_over_text, game_over_text_rect)
        display_surface.blit(game_restart_text, game_restart_text_rect)
    for db in dead_bees:
        display_surface.blit(db[0], db[1])

    pygame.display.update()
    #moderate the rate of loop iterations, thus achieve cooperative multitasking
    #the game must run at the same speed across different CPU's
    clock.tick(FPS)

#quit pygame
pygame.quit()