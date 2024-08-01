# XOXO
import random
import pygame as pg
import sys
import time
from pygame.locals import *
import json
import os
from gtts import gTTS
count = 0
width = 600
height = 400
line_color = (0, 0, 0)
white = (255, 255, 255)
winner = None
draw = None
pg.init()
pg.font.init()
pg.mixer.init()
pg.display.set_caption("X and O Online")
HEAD = pg.font.SysFont("bold", 25)
HEADER= pg.font.Font("Font/umberto/umberto.ttf", 20)
WINNER_FONT = pg.font.Font("Font/clickuper/Clickuper.ttf", 40)
WINNER_FONT2 = pg.font.Font("Font/clickuper/Clickuper.ttf", 20)
FIRSTFONT = pg.font.Font("Font/clickuper/Clickuper.ttf", 15)
PLAYFONT = pg.font.Font("Font/umberto/Umberto.ttf", 105)
FONT1 = pg.font.SysFont("consolas", 15)
INTRO_SOUND = pg.mixer.Sound(os.path.join("Audio", "intro.mp3"))
WIN_SOUND = pg.mixer.Sound(os.path.join("Audio", "win.mp3"))
KEY_SOUND = pg.mixer.Sound(os.path.join("Audio", "keyboard.mp3"))
DRAW_SOUND = pg.mixer.Sound(os.path.join("Audio", "draw.mp3"))
CLICK_SOUND = pg.mixer.Sound(os.path.join("Audio", "click.mp3"))
boxList1_3 = [" "," "," "]
boxList4_6 = [" "," "," "]
boxList7_9 = [" "," "," "]
the_list = [x for x in range(1,10)]
initiating_window = pg.image.load("Assets/X and O Online.png")
upward_bar = pg.image.load("Assets/yellow_bg.jpg")
x_img = pg.image.load("Assets/xicon.jpg")
y_img = pg.image.load("Assets/oicon.jpg")
initiating_window = pg.transform.scale(initiating_window, (width, height))
upward_bar = pg.transform.scale(upward_bar, (width, 30))
screen = pg.display.set_mode((width, height), 0, 32)
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(y_img, (80, 80))
x_score = 0
o_score = 0
fps = 30
initial = None
submitted = None
username = None 
# create rectangle 
start_rect = pg.Rect(95, 350, 120, 35)
highscore_rect = pg.Rect(390, 350, 120, 35)
comp_rect = pg.Rect(95, 220, 120, 35)
multiplayer_rect = pg.Rect(340, 220, 150, 35)
input_rect = pg.Rect(250, 150, 100, 30)
submit_rect = pg.Rect(250, 190, 100, 30)
back_rect = pg.Rect(10, 40, 100, 30)
color_active = pg.Color('thistle1') 
color_passive = pg.Color('black')
color = color_passive
font = pg.font.Font(None, 30)
font2 = pg.font.Font(None, 20)
comp = False
cancel_highscore = None
scroll_pos = 0  
max_scroll = 0  
pick = None
space = 90
def start():
    global XO,comp,initial,cancel_highscore
    done = None
    if cancel_highscore:
        cancel_highscore = None
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit() 
            if event.type == pg.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    cancel_highscore = True
                    done = True
                if comp_rect.collidepoint(event.pos):
                    XO = random.choice(['computer','player1'])
                    comp = True
                    done = True
                if multiplayer_rect.collidepoint(event.pos):
                    XO = random.choice(['player1','player2'])
                    done = True
            
        
        # it will set background color of screen 
        screen.fill((243, 188, 4)) 
        screen.blit(upward_bar,(0,0))
        pg.draw.rect(screen, 'black', back_rect)
        text1 = FONT1.render('BACK', 1, (255,255,255))
        screen.blit(text1,(back_rect.x + 15,back_rect.y + 7))
        pg.draw.rect(screen, 'black', comp_rect)
        pg.draw.rect(screen, 'white', multiplayer_rect)
        text1 = FIRSTFONT.render('COMPUTER', 1, (255,255,255))
        text2 = FIRSTFONT.render('MULTIPLAYER', 1, (0,0,0))
        text_surface2 = PLAYFONT.render("PLAY", 1, (0, 0, 0))
        screen.blit(text_surface2, (180, 100))
        screen.blit(text1, (comp_rect.x + 14,comp_rect.y + 8)) 
        screen.blit(text2, (multiplayer_rect.x + 13,multiplayer_rect.y + 7)) 
        pg.display.flip()
        clock = pg.time.Clock()
        clock.tick(60)
        pg.time.delay(200)
    if cancel_highscore:
        cover()
    initial = XO
