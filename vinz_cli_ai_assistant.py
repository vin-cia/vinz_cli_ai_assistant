import openai
import os
import time
import shelve
import argparse
from typing import Optional

# Initialize the OpenAI client
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set. Please set it before running the script.")
    
client = openai.OpenAI(api_key=api_key)

CACHE_FILE = "vcaa_cache"

RED_BOLD = "\033[1;31m"
YELLOW_BOLD = "\033[1;33m"
GREEN = "\033[1;32m"
BOLD = "\033[1m"
RESET = "\033[0m"

def get_answer_from_openai(question: str, cache: shelve.DbfilenameShelf, model: str) -> Optional[str]:
    """
    Fetches the answer for the given question from OpenAI API or cache.

    Args:
        question (str): The question to ask OpenAI.
        cache (shelve.DbfilenameShelf): The cache to store and retrieve answers.
        model (str): The model to use for OpenAI API.

    Returns:
        Optional[str]: The answer from OpenAI or None in case of an error.
    """
    if question in cache:
        return cache[question]

    messages = [
        {"role": "system", "content": "Assume that all commands will be run on a MacOS or Linux system."},
        {"role": "user", "content": "Only respond with code as plain text without code block syntax around it"},
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

def handle_question(question: str, model: str) -> Optional[str]:
    """
    Handle the question by getting the answer from OpenAI or cache.

    Args:
        question (str): The question to ask OpenAI.
        model (str): The model to use for OpenAI API.

    Returns:
        Optional[str]: The answer from OpenAI or None in case of an error.
    """
    with shelve.open(CACHE_FILE) as cache:
        return get_answer_from_openai(question, cache, model)

def main():
    """
    Main function to run the Vinz CLI AI-Assistant (VCAA).
    """
    parser = argparse.ArgumentParser(description="Run the Vinz CLI AI-Assistant (VCAA).")
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo', help='The model to use for OpenAI API.')

    args = parser.parse_args()

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

            answer = handle_question(question, args.model)
            if answer:
                print(f"\n{RED_BOLD}ANSWER:\n-------------\n{YELLOW_BOLD}{answer}\n{RESET}")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting Vinz CLI AI-Assistant (VCAA). Bye!")
            break

if __name__ == "__main__":
    main()
