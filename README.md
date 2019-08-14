# Morse 

### Inspect a directory full of images and assign Good/Bad/Maybe classes to each

## Setup
1. Put images to inspect in a directory somewhere
2. Create a csv file (e.g. mytgts.csv) with at least a column named 'ID'. These IDs should be in the filenames of the images you want to inspect. Example: for myfavoritestar_tic1234567_isawesome.png, I would put 1234567 in the ID column of mytgts.csv.
3. Inspect the images by
$ python morse.py /path/to/mytgts.csv /dir/with/myimages

Morse will create a column in the csv that will contain the verdict code corresponding to which button you press. The choices are:
Good = 2
Maybe = 1
Bad = 0

All targets are initially assigned 
Unclassified = -1

Any targets that Morse cannot find an image for will remain unclassified (-1).
