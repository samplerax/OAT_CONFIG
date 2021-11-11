# The OpenAstroTracker:
A cheap 3D printed tracking, GoTo and autoguiding mount for DSLR astrophotography.
[Website](https://openastrotech.com/)

## What is this?
A simple Python script to set-up your OAT mount in Linux environment. 

## How do I use it?
Put your mount RA and DEC axis in Home position:
[Usage](https://wiki.openastrotech.com/en/OpenAstroTracker/Usage)
Open terminal, and:
$ls /dev/tty* 
to display current USB devices, connect OAT and notice port name, navigate to script directory and: 
$python3 config.py
Enter correct port when asked.

## What are the prerequisites?
Python v3 or higher.

## What settings are set by this script?
Set Site Latitude (manual input)
Set Site Longitude (manual input)
Set Site Local Time (automatic, make sure system time is correct)
Set Site Local Date (automatic, make sure system time is correct)
Set Site UTC offset (automatic, make sure system time is correct)
Try to autohome RA axis
Set Home position current mount orientation

## Is there something to customize?
You can set your Home Coordinates to not have to enter them manually every time.
Enter you coordinates instead of 01*01 here:

```
    print("Home Site LAT is 01*01")     # Show your Home Latitude in DM (DegreesMinutes) format
    LAT_SIGN = "+01*01"                 # Enter your Latitude + for northern Hemisphere - for South
    LONG = "01*01"                      # Enter your Longitude in DM (DegreesMinutes) format
```