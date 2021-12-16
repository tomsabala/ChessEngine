import pygame as p

import chess
import chessEngine as chs


def main():
    # Initialise screen
    p.init()
    screen = p.display.set_mode((500, 500))
    p.display.set_caption('Chess Game')

    # Fill background
    background = p.Surface(screen.get_size())
    background = background.convert()
    background.fill(p.Color("lightsteelblue"))

    # Display some text
    font = p.font.Font(None, 36)
    textHead = font.render("Game Settings:", True, p.Color("cornflowerblue"))
    textpos = textHead.get_rect()
    textpos.centerx = background.get_rect().centerx

    text002 = font.render("Choose Difficulty: ", True, p.Color("cornflowerblue"))
    text002pos = text002.get_rect()
    text002pos.x = 20
    text002pos.y = 80

    text003 = font.render("Good Luck!", True, p.Color("cornflowerblue"))
    text003pos = text003.get_rect()
    text003pos.midbottom = background.get_rect().midbottom

    fontopt = p.font.Font(None, 26)
    opt1 = fontopt.render("Click -1- for a random component", True, p.Color("cornflowerblue"))
    opt1pos = opt1.get_rect()
    opt1pos.x = 50
    opt1pos.y = 130

    opt2 = fontopt.render("Click -2- for a level 1 component", True, p.Color("cornflowerblue"))
    opt2pos = opt2.get_rect()
    opt2pos.x = 50
    opt2pos.y = 160

    opt3 = fontopt.render("Click -3- for a level 2 component", True, p.Color("cornflowerblue"))
    opt3pos = opt3.get_rect()
    opt3pos.x = 50
    opt3pos.y = 190

    opt4 = fontopt.render("Click -4- for a level 3 component", True, p.Color("cornflowerblue"))
    opt4pos = opt4.get_rect()
    opt4pos.x = 50
    opt4pos.y = 220

    background.blit(text003, text003pos)
    background.blit(text002, text002pos)
    background.blit(textHead, textpos)
    background.blit(opt1, opt1pos)
    background.blit(opt2, opt2pos)
    background.blit(opt3, opt3pos)
    background.blit(opt4, opt4pos)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    p.display.flip()

    # Event loop
    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                return

        screen.blit(background, (0, 0))
        p.display.flip()


if __name__ == '__main__':
    main()