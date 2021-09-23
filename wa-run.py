import os, time, requests
import pyshorteners
from bs4 import BeautifulSoup, SoupStrainer
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import selenium.webdriver.common.keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from PIL import Image

from selenium.webdriver.common.action_chains import ActionChains
import moviepy.editor as mp

s = pyshorteners.Shortener(api_key='0fa394ea474e8545635fb17188c0cde02748d26e')
driver = webdriver.Firefox()
driver.get("https://web.whatsapp.com/")
driver.maximize_window()


wait = WebDriverWait(driver, 20)

####################################################################################

session = requests.Session()

def reply():
    a = ActionChains(driver)
    m = driver.find_elements_by_xpath('//div[@class= "_1Gy50"]')[-1]
    a.move_to_element(m).perform()
    try:
        click_to_reply = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class= "_3e9My"]'))).click()
        click_reply = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-label= "Reply"]'))).click()
    except:
        print("fail to reply")

def anime(x):
    textbox=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div/div/div[2]')
    global url
    global category
    global animes
    global soup
    global command

    url = x
    #SAVE URL TO SESSION
    session_url[sender_name] = url

    #print("MAIN URL IS "+url)
    print("MAIN URL IS "+session_url[sender_name])
    site = session.get(session_url[sender_name])
    soup = BeautifulSoup(site.text, 'lxml')
    
    nomor = 0

    session_category[sender_name] = False
    if command == "/genre":
        ### SHOW CATEGORY
        rawanimes = soup.find('div', {"id": "serieshome"})
        animes = rawanimes.findAll('li', {"class": "cat-item"})

        session_category[sender_name] = True
        # SHOW CATEGORY LIST
        for listcat in animes:
            nomor+=1
            print("["+str(nomor)+"] "+listcat.text)
            textbox.send_keys("["+str(nomor)+"] "+listcat.text)
            textbox.send_keys(Keys.SHIFT+Keys.ENTER)

    else:
        if "?s=" in session_url[sender_name]:
            try:
                check = soup.find('a', {"class": "search-google not-right"})
                print(check.text)
                textbox.send_keys("SHOW RESULT FOR: "+x.split("?s=",1)[1])
                textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                textbox.send_keys("Not found")
                return

            except:
                soup.find('div', {"class": "judul-anime"})
                print ("SHOW RESULT FOR: "+x.split("?s=",1)[1])
                textbox.send_keys("SHOW RESULT FOR: "+x.split("?s=",1)[1])
                textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                textbox.send_keys(Keys.SHIFT+Keys.ENTER)

                rawanimes = soup.find('div', {"class": "peliculas"})
                for anime in rawanimes.findAll('div', {"class": "item episode-home"}):
                    judul  = anime.find('div', {"class": "judul-anime"})
                    info = anime.find ('div', {"class": "fixyear"})
                    nomor+=1
                    print("["+str(nomor)+"]", judul.text+" "+info.text)
                    textbox.send_keys("["+str(nomor)+"]", judul.text+" "+info.text)
                    textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                    textbox.send_keys(Keys.SHIFT+Keys.ENTER)

        elif "/movies/" in session_url[sender_name] or "/tvshows-genre/" in session_url[sender_name]:
            if "/movies/" in session_url[sender_name]:
                print("[ ANIME MOVIES TERBARU ]")
                textbox.send_keys("[ ANIME MOVIES TERBARU ]")
            else:
                textbox.send_keys(" ")

            textbox.send_keys(Keys.SHIFT+Keys.ENTER)
            textbox.send_keys(Keys.SHIFT+Keys.ENTER)

            rawanimes = soup.find('div', {"class": "peliculas"})
            animes = rawanimes.findAll('h2', {"class": "title-episode-movie"})
            for anime in animes:
                nomor+=1
                print("["+str(nomor)+"]"+anime.text)
                textbox.send_keys("["+str(nomor)+"]"+anime.text)
                textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                textbox.send_keys(Keys.SHIFT+Keys.ENTER)

        elif "batch" in session_url[sender_name]:
            print("[ ANIME BATCH TERBARU ]")
            textbox.send_keys("[ ANIME BATCH TERBARU ]")
            textbox.send_keys(Keys.SHIFT+Keys.ENTER)
            textbox.send_keys(Keys.SHIFT+Keys.ENTER)

            rawanimes = soup.find('div', {"class": "peliculas"})
            animes = rawanimes.findAll('div', {"class": "item"})
            for anime in animes:
                nomor+=1
                print("["+str(nomor)+"]"+anime.text)
                textbox.send_keys("["+str(nomor)+"]"+anime.text)
                textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                textbox.send_keys(Keys.SHIFT+Keys.ENTER)

        elif "/episode/" in session_url[sender_name]:
            rawanimes = soup.find('tbody')
            print("[ ANIME TERBARU ]")
            textbox.send_keys("[ ANIME TERBARU ]")
            textbox.send_keys(Keys.SHIFT+Keys.ENTER)
            textbox.send_keys(Keys.SHIFT+Keys.ENTER)
            # SHOW POST LIST
            for animelist in rawanimes.findAll('tr'):
                anime = animelist.find('td', {"class": "bb"}).find('a')
                nomor+=1
                print ("["+str(nomor)+"]", anime.text)
                textbox.send_keys("["+str(nomor)+"] ", anime.text)
                textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                textbox.send_keys(Keys.SHIFT+Keys.ENTER)
        
        elif "/tvshows/" in session_url[sender_name]:
            rawanimes = soup.find('ul', {"class": "episodios"})
            animes = rawanimes.findAll('li')
            for anime in animes:
                nomor+=1
                animeeps = anime.find('div', {"class": "episodiotitle"}).find('a')
                print("["+str(nomor)+"] "+animeeps.text)
                textbox.send_keys("["+str(nomor)+"] "+animeeps.text)
                textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                textbox.send_keys(Keys.SHIFT+Keys.ENTER)

        else:
            print("ERROR MENU NOT FOUND")
            textbox.send_keys("ERROR MENU NOT FOUND")
            textbox.send_keys(Keys.SHIFT+Keys.ENTER)
            
        textbox.send_keys("===========================")
        textbox.send_keys(Keys.SHIFT+Keys.ENTER)

        pagelist()

