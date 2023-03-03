import openai
import tkinter as tk
import threading
import time
import speech_recognition as sr
import pyttsx3

# Initialize the engine
engine = pyttsx3.init()


openai.api_key = ('')
def gpt3_completion(prompt, engine='text-davinci-002', temp=0.7, top_p=1.0, tokens=400, freq_pen=0.0, pres_pen=0.0, stop=['JAX:', 'USER:']):
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=0.7,
        max_tokens=2000,
        top_p=top_p,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop)
    text = response['choices'][0]['text'].strip()
    return text


def send_message():
    # Get the user's message
    message = user_input.get()
    user_input.delete(0, tk.END)

    # Add the user's message to the conversation history
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "User: " + message + "\n")
    chat_history.config(state=tk.DISABLED)

    # Add the conversation history to the prompt
    conversation = chat_history.get("1.0", tk.END)
    prompt = ('The following is a conversation between USER and the Chatbot.<<BLOCK>>')
    prompt = prompt + '\nJAX:' + conversation

    # Get the chatbot's response using OpenAI GPT-3
    chatbot_response = gpt3_completion(prompt)

    engine.say(chatbot_response)
    engine.runAndWait()

    # Check if the response is off-topic
    if "I'm sorry, I don't understand" in chatbot_response:
        chatbot_response = "I'm sorry, I don't understand. Let's talk about something else."

    # Add the chatbot's response to the conversation history
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "Chatbot: " + chatbot_response + "\n")
    chat_history.config(state=tk.DISABLED)


def start_listening():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print('Listening...')
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio)
        user_input.delete(0, tk.END)
        user_input.insert(tk.END, query)
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        pass

    # Automatically send the message
    send_message()

    # Call the function again to listen for another message
    threading.Thread(target=start_listening).start()
root = tk.Tk()
root.title("Lach's chatbot")
root.geometry("600x800")
root.config(bg="#333333")

# set up the chat history text widget
chat_history = tk.Text(root, bg="#1f1f1f", fg="#f1f1f1", width=70, height=20, font=("Helvetica", 12))
chat_history.pack(pady=20)

# set up the user input text widget
user_input = tk.Entry(root, bg="#1f1f1f", fg="#f1f1f1", width=70, font=("Helvetica", 12))
user_input.pack()

# set up the send button
send_button = tk.Button(root, text="Send", bg="#1f1f1f", fg="#f1f1f1", font=("Helvetica", 12), command=send_message)
send_button.pack(pady=10)

# set up the voice input button
voice_input_button = tk.Button(root, text="Voice Input", bg="#1f1f1f", fg="#f1f1f1", font=("Helvetica", 12), command=start_listening)
voice_input_button.pack(pady=10)
def save_prompt():
    prompt = chat_history.get("1.0", tk.END)
    with open("prompt.txt", "w") as f:
        f.write(prompt)
    chat_history.delete("1.0", tk.END)
    chat_history.insert(tk.END, "Prompt saved successfully.")

def send_message():
    # Get the user's message
    message = user_input.get()
    user_input.delete(0, tk.END)

    # Add the user's message to the conversation history
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "User: " + message + "\n")
    chat_history.config(state=tk.DISABLED)

    # Add the conversation history to the prompt
    conversation = chat_history.get("1.0", tk.END)
    prompt = ('The following is a conversation between USER and the Chatbot.<<BLOCK>>')
    prompt = prompt + '\nJAX:' + conversation

    # Get the chatbot's response using OpenAI GPT-3
    chatbot_response = gpt3_completion(prompt)

    # Check if the response is off-topic
    if "I'm sorry, I don't understand" in chatbot_response:
        chatbot_response = "I'm sorry, I don't understand. Let's talk about something else."

    # Add the chatbot's response to the conversation history
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "Chatbot: " + chatbot_response + "\n")
    chat_history.config(state=tk.DISABLED)
root.mainloop()
