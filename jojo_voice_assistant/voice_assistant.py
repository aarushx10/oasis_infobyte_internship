import tkinter as tk
import customtkinter as ctk
from PIL import Image,ImageTk
import speech_recognition as sr
import wikipedia
import datetime
import pyttsx3
import os , sys
import smtplib
# from email.message import EmailMessage
from constant import GEMINI_API_KEY,WEATHER_FORECAST_API_KEY
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import webbrowser
import google.generativeai as genai
import pycountry
import threading


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

jojo_thread = None
jojo_running = False
stop_jojo_flag = False

root = ctk.CTk()
ctk.set_appearance_mode("system")
root.geometry("200x200")
root.iconbitmap(resource_path("D:\\visual code\\oasis_infotech_fellowship\\Jojo_voice_assistant\\voice_assistant_icon.ico"))
root.title("Jojo")
content_frame = ctk.CTkFrame(master=root)
content_frame.pack(pady=10,fill="both",expand=True)
output_text = ctk.CTkLabel(master=content_frame,text="Say something to JOJO....",font=("Arial",14))
output_text.pack(pady=20)

engine = pyttsx3.init()  # Start the pyttsx3 engine

def speak(text):
    # print(text)
    output_text.configure(text=text)
    root.update_idletasks() #process layout changes
    label_height = output_text.winfo_height()
    content_height = label_height + 200 #add padding for frame and button
    root.geometry(f"400x{content_height}")
    root.update() #force gui to print text on gui
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Choose a voice (1 = female, 0 = male)
    engine.say(text)  # Tell the engine what to say
    engine.runAndWait()  # Make the engine speak

"""or you can use this code
from pydub.playback import play
from pydub import AudioSegment

def speak(text):
    tts = gtts.gTTS(text,lan='en')
    tts.save("output.wav")
    audio = AudioSegment.from_file("output.wav")
    os.remove("output.wav")
    audio = audio.speedup(playback_speed=1.5)
    play(audion)
"""
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
            output_text.configure(text="Listening...")
            root.update_idletasks()
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
    try:
        output_text.configure(text="Recognizing...")
        root.update_idletasks()
        query = r.recognize_google(audio, language="en-IN")
        output_text.configure(text=f"YOU SAID: {query}")

        if "stop jojo".lower() in query.lower() or "jojo stop".lower() in query.lower() or "exit".lower() in query.lower() or "goodbye".lower() in query.lower():
            speak("Goodbye! Have a great day!")
            stop_program = True
            root.destroy()
            return ""
        
        return query.lower()
    except sr.UnknownValueError:
            speak("Sorry, I could not understand that. Can you please repeat that.")
            return ""
    except sr.RequestError:
            speak("Could not connect to the service. Please check your internet connection.")
            return ""


def weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_FORECAST_API_KEY}&units=metric"
    weather_data = requests.get(url)
    data = weather_data.json()
    if weather_data.status_code == 200:
        weather = data["weather"][0]["main"]
        temperature = round(data["main"]["temp"])
        humidity = data["main"]["humidity"]
        country = data["sys"]["country"]
        speak(f"weather in {city} is: {weather}. Temprature is {temperature}°C with {humidity}% humidity.")
        country_name = pycountry.countries.get(alpha_2=country)
        country_full = country_name.name if country_name is not None else country
        speak(f"{city} is located in : {country_full}")
    else:
        speak("No city found")



def wikipedia_summary(query):
    try:
        summary = wikipedia.summary(query,sentences=2)
        speak(summary)
    except wikipedia.exceptions.PageError:
        speak("Sorry, I couldn't find information on that.")

def send_email():
    for widget in content_frame.winfo_children():
        widget.destroy()

    email_input = ctk.CTkEntry(master=content_frame,placeholder_text="Enter your mail",font=("Helvetica",24),width=300)
    email_input.pack(pady=5)

    password_input = ctk.CTkEntry(master=content_frame,placeholder_text="Your password",show="*",width=300)
    password_input.pack(pady=5)
    
    recipient_email_input = ctk.CTkEntry(master=content_frame,placeholder_text="Enter recipient email",font=("Helvetica",24),width=300)
    recipient_email_input.pack(pady=5)

    def start_email_thread():
        threading.Thread(target=proceed_email,daemon=True).start()
    
    send_button = ctk.CTkButton(master=content_frame,text="Send",command=start_email_thread)
    send_button.pack(pady=10)

    def proceed_email():
        EMAIL= email_input.get()
        PASSWORD = password_input.get()
        recipient_email = recipient_email_input.get()

        if not EMAIL or not PASSWORD:
            speak("Enter both email and password")
            return
    
        if not recipient_email:
            return

        speak("What should be the subject?")
        subject = takecommand()
        if not subject:
            return

        speak("What is the message?")
        message = takecommand()
        if not message:
            return

        try:
            # Email setup
            msg = MIMEMultipart()
            msg['From'] = EMAIL
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            # Connect to SMTP server
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
            server.quit()
            speak("Email sent successfully!")
        except Exception as e:
            speak("Failed to send email.")
            print(f"Error: {e}")
   
def get_gemini_response(query):
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(query)
        return response.text.replace("*","")
    except Exception as e:
        print(f"Error getting Gemini response: {e}")
        return "I'm sorry, I couldn't process that request" 



