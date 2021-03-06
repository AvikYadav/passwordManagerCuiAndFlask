from flask import Flask,render_template,request,escape,session
from google_trans_new import google_translator
import speech_recognition as sr
import gtts
import playsound
import googletrans
from Cheker import check_log_in
from checkerPasswd import CheckPassword
import os

app = Flask(__name__)


recognizer = sr.Recognizer()
translator = google_translator()

def log_request(req: 'flask_request', res: str) -> None:
    with open("vsearch.log", "a") as log:
        print(req.form, req.remote_addr, req.user_agent, res, file=log, sep="|")


def Listen(input_lang):
    try:
        with sr.Microphone() as source:
            print('Speak Now')
            voice = recognizer.listen(source)
            text = recognizer.recognize_google(voice, language=input_lang)
            print(text)
            return text
    except Exception as err:
        print(err)
        message =  "sorry voice command is shortly unavailable or permission is denied,try Input instead"
        return message
@app.route("/")
@app.route("/entry")
def entry_page () -> 'html':
        title = "Welcome to Avik Translator on web"
        info = "if you don't know the languages available pls visit /languages"
        return render_template('langEntry.html',
                               the_title=title,
                               the_info=info,)
# @app.route("/entryText",methods=['POST'])
# def entry_page_Text () -> 'html':
#     title = "Pls enter text you want to convert"
#     info = "if you don't know the languages available pls visit /languages"
#     return render_template('textEntry.html',
#                            the_title=title,
#                            the_info=info,)
@app.route("/results",methods = ["POST"])
def to_do() -> "html":
    try:
        input_lang = request.form['Input_lang']
        output_lang = request.form['dest_lang']
        Inp = [ k for k,v in googletrans.LANGUAGES.items() if v == input_lang]
        IndDest = [ key for key,value in googletrans.LANGUAGES.items() if value == output_lang]
        Inp2 = str(Inp[0])
        IndDest2 = str(IndDest[0])
        title = "here are your results"
        text = request.form["Phrase"]
        translated = translator.translate(text, lang_tgt=IndDest2)
        result = translated
        """
        this code generates error in pythonAnywhere but runs fine in local machine
        converted_audio = gtts.gTTS(translated, lang=IndDest2)
        converted_audio.save('Audio.mp3')
        playsound.playsound('Audio.mp3')
        converted_audio2 = str(converted_audio)
        print(converted_audio2)
        os.remove("Audio.mp3")"""



        converted_audio = gtts.gTTS(translated, lang=IndDest2)
        converted_audio.save('Audio.mp3')
        playsound.playsound('Audio.mp3')
        converted_audio2 = str(converted_audio)
        print(converted_audio2)
        os.remove("Audio.mp3")
        log_request(request, result)
        return render_template('results.html',
                               the_title = title,
                                the_phrase= text,
                                  Input_lang = Inp2,
                              dest_lang = IndDest2,
                               the_results=result)
    except IndexError as err:
        print(err)
        return "pls check language spelling , if you don't know languages available just type /languages after .com"
    except AssertionError as err:
        print(err)
        return "pls enter the phrase you want to convert,don't leave it empty. it generates problems"
@app.route("/languages")
def languages() -> "html" :
    languages = googletrans.LANGUAGES.values()
    print(languages)
    return render_template("Languages.html",
                           the_title = "here are all languages available",
                           row_title="languages available",
                           combine = languages)
@app.route('/viewlog')
@check_log_in
def view_the_log () -> 'html':
    contents = []
    with open("vsearch.log") as log:
        for line in log:
            contents.append([])
            for item in line.split("|"):
                contents[-1].append(escape(item))
    titles = ("FormData","remote_addr","UserAgent","results")
    return render_template('viewlog.html',
                    the_title='view log',
                    the_row_titles=titles,
                    the_data=contents,)
@app.route('/errorlog')
@check_log_in
def View_error () -> "html":
    with open("error.txt","r") as error:
        return render_template("code.html",
                               text = error.read())
@app.route('/login')
def login():
    session['login'] = True
    return "you are loged in"

@app.route('/logout')
def logout():
    session.pop('login')
    return "you are loged out in"
@app.route('/sourceCode')
def sourceCodePassword() -> "sourceCode":
    return render_template("sourceCodePassword.html",
                           the_title = "please enter password")


passwd = "YouWillNeverGuessThis"
@app.route('/code',methods= ["POST"])
@CheckPassword
def sourceCode() ->"sourceCode":
    with open("code.txt","r") as code:
        return render_template('code.html', text=code.read())

@app.route('/developer')
def developerPassword() -> "developer":
    return render_template("developerPasswd.html",
                           the_title = "please enter password")
passwd2 = "developerAvik"
@app.route("/developerMode",methods= ["POST"])
def Developer() -> "html":
    passwdEntered2 = request.form["Password2"]
    if passwdEntered2 == passwd2:
        return render_template('developer.html',
                               the_title = "welcome to development and debug mode")
    return "password Incorrect"




app.secret_key="YouWillNeverGuessMySecretKey"
if __name__ == '__main__':
    app.run(debug=True)
# language dictory page and view log page