def selectanimes(x):
    textbox=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div/div/div[2]')
    global animemain
    global url
    global surl
    global command

    site = session.get(session_url[sender_name])
    soup = BeautifulSoup(site.text, 'lxml')

    angka = 0
    limit = 15

    if session_category[sender_name] == True:
        session_category[sender_name] = False
        rawanimes = soup.find('div', {"id": "serieshome"})
        animes = rawanimes.findAll('li', {"class": "cat-item"})
        limit= len(animes)
        print("LIMIT IS "+str(limit))
        for listcatlink in animes:
            angka+=1
            if x == angka:
                categoryurl = listcatlink.find('a').get('href')
                print("[ "+listcatlink.find('a').text+" ]")
                textbox.send_keys("[ "+listcatlink.find('a').text+" ]")
                to_anime(categoryurl)
                break
            elif x > limit:
                print("MASUKAN ANGKA YANG TERSEDIA")
                break
            else:
                continue

    else:
        if "?s=" in session_url[sender_name]:
            rawanimes = soup.find('div', {"class": "peliculas"})
            animes = rawanimes.findAll('div',{"class": "item episode-home"})
            for anime in animes:
                angka +=1
                if angka == x:
                    surl = (anime.find('a').get('href'))
                    post(surl)
                    break
                elif x > 15:
                    print ("[ERROR]Masukan nomor yang ada")
                    textbox.send_keys("[ERROR]Masukan nomor yang ada")
                    x = 0
                else:
                    continue

        elif "/tvshows/" in session_url[sender_name]:
            rawanimes = soup.find('ul', {"class": "episodios"})
            animes = rawanimes.findAll('li')
            limit = len(animes)
            for anime in animes:
                angka+=1
                if x == angka:
                    surl = anime.find('div', {"class": "episodiotitle"}).find('a').get('href')
                    post(surl)
                if x > limit:
                    print("MASUKAN NOMOR YANG TERSEDIA")
                    break
                else:
                    continue


        elif "/movies/" in session_url[sender_name] or "/tvshows-genre/" in session_url[sender_name]:
            rawanimes = soup.find('div', {"class": "peliculas"})
            animes = rawanimes.findAll('div', {"class": "item"})
            for anime in animes:
                angka+=1
                if x == angka:
                    surl = anime.find('a').get("href")
                    if "/movies/" in session_url[sender_name]:
                        post(surl)
                    else:
                        to_anime(surl)
                elif x > 15:
                    print("[ERROR]Masukan nomor yang ada")
                    textbox.send_keys("[ERROR]Masukan nomor yang ada")
                    break
                else:
                    continue


        elif "/batch/" in session_url[sender_name]:
            rawanimes = soup.find('div', {"class": "peliculas"})
            animes = rawanimes.findAll('div', {"class": "item"})
            for anime in animes:
                angka+=1
                if x == angka:
                    surl = anime.find('a').get("href")
                    post(surl)
                elif x > 15:
                    print("[ERROR]Masukan nomor yang ada")
                    textbox.send_keys("[ERROR]Masukan nomor yang ada")
                    break
                else:
                    continue

        elif "/episode/" in session_url[sender_name]:
            print(session_url[sender_name])
            print("TRY ENTER DOWN")
            rawanimes = soup.find('tbody')
            animes = rawanimes.findAll('tr')
            print("NOW ENTER DOWN")
            for anime in animes:
                angka +=1
                if angka == x:
                    surl = (anime.find('td', {"class": "bb"}).find('a').get('href'))
                    post(surl)
                    break
                elif x > 15:
                    print ("[ERROR]Masukan nomor yang ada")
                    textbox.send_keys("[ERROR]Masukan nomor yang ada")
                    x = 0
                else:
                    print ()


        else:
            print("ERROR URL LINK NOT FOUND")
            
        # FIND LINK OF ANIME THEN SEND IT TO ANIME()

