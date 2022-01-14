import socket 
from _thread import * 
import _pickle as pickle 
import time 
import random 
import math 
 
S = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
 
PORT = 5555 
 
BALL_RADIUS = 5 
START_RADIUS = 7 
 
ROUND_TIME = 60 * 5 
 
MASS_LOSS_TIME = 7 
 
W, H = 1600, 830 
 
HOST_NAME = socket.gethostname() 
SERVER_IP = socket.gethostbyname(HOST_NAME) 
 
try: 
    S.bind((SERVER_IP, PORT)) 
except socket.error as e: 
    print(str(e)) 
    print("[SERVER] Server could not start") 
    quit() 
 
S.listen()  
 
print(f"[SERVER] Server Started with local ip {SERVER_IP}") 
