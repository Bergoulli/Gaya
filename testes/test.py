import pyttsx3

engine = pyttsx3.init()


voices = engine.getProperty('voices')

print(voices)

engine.setProperty('voice', voices[-2].id)

engine.say("quero que você vá se foder")
engine.runAndWait()