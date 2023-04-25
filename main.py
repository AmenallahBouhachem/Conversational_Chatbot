from tkinter import *
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os
import pyttsx3
import speech_recognition
import threading
bot = ChatBot('Bot')
trainer = ListTrainer(bot)

for files in os.listdir('data/english/'):
    data = open('data/english/' + files, 'r', encoding='utf-8').readlines()
    trainer.train(data)


def botReply():
    question = questionField.get()
    question = question.capitalize()
    answer = bot.get_response(question)
    textarea.insert(END, 'You: ' + question + '\n\n')
    textarea.insert(END, 'Bot: ' + str(answer) + '\n\n')
    pyttsx3.speak(answer)
    questionField.delete(0, END)

def audioToText():
    while True :
        sr=speech_recognition.Recognizer()
        try:
            with speech_recognition.Microphone() as Mic :
                sr.adjust_for_ambient_noise(Mic, duration=0.2)
                audio=sr.listen(Mic)
                query=sr.recognize_google(audio)
                questionField.delete(0,END)
                questionField.insert(0,query)
                botReply()

        except EXCEPTION as e :
            print(e)




root = Tk()
root.geometry('500x570+100+30')
root.title(' ChatBot created by Bouhachem Amenallah ')
root.config(bg='white')
LogoPic = PhotoImage(file='pic.png')
LogoPicLabel = Label(root, image=LogoPic, bg='white')
LogoPicLabel.pack(pady=5)
centerFrame = Frame(root)
centerFrame.pack()
scrollbar = Scrollbar(centerFrame)
scrollbar.pack(side=RIGHT)
textarea = Text(centerFrame, font=(' times new roman ', 20, " bold "), height=10, yscrollcommand=scrollbar.set,
                wrap='word')
textarea.pack(side=LEFT)
scrollbar.config(command=textarea.yview)
questionField = Entry(root, font=(' verdana ', 20, 'bold '))
questionField.pack(pady=15, fill=X)
AskPic = PhotoImage(file='ask.png')
askButton = Button(root, image=AskPic, command=botReply)
askButton.pack()


def click(event):
    askButton.invoke()


root.bind('<Return>', click)
thread=threading.Thread(target=audioToText)
thread.setDaemon(True)
thread.start()
root.mainloop()
