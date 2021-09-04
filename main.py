import getpass
from Scraper.PhotoScraper import Scraper

if __name__ == "__main__":
		print("Photo Scraper")
		print("""Select from the following list:
1 : Instagram( Login Required )
2 : Facebook( Login Required ) **Please do not use your main account to scrape**
3 : Facebook( Without Login )
		""")
		selection = int(input('Scrape from: '))
		if(selection == 1):
			username = input('Username: ')
			password = getpass.getpass("Password: ")
			target = input('Target: ')
			scraper = Scraper(username = username, password = password,target = target)
			scraper.ig_Login()
			scraper.download_IG_img()
		elif(selection == 2):
			username = input('Username: ')
			password = getpass.getpass("Password: ")
			target = input('Target\' link: ')
			scraper = Scraper(username = username,password = password,target = target)
			scraper.fb_Login()

			version = int(input("Does the target have tagged photo?\n1. Yes\n2. No\n"))
			if(version == 1):
				scraper.download_FB_img()
			else:
				scraper.download_FB_img_alt()
		elif(selection == 3):
			target = input('Target\' link: ')
			scraper = Scraper(target)
			scraper.go_to_facebook_target()
			scraper.download_FB_img()