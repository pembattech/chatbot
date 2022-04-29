
import tkinter as tk
import requests
import wikipedia
import subprocess

def speak(text: str, pitch: int=50) -> int:
    """ Use espeak to convert text to speech. """
    return subprocess.run(['espeak', f'-p {pitch}', text]).returncode

class Function:
    def __init__(self, query):
        self.query = query

    def find_my_ip(self):
        ip_address = requests.get('https://api64.ipify.org?format=json').json()
        speak(ip_address["ip"])

    def search_on_wikipedia(self):
        results = wikipedia.summary(self.query, sentences=2)
        speak(results)

    def get_latest_news(self):
        news_headlines = []
        res = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&category=general").json()
        articles = res["articles"]
        for article in articles:
            news_headlines.append(article["title"])
        speak(news_headlines[:5])

    def get_random_joke(self):
        headers = {
            'Accept': 'application/json'
        }
        res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
        speak(res["joke"])

    def get_random_advice(self):
        res = requests.get("https://api.adviceslip.com/advice").json()
        speak(res['slip']['advice'])

def request(query):
    if "what is my ip" in query:
        Function(query).find_my_ip()

    elif "give me the latest news" in query:
        Function(query).get_latest_news()

    elif "tell me a joke" in query:
        Function(query).get_random_joke()

    elif "give me some advice" in query:
        Function(query).get_random_advice()
    
    else:
        Function(query).search_on_wikipedia()


class gui:
    def __init__(self):
        self.gui_bgimage = "bg.png"
        self.canvas = tk.Tk()
        self.canvas.geometry("1000x100")
        self.canvas.title("D.I.S.M.I.S")

        self.input_data = ""
        self.input_data =tk.StringVar()

        background_image = tk.PhotoImage(file = self.gui_bgimage)
        background_label = tk.Label(self.canvas, image=background_image)
        background_label.place(relwidth=1, relheight=1)
        
        self.textField = tk.Entry(self.canvas, textvariable = self.input_data, justify='center', width = 100, font="Calibri 12", bg ="black", fg='white', insertbackground='white')
        self.textField.pack(pady = 20)
        self.textField.focus()
        self.textField.bind('<Return>', self.DISMIS_userinterface)

        self.button = tk.Button(self.canvas, text = 'Close DISMIS Input Window', command=self.quit)
        self.button.pack()
        self.canvas.mainloop()

    def quit(self):
        self.canvas.destroy()
        self.canvas.mainloop()

    def DISMIS_userinterface(self, canvas):
        message = f"{self.input_data.get()}"

        # Clearing text
        self.textField.delete(0, tk.END)

        request(message)
        

gui()