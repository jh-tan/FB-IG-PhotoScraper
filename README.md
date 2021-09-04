# FB-IG-PhotoScraper

As the name says, it can be used to scrape the photo from Facebook and Instagram. 

<h2>Dependencies</h2>
To run it, you need Python 3.x on your system and a few other python packages. The required python packages can simply install through pip.

 1. Selenium
 2. Requests
 3. BeautifulSoup

<h2> Instruction </h2>

 1. Simply run from the main.py. Once the program started,  the main menu will be prompted in the terminal / console and an empty chrome browser will popout.
 2. Then, 3 choices will be shown on the screen, which are:
	 a. Instagram( Login Required )
	 b. Facebook( Login Required ) **Please do not use your main account to scrape**
	 c. Facebook( Without Login )
 3. Choose either one. If you choose ( a ) or ( b ). Then you will have to enter your username and password.
 4. Next, enter your scrape's target. For instagram, simply enter the profile name. The profile must be public or followed by you.
 5. For facebook, instead of enter the profile name, you have to enter the link. Then, it will ask if the target has tagged photo. How to know if the target has tagged photo is by observing the URL. If the URL end with ' ?ref=page_internal ', then choose **No**
 6. You can stop anytime by CTRL + C , and it will return all the scraped photos.

<h2>Limitation</h2>

 1. Facebook photo currently only support page photo.
 2. Any Two-factor Authentication must be turned off.
 3. Does not support video scraping.
 4. Minimize the browser will cause error.
 5. **Never** use your main account to scrape facebook photo, because it will  can trigger facebook to disable your account with the reason of not following the Community Standards.
 6. Facebook and  Instagram code tends to change from time to time, so some adjustment may be needed if the code changes.
