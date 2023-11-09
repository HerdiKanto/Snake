import pygame
import os
import json
from random import randrange
pygame.init()
pygame.font.init()


def main(location=None):
    high_score = 0
    with open('scores.json', 'r') as openfile:

        # Reading from json file
        data = json.load(openfile)

    high_score = data["highscore"]
    print(high_score)
    playing=True
    running=True
    window = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    kopfx = 0
    kopfy = 0
    Movement=["rechts","links","oben","unter"]
    Current_Direction= Movement[0]
    Body=[[0, 501], [0, 501]]
    applex= 400
    appley= 400
    borderx=[0,800]
    bordery=[800,0]
    score=0


    #game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                running = False
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    playing = True
                    kopfx =200
                    kopfy=200
                    Body = [[], [], []]
                    Current_Direction=Movement[0]
                    score=0
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing= False
                    running = False
                    continue
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and Current_Direction != "links":
                        Current_Direction = Movement[0]
                    if event.key == pygame.K_LEFT  and Current_Direction != "rechts":
                        Current_Direction = Movement[1]
                    if event.key == pygame.K_DOWN and Current_Direction != "oben":
                        Current_Direction = Movement[3]
                    if event.key == pygame.K_UP and Current_Direction != "unter":
                        Current_Direction = Movement[2]
            move_body(Body,kopfx,kopfy)
            kopfx, kopfy = move(kopfx, kopfy, Current_Direction)






            draw_apple(window, applex, appley)

            draw_body(window, Body)

            #draw_kopf(window, kopfx,kopfy)
            draw_head(window,kopfx,kopfy,Current_Direction)



            if detect_body_crash(kopfx,kopfy,Body):
                playing = False

            if detect_crash(kopfx, kopfy):
                playing = False

            if detect_food(kopfx,kopfy,applex,appley):
                Body.append([kopfx, kopfy])
                applex=randrange(16) * 50
                appley = randrange(16) * 50
                score=score+1
                if score > high_score:
                    high_score = score
                    data["highscore"] = high_score
                    with open('scores.json', 'w') as file:
                        json.dump(data, file)


            my_font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = my_font.render(f'Score: {score}', False, (0, 0, 0))
            window.blit (text_surface, (0, 50))

            my_font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = my_font.render(f'High Score: {high_score     }', False, (0, 0, 0))
            window.blit(text_surface, (0,0))


            pygame.display.update()
            clear_window(window)
            clock.tick(5)


def detect_food (kopfx,kopfy,applex,appley):
    if (kopfx,kopfy) == (applex,appley):
        return True
    else:
        return False

def detect_body_crash (kopfx,kopfy,Body):
    if [kopfx, kopfy] in Body:
        return True

def detect_crash (kopfx, kopfy):
    max_x=800
    max_y=800
    min_x=0
    min_y=0
    if kopfx>=max_x:
        return True
    if kopfx<min_x:
        return True
    if kopfy>max_y:
        return True
    if kopfy<min_y:
        return True

    else: return False




def draw_apple(window,applex,appley):
    picture = pygame.image.load(os.path.join("Images", "lasagna.png"))
    picture = pygame.transform.scale(picture, (70, 70))
    window.blit(picture, (applex- 15, appley- 15))

def draw_kopf(window, kopfx, kopfy):
    pygame.draw.circle(window,"#5ba831", [kopfx,kopfy], 30)
def draw_head(window,kopfx,kopfy,Current_Direction):
    picture = pygame.image.load(os.path.join("Images", "snake head oben.png"))

    if Current_Direction=="oben":
       picture=pygame.image.load(os.path.join("Images", "snake head oben.png"))
    if Current_Direction == "rechts":
        picture = pygame.image.load(os.path.join("Images", "snake head rechts.png"))

    if Current_Direction == "links":
        picture = pygame.image.load(os.path.join("Images", "snake head links.png"))

    if Current_Direction == "unter":
        picture = pygame.image.load(os.path.join("Images", "snake head unter.png"))
    picture=pygame.transform.scale(picture,(100,100))
    window.blit(picture,(kopfx-25,kopfy-25))

def draw_body(window, Body):
    for körper in Body:

        #pygame.draw.rect(window,"#333300",(körper[0]-15, körper[1]-15, 30,30))
        picture=pygame.image.load(os.path.join("images","R.jpg"))
        picture=pygame.transform.scale(picture,(50,50))
        try:
            window.blit(picture,(körper[0],körper[1]))
        except:
            print("körper",körper)

def clear_window(window):
    hell_blau="#0eb4c9"
    dunkel_blau="#0e59c9"
    größe = 50
    pygame.draw.rect(window,hell_blau, (0,0,800,800))
    pygame.draw.rect(window, dunkel_blau, (0, 0, 800, 800))
    for y in range(16):
        for x in range(16):
            if (x+y)%2 == 0:
                color = hell_blau
            else:
                color = dunkel_blau
            pygame.draw.rect(window,color, (x*größe,y*größe,größe,größe))


def move_body (Body, kopfx,kopfy):
    #  Kx Ky    Body[0]    Body[1]
    #1 0, 500 [[0, 501], [0, 502]]

    #2 1, 500 [[0, 500]
    for i in range(len(Body)-1, 0, -1):
        Body[i]=Body[i-1]


    Body[0]=[kopfx, kopfy]

def move (kopfx, kopfy, Current_Direction):
    if Current_Direction=="oben":
       kopfy=kopfy-50
    if Current_Direction == "rechts":
        kopfx = kopfx + 50
    if Current_Direction == "links":
        kopfx = kopfx - 50
    if Current_Direction == "unter":
        kopfy = kopfy + 50

    return kopfx, kopfy

if __name__ == '__main__':
    main()