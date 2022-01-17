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

def collision(rleft, rtop, width, height,   
              center_x, center_y, radius): 
    """ Detect collision between a rectangle and circle. """

    rright, rbottom = rleft + width/2, rtop + height/2

    cleft, ctop     = center_x-radius, center_y-radius
    cright, cbottom = center_x+radius, center_y+radius

    if rright < cleft or rleft > cright or rbottom < ctop or rtop > cbottom:
        return False  

    for x in (rleft, rleft+width):
        for y in (rtop, rtop+height):
            if math.hypot(x-center_x, y-center_y) <= radius:
                return True  

    if rleft <= center_x <= rright and rtop <= center_y <= rbottom:
        return True  

    return False 

zones = []
zones.append(pygame.Rect((0, 0, W // 2 - 1, H // 2 - 1)))
zones.append(pygame.Rect((W // 2, 0, W // 2, H // 2)))

zones.append(pygame.Rect((0, H // 2, W // 2 - 1, H // 2 - 1)))
zones.append(pygame.Rect((W // 2, H // 2, W // 2 - 1, H // 2 - 1)))

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


def redraw_window(players, balls, game_time, score, zone, local):
	WIN.fill((255,255,255)) # fill screen white, to clear old frames
	for ball in balls:
		pygame.draw.circle(WIN, ball[2], (ball[0], ball[1]), BALL_RADIUS)

	# draw each player in the list
	for player in sorted(players, key=lambda x: players[x]["score"]):
		p = players[player]
			if p == local:
			pygame.draw.circle(WIN, p["color"], (p["x"], p["y"]), PLAYER_RADIUS + round(p["score"]))
            # render and draw name for each player
			text = NAME_FONT.render(p["name"], 1, (0,0,0))
			WIN.blit(text, (p["x"] - text.get_width()/2, p["y"] - text.get_height()/2))
		else:
			if not "zone" in p:
				p["zone"] = 0
            
			if p["zone"] == zone:
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
def main(name):
	global players

	server = Network()
	current_id = server.connect(name)
	balls, players, game_time = server.send("get")

	clock = pygame.time.Clock()

	run = True
	while run:
		clock.tick(30) # 30 fps max
		player = players[current_id]
		vel = START_VEL - round(player["score"]/14)
		if vel <= 1:
			vel = 1

		keys = pygame.key.get_pressed()

		data = ""
		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			if player["x"] - vel - PLAYER_RADIUS - player["score"] >= 0:
				player["x"] = player["x"] - vel

		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			if player["x"] + vel + PLAYER_RADIUS + player["score"] <= W:
				player["x"] = player["x"] + vel

		if keys[pygame.K_UP] or keys[pygame.K_w]:
			if player["y"] - vel - PLAYER_RADIUS - player["score"] >= 0:
				player["y"] = player["y"] - vel

		if keys[pygame.K_DOWN] or keys[pygame.K_s]:
			if player["y"] + vel + PLAYER_RADIUS + player["score"] <= H:
				player["y"] = player["y"] + vel
						for i in range(len(zones)):
		if collision(zones[i].x,
				zones[i].y, zones[i].width, zones[i].height, player["x"], player["y"], PLAYER_RADIUS + round(player["score"])):
				player["zone"] = i
                
		if not "zone" in player:
			player["zone"] = 0
				

		data = "move " + str(player["x"]) + " " + str(player["y"]) + " " + str(player["zone"])

		balls, players, game_time = server.send(data)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					run = False


		redraw_window(players, balls, game_time, player["score"], player["zone"], player)
		pygame.display.update()


	server.disconnect()
	pygame.quit()
	quit()


while True:
 	name = input("Please enter your name: ")
 	if  0 < len(name) < 20:
 		break
 	else:
 		print("Error, this name is not allowed (must be between 1 and 19 characters [inclusive])")

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)

# setup pygame window
WIN = pygame.display.set_mode((W,H))
pygame.display.set_caption("Blobs")

main(name)
