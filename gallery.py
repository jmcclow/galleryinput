#!/usr/bin/python
import ConfigParser
import time
import math, operator 
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from getpass import getpass
import urllib
from collections import defaultdict
import re
import os

def find_images(path):
    return os.listdir(path)

def get_names(filename):
    names = defaultdict(str)
    f = open(filename)
    number = ''
    name = ''
    for line in f:
        match = re.search('--', line)
        if match:
            names[number] = name
            number = '' 
            name = ''
        elif re.search('^\d+', line):
            number = line.strip()
        else:
            if name == '':
                name = line.strip() + ' '
            else:
                name += line.strip() + ' '

    return names
    f.close()        


if __name__ == '__main__':
    config = ConfigParser.RawConfigParser()
    config.read('finest.cfg')
    inf = 'names.txt'
    name_to_num = get_names(inf)
    url_to_slurp = config.get('source', 'url')
    url_to_login = config.get('source', 'login')
    username = config.get('source', 'user')
    password = getpass() 
    igid = raw_input("Please enter igid: ") 
    browser = webdriver.Firefox()
    browser.get(url_to_login)
    user = browser.find_element_by_name("username")
    user.send_keys(username)
    passwd = browser.find_element_by_name("password")
    passwd.send_keys(password + Keys.RETURN)
    time.sleep(1)
    print "Going to " + url_to_slurp + igid
    browser.get(url_to_slurp + igid)
    time.sleep(9)
    photo_id = 0 
    try:
        element = browser.find_element_by_xpath("//html/body/div/div/form/div")
        photo_id = int(element.get_attribute('id'))
    except:
        print "Oh oh that was bad..."
    img_url = str("http://imgs.sthlmsfinest.com/imageGalleryImages/scaled/" + str(photo_id) + "_102_73_1.jpg") 
    print "Getting " + img_url 
    while ( 1 ):
        urllib.urlretrieve(img_url, str(photo_id) + '.jpg')
        image1 = Image.open(str(photo_id) + '.jpg')
        images = find_images('thumbnails')
        print images[0]
        image2 = Image.open(str('thumbnails/' + images[1]))
        h1 = image1.histogram()
        h2 = image1.histogram()
        rms = math.sqrt(reduce(operator.add,
            map(lambda a,b: (a-b)**2, h1, h2))/len(h1))
        print rms
        break
#        try: 
#            e = browser.find_element_by_name("imageDescription[" + photoid + "]")
#            e.send_keys("Description")
#        except:
#            print "Sorry couldn't find that element " + str(photoid)
#        try:
#            e = browser.find_element_by_value("Spara")
#            e.submit()
#        except:
#            print "Couldn't find submit button"
#            # Do phash on this image to what we have
#            photo_id += 1
#            img_url = "http://imgs.sthlmsfinest.com/imageGalleryImages/scaled/" + str(photo_id) + "_102_73_1.jpg" 
    browser.close()
