import os
from typing import Text
import playsound
import speech_recognition as sr
import time
import sys
import ctypes
import wikipedia
import datetime
import json
import re
import webbrowser
import smtplib
import pyttsx3
import requests
import urllib
import urllib.request as urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import perf_counter, strftime
from gtts import gTTS, tts
from youtube_search import YoutubeSearch
from googlesearch import search

wikipedia.set_lang('vi')
language = 'vi'
#path = ChromeDriverManager().install()

#chuyển văn bản thành giọng nói
def speak(text):
    print("Trợ lý ảo: ",text)
    '''
    tts = gTTS(text = text , lang = language , slow = False)
    tts.save("noi.mp3")  #lưu giọng nói
    playsound.playsound("noi.mp3" , True)
    os.remove("noi.mp3")  #xóa file sau mỗi lần nói
    '''
    robot_mouth = pyttsx3.init()
    voices = robot_mouth.getProperty('voices')
    rate = robot_mouth.getProperty('rate')
    volume = robot_mouth.getProperty('volume')
    robot_mouth.setProperty('volume', volume - 0.0)  # tu 0.0 -> 1.0
    robot_mouth.setProperty('rate', rate - 50)
    robot_mouth.setProperty('voice', voices[1].id)
    robot_mouth.say(text)
    robot_mouth.runAndWait()
    

#chuyển giọng nói (âm thanh) thành văn bản

def get_audio():
    robot_aer = sr.Recognizer()
    with sr.Microphone() as mic:  #dùng mic của máy để nghe người dùng nói
        print("Trợ lý ảo: đang nghe.....!")
        audio = robot_aer.listen(mic , phrase_time_limit=5) #truyền vào âm thanh thu dc từ mic vào biến audio, để bot nghe trong 8s
        try: #nhận dạng giọng nói
            text = robot_aer.recognize_google(audio, language = "vi-VN") # nhận dạng âm thanh ở biến audio chuyển thành văn bản
            print("Bạn: ", text)
            return text
        except: #nếu lỗi
            print("Trợ lý ảo: bị lỗi ạ...")
            return 0
'''
def get_audio_2():
    ear_robot = sr.Recognizer()
    with sr.Microphone() as source:
        ear_robot.pause_threshold = 2
        print("Trợ lý ảo: đang nghe.....!")
        audio = ear_robot.listen(source)
    try:
        text = ear_robot.recognize_google(audio, language="vi-VN")
    except:
        speak("Nhận dạng giọng nói thất bại. Vui lòng nhập lệnh ở dưới")
        text = input("Mời nhập: ")
    return text.lower()
'''

def stop():
    speak("Tạm biệt bạn, hẹn gặp lại bạn sau nha")


#có chức năng là máy tính sẽ cố gắng nhận dạng âm thanh của người đọc tối đa 3 lần cho đến khi máy tính hiểu
def get_text():
    for i in range(3): #vòng lặp này sẽ chạy 3 lần
        text = get_audio()  #nghe những gì nghe dc sẽ chuyển thành văn bản
        if text : #neeud true or !=0 thì if sẽ dc thực hiện
            return text.lower()
        elif i < 2:
            speak("mình không nghe rõ, bạn nói lại nha")
    time.sleep(3) #chương trình sẽ tạm dừng trong 3s
    stop()
    return 0


def hello(name):
    day_time = int(strftime('%H'))
    if 0 <= day_time < 11:
        speak(f'chào bạn {name}. chúc bạn một buổi sáng tốt lành nha <..>')
        speak("Bạn cần bot giúp gì vậy ạ: ")
    elif 11 <= day_time < 13 :
        speak(f'chào bạn {name}. buổi trưa tốt lành nha <..>')
        speak("Bạn cần bot giúp gì vậy ạ: ")
    elif 13<= day_time < 18 :
        speak(f'chào bạn {name}. buổi chiều an lành và thật nhiều niền vui nhé <..>')
        speak("Bạn cần bot giúp gì vậy ạ: ")
    elif 18<= day_time < 22 :
        speak(f'chào bạn {name}. trời đã tối rồi, chúc bạn có một bữa cơm vui vẻ và ấm cúng nha <..>')
        speak("Bạn cần bot giúp gì vậy ạ: ")
    elif 22<= day_time < 23 :
        speak(f'chào bạn {name}. muộn rồi bạn nên đi ngủ, ngủ sớm để đẹp da nhé <..>')
        speak("Bạn cần bot giúp gì vậy ạ: ")
    else:
        speak(f'chào bạn {name}. buổi tối vui vẻ <..>')


def get_time(text):
    now = datetime.datetime.now()
    if "giờ" in text:
        speak(f" Bây giờ là {now.hour} giờ {now.minute} phút {now.second} giây")
    elif "ngày" in text:
        speak(f" Hôm nay là ngày {now.day} tháng {now.month} năm {now.year}")
    else:
        speak("tôi chưa hiểu ý của bạn <'-'>")