###########################

def pagelist():
    textbox=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div/div/div[2]')
    global page
    page = soup.find('div', {"class": "paginado"})
    global currentpage
    currentpage = soup.find('a', {"class": "current"})

    # SHOW CURRENT PAGE AND PAGE LIST
    try:
        print ("[ Page "+currentpage.text+" ]"+" | ",end =" ")
        textbox.send_keys("[ Page "+currentpage.text+" ]"+" | ")
        for pagelist in page.findAll('li'):
            if pagelist.find('a') == None:
                break
            print (pagelist.find('a').text, end =" ")
            textbox.send_keys(pagelist.find('a').text+" ")
    
    # IF NO PAGE LIST HERE
    except:
        print()
        textbox.send_keys("Page not found")


def selectpage(x):

    # FIND LINK OF SELECTED PAGE THEN SEND IT TO ANIME()
    textbox=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div/div/div[2]')
    try:
        rawnumpage = int(currentpage.text)
        spliter = [int(s) for s in x.split() if s.isdigit()]
        intpage = spliter[0]
        if intpage > rawnumpage:
            for linkpage in page.findAll('li'):
                if linkpage.text == "First":
                    continue
                try:
                    if int(linkpage.text) == intpage:
                        url = linkpage.find('a').get('href')
                        anime(url)
                        return   
                except:
                    continue
            print ("[ERROR] masukan urutan page yang tampil\n")
            textbox.send_keys("[ERROR] masukan urutan page yang tampil")
        elif intpage < rawnumpage:
            pages = page.findAll('li')
            pages.reverse()
            for linkpage in pages:
                if linkpage.text == "First":
                    continue
                rawnumpage -=1
                try:
                    if int(linkpage.text) == intpage:
                        url = linkpage.find('a').get('href')
                        anime(url)
                        return
                except:
                    continue
                
            print ("[ERROR] masukan urutan page yang tampil\n")
            textbox.send_keys("[ERROR] masukan urutan page yang tampil")
        else:
            print ("[!] anda sudah berada di page ini")
            textbox.send_keys("[!] anda sudah berada di page ini")

    # IS THERE NO PAGE FOUND
    except:
        print()
        textbox.send_keys("There no pagelist found")

