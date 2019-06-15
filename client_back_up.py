import socket
import pygame
import time

GAME_TIME = 120

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 600
BRIGHT_BLUE = 30, 144, 255
BLUE = 0, 0, 255
RECT_SIZE = 150, 50
WHITE = 255, 255, 255
BLACK = 0, 0, 0
BACKGROUND_COLOR = 30, 30, 30
BRIGHT_GREEN = 124, 252, 0
GREEN = 60, 179, 113

MSG_SIZE = 200, 30
SPACE_BETWEEN_MSGS = MSG_SIZE[1] + 5

SELF_MESSAGE_X = 20
OTHER_MSG_X = WINDOW_WIDTH - 220
SELF_MSG_COLOR = 173,255,47  # green
OTHER_MSG_COLOR = 105, 105, 105
last_msg_y = 20
OTHER_USER_NAME = ''
BUTTONS = []
SCORE = 0
OTHER_SCORE = 0
HIGH_SCORE = 0
HIGH_SCORE_USER = ''
LOW_SCORE = 0
LOW_SCORE_USER = ''
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


def text_objects(text, font):
    text_surface = font.render(text, True, BLACK)
    return text_surface, text_surface.get_rect()


def determine_message_size(msg):
    if len(msg) <= 20:
        return 30, msg
    lines = (len(msg) / 20) + 1
    msg1 = ''
    for x in xrange(lines):
        msg1 = msg[x*20:(1+x)*20]+'\n'
        print x
    print 'lines: ' + str(lines)
    print 'msg: ' + msg1
    return lines*20, msg1


def show_message(msg, self_msg):
    global last_msg_y
    global BUTTONS
    print str(len(msg)) + ': ' + msg

    if self_msg:
        x = SELF_MESSAGE_X
        color = SELF_MSG_COLOR
    else:
        x = OTHER_MSG_X
        color = OTHER_MSG_COLOR
    h , msg = determine_message_size(msg)
    pygame.draw.rect(screen, color, ((x, last_msg_y), (MSG_SIZE[0],h)))
    small_text = pygame.font.Font("freesansbold.ttf", 15)
    textSurf, text_rect = text_objects(msg, small_text)
    text_rect.center = x + (MSG_SIZE[0] / 2), last_msg_y + (h / 2)
    screen.blit(textSurf, text_rect)
    pygame.display.flip()
    last_msg_y += SPACE_BETWEEN_MSGS
    if last_msg_y >= WINDOW_HEIGHT:
        screen.fill(BACKGROUND_COLOR)
        pygame.display.flip()
        last_msg_y = 20
        BUTTONS = []


def button(msg, x, y, w, h, bc, c, action,text_size):
    con = False
    global SCORE
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if click[0]:
        if action == 'PLAY' and x < mouse[0] < x + w and y + h > mouse[1] > y:
            print 'got here1'
            con = True
        elif action == 'EXIT'and x < mouse[0] < x + w and y + h > mouse[1] > y:
            print 'got here'
            #send err#QUIT msg
            pygame.quit()
            quit()
        if action == '1' and msg == 'other user' and x < mouse[0] < x + w and y + h > mouse[1] > y:
            SCORE += 1
            con = True
        elif action == '2' and msg == 'computer' and x < mouse[0] < x + w and y + h > mouse[1] > y:
            SCORE += 1
            con = True
        elif (action == '1' or action == '2') and x < mouse[0] < x + w and y + h > mouse[1] > y:
            con = True
        elif action == 'start_screen' or 'chat' and x < mouse[0] < x + w and y + h > mouse[1] > y:
            con = True
    if x < mouse[0] < x + w and y + h > mouse[1] > y:
        pygame.draw.rect(screen, bc, ((x,y), (w,h)))
    else:
        pygame.draw.rect(screen, c, ((x,y), (w,h)))
    small_text = pygame.font.Font("freesansbold.ttf", text_size)
    textSurf, text_rect = text_objects(msg, small_text)
    text_rect.center = x + (w / 2), y + (h / 2)
    screen.blit(textSurf, text_rect)
    pygame.display.flip()
    return con


def start_screen(my_socket):
    pygame.init()
    finish = False
    pygame.display.set_caption('Game')
    screen.fill(BACKGROUND_COLOR)
    con = False
    start_time = time.time()
    user_name = game_loop(WINDOW_WIDTH/3 - 30, 20, 140, 32,my_socket,'',start_time)
    while not finish and not con:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
        con = button('QUIT', 100, 250,RECT_SIZE[0],RECT_SIZE[1], BLACK, WHITE, 'EXIT',40)
        con = button('GO', 300, 250, RECT_SIZE[0],RECT_SIZE[1], BRIGHT_BLUE, BLUE, 'PLAY',40)
    return user_name


