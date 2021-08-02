from threading import Thread
import pygame
import socket
import brushes
import dubercomponent

#-------------------------------GLOBALS-------------------------------#
sock = None  # socket

user_id = None
join_code = None
username = None
ip = None
port = None

owner = False

logo = None
window_width = None
window_length = None
window = None


login_font = None

username_box = None
ip_box = None
port_box = None
join_code_box = None
create_room_button = None
join_button = None


def send(message):
    """
    sends a message to the server

    Args:
        message (string): the message to be sent to the server
    """
    global sock
    sock.send(message.encode())
    # incomplete function


def send_brush_mark(mark):
    """
    Sends a point drawn from the brush to the server

    Args:
        mark (BrushMark): the mark that the user drew on the canvas
    """
    message = f'<d>\n{join_code}\n{mark.get_coordinates()}\n{mark.get_width()}\n{mark.get_colour()}'
    send(message)


def send_rect(rect):
    """
    Sends a rectangle drawn by the user to the server

    Args:
        rect (Rectangle): the rectangle to be sent to the server
    """
    message = f'<r>\n{join_code}\n{rect.get_top_left()}\n{rect.get_bottom_right()}\n{rect.get_colour()}\n{rect.get_filled()}'
    send(message)


def send_ellipse(ellipse):
    """
    Sends an ellipse drawn by the user to the server

    Args:
        ellipse (Ellipse): the ellipse to be sent to the server
    """
    message = f'<e>\n{join_code}\n{ellipse.get_top_left()}\n{ellipse.get_bottom_right()}\n{ellipse.get_colour()}\n{ellipse.get_filles()}'
    send(message)


def send_line(line):
    """
    sends a line drawn by the user to the server

    Args:
        line (Line): the line to be sent to the server
    """
    message = f'<L>\n{join_code}\n{line.get_top_left}\n{line.get_bottom_right()}\n{line.get_colour()}'
    send(message)


def disconnect():
    message = f'<dc>\n{user_id}'
    send(message)


def kick_user(target_id):
    """
    Kicks a selected user if the current user is the owner of the room

    Args:
        target_id (string): the user id of the user to be kicked
    """

    if owner:
        message = f'<k>\n{target_id}'
        send(message)


def join_room():
    """
    Joins an existing room upon logging in

    """
    global sock
    sock = socket.create_connection((ip, port))
    send(f"<j>\n{username}\n{join_code}")
    # unfinished method

    print(f"Joining room with: {username}, {ip}, {port}, {join_code}")

    # need condition to check if the login went through
    return False


def create_room():
    """
    Creates a new room upon logging in

    Args:
       username (string): the username selected by the user
       ip (string): the ip address of the server
       port (string): the server's port to connect to

    """
    global sock
    global owner
    sock = socket.create_connection((ip, port))
    print(f"Creating room with {username}, {ip}, {port}")

    owner = True

    # need condition to check if the login went through
    return False


def server_listener():
    """
    Listens to the server then calls a function to respond based on what the server sends
    """
    global sock
    running = True
    while running:
        data = sock.recv()
        print(data)


