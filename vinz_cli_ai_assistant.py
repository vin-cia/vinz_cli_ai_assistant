#!/usr/bin/env python3

import openai
import os
import time
import shelve
import argparse
import shutil
from typing import Optional

# Constants
CACHE_FILE = "vcaa_cache"
INSTALL_PATH = "/usr/local/bin/v"

RED_BOLD = "\033[1;31m"
YELLOW_BOLD = "\033[1;33m"
GREEN = "\033[1;32m"
BOLD = "\033[1m"
RESET = "\033[0m"


def get_answer_from_openai(question: str, cache: shelve.DbfilenameShelf, model: str, client) -> Optional[str]:
    """
    Fetches the answer for the given question from OpenAI API or cache.

    Args:
        question (str): The question to ask OpenAI.
        cache (shelve.DbfilenameShelf): The cache to store and retrieve answers.
        model (str): The model to use for OpenAI API.
        client: The OpenAI client.

    Returns:
        Optional[str]: The answer from OpenAI or None in case of an error.
    """
    if question in cache:
        return cache[question]

    messages = [
        {"role": "system", "content": "Assume that all commands will be run on a MacOS or Linux system."},
        {"role": "user", "content": "Only respond with an answer if the question has to do with Unix and Shell "
                                    "scripting and if related do it with code as plain text without code block syntax "
                                    "around it"},
        {"role": "user", "content": question}
    ]

    while True:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
            )
            answer = response.choices[0].message.content.strip()
            cache[question] = answer  # Save to cache
            return answer
        except openai.RateLimitError:
            print("Rate limit exceeded. Retrying after 60 seconds...")
            time.sleep(60)
        except openai.OpenAIError as e:
            print(f"OpenAI API Error: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None


def handle_question(question: str, model: str, client) -> Optional[str]:
    """
    Handle the question by getting the answer from OpenAI or cache.

    Args:
        question (str): The question to ask OpenAI.
        model (str): The model to use for OpenAI API.
        client: The OpenAI client.

    Returns:
        Optional[str]: The answer from OpenAI or None in case of an error.
    """
    with shelve.open(CACHE_FILE) as cache:
        return get_answer_from_openai(question, cache, model, client)


def install_script():
    """
    Install the script in /usr/local/bin to make it executable as a normal shell command.
    """
    script_path = os.path.abspath(__file__)
    target_path = INSTALL_PATH

    # Copy the script to /usr/local/bin
    try:
        shutil.copy(script_path, target_path)
        # Make the script executable
        os.chmod(target_path, 0o755)
        print(f"Script has been installed to {target_path} and is now executable as 'v'.")
    except PermissionError:
        print("Permission denied: You need to run the install command with sudo.")
    except Exception as e:
        print(f"An error occurred during installation: {e}")


def uninstall_script():
    """
    Uninstall the script from /usr/local/bin and clean up related files.
    """
    try:
        if os.path.exists(INSTALL_PATH):
            os.remove(INSTALL_PATH)
            print(f"Script has been removed from {INSTALL_PATH}.")
        else:
            print(f"Script not found at {INSTALL_PATH}.")

        if os.path.exists(CACHE_FILE):
            os.remove(CACHE_FILE)
            print(f"Cache file {CACHE_FILE} has been removed.")
        else:
            print(f"Cache file {CACHE_FILE} not found.")
    except PermissionError:
        print("Permission denied: You need to run the uninstall command with sudo.")
    except Exception as e:
        print(f"An error occurred during uninstallation: {e}")


def main():
    """
    Main function to run the Vinz CLI AI-Assistant (VCAA).
    """
    parser = argparse.ArgumentParser(description="Run the Vinz CLI AI-Assistant (VCAA).")
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo', help='The model to use for OpenAI API.')
    parser.add_argument('--install', action='store_true', help='Install the script to /usr/local/bin.')
    parser.add_argument('--uninstall', action='store_true',
                        help='Uninstall the script from /usr/local/bin and clean up related files.')

    args = parser.parse_args()

    if args.install:
        install_script()
        return

    if args.uninstall:
        uninstall_script()
        return

    # Initialize the OpenAI client
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("The OPENAI_API_KEY environment variable is not set. Please set it before running the script.")

    client = openai.OpenAI(api_key=api_key)

    print("")
    print(f"{GREEN}{BOLD}************************************************")
    print("*                                              *")
    print("*  Welcome to Vinz CLI AI-Assistant (VCAA).    *")
    print("*  Ask a question about an operation you want  *")
    print("*  to perform, and I'll provide the command(s).*")
    print("*                                              *")
    print("************************************************")
    print(f"{RESET}")

    while True:
        try:
            question = input("> ").strip()
            if question.lower() in ["exit", "quit"]:
                print("Exiting Vinz CLI AI-Assistant (VCAA). Bye!")
                break

            if not question:
                continue

            answer = handle_question(question, args.model, client)
            if answer:
                print(f"\n{RED_BOLD}ANSWER:\n-------------\n{YELLOW_BOLD}{answer}\n{RESET}")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting Vinz CLI AI-Assistant (VCAA). Bye!")
            break


if __name__ == "__main__":
    main()