############################


def post(x):
    global url
    global surl
    print(url)
    print("=====")
    print(session_url[sender_name])
    print("=====")
    textbox=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div/div/div[2]')
    
    site = session.get(x)
    animemain = BeautifulSoup(site.text, 'lxml')


    if "/batch/" in session_url[sender_name] or "/batch/" in surl:
        try:
            surl = "None"
        except:
            print(" ")

        # SEND JUDUL
        judulbatch = animemain.find('h1')
        textbox.send_keys(judulbatch.text)
        textbox.send_keys(Keys.SHIFT+Keys.ENTER)
        textbox.send_keys(Keys.ENTER)

        # SEND SINOPSIS
        sinopsis = animemain.find('div', {"class": "entry-content"}).findAll('p')
        if "*" in sinopsis[2].text:
            print("SINOPSIS")
            textbox.send_keys("SINOPSIS")
            textbox.send_keys(Keys.SHIFT+Keys.ENTER)
            print(sinopsis[3].text)
            textbox.send_keys(sinopsis[3].text)
            textbox.send_keys(Keys.SHIFT+Keys.ENTER)
            textbox.send_keys(Keys.ENTER)
        else:
            print (sinopsis[2])
            textbox.send_keys(sinopsis[2].text)
            textbox.send_keys(Keys.SHIFT+Keys.ENTER)
            textbox.send_keys(Keys.ENTER)

        # SEND JUDUL DOWNLOAD
        jdownload = animemain.find('p', {"class": "smokettl"})
        print(jdownload.text)
        textbox.send_keys(jdownload.text)
        textbox.send_keys(Keys.SHIFT+Keys.ENTER)

        # SEND LINK
        mirrors = animemain.findAll('p', {"class": "smokeurl"})
        for mirror in mirrors:
            res = mirror.find('strong')
            print("[ "+res.text+" ]")
            textbox.send_keys("[ "+res.text+" ]")
            textbox.send_keys(Keys.SHIFT+Keys.ENTER)
            links = mirror.findAll('a')
            for link in links:
                
                try:
                    shortlink = s.bitly.short(link.get('href'))
                    print(link.text+" = "+shortlink)
                    textbox.send_keys(link.text+" = "+shortlink)
                    textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                except:
                    print ("-")
                    textbox.send_keys("-")
                    textbox.send_keys(Keys.SHIFT+Keys.ENTER)

    elif "/movies/" in session_url[sender_name]:
        # SEND JUDUL
        judulbatch = animemain.find('div', {"class": "entry-content"}).find('p')
        textbox.send_keys(judulbatch.text)
        textbox.send_keys(Keys.SHIFT+Keys.ENTER)
        textbox.send_keys(Keys.ENTER)

        # SEND SINOPSIS
        sinopsis = animemain.find('div', {"itemprop": "description"}).findAll('p')
        if "*" in sinopsis[1].text:
            print("SINOPSIS")
            textbox.send_keys("SINOPSIS")
            textbox.send_keys(Keys.SHIFT+Keys.ENTER)
            print(sinopsis[2].text)
            textbox.send_keys(sinopsis[2].text)
            textbox.send_keys(Keys.SHIFT+Keys.ENTER)
            textbox.send_keys(Keys.ENTER)
        else:
            print (sinopsis[1])
            textbox.send_keys(sinopsis[1].text)
            textbox.send_keys(Keys.SHIFT+Keys.ENTER)
            textbox.send_keys(Keys.ENTER)

        # SEND JUDUL DOWNLOAD
        jdownload = animemain.find('div', {"class": "entry-content"}).findNext('div', {"class": "entry-content"})
        print(jdownload.text)
        textbox.send_keys(jdownload.text)
        textbox.send_keys(Keys.SHIFT+Keys.ENTER)

        # SHOW MIRROR LIST
        rawmirrors = animemain.find('div', {"class": "entry-content"}).findNext('div', {"class": "entry-content"}).findNext('div').find('ul')
        for mirrors in rawmirrors.findAll('li'):
            file = mirrors
            if file.text == "MP4":
                print ("==========["+file.text+"]==========")
                textbox.send_keys("==========["+file.text+"]==========")
                textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                for mirror in rawmirrors.findAll('ul'):
                    if mirror.find('li').find('label').text[0:3] == "MKV":
                        pass
                    else:
                        print ("["+mirror.find('label').text+"]")
                        textbox.send_keys("[ "+mirror.find('label').text+"]")
                        textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                        for linkmirror in mirror.findAll('a'):
                            print (linkmirror.text+": ")
                            textbox.send_keys(linkmirror.text+": ")
                            link = linkmirror
                            if link == None:
                                print ("-")
                                textbox.send_keys("-")
                                textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                                continue
                            try:
                                shortlink = s.bitly.short(link.get('href'))
                                print (shortlink)
                                textbox.send_keys(shortlink)
                                textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                            except:
                                print ("-")
                                textbox.send_keys("-")
                                textbox.send_keys(Keys.SHIFT+Keys.ENTER)

            if file.text == "MKV":
                print ("==========["+file.text+"]==========")
                textbox.send_keys("==========["+file.text+"]==========")
                textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                for mirrors in file.find_next_siblings('ul'):
                    print ("["+mirror.find('label').text+"]")
                    textbox.send_keys("["+mirror.find('label').text+"]")
                    textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                    for linkmirror in mirror.findAll('a'):
                        print (linkmirror.text)
                        textbox.send_keys(linkmirror.text+": ")
                        link = linkmirror
                        if link == None:
                            print ("-")
                            textbox.send_keys("-")
                            textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                            continue
                        try:
                            shortlink = s.bitly.short(link.get('href'))
                            print (shortlink)
                            textbox.send_keys(shortlink)
                            textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                        except:
                            print ("-")
                            textbox.send_keys("-")
                            textbox.send_keys(Keys.SHIFT+Keys.ENTER)

    elif "/episode/" in session_url[sender_name] or "/tvshows/" in session_url[sender_name] or "/?s=" in session_url[sender_name]:
        # FIND TITLE THEN SHOW IT
        judul = animemain.find('h2', {"class": "css3 link-download"})
        print(judul.text)
        textbox.send_keys(judul.text)
        textbox.send_keys(Keys.SHIFT+Keys.ENTER)
        textbox.send_keys(Keys.ENTER)

         # SHOW DESC
        desc = animemain.find("div", itemprop="description")
        print("SINOPSIS")
        textbox.send_keys("SINOPSIS")
        textbox.send_keys(Keys.SHIFT+Keys.ENTER)
        for des in desc.findAll("p"):
            if des.text[0:9] == "Streaming":
                continue
            else:
                print (des.text)
                textbox.send_keys(des.text)
                textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                textbox.send_keys(Keys.ENTER)

            # SHOW MIRROR LIST
        rawmirrors = judul.find_next('div').find('ul')
        for mirrors in rawmirrors.findAll('li'):
            file = mirrors
            if file.text == "MP4":
                print ("==========["+file.text+"]==========")
                textbox.send_keys("==========["+file.text+"]==========")
                textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                for mirror in rawmirrors.findAll('ul'):
                    if mirror.find('li').find('label').text[0:3] == "MKV":
                        pass
                    else:
                        print ("["+mirror.find('label').text+"]")
                        textbox.send_keys("[ "+mirror.find('label').text+"]")
                        textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                        for linkmirror in mirror.findAll('a'):
                            print (linkmirror.text+": ")
                            textbox.send_keys(linkmirror.text+": ")
                            link = linkmirror
                            if link == None:
                                print ("-")
                                textbox.send_keys("-")
                                textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                                continue
                            try:
                                shortlink = s.bitly.short(link.get('href'))
                                print (shortlink)
                                textbox.send_keys(shortlink)
                                textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                            except:
                                print ("-")
                                textbox.send_keys("-")
                                textbox.send_keys(Keys.SHIFT+Keys.ENTER)

            if file.text == "MKV":
                print ("==========["+file.text+"]==========")
                textbox.send_keys("==========["+file.text+"]==========")
                textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                for mirrors in file.find_next_siblings('ul'):
                    print ("["+mirror.find('label').text+"]")
                    textbox.send_keys("["+mirror.find('label').text+"]")
                    textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                    for linkmirror in mirror.findAll('a'):
                        print (linkmirror.text)
                        textbox.send_keys(linkmirror.text+": ")
                        link = linkmirror
                        if link == None:
                            print ("-")
                            textbox.send_keys("-")
                            textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                            continue
                        try:
                            shortlink = s.bitly.short(link.get('href'))
                            print (shortlink)
                            textbox.send_keys(shortlink)
                            textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                        except:
                            print ("-")
                            textbox.send_keys("-")
                            textbox.send_keys(Keys.SHIFT+Keys.ENTER)


    else:
        print("it on except "+x)
        print("ERROR POST NOT FOUND")


