import naoqi
import codecs, json 
from naoqi import ALProxy
from time import sleep

# find my robot - set IP and robot says "hello"
ip_addr = '10.10.48.232'

print(ip_addr)
tts_say = ALProxy("ALTextToSpeech", ip_addr, 9559)
tts_say.setLanguage("English")
tts_say.setVolume(0.7)
lyrics = """Hello"""
tts_say.say(lyrics)

# remove connected users/devices/services - make me some space! only up to 6 connections at a time alowed
try:
    for i in tts_say.getSubscribers():
        try:
            tts_say.unsubscribe(i)
        except:
            pass
except:
    pass