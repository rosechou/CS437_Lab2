import socket
# import picar_4wd as fc
import time
import random
import os
import subprocess
import json

# HOST = "192.168.0.171" # IP address of your Raspberry PI
HOST = "0.0.0.0" # IP address of your Raspberry PI
PORT = 11111          # Port to listen on (non-privileged ports are > 1023)

speed = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)

            d = {}
            
            data = client.recv(1024)
            data = str(data)[1:].strip('\'')
            # print(data)
            # Action for Submit Button
            if(data[0] == "S"): 
                # ===== Display what in Textbox =====
                print(data)# receive 1024 Bytes of message in binary format
                d["bluetooth"] = data[1:]

            # Action for Motor Control
            # TODO
            if(data[0] == "C"):
                d["startTime"] = time.time()
                print("Action for Motor Control")
                print(data[1])
                speed = 10

                if data[1] == "f":
                    # fc.forward(speed)
                    d["direction"] = "forward"
                    print("forward")
                elif data[1] == "b":
                    # fc.backward(speed)
                    d["direction"] = "backward"
                    print("backward")
                elif data[1] == "l":
                    # fc.turn_right(speed)
                    d["direction"] = "turn left"
                    print("turn left")
                elif data[1] == "r":
                    # fc.turn_left(speed)
                    d["direction"] = "turn right"
                    print("turn right")
                
            if(data == "!STOP"):
                print("Stop Motor Control")
                speed = 0
                d["direction"] = ""
                d["endTime"] = time.time()
                # fc.stop()

            d["speed"] = speed
            # ===== Temperature Section =========
            # TODO
            # temp = subprocess.run(['vcgencmd', 'measure_temp'], stdout = subprocess.PIPE)
            # temp = "T" + str(temp.stdout)
            d["temp"] = "55'C"
            # print(temp)


            # if data != b"":
            #     data = "B" + str(data)
            #     print(type(data))     
            #     client.sendall(bytes(data, 'utf-8'))
            #     data = data[1:]

            
            # client.sendall(bytes(data+temp, 'utf-8'))
            client.sendall( bytes(json.dumps(d), 'utf-8') )
            # Echo back to client
    except: 
        print("Closing socket")
        client.close()
        s.close()
   