def to_anime(x):
    anime(x)

####################################################################################

# TIME TO SCAN QR CODE
time.sleep(10)

# IT S A DUMMY TO FIX AUTO READ WHATSAPP
namelist = ["Yusa"]
def dummy():
    getsearchbox = driver.find_element_by_xpath("//div[@id='side']/div/div/label/div/div[position()=last()]")
    getsearchbox.click()
    print("GETTING SEARCHBOX")

    getsearchbox.send_keys("Yusa")
    print("SEND KEYS YUSA")

    #_3GYfN
    #dummy = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid = 'cell-frame-container']"))).click()
    time.sleep(1)
    #dummy = driver.find_elements_by_xpath("//div[@data-testid = 'cell-frame-container']")[-1]
    dummy = driver.find_elements_by_xpath("//span[@title = 'Yusa']")[-1]
    print("YUSA FOUND")
    dummy.click()
    print("CLICKED ON YUSA")
    back = driver.find_element_by_xpath("//div[@id='side']/div/div/button")
    back.click()
    print("clicked back")

def idle():
    global command
    global sender_name
    while(1):
        for name in namelist:
            
            # Check if there is any unread message
            unreadMsgs=False

            getlist=driver.find_elements_by_xpath("//div[@data-testid='cell-frame-container']/div[2]/div[2]/div[2]/span/div")
            if(len(getlist)):
                unreadMsgs=True
                print("its true")
            
            # If there is no unread message, then click on back in the search bar
            if not unreadMsgs:
                continue
            
            # If an unread message exists, reply to the contact
            else:
                # Click on the Chat
                user=driver.find_elements_by_xpath("//div[@data-testid='cell-frame-container']/div[2]/div[2]/div[2]/span/div")[-1]
                user.click()

                #GET THE NAME OF SENDER
                try:
                    sender_name = driver.find_element_by_xpath("//div[@id='main']/div[position()=last()-2]/div/div/div[position()=last()-1]/div[position()=last()]/div/div/div/div[1]/span").text
                except:
                    sender_name = driver.find_element_by_xpath("//header/div[2]/div/div/span").text

                #GET LAST MESSAGE THEN DEFINE IT AS COMMAND
                command = driver.find_elements_by_xpath("//div[@class='_1Gy50']")[-1].text
                #TRYYY NUMBA
                try:
                    command = int(command[1:])
                except:
                    print("fail")
                print(sender_name+" is sending "+str(command))


                if command == "/help":
                    reply()
                    textbox=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div/div/div[2]')
                    
                    textbox.send_keys("=====[ALL COMMAND]=====")
                    textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                    textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                    textbox.send_keys("/anime | Show latest anime list")
                    textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                    textbox.send_keys("/batch | Show anime batch list")
                    textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                    textbox.send_keys("/movie | Show anime movie list")
                    textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                    textbox.send_keys("/genre | Show anime genre list")
                    textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                    textbox.send_keys("/search (name) | Find anime specifically")
                    textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                    textbox.send_keys("/(number) | Select anime from list")
                    textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                    textbox.send_keys("/page (number) | Select page from pagelist")
                    textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                    textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                    textbox.send_keys("=====[UPDATE SOON]=====")
                    textbox.send_keys(Keys.SHIFT+Keys.ENTER)

                    send=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]/button')
                    send.click()
                    dummy()

                elif command == "/anime":
                    reply()
                    anime("https://neonime.live/episode/")
                    
                    # Send Message
                    send=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]/button')
                    send.click()
                    # Print in contact name in the terminal
                    print(name,"texted you!")
                    dummy()

                elif command == "/movie":
                    reply()
                    anime("https://neonime.live/movies/")
                    
                    # Send Message
                    send=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]/button')
                    send.click()
                    # Print in contact name in the terminal
                    print(name,"texted you!")
                    dummy()

                elif command == "/batch":
                    reply()
                    anime("https://neonime.live/batch/")
                    
                    # Send Message
                    send=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]/button')
                    send.click()
                    # Print in contact name in the terminal
                    print(name,"texted you!")
                    dummy()
                    
                elif command == "/genre":
                    reply()
                    anime("https://neonime.live/")

                    # Send Message
                    send=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]/button')
                    send.click()

                    dummy()

                elif type(command) == int:
                    reply()
                    if sender_name in session_url:
                        selectanimes(command)

                        # Send Message
                        send=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]/button')
                        send.click()
                        dummy()
                    else:
                        dummy()

                elif command[0:5] == "/page":
                    reply()
                    if sender_name in session_url:
                        selectpage(command)

                        # Send Message
                        send=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]/button')
                        send.click()
                        dummy()
                    else:
                        dummy()

                elif command[0:7] == "/search":
                    reply()
                    search = command[8:]
                    url = "https://neonime.live/?s="+search
                    anime(url)

                    # Send Message
                    send=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]/button')
                    send.click()
                    dummy()

                elif command[0:6] == "/price":
                    reply()
                    rawurl = command[7::]
                    jmlh = 5

                    if '-l' in command:
                        jmlh = int(command[-2::])
                        rawurl = command[7:-5]

                    url = "https://www.tokopedia.com/search?goldmerchant=true&official=true&rt=4%2C5&shop_tier=3&source=universe&st=product&q="+rawurl


                    pricesearch(url, jmlh)
                    dummy()

                elif '/sfw' in command:
                    if '/sfw' == command:
                        reply()
                        textbox=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div/div/div[2]')
                        textbox.send_keys("waifu, neko, shinobu, megumin, bully, cuddle, cry, hug, awoo, kiss, lick, pat, smug, bonk. yeet, blush, smile, wave, highfive, handhold, nom, bite, glomp, slap, kill, kick, happy, wink, poke, dance, cringe")

                        # Send Message
                        send=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]/button')
                        send.click()
                        dummy()
                    else:
                        sfw_category = command[5:]
                        try:
                            url = sfw[('sfw_'+sfw_category)]
                            raw_img_url = requests.get(url).json()
                            img_url = raw_img_url['url']
                            
                            reply()
                            animeimg(img_url)
                            dummy()
                            
                        except:
                            reply()
                            textbox=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div/div/div[2]')
                            textbox.send_keys("masukan sfw yang tepat. ketik /sfw untuk melihat list")

                            # Send Message
                            send=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]/button')
                            send.click()
                            dummy()

                elif command[0] == "/":
                    reply()
                    textbox=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div/div/div[2]')
                    textbox.send_keys("wrong command")

                    # Send Message
                    send=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]/button')
                    send.click()
                    dummy()




                else:
                    dummy()
        
        # The code will run again after 

