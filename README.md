# airline-check-in
Collection of Python scripts using Selenium to check passengers into airlines

## Southwest Login

Visit https://github.com/iancleary/airline-check-in/blob/master/selenium_southwest.py

Download ChromeDriver for your OS: https://sites.google.com/a/chromium.org/chromedriver/downloads
- safest option is to make sure the chromedrive path is absolute
- see DEBUG flags in code

If on Windows:
- ensure that the you make a .bat file is correct (correct PATH user environment variable for folder, etc.)
- for task scheduler, ensure that you select the drop down for "Configure for: ' Windows 7, Windows ServerTM 2008 R2'" (the default is the oldest OS version...make sure that's right

Run the script 24 hours and 2 minutes before your flight. 
It will loop until Southwest allows passers to login.
The script logs in all users in simultaneously using parallel threads.

## Other Airlines
Development is halted until I have a use case for a scripted check in