def history():
    global cancel_highscore,pick, scroll_pos,max_scroll,space
    if cancel_highscore:
        cancel_highscore = None
    while cancel_highscore == None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                cancel_highscore = True
                pg.quit()
                sys.exit() 
            if event.type == pg.MOUSEBUTTONDOWN:
                    if back_rect.collidepoint(event.pos):
                        cancel_highscore = True
        with open('Scores/xando.txt', 'r') as file:
            data = file.read()
        data = data.split('][')
        new_data = ','.join(data)
        with open('Scores/xando.txt', 'w') as file:
            file.write(new_data)
        with open('Scores/xando.txt', 'r') as file:
            try:
                all = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):  # Handle errors gracefully
                all = 'NO HISTORY TO DISPLAY'
        screen.fill((243, 188, 4))
        
        pg.draw.rect(screen, 'black', back_rect)
        visible_scores = 10  
        score_height = FONT1.get_linesize() + 10
        num_scores = len(all)
        max_scroll = max(0, (num_scores - visible_scores) * score_height)
        y_pos = space + scroll_pos # Starting position for the first score
        screen_width = screen.get_width()
        
        if 'NO HISTORY TO DISPLAY' in all:
            score_text = FONT1.render(
                all,
                True,
                (0,0,0),  # White text
            )
            text_width = score_text.get_width()
            screen.blit(score_text, ((screen_width - text_width) // 2, y_pos))
        else:
            
            start_index = max(0, len(all) - visible_scores - int(scroll_pos / score_height))  # Calculate starting index for visible scores
            end_index = min(len(all), start_index + visible_scores)
            for i, score in enumerate(all[start_index:end_index]):
                player1 = score["player_1"]
                player2 = score["player_2"]
                x_score, o_score = score["x_score"], score["o_score"]
                date = score.get("date", "")
                score_text = FONT1.render(
                    f"{player1}: {x_score} vs {o_score}: {player2} ({date})",
                    True,
                    (0,0,0),  # White text
                )
                text_width = score_text.get_width()
                screen.blit(score_text, ((screen_width - text_width) // 2, y_pos))
                y_pos += FONT1.get_linesize()
        screen.blit(upward_bar,(0,0))
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                scroll_pos = max(0, scroll_pos - score_height) 
            elif event.key == pg.K_DOWN:
                scroll_pos = min(max_scroll, scroll_pos + score_height)
        text1 = FONT1.render('GO BACK', 1, (255,255,255))
        screen.blit(text1,(back_rect.x + 15,back_rect.y + 7))
        pg.display.flip()
        clock = pg.time.Clock()
        clock.tick(60)
        pg.time.delay(200)
    cover()
    
def cover():
    global pick
    mute = 0
    if pick:
        pick = None
    else:
        INTRO_SOUND.play()
    while pick == None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pick = True
                pg.quit()
                sys.exit() 
            if event.type == pg.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    mute +=1
                    if mute % 2 == 0:
                        INTRO_SOUND.play()
                    else:
                        INTRO_SOUND.stop()
                if start_rect.collidepoint(event.pos):
                    pick = 'start'
                elif highscore_rect.collidepoint(event.pos):
                    pick = 'highscores'
        screen.blit(initiating_window, (0, 0))
        pg.draw.rect(screen, 'black', start_rect)
        pg.draw.rect(screen, 'white', highscore_rect)
        pg.draw.rect(screen, 'black', back_rect)
        text1 = FIRSTFONT.render('START', 1, (255,255,255))
        text3 = FIRSTFONT.render('MUTE', 1, (255,255,255))
        text4 = FIRSTFONT.render('UNMUTE', 1, (255,255,255))
        text2 = FIRSTFONT.render('HISTORY', 1, (0,0,0))
        screen.blit(text1, (start_rect.x + 30,start_rect.y + 8)) 
        screen.blit(text2, (highscore_rect.x + 25,highscore_rect.y + 7)) 
        if mute % 2 == 0:
           screen.blit(text3,(back_rect.x + 15,back_rect.y + 7)) 

        else:
            screen.blit(text4,(back_rect.x + 15,back_rect.y + 7))
        pg.display.flip()
        clock = pg.time.Clock()
        clock.tick(60)
        pg.time.delay(200)
    if pick == 'start':
        start()
    if pick == 'highscores':
        history()
cover()

def name():
    global XO,comp,username,submitted
    user_text = '' 
    active = False
    while submitted == None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit() 
            if event.type == pg.MOUSEBUTTONDOWN:
                if submit_rect.collidepoint(event.pos):
                    KEY_SOUND.fadeout(1000)
                    if comp:
                        INTRO_SOUND.fadeout(1000)
                    if user_text != "":
                        submitted = True
                        return 'SUBMITTED'
                elif input_rect.collidepoint(event.pos): 
                    active = True
                else: 
                    active = False
            if event.type == pg.KEYDOWN:
                KEY_SOUND.stop()
                KEY_SOUND.play()
                # Check for backspace 
                if event.key == pg.K_BACKSPACE: 
    
                    # get text input from 0 to -1 i.e. end. 
                    user_text = user_text[:-1] 
    
                # Unicode standard is used for string 
                # formation 
                else: 
                    user_text += event.unicode
        text1 = FONT1.render('GO BACK', 1, (255,255,255))
        screen.blit(text1,(back_rect.x + 15,back_rect.y + 7))
        # it will set background color of screen 
        screen.fill('gray87') 
    
        if active: 
            color = color_active 
        else: 
            color = color_passive 
            
        # draw rectangle and argument passed which should 
        # be on screen 
        pg.draw.rect(screen, color, input_rect) 
        pg.draw.rect(screen, (243, 188, 4), submit_rect) 
        text_surface = font2.render(user_text, True, (0,0,0)) 
        text_surface2 = WINNER_FONT2.render("Player 1 enter your name below", 1, (0, 0, 0)) 
        text1 = FONT1.render('SUBMIT', 1, (0,0,0))
        # render at position stated in arguments 
        screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
        # render at position stated in arguments 
        screen.blit(text1, (submit_rect.x + 23,submit_rect.y + 9))   
        screen.blit(text_surface2, (100, 110)) 
        username = user_text
        clock = pg.time.Clock()
        clock.tick(60)
        pg.display.flip()
        
        
name()
submitted = None
def name2():
    global XO,comp,username2,submitted
    
    user_text = '' 
    active = False
    while submitted == None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit() 
            if event.type == pg.MOUSEBUTTONDOWN:
                if submit_rect.collidepoint(event.pos):
                    INTRO_SOUND.fadeout(1000)
                    if user_text != "":
                        submitted = True
                        return print('SUBMITTED')
                elif input_rect.collidepoint(event.pos): 
                    active = True
                else: 
                    active = False
            if event.type == pg.KEYDOWN: 
                # Check for backspace 
                if event.key == pg.K_BACKSPACE: 
    
                    # get text input from 0 to -1 i.e. end. 
                    user_text = user_text[:-1]
    
                # Unicode standard is used for string 
                # formation 
                else: 
                    user_text += event.unicode

        # it will set background color of screen 
        screen.fill('gray87') 
    
        if active: 
            color = color_active 
        else: 
            color = color_passive 
            
        # draw rectangle and argument passed which should 
        # be on screen 
        pg.draw.rect(screen, color, input_rect) 
        pg.draw.rect(screen, (243, 188, 4), submit_rect) 
        text_surface = font2.render(user_text, True, (0,0,0)) 
        text_surface2 = WINNER_FONT2.render("Player 2 enter your name below", 1, (0, 0, 0)) 
        text1 = FONT1.render('SUBMIT', 1, (0,0,0))
        # render at position stated in arguments 
        screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
        # render at position stated in arguments 
        screen.blit(text1, (submit_rect.x + 23,submit_rect.y + 9))   
        screen.blit(text_surface2, (100, 110)) 
        username2 = user_text
        clock = pg.time.Clock()
        clock.tick(60)
        pg.display.flip()
if not comp:
    name2()
def game_initiating_window():
    global x_score,o_score,username,username2,count,initial,XO
    if count == 1:
        XO = initial
    if len(username) > 10:
        username = username[:11]
    if not comp:
        if username2:
            if len(username2) > 10:
                username2 = username2[:11]
    screen.fill(white)
    # drawing vertical lines
    pg.draw.line(screen, line_color, (width / 3, 30), (width / 3, height), 7)
    pg.draw.line(screen, line_color, (width / 3 * 2, 30),
                 (width / 3 * 2, height), 7)
 
    # drawing horizontal lines
    pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7)
    pg.draw.line(screen, line_color, (0, height / 3 * 2),
                 (width, height / 3 * 2), 7)
    x = 'X Score :' + str(x_score)
    if comp:
        o = 'Comp Score :' + str(o_score)
    else:
        o = 'O Score :' + str(o_score)
    text1 = FONT1.render(x, 1, (white))
    text2 = FONT1.render(o, 1, (white))
    screen.blit(upward_bar,(0,0))
    text_rect1 = text1.get_rect(center=(width / 3 - 130, 10))
    if comp:
        text_rect2 = text1.get_rect(center=(width - 100, 10))
    else:
        text_rect2 = text1.get_rect(center=(width - 90, 10))
    screen.blit(text1, text_rect1)
    screen.blit(text2, text_rect2)
    pg.display.update()
    draw_status()
def draw_status():
    global count
    count += 1
    if winner is None:
        if XO == 'computer':
           message = "Computer Played" 
        if XO == 'player1':
            message = username + "'s Turn"
        if XO == 'player2':
            message = username2 + "'s Turn"
    else:
        if username != None and winner == 'Player1':
            message = username + " Won !"
        elif not comp:
            if username2 and winner == 'Player2':
                message = username2 + " Won !"
        else:
            message = 'Computer Won !'
    if draw:
        message = "Game Draw !"
    BACK = pg.Rect(width/2 - 90, -10, 180, 40)
    pg.draw.rect(screen, (0,0,0), BACK)
    if winner:
        text = WINNER_FONT.render(message, 1, (243, 188, 4))
        text_rect = text.get_rect(center=(width / 2, height / 2))
        text2 = WINNER_FONT.render(message, 1, (0,0,0))
        text_rect2 = text.get_rect(center=((width / 2) - 2, height / 2 +1))
        screen.blit(text2, text_rect2)
        screen.blit(text, text_rect)
        
        pg.display.update()
    else:
        text = FONT1.render(message, 1, (255, 255, 255))
        text_rect = text.get_rect(center=(width / 2, 10))
        screen.blit(text, text_rect)
        pg.display.update()
def drawXO(picked):
    global boxList1_3,boxList4_6,boxList7_9, XO, comp
    if picked == 1:
        posx = 45
        posy = 33
    if picked == 2:
        posx = width / 3 + 50
        posy = 33
    if picked == 3:
        posx = width / 3 * 2 + 40
        posy = 33
    if picked == 4:
        posx = 45
        posy = height / 3 + 30
    if picked == 5:
        posx = width / 3 + 50
        posy = height / 3 + 30
    if picked == 6:
        posx = width / 3 * 2 + 40
        posy = height / 3 + 30
    if picked == 7:
        posx = 45
        posy = height / 3 * 2 + 30
    if picked == 8:
        posx = width / 3 + 50
        posy = height / 3 * 2 + 30
    if picked == 9:
        posx = width / 3 * 2 + 40
        posy = height / 3 * 2 + 30

    if(XO == 'player1') and picked in the_list:
        screen.blit(x_img, (posx, posy))
        if comp:
            XO = 'computer'
        else:
            XO = 'player2'
    else:
        if picked in the_list:
            screen.blit(o_img, (posx, posy))  
            XO = 'player1'
    pg.display.update()
def user_click():
    global boxList1_3,boxList4_6,boxList7_9,XO
    if XO == 'computer':
        time.sleep(0.2)
        data = tuple(x for x in the_list)
        player1 = 'X'
        player2 = 'O'
        picked = computer(list(boxList1_3),list(boxList4_6),list(boxList7_9),player1,player2,list(data))
       
        if picked in range(4) and picked in the_list:
            boxList1_3[int(picked)-1] = "O"
            
        elif picked in range(7) and picked in the_list:
            boxList4_6[int(picked)-4] = "O"

        elif picked in range(10) and picked in the_list:
            boxList7_9[int(picked)-7] = "O"
    else:
        x, y = pg.mouse.get_pos()        
        if(x < (width / 3) - 4) and y < (height / 3) - 4:
            picked = 1
            if XO == 'player1'  and picked in the_list:
                boxList1_3[0] = 'X'
            elif picked in the_list:
                boxList1_3[0] = 'O' 
    
        elif (x < width / 3 * 2) and y < (height / 3) - 4:
            picked = 2
            if XO == 'player1'  and picked in the_list:
                boxList1_3[1] = 'X'
            elif picked in the_list:
                boxList1_3[1] = 'O'

        elif(x < width - 4) and y < (height / 3) - 4:
            picked = 3
            if XO == 'player1' and picked in the_list:
                boxList1_3[2] = 'X'
            elif picked in the_list:
                boxList1_3[2] = 'O'
        elif(x < (width / 3) - 4) and (y < (height / 3 * 2) - 4):
            picked = 4
            if XO == 'player1'  and picked in the_list:
                boxList4_6[0] = 'X'
            elif picked in the_list:
                boxList4_6[0] = 'O'
    
        elif (x < (width / 3 * 2) - 4) and (y < (height / 3 * 2) - 4):
            picked = 5
            if XO == 'player1' and picked in the_list:
                boxList4_6[1] = 'X'
            elif picked in the_list:
                boxList4_6[1] = 'O'
    
        elif(x < width - 4) and (y < (height / 3 * 2) - 4):
            picked = 6
            if XO == 'player1'  and picked in the_list:
                boxList4_6[2] = 'X'
            elif picked in the_list:
                boxList4_6[2] = 'O'
        elif(x < (width / 3) - 4) and (y < height - 4):
            picked = 7
            if XO == 'player1'  and picked in the_list:
                boxList7_9[0] = 'X'
            elif picked in the_list:
                boxList7_9[0] = 'O'
    
        elif (x < (width / 3 * 2) - 4) and (y < height - 4):
            picked = 8
            if XO == 'player1'  and picked in the_list:
                boxList7_9[1] = 'X'
            elif picked in the_list:
                boxList7_9[1] = 'O'
    
        elif(x < width - 4) and (y < height - 4):
            picked = 9
            if XO == 'player1'  and picked in the_list:
                boxList7_9[2] = 'X'
            elif picked in the_list:
                boxList7_9[2] = 'O'
    try:
        if(picked) and picked in the_list:
            CLICK_SOUND.play()
            drawXO(picked)
            the_list.remove(int(picked))
            check_win()
    except:
        check_win()

def check_win():
    global boxList1_3,boxList4_6,boxList7_9, winner, draw,x_score,o_score
    if boxList1_3.count('X') == 3 or boxList1_3.count('O') == 3:
        pg.draw.line(screen, (243, 188, 4),
                         (10, 74),
                         (width-20, 74),
                         7)
        pg.display.update()
        time.sleep(2)
    elif boxList4_6.count('X') == 3 or boxList4_6.count('O') == 3:
        row = 1
        pg.draw.line(screen, (243, 188, 4),
                         (10, (row + 1)*height / 3 - height / 6),
                         (width-20, (row + 1)*height / 3 - height / 6),
                         7)
        pg.display.update()
        time.sleep(2)
    elif boxList7_9.count('X') == 3 or boxList7_9.count('O') == 3:
        row = 2
        pg.draw.line(screen, (243, 188, 4),
                         (30, (row + 1)*height / 3 - height / 6),
                         (width-20, (row + 1)*height / 3 - height / 6),
                         7)
        pg.display.update()
        time.sleep(2)
    elif 'X' == boxList1_3[0] == boxList4_6[0] == boxList7_9[0] or 'O' == boxList1_3[0] == boxList4_6[0] == boxList7_9[0]:
        pg.draw.line(screen, (243, 188, 4),
                         (84, 30),
                         (84, height-30),
                         7)
        pg.display.update()
        time.sleep(2)
    elif 'X' == boxList1_3[1] == boxList4_6[1] == boxList7_9[1] or 'O' == boxList1_3[1] == boxList4_6[1] == boxList7_9[1]:
        pg.draw.line(screen, (243, 188, 4),
                         (width/ 3 * 2 - 110, 30),
                         (width/ 3 * 2 -110, height-10),
                         7)
        pg.display.update()
        time.sleep(2)
    elif 'X' == boxList1_3[2] == boxList4_6[2] == boxList7_9[2] or 'O' == boxList1_3[2] == boxList4_6[2] == boxList7_9[2]:
        pg.draw.line(screen, (243, 188, 4),
                         (width - 115, 30),
                         (width - 115, height-20),
                         10)
        pg.display.update()
        time.sleep(2)
    elif 'X' == boxList1_3[0] == boxList4_6[1] == boxList7_9[2] or 'O' == boxList1_3[0] == boxList4_6[1] == boxList7_9[2]:
        pg.draw.line(screen, (243, 188, 4),
                         (25, 32),
                         (width - 70, height-30),
                         10)
        pg.display.update()
        time.sleep(2)
    elif 'X' == boxList1_3[2] == boxList4_6[1] == boxList7_9[0] or 'O' == boxList1_3[2] == boxList4_6[1] == boxList7_9[0]:
        pg.draw.line(screen, (243, 188, 4),
                         (width - 70, 30),
                         (25,  height-30),
                         10) 
        pg.display.update()
        time.sleep(2)
    if boxList1_3.count('X') == 3 or boxList4_6.count('X') == 3 or boxList7_9.count('X') == 3:
        winner = 'Player1'
        x_score += 1
        
    elif 'X' == boxList1_3[0] == boxList4_6[0] == boxList7_9[0] or 'X' == boxList1_3[1] == boxList4_6[1] == boxList7_9[1] or 'X' == boxList1_3[2] == boxList4_6[2] == boxList7_9[2]:
        winner = 'Player1'
        x_score += 1
    elif 'X' == boxList1_3[0] == boxList4_6[1] == boxList7_9[2] or 'X' == boxList1_3[2] == boxList4_6[1] == boxList7_9[0]:
        winner = 'Player1'
        x_score += 1
    elif boxList1_3.count('O') == 3 or boxList4_6.count('O') == 3 or boxList7_9.count('O') == 3:
        if comp:
            winner = 'computer'
            o_score += 1
        else:
            winner = 'Player2'
            o_score += 1
    elif 'O' == boxList1_3[0] == boxList4_6[0] == boxList7_9[0] or 'O' == boxList1_3[1] == boxList4_6[1] == boxList7_9[1] or 'O' == boxList1_3[2] == boxList4_6[2] == boxList7_9[2]:
        if comp:
            winner = 'computer'
            o_score += 1
        else:
            winner = 'Player2'
            o_score += 1
    elif 'O' == boxList1_3[0] == boxList4_6[1] == boxList7_9[2] or 'O' == boxList1_3[2] == boxList4_6[1] == boxList7_9[0]:
        if comp:
            winner = 'computer'
            o_score += 1
        else:
            winner = 'Player2'
            o_score += 1
    elif ' ' not in boxList1_3 and ' ' not in boxList4_6 and ' ' not in boxList7_9:
        draw = True
    if winner:
        WIN_SOUND.play()
    elif draw:
        DRAW_SOUND.play()
    draw_status()
def computer(boxList1_3,boxList4_6,boxList7_9,player1,player2,real_list):
    ideal = tuple(real_list)
    ideal_list = list(ideal)
    check_list = list(ideal)
    box1 = list(tuple(boxList1_3))
    box2 = list(tuple(boxList4_6))
    box3 = list(tuple(boxList7_9))
    while len(ideal_list) >0:
        number = 0
        player2_pick = ideal_list[number]
        if player2_pick in range(4) and player2_pick in real_list:
            box1[int(player2_pick)-1] = player2
            ideal_list.remove(int(player2_pick))
            
        elif player2_pick in range(7) and player2_pick in real_list:
            box2[int(player2_pick)-4] = player2
            ideal_list.remove(int(player2_pick))

        elif player2_pick in range(10) and player2_pick in real_list:
            box3[int(player2_pick)-7] = player2
            ideal_list.remove(int(player2_pick))
        if box1.count(player2) == 3 or box2.count(player2) == 3 or box3.count(player2) == 3:
            
            
            return player2_pick
        elif player2 == box1[0] == box2[0] == box3[0] or player2 == box1[1] == box2[1] == box3[1] or player2 == box1[2] == box2[2] == box3[2]:
            
            return player2_pick
        elif player2 == box1[0] == box2[1] == box3[2] or player2 == box1[2] == box2[1] == box3[0]:
            
            return player2_pick
        else:
            if player2_pick in range(4) and player2_pick in real_list:
                box1[int(player2_pick)-1] = " "
            elif player2_pick in range(7) and player2_pick in real_list:
                box2[int(player2_pick)-4] = " "
            elif player2_pick in range(10) and player2_pick in real_list:
                box3[int(player2_pick)-7] = " "
    else:
        player2_pick = random.choice(check_list)
        picked = None
        if 'X' == box1[0] or 'X' == box1[2]:
            if 5 in real_list:
                player2_pick = 5
                picked = True
        if picked == None:
            if 'X' == box1[0] == box3[2] and 'O' == box2[1]:
                for x in [4,6]:
                    if x in real_list:
                        player2_pick = x
                        picked = True
                        break
        if picked == None:
            if 'X' == box1[2] == box3[0] and 'O' == box2[1]:
                for x in [4,6]:
                    if x in real_list:
                        player2_pick = x
                        picked = True
                        break

        if picked == None:
            if 'X' == box2[1]:
                for x in [1,3,7,9]:
                    if x in real_list:
                        player2_pick = x
                        picked = True
                        break
        if picked == None:
            if 'X' == box2[1] == box3[0] and 'O' == box1[2]:
                if 9 in real_list:
                    player2_pick = 9
                    picked = True
        if picked == None:
            if 'X' == box2[1] == box3[2] and 'O' == box1[0]:
                if 3 in real_list:
                    player2_pick = 3
                    picked = True
        if picked == None:
            if 'X' == box2[1] == box1[0] and 'O' == box3[2]:
                if 7 in real_list:
                    player2_pick = 7
                    picked = True
        if picked == None:
            if 'X' == box1[2] == box2[1] and 'O' == box3[1]:
                if 1 in real_list:
                    player2_pick = 1
                    picked = True
        checker = [box1[0],box1[2],box3[0],box3[2]]
        count = 0
        if picked == None:
            for x in checker:
                if x == 'X':
                    count += 1
            if count >= 2:
                for x in [box1[1],box2[1],box3[1]]:
                    if x in real_list:
                        player2_pick = x
                        break
        if player2_pick in range(4) and player2_pick in real_list:
            box1[int(player2_pick)-1] = player2
            check_list.remove(int(player2_pick))
        elif player2_pick in range(7) and player2_pick in real_list:
            box2[int(player2_pick)-4] = player2
            check_list.remove(int(player2_pick))

        elif player2_pick in range(10) and player2_pick in real_list:
            box3[int(player2_pick)-7] = player2
            check_list.remove(int(player2_pick))
    while len(check_list) > 0:
        number = 0
        player1_pick = check_list[number]
        if player1_pick in range(4) and player1_pick in real_list:
            box1[int(player1_pick)-1] = player1
            check_list.remove(int(player1_pick))
        elif player1_pick in range(7) and player1_pick in real_list:
            box2[int(player1_pick)-4] = player1
            check_list.remove(int(player1_pick))

        elif player1_pick in range(10) and player1_pick in real_list:
            box3[int(player1_pick)-7] = player1
            check_list.remove(int(player1_pick))

        if box1.count(player1) == 3 or box2.count(player1) == 3 or box3.count(player1) == 3:
            return player1_pick
        
        elif player1 == box1[0] == box2[0] == box3[0] or player1 == box1[1] == box2[1] == box3[1] or player1 == box1[2] == box2[2] == box3[2]:
            return player1_pick
        elif player1 == box1[0] == box2[1] == box3[2] or player1 == box1[2] == box2[1] == box3[0]:
            return player1_pick
        else:
            if player1_pick in range(4) and player1_pick in real_list:
                box1[int(player1_pick)-1] = " "
            elif player1_pick in range(7) and player1_pick in real_list:
                box2[int(player1_pick)-4] = " "

            elif player1_pick in range(10) and player1_pick in real_list:
                box3[int(player1_pick)-7] = " "  
        number += 1
    else:      
        return player2_pick 

def reset_game():
    global boxList1_3,boxList4_6,boxList7_9, winner, XO, draw,the_list,initial,count
    draw_status()
    count = 0
    if comp:
        if initial == 'computer':
            initial = 'player2'
    else:
        if initial == 'player1':
            initial = 'player2'
        if initial == 'player2':
            initial = 'player1'
    pg.time.delay(1200)
    boxList1_3 = [" "," "," "]
    boxList4_6 = [" "," "," "]
    boxList7_9 = [" "," "," "]
    the_list = [x for x in range(1,10)]
    winner = None
    draw = None
    game_initiating_window()
game_initiating_window()
def main():
    global XO,username,username2,x_score,o_score
    clock = pg.time.Clock()
    run = True
    while run:
        clock.tick(fps)
        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                high_score = []
                timely = time.time()
                date_str = time.ctime(timely)
                game_info = {
                    "player_1": username,
                    'player_2': username2 if not comp else "Computer",
                    "x_score": x_score,
                    "o_score": o_score,
                    "date": date_str,
                }
                high_score.append(game_info)
                
                with open('Scores/xando.txt', 'a') as file:
                    json.dump(high_score, file, indent=4)
                    file.close()
                delete =os.path.join(f"{os.getcwd()}", "playeraudio/")
                try:
                    for fname in os.listdir(delete):
                        if fname.endswith('.mp3'):
                            os.remove(fname)
                except:
                    print('None')
                path =os.path.join(f"{os.getcwd()}", "playeraudio/speech.mp3")
                try:
                    if comp:
                        myobj = gTTS(text=f'{username} won {x_score} times and Computer won {o_score} times', lang='en')
                    else:
                        myobj = gTTS(text=f'{username} won {x_score} times and {username2} won {o_score} times', lang='en')                   
                    myobj.save(path)
                except:
                    pass
                try:
                    WINNER_SOUND = pg.mixer.Sound(os.path.join("playeraudio", "speech.mp3"))
                    WINNER_SOUND.play()
                    length = WINNER_SOUND.get_length()
                    pg.display.update()
                    pg.time.delay(int(length*1000))
                    WINNER_SOUND.stop()
                except:
                    pass
                
                
                run = False
                pg.quit()
                sys.exit()

            if XO == "computer":
                user_click()
                if(winner or draw):
                    reset_game()
            if event.type == pg.MOUSEBUTTONDOWN:
                    user_click()
                    if(winner or draw):
                        reset_game()
                
        pg.display.update()
if __name__ == "__main__":
    main()