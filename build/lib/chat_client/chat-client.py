
import subprocess
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description='OpenAI Chat Client')
    parser.add_argument('--base_url', type=str, required=True, help='Base URL of the OpenAI server')
    parser.add_argument('--model', type=str, required=True, help='Model to use for the completion')
    parser.add_argument('--system_message', type=str, default="You are a helpful assistant.", help='System message to set the behavior of the assistant')
    parser.add_argument('--temperature', type=float, default=0.7, help='Temperature for the completions')

    args = parser.parse_args()

    conversation = [{"role": "system", "content": args.system_message}]

    print("Chat Client initialized. Type 'exit' to quit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        conversation.append({"role": "user", "content": user_input})
        
        data = {
            "model": args.model,
            "messages": conversation,
            "temperature": args.temperature,
            "max_tokens": -1,
            "stream": False
        }
        
        result = subprocess.run([
            'curl', f'{args.base_url}/chat/completions',
            '-H', 'Content-Type: application/json',
            '-d', json.dumps(data)
        ], capture_output=True, text=True)
        
        response = json.loads(result.stdout)
        reply = response['choices'][0]['message']['content']
        print(f"Assistant: {reply}")
        conversation.append({"role": "assistant", "content": reply})

if __name__ == '__main__':
    main()
