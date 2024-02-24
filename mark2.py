import json
import requests
import gradio as gr

def generate_completion(prompt):
    url = "https://9xnaul2qkfbbem-5000.proxy.runpod.net/v1/completions"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "prompt": prompt,
        "max_tokens": 2000,
        "temperature": 1,
        "top_p": 0.9,
        "seed": 10,
        "stream": True,
    }

    try:
        response = requests.post(url, headers=headers, json=data, verify=False, stream=True)
        response.raise_for_status()  # Raise HTTPError for bad responses

        result = data['prompt']

        for line in response.iter_lines(chunk_size=1):
            if line:
                # Remove the "data: " prefix
                line = line.decode('utf-8').lstrip('data: ')

                try:
                    payload = json.loads(line)
                    result += payload['choices'][0]['text']
                except json.JSONDecodeError as json_err:
                    print("JSON Decode Error:", json_err)

        return result

    except requests.exceptions.HTTPError as errh:
        return f"HTTP Error: {errh}"
    except requests.exceptions.ConnectionError as errc:
        return f"Error Connecting: {errc}"
    except requests.exceptions.Timeout as errt:
        return f"Timeout Error: {errt}"
    except requests.exceptions.RequestException as err:
        return f"Request Error: {err}"

iface = gr.Interface(fn=generate_completion, inputs="text", outputs="text")
iface.launch()
