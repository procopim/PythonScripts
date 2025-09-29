#!/usr/bin/python3

from cryptography.fernet import Fernet
import os, json, sys

def store_secret(service_name, api_key ,fernet_obj):
    global STORE, KEY
    if service_name in STORE:
        raise ValueError("Service already exists")
    with open("secret_store.json","w") as secret_file:
        STORE[service_name] = fernet_obj.encrypt(api_key.encode()).decode() #string object
        json.dump(STORE, secret_file)
    print(f"Stored secret for {service_name}")
    return True

def retrieve_secret(service_name, fernet_obj):
    global STORE, KEY
    if service_name not in STORE:
        raise ValueError("Service not found")
    secret = fernet_obj.decrypt(STORE[service_name].encode()).decode() #returns string
    print(f"Retrieved secret for {service_name}: {secret}")
    return True

if __name__ == "__main__":
    #check if key was already generated
    if not os.path.exists("secret.key"):
        KEY = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(KEY)
        os.chmod("secret.key", 0o600) #read/write for owner only
    else:
        with open("secret.key", "rb") as key_file:
            KEY = key_file.read()
    #check if we have a json secret store already
    if os.path.exists("secret_store.json"):
        with open("secret_store.json", "rb") as secret_file:
            # STORE = secret_file.readlines()
            STORE = json.load(secret_file)
        os.chmod("secret.key", 0o600) #read/write for owner only
    else:
        STORE = {}
    if len(sys.argv) < 2:
        print("Usage: python keystore.py <store|retrieve> <service_name>")
        sys.exit(1)

    command = sys.argv[1]
    service_name = sys.argv[2]
    fernet_obj = Fernet(KEY)
    if command == "store":
        api_key = input(f"Enter API key for {service_name}: ")
        if not api_key:
            print("Usage: python keystore.py must have at least one character")
            sys.exit(1)
        try:
            store_secret(service_name, api_key, fernet_obj)
        except ValueError as ve:
            print(ve)
            sys.exit(1)
    elif command == "retrieve":
        try:
            retrieve_secret(service_name, fernet_obj)
        except ValueError as ve:
            print(ve)
            sys.exit(1)
    else:
        print("Invalid command")
        sys.exit(1)