import socket
import threading
import dframe as df
from threading import Thread
from dframe import *
import logging
import shutil
import time

lock = threading.Lock()

# Configure logging
logging.basicConfig(filename='voting.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def log_activity(message):
    threading.Thread(target=logging.info, args=(message,)).start()

def backup_data():
    while True:
        shutil.copy2('database/voterList.csv', 'backup/voterList_backup.csv')
        shutil.copy2('database/cand_list.csv', 'backup/cand_list_backup.csv')
        time.sleep(10)  # Backup every hour

def client_thread(connection):
    data = connection.recv(1024)  # Receiving voter details
    log_activity(f"Received voter details: {data.decode()}")

    # Verify voter details
    log = (data.decode()).split(' ')
    try:
        log[0] = int(log[0])

        if df.verify(log[0], log[1]):  # Authenticate
            if df.isEligible(log[0]):
                log_activity(f"Voter Logged in... ID: {log[0]}")
                connection.send("Authenticate".encode())
            else:
                log_activity(f"Vote Already Cast by ID: {log[0]}")
                connection.send("VoteCasted".encode())
        else:
            log_activity(f"Invalid Voter: {log[0]}")
            connection.send("InvalidVoter".encode())
            return

    except:
        log_activity("Invalid Credentials")
        connection.send("InvalidVoter".encode())
        return

    data = connection.recv(1024)  # Get Vote
    log_activity(f"Vote Received from ID: {log[0]} - Processing...")
    lock.acquire()
    # Update Database
    if df.vote_update(data.decode(), log[0]):
        log_activity(f"Vote Casted Successfully by voter ID = {log[0]}")
        connection.send("Successful".encode())
    else:
        log_activity(f"Vote Update Failed by voter ID = {log[0]}")
        connection.send("Vote Update Failed".encode())

    lock.release()
    connection.close()

def voting_Server():
    serversocket = socket.socket()
    host = socket.gethostname()
    port = 4001

    ThreadCount = 0

    try:
        serversocket.bind((host, port))
    except socket.error as e:
        print(str(e))
    print("Waiting for the connection")

    serversocket.listen(10)

    print("Listening on " + str(host) + ":" + str(port))

    while True:
        client, address = serversocket.accept()
        log_activity(f"Connected to: {address}")

        print('Connected to :', address)

        client.send("Connection Established".encode())  # 1
        t = Thread(target=client_thread, args=(client,))
        t.start()
        ThreadCount += 1

    serversocket.close()

if __name__ == '__main__':
    voting_Server()