def open_app(text):
    if "google" in text:
        speak("mở google chrome")
        os.system("C:\\Users\\ADMIN\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe") 
        #mở ứng dụng dẽ ko tắt chương tr, tắt ứng dụng thì mới tát ct  
    elif "tin nhắn" in text:
        speak(" mở ứng dụng tin nhắn messenger ")
        os.system("C:\\Users\\ADMIN\\AppData\\Local\\Programs\\Messenger\\Messenger.exe")
    elif "zalo" in text:
        speak(" mở ứng dụng zalo")
        os.system("C:\\Users\\ADMIN\\AppData\\Local\\Programs\\Zalo\\Zalo.exe")
    elif "microsoft team" in text:
        speak(" mở microsoft team ")
        os.system("C:\\Program Files\\Sublime Text 3\\sublime_text.exe")
    else:
        speak("ứng dụng chưa được cài đặt ạ :)")


def open_web(text):
    reg_ex = re.search('mở (.+)' , text)
    if reg_ex:
        domain = reg_ex.group(1)
        url = "https://www." + domain
        webbrowser.open(url)
        speak("Trang web bạn yêu cầu đã được mở ạ. ")
        if input("hãy nhập a để tiếp tục: ") == "a": #sau khi mở web thì chương trình sẽ dừng lại đến khi bạn nhập "a"
            pass
        return True
    else:
        return False


def open_google_search():
    speak("Bạn cần tìm kiếm gì trên google vậy:..")
    search = str(get_text()).lower()
    url = f"https://www.google.com/search?q={search}"
    webbrowser.get().open(url)
    speak(f'Đây là thông tin về {search} mà bạn tìm kiếm trên google')


def open_youtube_search():
    speak("Bạn muốn xem vi deo nào trên youtube vậy:..")
    search = str(get_text()).lower()
    url = f"https://www.youtube.com/search?q={search}"
    webbrowser.get().open(url)
    speak(f'Đây là những vi deo liên quan đến {search} mà bạn tìm kiếm trên youtube <..>')


def open_youtube_2():
    speak("Bạn muốn xem vi deo nào trên youtube vậy:..")
    search = get_text()
    while True:
        result = YoutubeSearch(search, max_results=10).to_dict()
        if result:
            break
    url = f"https://www.youtube.com" + result[0]['url_suffix']
    webbrowser.get().open(url)
    speak(f'Đây là vi deo {search} mà bạn tìm kiếm trên youtube <..>')
    print(result)

def current_weather():
    speak("Bạn muốn xem thời tiết ở đâu ạ.")
    ow_url = "http://api.openweathermap.org/data/2.5/weather?" # Đường dẫn trang web để lấy dữ liệu về thời tiết
    city = get_text()   # lưu tên thành phố vào biến city
    if not city:    # nếu biến city != 0 và = False thì để đấy ko xử lí gì cả
        pass
    api_key = "321736900281f24ef0a888c9112b0758"    # api_key lấy trên open weather map
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"    # tìm kiếm thông tin thời thời tiết của thành phố
    # truy cập đường dẫn lấy dữ liệu thời tiết
    response = requests.get(call_url) #gửi yêu cầu lấy dữ liệu
    data = response.json()    # lưu dữ liệu thời tiết dưới dạng json và cho vào biến data
    if data["cod"] != "404":     # kiểm tra nếu ko gặp lỗi 404 thì xem xét và lấy dữ liệu
        # lấy dữ liệu của key main
        city_res = data["main"]
        # nhiệt độ hiện tại
        current_temperature = city_res["temp"]
        # áp suất hiện tại
        current_pressure = city_res["pressure"]
        # độ ẩm hiện tại
        current_humidity = city_res["humidity"]
        # thời gian mặt trời
        suntime = data["sys"]
        # 	lúc mặt trời mọc, mặt trời mọc
        sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
        # lúc mặt trời lặn
        sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
        # thông tin thêm
        wthr = data["weather"]
        # mô tả thời tiết
        weather_description = wthr[0]["description"]
        # Lấy thời gian hệ thống cho vào biến now
        now = datetime.datetime.now()
        # hiển thị thông tin với người dùng
        content = f"""
        Hôm nay là ngày {now.day} tháng {now.month} năm {now.year}
        Mặt trời mọc vào {sunrise.hour} giờ {sunrise.minute} phút
        Mặt trời lặn vào {sunset.hour} giờ {sunset.minute} phút
        Nhiệt độ trung bình là {current_temperature} độ C
        Áp suất không khí là {current_pressure} héc tơ Pascal
        Độ ẩm là {current_humidity}%
        """
        speak(content)
    else:
        # nếu tên thành phố không đúng thì nó nói dòng dưới 227
        speak("Không tìm thấy địa chỉ của bạn")


