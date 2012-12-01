Some prereqs:
Run the following:
$ pip install -U selenium
$ wget http://www.phash.org/releases/pHash-0.9.5.tar.gz
$ tar xvfz pHash-0.9.5.tar.gz
$ cd pHash-0.9.5
$ ./configure
$ make
$ sudo make install

Pretty straight forward
===================================
Included things
File names and purposes
gallery.py - main script to be used to run the script
    - Requires PLIB 
    - Requires selenium and some driver, this instance uses Firefox driver
gallery.cfg - Where most of your information is stored, such as url, and username for the gallery login
names.txt - Names of files should be formated as such
    000001
    Name One
    Name Two 
    --
    000002
    Name One
    --
The two dashes at the end of the section deliminates the end of the names being entered

That's all for now
