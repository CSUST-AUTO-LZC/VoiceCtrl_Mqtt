import pyttsx3


def Changing_volume():
    while input('Continue or no?') == 'y':
        engine = pyttsx3.init()
        volume = engine.getProperty('volume')
        engine.setProperty('volume', volume+1.25)
        print(volume)
        engine.say('The quick brown fox jumped over the lazy dog.')
        engine.runAndWait()


def Changing_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        engine.setProperty('voice', voice.id)
        engine.say('The quick brown fox jumped over the lazy dog.')
    engine.runAndWait()


if __name__ == '__main__':
    # Changing_volume()
    Changing_voices()
