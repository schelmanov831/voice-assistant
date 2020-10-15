# импорт модулей
import webbrowser
import time
import speech_recognition as sr
import pyttsx3
import datetime
from fuzzywuzzy import fuzz

# настройки
opts = {
    "alias": ('маша', 'мария', 'мша', 'мэрия', 'мэша'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час'),
        "joke": ('расскажи анекдот', 'рассмеши меня', 'ты знаешь анекдоты'),
        "browse": ('открой браузер', 'открой интернет', 'открой гугл',
                   'запусти браузер', 'запусти интернет', 'запусти гугл')
    }
}


# функции
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startswith(opts["alias"]):
            # обращение к голосовому ассистенту
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # распознование и выполнение команд
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")

    except sr.RequestError:
        print("[log] Неизвестная ошибка, проверьте подключение к интернету!")


# нечеткий поиск команд
def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    return RC


# преобразованеи команды в действие
def execute_cmd(cmd):
    if cmd == 'ctime':
        # узнать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'joke':
        # рассказать анекдот
        speak("К сожалению, разработчик не дал мне возможности рассказывать анекдоты")

    elif cmd == 'browse':
        webbrowser.open('https://google.ru')

    else:
        print("Команда не распознана, повторите!")


# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index = 1)

with m as source:
    # отсекат шум от речи человека
    r. adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

speak("Здраствуйте, я вас слушаю")

stop_listening = r.listen_in_background(m, callback)
while True:
    time.sleep(0.1)
