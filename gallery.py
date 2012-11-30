#!/usr/bin/python
import ConfigParser
import time
import math, operator 
import Image
import numpy
import sys
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
    photo_url = config.get('source', 'photo_url')
    suffix = config.get('source', 'suffix')
    password = getpass() 
    igid = raw_input("Please enter igid: ") 
    browser = webdriver.Firefox()
    browser.get(url_to_login)
    user = browser.find_element_by_name("username")
    user.send_keys(username)
    passwd = browser.find_element_by_name("password")
    passwd.send_keys(password + Keys.RETURN)
    time.sleep(1)
    browser.get(url_to_slurp + igid)
    time.sleep(9)
    photo_id = 0 
    try:
        element = browser.find_element_by_xpath("//html/body/div/div/form/div")
        photo_id = int(element.get_attribute('id'))
    except:
        print "Oh oh that was bad..."
    image_url = str(photo_url + str(photo_id) + suffix) 
    print "Getting " + image_url 
    while ( 1 ):
        urllib.urlretrieve(image_url, str(photo_id) + '.jpg')
        image1 = Image.open(str(photo_id) + '.jpg')
        images = find_images('thumbnails')
        h1 = image1.histogram()
        for i in images:
            image2 = Image.open(str('thumbnails/' + i))
            h2 = image1.histogram()
            s = 0
            if image1.size != image2.size or image1.getbands() != image2.getbands():
                break 
            for band_index, band in enumerate(image1.getbands()):
                m1 = numpy.fft.fft2(numpy.array([p[band_index] for p in image1.getdata()]).reshape(*image1.size))
                m2 = numpy.fft.fft2(numpy.array([p[band_index] for p in image2.getdata()]).reshape(*image2.size))
                s += numpy.sum(numpy.abs(m1-m2))
            print s
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
#            image_url = "http://images.sthlmsfinest.com/imageGalleryImages/scaled/" + str(photo_id) + "_102_73_1.jpg" 
    browser.close()
