# Vinz CLI AI-Assistant (VCAA)

A CLI AI Assistant using OpenAI API that provides command-line commands and hints based on user queries. Working on both MacOS and GNU/Linux.

## Features

- Interact with OpenAI's GPT models to get command-line instructions.
- Caches responses to avoid redundant API calls and save on usage.
- Easy installation and usage on MacOS and Linux.
- Configurable to use different GPT models.

## Prerequisites

- Python 3.6 or higher
- `pip` (Python package installer)
- OpenAI API key

## Installation

1. **Clone the Repository:**

   ```sh
   git clone https://github.com/your-username/vinz-cli-ai-assistant.git
   cd vinz-cli-ai-assistant
   ```

2. **Install Dependencies:**

   ```sh
   pip install openai
   ```

## Set Up Environment Variables:

Set your OpenAI API key as an environment variable:

   ```sh
   export OPENAI_API_KEY="your-api-key"
   ```


## Usage Examples

   ```sh
   python3 vinz_cli_ai_assistant.py
   ```

   ```
   > How do I list all files in the current directory?

   ANSWER:
   -------------
   ls
   ```

   ```
   > How do I view all running processes?

   ANSWER:
   -------------
   ps aux
   ```

   ```
   > How do I kill a process with a PID of 1234?

   ANSWER:
   -------------
   kill 1234
   ```

   ```
   > how do i upgrade my Ubuntu system?

   ANSWER:
   -------------
   sudo apt update
   sudo apt upgrade
   sudo apt dist-upgrade
   ```

   ```
   > i want to check if my MacOS is updated

   ANSWER:
   -------------
   softwareupdate -l
   ```

## Specify a MODEL, INSTALL, UNINSTALL

At the moment, Vinz CLI AI-Assistant is using OpenAI API to operate. You can only change the default model (gpt-3.5-turbo) by using the proper argument (--model). Or you can install the CLI Assistant as a shell command and invoke it easily by running "v" from your command line. Use the (--install) or (--uninstall) flags.

   ```sh
   python3 vinz_cli_ai_assistant.py --help

   usage: vinz_cli_ai_assistant.py [-h] [--model MODEL] [--install] [--uninstall]

   Run the Vinz CLI AI-Assistant (VCAA).

   optional arguments:
      -h, --help     show this help message and exit
      --model MODEL  The model to use for OpenAI API.
      --install      Install the script to /usr/local/bin.
      --uninstall    Uninstall the script from /usr/local/bin and clean up related files.

   ```

## CREDITS

Vinz CLI AI-Assistant is a tool developed and maintened by Vincenzo Ciaglia <vinciaglia@gmail.com>.