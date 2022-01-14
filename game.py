import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from client import Network
import random
import os
pygame.font.init()

PLAYER_RADIUS = 10
START_VEL = 9
BALL_RADIUS = 5

W, H = 1600, 830

NAME_FONT = pygame.font.SysFont("comicsans", 20)
TIME_FONT = pygame.font.SysFont("comicsans", 30)
SCORE_FONT = pygame.font.SysFont("comicsans", 26)

COLORS = [(255,0,0), (255, 128, 0), (255,255,0), (128,255,0),(0,255,0),(0,255,128),(0,255,255),(0, 128, 255), (0,0,255), (0,0,255), (128,0,255),(255,0,255), (255,0,128),(128,128,128), (0,0,0)]

players = {}
balls = []

# FUNCTIONS
def convert_time(t):
	if type(t) == str:
		return t

	if int(t) < 60:
		return str(t) + "s"
	else:
		minutes = str(t // 60)
		seconds = str(t % 60)

		if int(seconds) < 10:
			seconds = "0" + seconds

		return minutes + ":" + seconds


def redraw_window(players, balls, game_time, score):
	WIN.fill((255,255,255)) # fill screen white, to clear old frames
	for ball in balls:
		pygame.draw.circle(WIN, ball[2], (ball[0], ball[1]), BALL_RADIUS)

	# draw each player in the list
	for player in sorted(players, key=lambda x: players[x]["score"]):
		p = players[player]
		pygame.draw.circle(WIN, p["color"], (p["x"], p["y"]), PLAYER_RADIUS + round(p["score"]))
		# render and draw name for each player
		text = NAME_FONT.render(p["name"], 1, (0,0,0))
		WIN.blit(text, (p["x"] - text.get_width()/2, p["y"] - text.get_height()/2))

	# draw scoreboard
	sort_players = list(reversed(sorted(players, key=lambda x: players[x]["score"])))
	title = TIME_FONT.render("Scoreboard", 1, (0,0,0))
	start_y = 25
	x = W - title.get_width() - 10
	WIN.blit(title, (x, 5))

	ran = min(len(players), 3)
	for count, i in enumerate(sort_players[:ran]):
		text = SCORE_FONT.render(str(count+1) + ". " + str(players[i]["name"]), 1, (0,0,0))
		WIN.blit(text, (x, start_y + count * 20))

	# draw time
	text = TIME_FONT.render("Time: " + convert_time(game_time), 1, (0,0,0))
	WIN.blit(text,(10,10))
	# draw score
	text = TIME_FONT.render("Score: " + str(round(score)),1,(0,0,0))
	WIN.blit(text,(10,15 + text.get_height()))

