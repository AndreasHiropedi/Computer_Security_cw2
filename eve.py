import os
import sys
import argparse
from common import *
from const import *

# create argument parser and add all possible flags
arguments_parser = argparse.ArgumentParser()
arguments_parser.add_argument("--relay", help="Relay message from Bob to Alice.", action="store_true")
arguments_parser.add_argument("--break-heart", help="End Alice and Bob's relationship.", action="store_true")
arguments_parser.add_argument("--custom", help="Send custom messages.", action="store_true")

# parse the arguments
arguments = arguments_parser.parse_args()

# check correct number of arguments was provided
if len(sys.argv) != 2:
    print("Incorrect number of arguments provided!")
    sys.exit(1)

# output appropriate message based on given flag
if arguments.relay:
    print("EVE IS ON RELAY MODE.")
elif arguments.break_heart:
    print("EVE IS ON BREAK HEART MODE.")
elif arguments.custom:
    print("EVE IS ON CUSTOM MODE.")

print('|||||||||||||||||||||||||||||||||||||||||||||||||||||||||')
dialog = Dialog('print')

# socket for pretending to be bob
print('PRETENDING TO BE BOB...')
bob_socket, bob_aes = setup('bob', BUFFER_DIR, BUFFER_FILE_NAME)
os.rename(BUFFER_DIR + BUFFER_FILE_NAME, BUFFER_DIR + "different_buffer")
print('SOCKET FOR COMMUNICATING WITH BOB ESTABLISHED!')

# socket for pretending to be alice
print('PRETENDING TO BE ALICE...')
alice_socket, alice_aes = setup('alice', BUFFER_DIR, BUFFER_FILE_NAME)
print('SOCKET FOR COMMUNICATING WITH ALICE ESTABLISHED!')

message_from_bob = receive_and_decrypt(alice_aes, alice_socket)

# relay is the flag
if arguments.relay:

    encrypt_and_send(message_from_bob, bob_aes, bob_socket)
    dialog.chat('Bob said: "{}"'.format(message_from_bob))

    dialog.info('Message sent! Waiting for reply...')
    message_from_alice = receive_and_decrypt(bob_aes, bob_socket)

    dialog.chat('Alice said: "{}"'.format(message_from_alice))

    encrypt_and_send(message_from_alice, alice_aes, alice_socket)

# break_heart is the flag
elif arguments.break_heart:
    
    # Make Bob send BAD_MSG to Alice
    bob_bad_message = BAD_MSG['bob'] 
    encrypt_and_send(bob_bad_message, bob_aes, bob_socket)
    dialog.chat('Bob said: "{}"'.format(bob_bad_message))

    dialog.info('Message sent! Waiting for reply...')
    message_from_alice = receive_and_decrypt(bob_aes, bob_socket)
    dialog.chat('Alice said: "{}"'.format(message_from_alice))
    encrypt_and_send(message_from_alice, alice_aes, alice_socket)

# custom is the flag
elif arguments.custom:
    
    dialog.chat('Bob said: "{}"'.format(message_from_bob))

    # Allow the user to alter Bob's message
    dialog.prompt('Input what you would like Bob to say to Alice')
    bob_new_message = input()
    encrypt_and_send(bob_new_message, bob_aes, bob_socket)

    dialog.info('Message sent! Waiting for reply...')
    message_from_alice = receive_and_decrypt(bob_aes, bob_socket)
    dialog.chat('Alice said: "{}"'.format(message_from_alice))

    # Allow the user to alter Alice's message
    dialog.prompt('Input what you would like Alice to say to Bob')
    alice_new_message = input()
    encrypt_and_send(alice_new_message, alice_aes, alice_socket)

# close alice and bob's sockets
tear_down(alice_socket, BUFFER_DIR,BUFFER_FILE_NAME)
tear_down(bob_socket, BUFFER_DIR,"different_buffer" )
