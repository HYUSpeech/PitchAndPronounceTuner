import speech_recognition as sr
#import sys #-- 텍스트 저장시 사용

class SpeechRecognition:

    def recognition(convert_path):
        r = sr.Recognizer()
        kr_audio = sr.AudioFile(convert_path)

        with kr_audio as source:
            audio = r.record(source)

        #sys.stdout = open('news_out.txt', 'w') #-- 텍스트 저장시 사용
        return r.recognize_google(audio, language='ko-KR') #-- 한글 언어 사용
    


