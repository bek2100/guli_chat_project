import socket
import threading
import time
import random

GAME_TIME = 120
USERS = []
random_messages = ['happy holiday!', 'see you next summer', 'miss you bae',
                   'my mom says hi', 'wanna go to a party this friday?', 'ok', 'let me know', 'im hungryyyy',
                   'let it go', 'I love you', 'how long is that game?', 'how you doing?', 'ma osim ahar kah?', 'ma?',
                   'LOL', 'WTF', 'hhhhhhhh', 'haha', 'tell me a joke', 'do you like this game?', 'this game sucks',
                   'so original', 'k', 'this is boring', 'love it']
MSG_RND_TIME = 5
msg = ''

clients = []


def recv_message(s):
    data = ''
    while data[-3:] != '###':
        data += s.recv(1024)
        if data == '':
            break
    data = data[:-3]
    return data


def send_msg(client_socket, msg):
    client_socket.send(msg + '###')


def rcv_start_message(client_socket):
    msg = recv_message(client_socket)
    user_name = msg[9:]
    USERS.append(user_name)


def send_err_msg(client_socket):
    send_msg(client_socket, 'err#QUIT')


def send_start_msg(client_socket):
    send_msg(client_socket, 'GO')
    print 'here'


def recv_any_msg(client_socket):
    msg = (recv_message(client_socket))
    if msg == '':
        print 'didnt get a message'
        return '-1', ''
    print msg
    msg = msg.split('#')
    print 'message got type:' + msg[0]
    if msg[0] == 'rgl':
        print 'got a rgl msg'
        msg = '#'.join(msg)
        return '1', msg
    if msg[0] == 'err':
        msg = '#'.join(msg)
        return '0', msg
    if msg[0] == 'end':
        msg = '#'.join(msg)
        return '2', msg
    msg = '#'.join(msg)
    return 3, msg


def forward_msg(client_socket, msg):
    send_msg(client_socket, msg)


def send_msg_from_server(client_socket):
    msg = (random_messages[random.randint(0, len(random_messages) - 1)])
    msg = 'rgl#server#' + msg
    send_msg(client_socket, msg)
    MSG_RND_TIME = random.randint(0, GAME_TIME / 5)


def handle_client(client_socket, j):
    rcv_start_message(client_socket)
    while len(USERS) < 2:
        if len(USERS) == 2:
            break
    send_start_msg(client_socket)
    start_time = time.time()
    s_time = time.time()

    while 1:
        code_msg, msg = recv_any_msg(client_socket)
        print 'im here and i got a msg'
        if code_msg == '0':
            send_err_msg(client_socket)
            print 'something went wrong. finishing game.'
            break
        elif code_msg == '1':
            print 'got a msg from client, will now forward it'
            for i, cl_socket in enumerate(clients):
                print 'i am j: {}'.format(j)
                if i != j:
                    print 'sending to i {} {}'.format(i, msg)
                    cl_socket.send(msg + '###')
        elif code_msg == '2':
            for i, cl_socket in enumerate(clients):
                print 'i am j: {}'.format(j)
                if i != j:
                    print 'sending to i {} {}'.format(i, msg)
                    cl_socket.send(msg + '###')
            break
        end_time = time.time()
        if end_time - start_time >= GAME_TIME:
            print 'finishing game'
            break
        if end_time - s_time >= MSG_RND_TIME:
            send_msg_from_server(client_socket)
            s_time = time.time()
            print 'here1'


def main():
    print 'im the server and i am ready to rock!'
    threads = []
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 587))
    server_socket.listen(20)
    j = 0
    while True:
        (client_socket, client_address) = server_socket.accept()
        t = threading.Thread(target=handle_client, args=(client_socket, j,))
        j += 1
        t.start()
        clients.append(client_socket)
        threads.append(t)
        for i in threads:
            i.join(0)
    server_socket.close()


if __name__ == '__main__':
    main()