# url = 'https://api.unsplash.com/photos/random?client_id=' + \
#       api_key
def change_wallpaper():
    api_key = "j9wIguJEDU8EfbpRAZJFcm85ouwacWwBqFYBywkpuEw"
    url = 'https://api.unsplash.com/photos/random?client_id=' + \
        api_key  # pic from unspalsh.com
    f = urllib2.urlopen(url) #lấy kết qur trả về của trang web
    json_string = f.read() #đọc dự liệu ở trang web
    f.close() #đóng lại trình duyệt ẩn
    parsed_json = json.loads(json_string)  #sử lý dữ liệu
    photo = parsed_json['urls']['full'] #lấy ảnh ở link urls với chất lượng full
    urllib2.urlretrieve(photo, "D:\\NĂM 3\\pictures\\a.png") #tải về máy
    image = os.path.join("D:\\NĂM 3\\pictures\\a.png")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 3)
    speak("Hình nền máy tính bạn đã được thay đổi. Bạn ra home xem có đẹp không nha ?")


def read_news():
    speak("Bạn muốn đọc báo về gì")
    
    queue = get_text()
    params = {'apiKey': '6f82b36a92b9436290e981158e34c3fd',"q": queue, }

    api_result = requests.get('https://newsapi.org/v2/everything?', params)
    api_response = api_result.json()
    print("Tin tức")

    for number, result in enumerate(api_response['articles'], start=1):
        print(f"Tin {number}:\nTiêu đề: {result['title']}\nTrích dẫn: {result['description']}\nLink: {result['url']}")
        if number <= 3:
            webbrowser.open(result['url'])


def tell_me_about():
    try:
        speak("Bạn muốn nghe về gì ạ")
        text = get_text()
        contents = wikipedia.summary(text).split('\n')
        speak(contents[0])
        time.sleep(5)
        for content in contents[1:]:
            speak("Bạn muốn nghe thêm không")
            ans = get_text()
            if "có" not in ans:
                break    
            speak(content)
            time.sleep(5)

        speak('Cảm ơn bạn đã lắng nghe!!!')
    except:
        speak("Bot không định nghĩa được thuật ngữ của bạn. Xin mời bạn nói lại")

def help_me():
    speak("""bot có thể giúp bạn thực hiện các việc sau đây:
    <<........>>>
    1. chào hỏi
    2. Hiển thị giờ
    3. Mở website, ứng dụng desktop
    4. Tìm kiếm với google
    5. Tìm kiếm video với youtube
    6. Dự báo thời tiết
    7. Đọc báo
    8. Thay đổi hình nền máy tính
    9. Định nghĩa với từ điển bách khoa toàn thư ( Wikipedia )
    10. Mở nhạc với youtube
    <<.........>>>
    """)


def main_brain():
    speak("xin chào bạn tớ là bot đây ạ, vui lòng nhập mật khẩu để xác nhận danh tính nha hi hi")
    passs = get_text()
    name = "lan anh"
    if(passs == "đề án"):
        speak(f'xin chào bạn {name}.')
    else:
        speak("mật khẩu ko chính xác rồi ạ.")
        stop()
        sys.exit()
    if name :
        #speak("Bạn cần bot giúp gì không ạ: ")
        while True:
            text = get_text()

            if not text:
                break
            elif "tạm biệt" in text or "hẹn gặp lai" in text:
                    stop()
                    break
            elif "xin chào" in text:
                hello(name)
            elif "hiện tại" in text:
                get_time(text)
            elif "mở " in text:
                if "." in text:
                    open_web(text)
                else:
                    open_app(text)
            elif "google" in text:
                open_google_search()
                if input("Để tiếp tục y/n: ") == "y" :
                        pass
            elif 'youtube' in text:
                speak("Bạn muốn tìm kiếm đơn giản hay phức tạp")
                yeu_cau = get_text()
                if "đơn giản" in yeu_cau:
                    open_youtube_search()
                    if input("Để tiếp tục y/n: ") == "y" :
                        pass
                elif "phức tạp" in yeu_cau:
                    open_youtube_2()
                    if input("Để tiếp tục y/n: ") == "y":
                        pass
            elif "thời tiết" in text:
                current_weather()
            elif "hình nền" in text:
                change_wallpaper()
            elif "đọc báo" in text:
                read_news()
                if input("Để tiếp tục y/n: ") == "y" :
                        pass
            elif "định nghĩa" in text:
                tell_me_about()
            elif "chức năng" in text:
                help_me()
            else:
                speak(f'chắc năng này chưa có bạn vui lòng chọn lại sau nha <..>')

main_brain()