#rect parameters
def game_loop(x, y, w, h, my_socket, user_name,start_time):
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(x,y,w,h)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done and time.time()-start_time <= GAME_TIME:
        if user_name != '':
            code_msg, msg = recv_any_msg(my_socket, user_name)
            if code_msg == 0:
                pygame.quit()
                quit()
                break
            if code_msg == 1:
                print 'message received'
                print 'this is msg: ' + msg
                show_message(msg, False)
                BUTTONS.append(('other user', OTHER_MSG_X - MSG_SIZE[0] - 10, last_msg_y-SPACE_BETWEEN_MSGS, 60, 20, BRIGHT_BLUE, BLUE, '1',10))
                BUTTONS.append(('computer', OTHER_MSG_X - MSG_SIZE[0] - 70, last_msg_y-SPACE_BETWEEN_MSGS, 60,20, BRIGHT_GREEN,GREEN, '1',10))
            if code_msg == 2:
                print 'message received'
                print 'this is msg: ' + msg
                show_message(msg, False)
                BUTTONS.append(('other user', OTHER_MSG_X - MSG_SIZE[0] - 10, last_msg_y-SPACE_BETWEEN_MSGS, 60,20, BRIGHT_BLUE, BLUE, '2',10))
                BUTTONS.append(('computer', OTHER_MSG_X - MSG_SIZE[0] -70, last_msg_y-SPACE_BETWEEN_MSGS, 60,20, BRIGHT_GREEN,GREEN, '2',10))
            if code_msg == 3:
                return msg
        check_buttons()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text)
                        if user_name != '':
                            show_message(text, True)
                            send_rgl_msg(my_socket,user_name,text)
                        return text
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                        pygame.draw.rect(screen,BACKGROUND_COLOR,(x,y,w + 300,h+5), 0)
                        # Render the current text.
                        txt_surface = font.render(text, True, color)
                        # Resize the box if the text is too long.
                        width = max(200, txt_surface.get_width() + 10)
                        input_box.w = width
                        # Blit the text.
                        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
                        # Blit the input_box rect.
                        pygame.draw.rect(screen, color, input_box, 2)

                        pygame.display.flip()
                    else:
                        text += event.unicode
        # Render the current text.
        pygame.draw.rect(screen, (30,30,30), input_box, 2)
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)

        try:
            '{}'.format(text)
        except:
            text = ''
            writing_in_hebrew(x, y, 175, h+5,'chat')

        pygame.display.flip()
        clock.tick(30)


def writing_in_hebrew(x,y,w,h, action):
    pygame.draw.rect(screen, BRIGHT_GREEN, (x,y,w,h))
    small_text = pygame.font.Font("freesansbold.ttf", 15)
    textSurf, text_rect = text_objects('Please Write in English', small_text)
    text_rect.center = x + (w / 2), y + (h / 2)
    screen.blit(textSurf, text_rect)
    pygame.display.flip()
    conti = False

    while not conti:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
        conti = button('GOT IT', x+w, y, 80, h, BRIGHT_BLUE, BLUE, action, 18)
    pygame.draw.rect(screen, BACKGROUND_COLOR, (x, y, w+100, h+20), 0)


def check_buttons():
    for b in BUTTONS:
        msg, x, y, w, h, bc, c, action, text_size = b
        pressed = button(msg, x, y, w, h, bc, c, action, text_size)
        if pressed:
            ind = BUTTONS.index(b)
            if msg == 'other user':
                del BUTTONS[ind]
                del BUTTONS[ind]
            if msg == 'computer':
                del BUTTONS[ind]
                del BUTTONS[ind-1]


def recv_s_msg(s):
    data = ''
    while data[-3:] != '###':
        data += s.recv(1024)
        if data == '':
            break
    data = data[:-3]
    return data


def recv_msg(s):
    data = ''
    while data[-3:] != '###':
        try:
            s.settimeout(0.1)
            data += s.recv(1024)
            print data
        except:
            pass
        if data == '':
            break
    data = data[:-3]
    if data != '':
        print 'got a msg:'
        print data
    return data


def send_message(my_socket, msg):
    my_socket.send(msg + '###')


def send_start_message(my_socket ,user_name):
    msg = 'username:{}'.format(user_name)
    send_message(my_socket, msg)


def send_rgl_msg(socket, user_name, msg):
    msg = 'rgl' + '#' + user_name + '#' + msg
    send_message(socket, msg)


def receive_start_msg(my_socket):
    msg = recv_s_msg(my_socket)
    print msg
    if msg == 'GO':
        return
    else:
        print 'something went wrong'
        pygame.quit()
        quit()


