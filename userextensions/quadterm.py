#/usr/bin/python
#####################################################
# Creates 4 terminals evenly quartering a screen
#
# Linux only right now. Map it to a keystroke for 
# maximum convenience.
#
# If you don't want to use gnome-terminal, change the 
# next variable. Warning: The width and height 
# specified are in characters and rows for gnome-
# terminal; they might have to be in pixels for other 
# apps.
#####################################################
terminal = "gnome-terminal"
#####################################################
# If you are not using TwinView, toggle the following:
#####################################################
twinview = True
#####################################################
# Which monitor (if Dual) you want them on:
#####################################################
side = "right"
#####################################################
# Dir the terminals will be in:
#####################################################
workingdir = "~"
#####################################################
import commands 
# Get the screen dimensions:
dimeninfo = commands.getoutput("xdpyinfo | grep dimensions")
# Read out the needed numbers:
dimeninfosplit = dimeninfo.split()
dimensions = dimeninfosplit[1]
prex = dimensions.split("x")
x = int(prex[0])
prey = dimensions.split("x")
y = int(prey[1])
# Take some visual buffers into account:
widthsansborder = x - 50
heightsansborder = y - 50
# Calculate dimensions in pixels:
termwidthpixels = widthsansborder / 2
termheightpixels =  heightsansborder / 2
# Convert to characters/rows for most apps (like gnome-terminal).
# No idea what the conversion rate should be... 
termwidth = termwidthpixels / 20
termheight = termwidthpixels / 65 
# Constant width/height for all 4.
t1width = t2width = t3width = t4width = termwidth
t1height = t2height = t3height = t4height = termheight
# Find the offset position for appropriate pairs (in pixels):
t1posx = t3posx = 50
t2posx = t4posx = (50 * 2) + termwidthpixels
t1posy = t2posy = 50
t3posy = t4posy = 50 + termheightpixels
# If TwinView is being used, we need to halve some offsets:
if twinview is True:
    t2posx = (((50 * 2) + termwidthpixels) / 2)
    t4posx = (((50 * 2) + termwidthpixels) / 2)
    if side == "right":
        t1posx = 50 + (x / 2)
        t2posx = x * .75 
        t3posx = 50 + (x / 2)
        t4posx = x * .75
# Spawn the 4 terminals, with needed positions and sizes, then exit quietly:
commands.getoutput("%s --geometry=%dx%d+%d+%d --working-directory=%s" % \
    (terminal, t1width, t1height, t1posx, t1posy, workingdir))
commands.getoutput("%s --geometry=%dx%d+%d+%d --working-directory=%s" % \
    (terminal, t2width, t2height, t2posx, t2posy, workingdir))
commands.getoutput("%s --geometry=%dx%d+%d+%d --working-directory=%s" % \
    (terminal, t3width, t3height, t3posx, t3posy, workingdir))
commands.getoutput("%s --geometry=%dx%d+%d+%d --working-directory=%s" % \
    (terminal, t4width, t4height, t4posx, t4posy, workingdir))
# For debugging, print what we have calculated:
#print "%s at: %d x %d + %d + %d" % (terminal, t1width, t1height, t1posx, t1posy)
#print "%s at: %d x %d + %d + %d" % (terminal, t2width, t2height, t2posx, t2posy)
#print "%s at: %d x %d + %d + %d" % (terminal, t3width, t3height, t3posx, t3posy)
#print "%s at: %d x %d + %d + %d" % (terminal, t4width, t4height, t4posx, t4posy)
