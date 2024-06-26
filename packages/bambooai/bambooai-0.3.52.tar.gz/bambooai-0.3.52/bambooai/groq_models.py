import os
import time
from groq import Groq
import tiktoken

try:
    # Attempt package-relative import
    from . import output_manager
except ImportError:
    # Fall back to script-style import
    import output_manager

output_manager = output_manager.OutputManager()

def init():
    API_KEY = os.environ.get('GROQ_API_KEY')
    if API_KEY is None:
        output_manager.print_wrapper("Warning: GROQ_API_KEY environment variable not found.")
        return
    else:
        client = Groq()
        client.api_key = API_KEY
        return client

def llm_call(messages: str,model: str,temperature: str,max_tokens: str):  

    client = init()

    start_time = time.time()

    response = client.chat.completions.create(
        model=model, 
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    end_time = time.time()

    elapsed_time = end_time - start_time

    content = response.choices[0].message.content.strip()
    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens
    total_tokens = response.usage.total_tokens

    prompt_tokens_used = prompt_tokens
    completion_tokens_used = completion_tokens
    total_tokens_used = total_tokens
    if elapsed_time > 0:
        tokens_per_second = completion_tokens_used / elapsed_time
    else:
        tokens_per_second = 0

    return content, messages, prompt_tokens_used, completion_tokens_used, total_tokens_used, elapsed_time, tokens_per_second

def llm_stream(log_and_call_manager, chain_id: str, messages: str,model: str,temperature: str,max_tokens: str, tools: str = None):  

    collected_chunks = []
    collected_messages = []

    client = init()

    response = client.chat.completions.create(
        model=model, 
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream =True,
    )

    start_time = time.time()
    for chunk in response:
        collected_chunks.append(chunk)
        if chunk.choices[0].delta.content is not None:
            chunk_message = chunk.choices[0].delta.content
            collected_messages.append(chunk_message)
            output_manager.print_wrapper(chunk_message, end='', flush=True)  

    end_time = time.time()
    elapsed_time = end_time - start_time

    output_manager.print_wrapper("")

    full_reply_content = ''.join([m for m in collected_messages])

    # count the number of response tokens used
    completion_tokens_used = len(collected_chunks)

    # count the number of prompt tokens used
    encoding = tiktoken.encoding_for_model("gpt-4")   
    tokens_per_message = 3
    tokens_per_name = 1
    prompt_tokens_used = 0
    for message in messages:
        prompt_tokens_used += tokens_per_message
        for key, value in message.items():
            prompt_tokens_used += len(encoding.encode(value))
            if key == "name":
                prompt_tokens_used += tokens_per_name
    prompt_tokens_used += 3  # every reply is primed with <|start|>assistant<|message|>

    # calculate the total tokens used
    total_tokens_used = prompt_tokens_used + completion_tokens_used
    
    if elapsed_time > 0:
        tokens_per_second = completion_tokens_used / elapsed_time
    else:
        tokens_per_second = 0

    return full_reply_content, messages, prompt_tokens_used, completion_tokens_used, total_tokens_used, elapsed_time, tokens_per_second