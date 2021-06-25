import os
from time import sleep

f = open("./commands.txt", "r")
command = True
while(command):
    command = f.readline()[:-1]
    command = command.replace("'", "'\"'\"'")
    os.system("mosquitto_pub -h localhost -p 8888 -t led/wemos17/action -m " + "'" + command + "'")
    sleep(2)
f.close()
