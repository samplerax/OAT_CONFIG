# The OpenAstroTracker:
A cheap 3D printed tracking, GoTo and autoguiding mount for DSLR astrophotography.<br />
[Website](https://openastrotech.com/)<br />

## What is this?
A simple Python script to set-up your OAT mount in Linux environment. <br />

## How do I use it?
Put your mount RA and DEC axis in Home position:<br />
[Usage](https://wiki.openastrotech.com/en/OpenAstroTracker/Usage)<br />
Open terminal, and:<br />
$ls /dev/tty* <br />
to display current USB devices, connect OAT and notice port name, navigate to script directory and: <br />
$python3 config.py<br />
Enter correct port when asked.<br />

## What are the prerequisites?
Python v3 or higher.<br />

## What settings are set by this script?
Set Site Latitude (manual input)<br />
Set Site Longitude (manual input)<br />
Set Site Local Time (automatic, make sure system time is correct)<br />
Set Site Local Date (automatic, make sure system time is correct)<br />
Set Site UTC offset (automatic, make sure system time is correct)<br />
Try to autohome RA axis<br />
Set Home position current mount orientation<br />

## Is there something to customize?
You can set your Home Coordinates to not have to enter them manually every time.<br />
Enter you coordinates instead of 01*01 here:<br />

```
    print("Home Site LAT is 01*01")     # Show your Home Latitude in DM (DegreesMinutes) format
    LAT_SIGN = "+01*01"                 # Enter your Latitude + for northern Hemisphere - for South
    LONG = "01*01"                      # Enter your Longitude in DM (DegreesMinutes) format
```