def pricesearch(x, jmlh):
    textbox=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div/div/div[2]')
    

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(x)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    judul = []
    rawsjudul = driver.find_elements_by_xpath('//div[@class="css-1f4mp12"]')[4::]
    for rawjudul in rawsjudul:  
        judul.append(rawjudul.text)

    price = []
    rawsprice = driver.find_elements_by_xpath('//div[@class="css-7fmtuv"]/a/div[@class="css-rhd610"]')[4::]
    for rawprice in rawsprice:
        price.append(rawprice.text)

    rate = []
    rawsrate = driver.find_elements_by_xpath('//span[@class="css-etd83i"]')[4::]
    for rawrate in rawsrate:
        rate.append(rawrate.text)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    for i in range(jmlh):
        try:
            textbox.send_keys(judul[i])
            textbox.send_keys(Keys.SHIFT+Keys.ENTER)
            textbox.send_keys("=> "+price[i])
            textbox.send_keys(Keys.SHIFT+Keys.ENTER)
        except:
            break

    textbox.send_keys(Keys.ENTER)


def animeimg(x):
    url = x
    print(url)
    if url[-3:] == 'gif':
        with open(r'E:\Project\python\2021\imgtopdf\result\result.gif', 'wb') as f:
            f.write(requests.get(url).content)

        clip = mp.VideoFileClip(r'E:\Project\python\2021\imgtopdf\result\result.gif')
        clip.write_videofile(r'E:\Project\python\2021\imgtopdf\result\result.mp4')

        driver.find_element_by_xpath("//span[@data-icon='clip']").click()
        inputer = driver.find_element_by_xpath("//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']")
        inputer.send_keys(r'E:\Project\python\2021\imgtopdf\result\result.mp4')

    else:
        print("downloading")
        image1 = Image.open(requests.get(url, stream=True).raw)
        print("downloaded")
        im1 = image1.convert('RGB')
        print("converted")
        im1.save(r'E:\Project\python\2021\imgtopdf\result\result.jpg')
        driver.find_element_by_xpath("//span[@data-icon='clip']").click()
        inputer = driver.find_element_by_xpath("//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']")
        inputer.send_keys(r'E:\Project\python\2021\imgtopdf\result\result.jpg')


    send = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@data-testid='send']")))
    send.click()

