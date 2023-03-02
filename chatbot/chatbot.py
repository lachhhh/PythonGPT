import openai
import tkinter as tk
from tkinter import font
import threading
import speech_recognition as sr
openai.api_key = "put key here"

def send_message():
    pass

def start_listening():
    pass

def stop_listening():
    pass

def update_chat_history(message):
    pass

# create the GUI window
root = tk.Tk()
root.title("chat but the bot is mentally disabled")
root.geometry("600x800")
root.config(bg="#333333")

# set up the chat history text widget
chat_history = tk.Text(root, bg="#1f1f1f", fg="#f1f1f1", width=70, height=20, font=("Helvetica", 12))
chat_history.pack(pady=20)

# set up the user input text widget
user_input = tk.Text(root, bg="#1f1f1f", fg="#f1f1f1", width=70, height=5, font=("Helvetica", 12))
user_input.pack()

# set up the send button
send_button = tk.Button(root, text="Send", bg="#1f1f1f", fg="#f1f1f1", font=("Helvetica", 12), command=send_message)
send_button.pack(pady=10)
def send_message():
    message = user_input.get("1.0", tk.END).strip()
    if message != "":
        user_input.delete("1.0", tk.END)
        update_chat_history("User: " + message)
        response = openai.Completion.create(
            engine="davinci",
            prompt=message,
            temperature=0.5,
            max_tokens=2048,
            n=1,
            stop=None,
            frequency_penalty=0,
            presence_penalty=0
        )
        update_chat_history("OpenAI: " + response.choices[0].text)
def update_chat_history(message):
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, message + "\n")
    chat_history.config(state=tk.DISABLED)
    t = threading.Thread(target=typing_effect, args=(message,))
    t.start()

def typing_effect(message):
    for char in message:
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, char)
        chat_history.see(tk.END)
        chat_history.config(state=tk.DISABLED)
        chat_history.update_idletasks()
        time.sleep(0.03)
import speech_recognition as sr

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

def stop_listening():
    pass

voice_input_button = tk.Button(root, text="Voice Input", bg="#1f1f1f", fg="#f1f1f1", font=("Helvetica", 12), command=start_listening)
voice_input_button.pack(pady=10)
def get_bot_response(user_input):
    response = openai.Completion.create(
        engine="davinci",
        prompt=user_input,
        temperature=0.5,
        max_tokens=50,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    message = response.choices[0].text.strip()
    return message 
root.mainloop()
