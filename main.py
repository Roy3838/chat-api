
import subprocess
import json
import argparse
import os

def load_settings():
    with open('settings.json', 'r') as file:
        settings = json.load(file)
    return settings

def stream_response(base_url, model, conversation, temperature, debug):
    data = {
        "model": model,
        "messages": conversation,
        "temperature": temperature,
        "max_tokens": -1,
        "stream": True
    }

    command = [
        'curl', '-N', f'{base_url}/chat/completions',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps(data)
    ]
    
    if debug:
        print(f"Debug: Running command: {' '.join(command)}")

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

    print("Assistant: ", end="", flush=True)
    collected_response = ""
    try:
        while True:
            line = process.stdout.readline()
            if not line:
                break
            if debug:
                print(f"Debug: Received line: {line.strip()}")
            if line.startswith("data: "):
                line_content = line[len("data: "):].strip()
                if line_content == "[DONE]":
                    break
                if line_content:
                    try:
                        response_data = json.loads(line_content)
                        if debug:
                            print(f"Debug: Parsed JSON: {response_data}")
                        if "choices" in response_data and "delta" in response_data["choices"][0]:
                            word = response_data["choices"][0]["delta"].get("content", "")
                            collected_response += word
                            print(word, end="", flush=True)
                    except json.JSONDecodeError as e:
                        if debug:
                            print(f"Debug: JSONDecodeError: {e}")
                            print(f"Debug: Failed line content: {line_content}")
                        continue
        print()  # New line after the response is complete
    except KeyboardInterrupt:
        process.kill()
    
    return collected_response

def main():
    settings = load_settings()

    parser = argparse.ArgumentParser(description='OpenAI Chat Client')
    parser.add_argument('--base_url', type=str, default=settings.get('base_url'), help='Base URL of the OpenAI server')
    parser.add_argument('--model', type=str, default=settings.get('model'), help='Model to use for the completion')
    parser.add_argument('--system_message', type=str, default=settings.get('system_message'), help='System message to set the behavior of the assistant')
    parser.add_argument('--temperature', type=float, default=settings.get('temperature'), help='Temperature for the completions')
    parser.add_argument('--debug', action='store_true', default=settings.get('debug'), help='Enable debug output')

    args = parser.parse_args()

    conversation = [{"role": "system", "content": args.system_message}]

    print("Chat Client initialized. Type 'exit' to quit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        conversation.append({"role": "user", "content": user_input})

        reply = stream_response(args.base_url, args.model, conversation, args.temperature, args.debug)
        conversation.append({"role": "assistant", "content": reply})

if __name__ == '__main__':
    main()