sfw = {
    'sfw_waifu' : 'https://api.waifu.pics/sfw/waifu',
    'sfw_neko' : 'https://api.waifu.pics/sfw/neko',
    'sfw_shinobu' : 'https://api.waifu.pics/sfw/shinobu',
    'sfw_megumin' : 'https://api.waifu.pics/sfw/megumin',
    'sfw_bully' : 'https://api.waifu.pics/sfw/bully',
    'sfw_cuddle' : 'https://api.waifu.pics/sfw/cuddle',
    'sfw_cry' : 'https://api.waifu.pics/sfw/cry',
    'sfw_hug' : 'https://api.waifu.pics/sfw/hug',
    'sfw_awoo' : 'https://api.waifu.pics/sfw/awoo',
    'sfw_kiss' : 'https://api.waifu.pics/sfw/kiss',
    'sfw_lick' : 'https://api.waifu.pics/sfw/lick',
    'sfw_pat' : 'https://api.waifu.pics/sfw/pat',
    'sfw_smug' : 'https://api.waifu.pics/sfw/smug',
    'sfw_bonk' : 'https://api.waifu.pics/sfw/bonk',
    'sfw_yeet' : 'https://api.waifu.pics/sfw/yeet',
    'sfw_blush' : 'https://api.waifu.pics/sfw/blush',
    'sfw_smile' : 'https://api.waifu.pics/sfw/smile',
    'sfw_wave' : 'https://api.waifu.pics/sfw/wave',
    'sfw_highfive' : 'https://api.waifu.pics/sfw/highfive',
    'sfw_handhold' : 'https://api.waifu.pics/sfw/handhold',
    'sfw_nom' : 'https://api.waifu.pics/sfw/nom',
    'sfw_bite' : 'https://api.waifu.pics/sfw/bite',
    'sfw_glomp' : 'https://api.waifu.pics/sfw/glomp',
    'sfw_slap' : 'https://api.waifu.pics/sfw/slap',
    'sfw_kill' : 'https://api.waifu.pics/sfw/kill',
    'sfw_kick' : 'https://api.waifu.pics/sfw/kick',
    'sfw_happy' : 'https://api.waifu.pics/sfw/happy',
    'sfw_wink' : 'https://api.waifu.pics/sfw/wink',
    'sfw_poke' : 'https://api.waifu.pics/sfw/poke',
    'sfw_dance' : 'https://api.waifu.pics/sfw/dance',
    'sfw_cringe' : 'https://api.waifu.pics/sfw/cringe'}


# DICT TO MAKE TEMP SESSION
session_url = {}
session_category = {}
surl = "None"
idle()

driver.Close()