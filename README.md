# Morse 

### Inspect a directory full of images and assign Good/Bad/Maybe classes to each

## Setup
1. Put images to inspect in a directory somewhere
2. Create a csv file (e.g. mytgts.csv) with at least a column named 'ID'. These IDs should be in the filenames of the images you want to inspect. Morse will do a double wildcard search for filenames that include ID. 
Example: 
For ID = 1234567, Morse would list /path/to/images/*1234567*.png, which should hopefully return  myfavoritestar_tic1234567_isawesome.png. 
Note it's probably best to use the full 0 padded tic number (length 16), so: ID = '0000000001234567', in case the wildcard search gets confused.
3. Inspect the images by
$ python morse.py /path/to/mytgts.csv /dir/with/myimages

Morse will create a column in the csv that will contain the verdict code corresponding to which button you press. The choices are:
- Good = 2
- Maybe = 1
- Bad = 0
- Interesting/weird = 3

All targets are initially assigned Unclassified = -1. Any targets that Morse cannot find an image for will remain unclassified (-1). There is also the option to just skip the image, in which case Morse will just assign -1. 

# MORSE WILL PICK UP WHERE YOU LEFT OFF.
Morse writes to the csv file every time you press one of the options, so if you close the inspection window and reopen it later, it will pick up where you left off. 
