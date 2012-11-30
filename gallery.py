#!/usr/bin/python
import ConfigParser
import time
import sys
import Image
import pHash
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
    photo_to_id = defaultdict(str)
    name_to_num = get_names(inf)
    url_to_slurp = config.get('source', 'url')
    url_to_login = config.get('source', 'login')
    username = config.get('source', 'user')
    photo_url = config.get('source', 'photo_url')
    password = getpass() 
    igid = raw_input("Please enter igid: ") 
    browser = webdriver.Firefox()
    browser.get(url_to_login)
    user = browser.find_element_by_name("username")
    user.send_keys(username)
    passwd = browser.find_element_by_name("password")
    passwd.send_keys(password + Keys.RETURN)
    browser.get(url_to_slurp + igid)
    photo_id = 0 
    end_id = 0
    try:
        element = browser.find_element_by_xpath("//html/body/div/div/form/div")
        orig_photo_id = int(element.get_attribute('id'))
    except:
        print "Oh oh that was bad..."
    photo_id = orig_photo_id
    while ( 1 ):
        image_url = str(photo_url + str(photo_id) + "_102_73_1.jpg") 
        try:
            e = browser.find_element_by_name('imageDescription[' + str(photo_id) + ']')
        except:
            print "We've reached all the images we could find"
            end_id = photo_id - 1
            break
        urllib.urlretrieve(image_url, str(photo_id) + '.jpg')
        image1 = Image.open(str(photo_id) + '.jpg')
        images = find_images('thumbnails')
        photo_id += 1
    photo_id = orig_photo_id
    for i in images:
        digest1 = pHash.image_digest(str(photo_id) + '.jpg', 1.0, 1.0, 180)
        digest2 = pHash.image_digest(str('thumbnails/' + i), 1.0, 1.0, 180)
        if pHash.crosscorr(digest1, digest2) == 1:
            if photo_id < end_id:
                photo_to_id[photo_id] = i
                photo_id += 1
    print name_to_num
    for ident in photo_to_id:
        repl = re.sub('IMG_', '', str(photo_to_id[ident]))
        photo_num = re.sub('.jpg', '', repl) 
        if name_to_num[photo_num]:
            try: 
                e = browser.find_element_by_name("imageDescription[" + str(ident) + "]")
                e.send_keys(name_to_num[photo_num])
            except:
                print "Sorry couldn't find that element " + str(ident)
        try:
            e = browser.find_element_by_value("Spara")
            e.submit()
        except:
            print "Couldn't find submit button"
            # Do phash on this image to what we have
            photo_id += 1
            image_url = "http://images.sthlmsfinest.com/imageGalleryImages/scaled/" + str(photo_id) + "_102_73_1.jpg" 
    browser.close()