def show_message_received(msg):
    print 'you got the following msg:'
    print msg


def recv_any_msg(my_socket, user_name):
    msg = recv_msg(my_socket)
    msg = msg.split('#')
    if msg[0] == 'err':
        return 0, msg[1]
    if msg[0] == 'rgl' and msg[1] == 'server':
        print 'im here'
        print msg[2]
        return 2, msg[2]
    if msg[0] == 'rgl':
        return 1, msg[2]
    if msg[0].lower() == 'end':
        msg = '#'.join(msg)
        return 3, msg
    return 4, msg


def send_end_message(my_socket,user_name):
    my_socket.send('end#{}#{}###'.format(user_name,SCORE))


def end_game(my_socket, user_name,msg):
    win = 0  # 0=> tie 1=> win 2=> lost
    send_end_message(my_socket, user_name)
    print 'checking scores'
    if msg is None:
        msg = recv_s_msg(my_socket)
    print msg
    msg = msg.split('#')
    global OTHER_USER_NAME, OTHER_SCORE
    OTHER_USER_NAME, OTHER_SCORE = msg[1], int(msg[2])
    print 'other user name: {},other user score{}: '.format(OTHER_USER_NAME,OTHER_SCORE)
    if msg[0].lower() == 'end':
        if SCORE > OTHER_SCORE:
            HIGH_SCORE_USER = user_name
            HIGH_SCORE = SCORE
            LOW_SCORE = OTHER_SCORE
            LOW_SCORE_USER = msg[1]
            return 1
        elif SCORE < OTHER_SCORE:
            LOW_SCORE = SCORE
            LOW_SCORE_USER = user_name
            HIGH_SCORE = OTHER_SCORE
            HIGH_SCORE_USER = msg[1]
            return 2
        else:
            HIGH_SCORE = SCORE
            LOW_SCORE = 0
            return 3



def text_objects_white(text, font):
    text_surface = font.render(text, True, WHITE)
    return text_surface, text_surface.get_rect()


def end_screen(state):
    if state == 0:
        print 'this is a tie'
        img = pygame.image.load('game_over.png')
    elif state == 1:
        print 'YOU WIN'
        img = pygame.image.load('YOU_WIN.png')
    else:
        img = pygame.image.load('lose-screen.png')
        print 'YOU LOSE'
    screen.blit(img, (0, 0))
    pygame.display.flip()

    small_text = pygame.font.Font("freesansbold.ttf", 30)
    textSurf, text_rect = text_objects_white('YOUR SCORE: {}'.format(SCORE), small_text)
    text_rect.center = 80 + (RECT_SIZE[0] / 2), WINDOW_HEIGHT-100 + (RECT_SIZE[1] / 2)
    screen.blit(textSurf, text_rect)
    pygame.display.flip()

    small_text = pygame.font.Font("freesansbold.ttf", 30)
    textSurf, text_rect = text_objects_white('{}\'S SCORE: {}'.format(OTHER_USER_NAME.upper(),OTHER_SCORE), small_text)
    text_rect.center = 80 + (RECT_SIZE[0] / 2), WINDOW_HEIGHT - 50 + (RECT_SIZE[1] / 2)
    screen.blit(textSurf, text_rect)
    pygame.display.flip()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


def wait_screen():
    screen.fill(BACKGROUND_COLOR)
    small_text = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, text_rect = text_objects_white('waiting for the another user to connect...'.format(SCORE), small_text)
    text_rect.center = 180 + (RECT_SIZE[0] / 2), 200 + (RECT_SIZE[1] / 2)
    screen.blit(textSurf, text_rect)
    pygame.display.flip()


def main():
    my_socket = socket.socket()
    my_socket.connect(('127.0.0.1', 587))  # change it to argv in the end.

    # doing actions by protocol
    user_name = start_screen(my_socket)
    send_start_message(my_socket,user_name)
    wait_screen()
    receive_start_msg(my_socket)
    screen.fill(BACKGROUND_COLOR)
    start_time = time.time()
    while time.time() - start_time <= GAME_TIME:
        msg = game_loop(10, WINDOW_HEIGHT - 50, 60, 30, my_socket, user_name, start_time)
        pygame.draw.rect(screen, BACKGROUND_COLOR, (0, WINDOW_HEIGHT - 50, 500, 40), 0)
        pygame.draw.rect(screen,BACKGROUND_COLOR,(10, WINDOW_HEIGHT - 50, 130, 70),0)
    print 'end game'
    state = end_game(my_socket, user_name,msg)
    end_screen(state)
    pygame.draw.rect(screen, BACKGROUND_COLOR, (0, WINDOW_HEIGHT - 50, 500, 40), 0)


if __name__ == '__main__':
    main()
