'''
Derived from freeCodeCamp.org

https://www.youtube.com/watch?v=XpYz-q1lxu8
'''
import numpy as np
import pygame
import sys
import math

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if  board[r][c] == piece and \
                board[r][c+1] == piece and \
                board[r][c+2] == piece and \
                board[r][c+3] == piece:
                return True
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if  board[r][c] == piece and \
                board[r+1][c] == piece and \
                board[r+2][c] == piece and \
                board[r+3][c] == piece:
                return True

    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if  board[r][c] == piece and \
                board[r+1][c+1] == piece and \
                board[r+2][c+2] == piece and \
                board[r+3][c+3] == piece:
                return True
    
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if  board[r][c] == piece and \
                board[r-1][c+1] == piece and \
                board[r-2][c+2] == piece and \
                board[r-3][c+3] == piece:
                return True

def draw_board(board):
    board = np.flip(board, 0)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, (0,0,255), (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            if board[r][c] == 0:
                pygame.draw.circle(screen, (0,0,0), (c*SQUARESIZE+SQUARESIZE//2, r*SQUARESIZE+SQUARESIZE+SQUARESIZE//2), SQUARESIZE//2 - 5)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, (255,0,0), (c*SQUARESIZE+SQUARESIZE//2, r*SQUARESIZE+SQUARESIZE+SQUARESIZE//2), SQUARESIZE//2 - 5)
            else:
                pygame.draw.circle(screen, (255,255,0), (c*SQUARESIZE+SQUARESIZE//2, r*SQUARESIZE+SQUARESIZE+SQUARESIZE//2), SQUARESIZE//2 - 5)
    pygame.display.update()

board = create_board()
game_over = False
turn = 0

pygame.init()
SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

screen = pygame.display.set_mode((width, height))

draw_board(board)
pygame.display.update()
font = pygame.font.SysFont("monospace", 75)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, (0,0,0), (0,0,width,SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, (255,0,0), (posx, SQUARESIZE//2), SQUARESIZE//2 - 5)
            else:
                pygame.draw.circle(screen, (255,255,0), (posx, SQUARESIZE//2), SQUARESIZE//2 - 5)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, (0,0,0), (0,0,width,SQUARESIZE))
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        game_over = True
                        label =  font.render("Player 1 Wins!", 1, (255,0,0))
                        screen.blit(label, (40,10))
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        game_over = True
                        label =  font.render("Player 2 Wins!", 1, (255,255,0))
                        screen.blit(label, (40,10))

            draw_board(board)
            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)