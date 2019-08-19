# Morse 

### Inspect a directory full of images and assign Good/Bad/Maybe classes to each

## Setup
1. Put images to inspect in a directory somewhere
2. Create a csv file (e.g. mytgts.csv) with at least a column named 'ID'. These IDs should be in the filenames of the images you want to inspect. Morse will do a double wildcard search for filenames that include ID. 
Example: 
For ID = 1234567, Morse would list /path/to/images/*1234567*.png, which should hopefully return  myfavoritestar_tic1234567_isawesome.png. 
Note it's probably best to use the full 0 padded tic number (length 16), so: ID = '0000000001234567', in case the wildcard search gets confused.
3. Inspect the images by
```
$ python morse.py /path/to/mytgts.csv /dir/with/myimages
```
Use the ```--shuffle``` option to shuffle the targetlist. 

Morse will create a column in mytgts.csv that will contain the verdict code corresponding to which button you press. The choices are:
- _G_ood = 2
- _M_aybe = 1
- _B_ad = 0
- _I_nteresting = 3

Buttons are hotkeyed to underscored characters.

All targets are initially assigned Unclassified = -1. Any targets that Morse cannot find an image for will remain unclassified (-1). There is also the option to just skip the image, in which case Morse will just assign -1. 

**Morse will pick up where you left off.**

Morse writes to the CSV file every time you press one of the options, so if you close the inspection window and reopen it later, it will just find the next unclassified target in the list. 

## What do the verdict codes mean?
- Good: Oscillation spectrum clearly shows excess, or 2DACF produces a clear peak in numax collapsogram for example.
- Maybe: Same as above, but to a less certain degree. Cases where better reduction could potentially produce better SNR
- Bad: no oscillations in spectrum or ACFs
- Interesting: If there is something strange going on with the target. For personal interest mainly, if you want to go back and have a look at the target in more detail.


