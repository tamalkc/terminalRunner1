
import subprocess
# import re
from openai import OpenAI

# Configure OpenAI client to use the local LM Studio server
client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")

# function to take a prompt and ask ai to convert to a terminal command
SYSTEM_PROMPT = "You are an expert in using the terminal on Linux-based operating systems. Your task is to translate the user's natural language instructions into the most appropriate and correct terminal command. Output only the terminal command, ready to be executed. Do not include explanations, suggestions, or any additional text. DO NOT include any other symbol or character other than required in the shell command. If the instruction is ambiguous or incomplete, respond with the command as best as possible based on the given information, without asking for clarification."
messages = [
    {"role": "user", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "Create a new directory named 'projects' in my current location."},
    {"role": "assistant", "content": "mkdir projects"},
    {"role": "user", "content": "List all the files in the current directory with detailed information."},
    {"role": "assistant", "content": "ls -l"},
    {"role": "user", "content": "Find all files ending with '.txt' in the 'documents' folder."},
    {"role": "assistant", "content": "find documents -name \'*.txt\'"},
    {"role": "user", "content": "Remove the file named 'old_file.txt'."},
    {"role": "assistant", "content": "rm old_file.txt"},
    {"role": "user", "content": "Create an empty file named 'notes.md'."},
    {"role": "assistant", "content": "touch notes.md"},
]

def convert_to_command(prompt):
    messages.append({"role": "user", "content": prompt})
    # print("Messages:",messages)
    response = client.chat.completions.create(
        # model="deepseek-r1-distill-qwen-7b",
        model="mistral-7b-instruct-v0.3",
        messages=messages,
        max_tokens=18,
        temperature=0.3
    )   

    content = response.choices[0].message.content.strip()

    # remove $$ from response eg: response=sometext$$ change it to sometext without using import re
    content = content.replace("$$", "")

    # if content contains \n then remove it and anything after it
    if "\n" in content:
        content = content[:content.index("\n")]
    
    # content = content.replace("\n", "")
    
    # content = re.sub(r'\n', '', content)
    # content = re.sub(r'$$', '', content)
    # print("Response:",content)
    messages.append({"role": "assistant", "content": content})
    return content

def run_command(command):
    """Runs a terminal command and prints the output."""
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if stdout:
            print("Command Output:")
            print(stdout)
        if stderr:
            print("📍2 Command Error:")
            print(stderr)
        return process.returncode
    except FileNotFoundError:
        print(f"📍3 Error: Command not found: {command}")
        return 1
    except Exception as e:
        print(f"📍4 An error occurred: {e}")
        return 1

if __name__ == "__main__":
    while True:
        prompt = input("Enter a prompt (or 'exit' to quit): ")
        if prompt.lower() == 'exit' or prompt.lower() == 'quit':
            break

        command = convert_to_command(prompt)    
        print("Command:",command)
        return_code = run_command(command)
        if return_code == 0:
            print("Command executed successfully.")
        else:
            print(f"📍5 Command failed with return code: {return_code}")
        


