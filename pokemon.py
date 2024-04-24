"""
Created on Wed Apr 24 13:21:44 2024

@author: Brent
"""
import pygame
import socket
import threading

def client_thread(conn, addr):
    print(f"Connected by {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            # Process data here (e.g., player moves)
            print(f"Received: {data.decode()}")
            response = "Data received"
            conn.sendall(response.encode())
    finally:
        conn.close()

def start_server():
    host = '0.0.0.0'
    port = 5555  # Port to listen on
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"Server started on {host}:{port}")
    
    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=client_thread, args=(conn, addr))
            thread.start()
    finally:
        server.close()


def play_music(file_path):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    
def game():
    while True:
        
        print("1. Fight\n2. Bag\n3. Pokeball\n4. Run")
        selection = int(input("Enter your selection: "))

        if selection == 1:
            print("You have selected fight.\n\nChoose the following options:")
            
            # Call function for the move list
        elif selection == 2:
            print("Your bag is empty")
        elif selection == 3:
            print("You can't capture another trainer's pokemon!")
        elif selection == 4:
            print("You cannot run away from a trainer battle")
        else:
            print("Bad selection. Try again!")


def movelist_gengar():
    while True:
        selection = int(input("1. Smog\n2. Shadowball\n3. Sludge bomb\n4. Thunderbolt\nEnter your selection: "))
        # Add actions based on selection


def movelist_nidorino():
    while True:
        selection = int(input("1. Horn attack\n2. Poison sting\n3. Double kick\n4. Peck\nEnter your selection: "))
        # Add actions based on selection


def waiting():
    print("Waiting for opponent's response...")


def main():
    print("Welcome to PokÃ©mon.\nClick any key to enter.")
    input()  # Wait for a key press
    file_path = "pokemon-red-and-blue-extended.mp3"
    play_music(file_path)
    game()  # Start the game
    




if __name__ == "__main__":
    start_server()
