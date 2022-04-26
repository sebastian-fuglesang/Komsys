from socket import timeout
import paho.mqtt.client as mqtt
import threading
import logging
import json
import pygame, sys
import numpy as np
import re
import sys
import winner

MQTT_BROKER = 'mqtt.item.ntnu.no'
MQTT_PORT = 1883

MQTT_TOPIC = 'ttm4115/team07/gameLobby'
MQTT_MOVES = [9,9,9]
def on_connect(client, userdata, flags, rc):
	print("Connection returned result: " + str(rc) )

def on_message(client, userdata, msg):
	#print("on_message(): topic: {} with payload: {}".format(msg.topic, msg.payload))
	print(msg.topic+" "+str(msg.payload))
	#Extract numbers from string
	data = str(msg.payload)
	mylist = re.findall(r'\d+', data)
	global MQTT_MOVES 
	MQTT_MOVES= mylist

mqtt_client = mqtt.Client()
# callback methods
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
# Connect to the broker
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
#Subscribe to administrative topics
# start the internal loop to process MQTT messages

mqtt_client.subscribe(MQTT_TOPIC)
mqtt_client.loop_start()

pygame.init()

WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

RED = (255, 0, 0)
BG_COLOR = (20, 200, 160)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption( 'TIC TAC TOE' )
screen.fill( BG_COLOR )

board = np.zeros( (BOARD_ROWS, BOARD_COLS) )



def draw_lines():
	
	pygame.draw.line( screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH )
	
	pygame.draw.line( screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH )

	pygame.draw.line( screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH )

	pygame.draw.line( screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH )

# player 1 = Circle O, player 2 = Cross X
def draw_figures():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == 1:
				pygame.draw.circle( screen, CIRCLE_COLOR, (int( col * SQUARE_SIZE + SQUARE_SIZE//2 ), int( row * SQUARE_SIZE + SQUARE_SIZE//2 )), CIRCLE_RADIUS, CIRCLE_WIDTH )
			elif board[row][col] == 2:
				pygame.draw.line( screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH )	
				pygame.draw.line( screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH )

def mark_square(row, col, player):
	board[row][col] = player

def available_square(row, col):
	return board[row][col] == 0

def is_board_full():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == 0:
				return False

	return True

def check_win(player):
	for col in range(BOARD_COLS):
		if board[0][col] == player and board[1][col] == player and board[2][col] == player:
			print_winner(player)
			draw_vertical_winning_line(col, player)
			return True

	for row in range(BOARD_ROWS):
		if board[row][0] == player and board[row][1] == player and board[row][2] == player:
			print_winner(player)
			draw_horizontal_winning_line(row, player)
			return True

	#Diagonal win:
	if board[2][0] == player and board[1][1] == player and board[0][2] == player:
		print_winner(player)
		draw_asc_diagonal(player)
		return True

	if board[0][0] == player and board[1][1] == player and board[2][2] == player:
		print_winner(player)
		draw_desc_diagonal(player)
		return True

	return False

"""
Maybe use this function to send to mqtt.
Ideas:
-At the beginning, define through mqtt who's player 1 & 2, from each round publish winner 1 || 2,  through mqtt add up score.
-Or keep track of the score locally, at the end of the dialogue publish the final results through mqtt, which forwards it to leaderboard database?
-Or maybe find a way to track score different than 1 || 2, by adding names. ( Can take a while)
"""
def print_winner(player):
	#data ={
	#		'winner' : player
	#		}
	#payload = json.dumps(data)
	#mqtt_client.publish(MQTT_TOPIC, payload=payload , qos=2)
	if player==1:
		print("Player 1 (O) has won the game")
	else:
		print("Player 2 (X) has won the game")


def draw_vertical_winning_line(col, player):
	posX = col * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (posX, 15), (posX, HEIGHT - 15), LINE_WIDTH )

def draw_horizontal_winning_line(row, player):
	posY = row * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (15, posY), (WIDTH - 15, posY), WIN_LINE_WIDTH )

def draw_asc_diagonal(player):
	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), WIN_LINE_WIDTH )

def draw_desc_diagonal(player):
	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), WIN_LINE_WIDTH )



draw_lines()

player = 1
game_over = False
if sys.argv[1] == "True" :
	clicked_last =  True
else: 
	clicked_col = False

# main loop
while True:
	
	#Gets the next move through MQTT - User cant play before mqtt move has been made.
	if clicked_last and MQTT_MOVES[0] != 9:
		if available_square( int(MQTT_MOVES[0]), int(MQTT_MOVES[1]) ):
			mark_square( int(MQTT_MOVES[0]), int(MQTT_MOVES[1]), int(MQTT_MOVES[2]) )
			draw_figures()
			clicked_last = False

			if check_win( player ):
				th = threading.Thread(target=winner.winner, args=(player,))
				th.start()
				game_over = True
			player = player % 2 + 1

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN and not game_over and not clicked_last:

			mouseX = event.pos[0] 
			mouseY = event.pos[1] 

			clicked_row = int(mouseY // SQUARE_SIZE)
			clicked_col = int(mouseX // SQUARE_SIZE)

			if available_square( clicked_row, clicked_col ):

				mark_square( clicked_row, clicked_col, player )
				
				# Send over mqtt clicked_row, clicked_col, player (?)
				data ={
					'row' : clicked_row,
					'col' : clicked_col,
					'play' : player
				}
				payload = json.dumps(data)
				mqtt_client.publish(MQTT_TOPIC, payload=payload, qos=2)
				clicked_last = True 

				draw_figures()

				
				if check_win( player ):
					th = threading.Thread(target=winner.winner, args=(player,))
					th.start()
					game_over = True
				player = player % 2 + 1


		# if not clicked_last:
		# 	print("Now listening?")
		# 	mqtt_client.subscribe(MQTT_TOPIC)


	pygame.display.update()
	#https://github.com/KenObie/mqtt-iot see for inspiration