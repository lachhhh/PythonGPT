import openai
import tkinter as tk
import threading
import time
import speech_recognition as sr
import pyttsx3
import atexit

# Initialize the engine
engine = pyttsx3.init()

chatlog = []

def save_chatlog():
    with open("chatlog.txt", "w") as file:
        for line in chatlog:
            file.write(line + "\n")

def log_message(message):
    chatlog.append(message)

atexit.register(save_chatlog)



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
    log_message(message)




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

def login():
    # create a new toplevel window for login
     login_window = tk.Toplevel(root)
    
    # add login widgets to the window
     tk.Label(login_window, text="Username").grid(row=0, column=0)
     username_entry = tk.Entry(login_window)
     username_entry.grid(row=0, column=1)
    
     tk.Label(login_window, text="Password").grid(row=1, column=0)
     password_entry = tk.Entry(login_window, show="*")
     password_entry.grid(row=1, column=1)
    
def submit_login():
        # store the login credentials and close the window
        username = username_entry.get()
        password = password_entry.get()
        # do some validation and check credentials against database, etc.
        login_window.destroy()
        
        # update the menu to include options for logged-in users
        logged_in_menu = tk.Menu(menu_bar, tearoff=0)
        logged_in_menu.add_command(label="Profile")
        logged_in_menu.add_command(label="Logout", command=logout)
        menu_bar.add_cascade(label="Logged In", menu=logged_in_menu)
        menu_bar.delete("Login")
    
        tk.Button(login_window, text="Submit", command=submit_login).grid(row=2, column=1)

def logout():
    # remove the logged-in menu and add back the login option
    menu_bar.delete("Logged In")
    menu_bar.add_command(label="Login", command=login)

    root = tk.Tk()

# create the main menu bar
    menu_bar = tk.Menu(root)

# add some initial options
    

# add the login option
    menu_bar.add_command(label="Login", command=login)

# display the menu bar
    root.config(menu=menu_bar)
root.mainloop()
menu_bar.mainloop()
with open('chat_log.txt', 'w') as f:
    for item in chat_log:
        f.write("%s\n" % item)
print(chatlog)
