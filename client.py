import threading
import socket

# Choosing Nickname
nickname = input('Enter your name: ')
if nickname =='admin':
   password =input ("Enter password for admin: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 59000))

stop_thread=False

# Listening to Server and Sending Nickname
def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
        
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('utf-8')
            if message == "NICK":
                client.send(nickname.encode('utf-8'))
                next_message= client.recv(1024).decode('utf-8')
                if next_message == 'PASS':
                   client.send(password.encode('utf-8'))
                   if client.recv(1024).decode('utf-8') == 'REFUSE':
                       print("connection was refused! wrong password!")
                       stop_thread=True 
                elif next_message == 'BAN':
                    print('Connection refused because of ban!')
                    client.close()
                    stop_thread=True                    
            else:
                print(message)
        except:
        
            # Close Connection When Error
            print('Error!')
            client.close()
            break

# Sending Messages To Server
def write():
    while True:
        if stop_thread:
            break      
        message = f'{nickname}:{input("")}'
        if message[len(nickname)+1:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname)+1:].startswith('/kick'):
                    client.send(f'KICK {message[len(nickname)+1+6:]}'.encode('utf-8'))
                elif message[len(nickname)+1:].startswith('/ban'):
                    client.send(f'BAN {message[len(nickname)+1+5:]}'.encode('utf-8'))
        
            else:
                print("Commands can only be executed by admin")    
        else:         
            client.send(message.encode('utf-8'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_thread = threading.Thread(target=write)
send_thread.start()