def main():
    """
    The main function
    """
    # Initialize pygame

    global logo
    global window_width
    global window_length
    global window

    global user_id
    global join_code
    global username
    global ip
    global port

    global login_font
    global username_box
    global ip_box
    global port_box
    global join_code_box
    global create_room_button
    global join_button

    pygame.init()
    pygame.display.set_caption("Duber Paint")
    logo = pygame.image.load("./assets/duberpaint.png")
    pygame.display.set_icon(logo)

    # screen size subject to change
    window_width = 1080
    window_length = 720
    window = pygame.display.set_mode((window_width, window_length))

    # uniform font for the login screen
    login_font = pygame.font.Font(None, 32)

    # textboxes for login information
    username_box = dubercomponent.DuberTextBox(
        450, 400, 300, 25, (255, 255, 255), '', login_font, (200, 200, 200))
    ip_box = dubercomponent.DuberTextBox(
        450, 430, 300, 25, (255, 255, 255), '', login_font, (200, 200, 200))
    port_box = dubercomponent.DuberTextBox(
        450, 460, 300, 25, (255, 255, 255), '', login_font, (200, 200, 200))
    join_code_box = dubercomponent.DuberTextBox(
        175, 550, 300, 25, (255, 255, 255), '', login_font, (200, 200, 200))
    create_room_button = dubercomponent.DuberTextBox(
        650, 550, 150, 25, (255, 255, 255), 'Create Room', login_font, (200, 200, 200))
    join_button = dubercomponent.DuberTextBox(
        275, 610, 55, 25, (255, 255, 255), 'Join', login_font, (200, 200, 200))
    # boolean to operate main program
    run = True
    login_screen = True
    editing_username = False
    editing_ip = False
    editing_port = False
    editing_join_code = False

    while run:
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # only detects user input for these objects if they are in the
            # login screen
            if login_screen:

                # detects if a user clicked on a text box to enter information
                if (event.type == pygame.MOUSEBUTTONDOWN) and (
                        event.button == 1):
                    if username_box.selected(pygame.mouse.get_pos()):
                        editing_username = True
                        editing_ip = False
                        editing_port = False
                        editing_join_code = False
                    elif ip_box.selected(pygame.mouse.get_pos()):
                        editing_username = False
                        editing_ip = True
                        editing_port = False
                        editing_join_code = False
                    elif port_box.selected(pygame.mouse.get_pos()):
                        editing_username = False
                        editing_ip = False
                        editing_port = True
                        editing_join_code = False
                    elif join_code_box.selected(pygame.mouse.get_pos()):
                        editing_username = False
                        editing_ip = False
                        editing_port = False
                        editing_join_code = True
                    elif join_button.selected(pygame.mouse.get_pos()):

                        username = username_box.get_text()
                        ip = ip_box.get_text()
                        port = port_box.get_text()
                        join_code = join_code_box.get_text()

                        login_screen = join_room()
                    elif create_room_button.selected(pygame.mouse.get_pos()):

                        username = username_box.get_text()
                        ip = ip_box.get_text()
                        port = port_box.get_text()

                        login_screen = create_room()

                # lets the user remove information for logging in
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if editing_username:
                            username_box.set_text(
                                username_box.get_text()[0:-1])
                        elif editing_ip:
                            ip_box.set_text(ip_box.get_text()[0:-1])
                        elif editing_port:
                            port_box.set_text(port_box.get_text()[0:-1])
                        elif editing_join_code:
                            join_code_box.set_text(
                                join_code_box.get_text()[0:-1])

                    # lets the user enter in information for logging in
                    else:
                        if editing_username and len(
                                username_box.get_text()) < 10:
                            username_box.set_text(
                                username_box.get_text() + event.unicode)
                        elif editing_ip and len(ip_box.get_text()) < 15:
                            ip_box.set_text(ip_box.get_text() + event.unicode)
                        elif editing_port and len(port_box.get_text()) < 4:
                            port_box.set_text(
                                port_box.get_text() + event.unicode)
                        elif editing_join_code and len(join_code_box.get_text()) < 6:
                            join_code_box.set_text(
                                join_code_box.get_text() + event.unicode)

            # user interactions for the main program after loggin in
            # (UNFINISHED)
            else:
                # there are supposed to be inputs here for the main screen but
                # we haven't gotten to that part yet
                window.fill((0, 0, 0))

        # update the screen
        if login_screen:
            update_login_screen()
        else:
            update_main_screen()


def update_main_screen():
    window.fill((0, 0, 0))
    window.blit(pygame.transform.scale(logo, (105, 73)), (0, 0))
    pygame.display.flip()


def update_login_screen():
    """
    Updates the login window when it is being used
    """

    window.fill((0, 0, 0))
    window.blit(logo, (330, 30))
    window.blit(
        login_font.render(
            'Username:', True, (255, 255, 255)), (300, 400))
    window.blit(
        login_font.render(
            'IP Address:', True, (255, 255, 255)), (300, 430))
    window.blit(
        login_font.render(
            'Port:', True, (255, 255, 255)), (300, 460))
    window.blit(
        login_font.render(
            'Join Code:', True, (255, 255, 255)), (25, 550))
    window.blit(
        login_font.render(
            'Or', True, (255, 255, 255)), (530, 550))
    username_box.draw(window)
    ip_box.draw(window)
    port_box.draw(window)
    join_code_box.draw(window)
    create_room_button.draw(window)
    join_button.draw(window)

    pygame.display.flip()


if __name__ == "__main__":
    main()