def open_app_or_website():
    command = takecommand().lower()

    if command:
        # Open websites
        if "google" in command:
            webbrowser.open("https://www.google.com")
            speak("Opening Google.")
        elif "youtube" in command:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube.")
        elif "spotify" in command:
            webbrowser.open("https://open.spotify.com/")
            speak("Opening spotify")
        elif "wikipedia" in command:
            webbrowser.open("https://www.wikipedia.org/")
            speak("Opening wikipedia")
        elif "facebook" in command:
            webbrowser.open("https://www.facebook.com")
            speak("Opening Facebook.")
        elif "twitter"  in command:
            webbrowser.open("https://www.twitter.com")
            speak("Opening Twitter.")
        elif "gmail" in command:
            webbrowser.open("https://mail.google.com")
            speak("Opening Gmail.")
        
        # Open apps (Windows)
        elif "chrome" in command:
            os.system("start chrome")
            speak("Opening Chrome.")
        elif "notepad" in command:
            os.system("notepad")
            speak("Opening Notepad.")
        elif "word" in command:
            os.system("start winword")
            speak("Opening Microsoft Word.")
        elif "excel" in command:
            os.system("start excel")
            speak("Opening Microsoft Excel.")
        elif "powerpoint" in command:
            os.system("start powerpnt")
            speak("Opening Microsoft PowerPoint.")
        elif "vs code" in command or "visual studio code" in command:
            os.system("code")
            speak("Opening Visual Studio Code.")
        elif "command prompt" in command or "cmd" in command:
            os.system("start cmd")
            speak("Opening Command Prompt.")
        else:
            speak("Sorry, I couldn't find that application or website.")

def close_browser():
    speak("which browser or app you want to close")
    command = takecommand()
    if command:
        # Close browsers
        if "chrome" in command:
            os.system("taskkill /F /IM chrome.exe")
            speak("Closing Chrome.")
        elif "firefox" in command:
            os.system("taskkill /F /IM firefox.exe")
            speak("Closing Firefox.")
        elif "edge" in command:
            os.system("taskkill /F /IM msedge.exe")
            speak("Closing Microsoft Edge.")
        
        # Close common apps
        elif "notepad" in command:
            os.system("taskkill /F /IM notepad.exe")
            speak("Closing Notepad.")
        elif "word" in command:
            os.system("taskkill /F /IM WINWORD.EXE")
            speak("Closing Microsoft Word.")
        elif "excel" in command:
            os.system("taskkill /F /IM EXCEL.EXE")
            speak("Closing Microsoft Excel.")
        elif "powerpoint" in command:
            os.system("taskkill /F /IM POWERPNT.EXE")
            speak("Closing Microsoft PowerPoint.")
        elif "vs code" in command or "visual studio code" in command:
            os.system("taskkill /F /IM Code.exe")
            speak("Closing Visual Studio Code.")
        elif "command prompt" in command or "cmd" in command:
            os.system("taskkill /F /IM cmd.exe")
            speak("Closing Command Prompt.")
        else:
            speak("Sorry, I couldn't find that application running.")
    else:
        speak("I didn't catch that. Please try again.")

def main():
    global jojo_running,stop_jojo_flag

    if jojo_running:
        # if already running, it will restart it
        stop_jojo_flag = True
        speak("Restarting Jojo...")
        return
    
    def jojo_loop():
        global jojo_running,stop_jojo_flag
        jojo_running = True
        stop_jojo_flag = False
        speak("Hello, I am JOJO. How can I assist you today?")
        while not stop_jojo_flag:
            query = takecommand()
            if "stop jojo".lower() in query.lower() or "jojo stop".lower() in query.lower() or "exit".lower() in query.lower() or "goodbye".lower() in query.lower():
                speak("Goodbye! Have a great day!")
                stop_program = True
                root.destroy()
                break
            elif "hello".lower() in query.lower():
                speak("Hello! How can I help you?")
            elif "time".lower() in query.lower():
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                speak(f"The current time is {current_time}")
            elif "city weather" in query:
                speak("Please tell me the city name.")
                city = takecommand()
                if city:
                    weather(city)
            elif "search on wikipedia".lower() in query.lower():
                speak("What should I search on Wikipedia?")
                query = takecommand()
                if query:
                    wikipedia_summary(query)
            elif "what is your name" in query:
                speak("my name is jojo")
            elif "send mail".lower() in query.lower():
                send_email()
            elif "open app".lower() in query.lower() or "open site".lower()in query.lower():
                speak("which app or site do you want to open")
                open_app_or_website() 
            elif f"close browser".lower() in query.lower() or "close site" in query.lower():
                    close_browser()
            else:
                gemini_response = get_gemini_response(query)
                if gemini_response and gemini_response != "I'm sorry, I couldn't process that request":
                    speak(gemini_response)
                else:
                    output_text.configure(text=f'You said: {query}')
            
        jojo_running = False
        stop_jojo_flag = False 

    threading.Thread(target=jojo_loop, daemon=True).start()
   
            
                  
    

if __name__ == "__main__":
    # print(""" 
    # For finding city weather please speak city
    # **************************************************\n
    # For open wikipedia speak search on wikipedia first
    # *****************************************************\n
    # For open sites please speak  open site and same for opening an app   
    # *****************************************************\n 
    # for sending mail speak send mail
    # *****************************************************\n
    # For exit the voice assistant speak exit  """)
    # main()

    img = ImageTk.PhotoImage(Image.open(resource_path("D:\\visual code\\oasis_infotech_fellowship\\Jojo_voice_assistant\\voice_icon.png")).resize((20,20),Image.Resampling.LANCZOS))
    button = ctk.CTkButton(master=root,image=img,text="",fg_color="#f2f2f2",hover_color="#ffe6e6",corner_radius=50,width=50,height=50,command=main).place(relx=0.5,rely=0.9,anchor=tk.CENTER)
    threading.Thread(target=main,daemon=True).start()
    root.mainloop()
