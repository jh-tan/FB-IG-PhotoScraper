import os
import shutil
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys

BASE_IG_URL = 'https://www.instagram.com'
BASE_FB_URL = 'https://www.facebook.com'
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('start-maximized')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--incognito')
# chrome_options.add_argument('--headless')
DRIVER = webdriver.Chrome("/usr/bin/chromedriver",options = chrome_options,desired_capabilities=caps)


class Scraper:
	def __init__(self,target, username = None ,password = None):
		self.username = username
		self.password = password
		self.target = target
		self.image_list = []
	
	def ig_Login(self):
		DRIVER.get(BASE_IG_URL)
		WebDriverWait(DRIVER,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input._2hvTZ.pexuQ.zyHYP[type='text']"))).send_keys(self.username)
		WebDriverWait(DRIVER,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input._2hvTZ.pexuQ.zyHYP[type='password']"))).send_keys(self.password)
		WebDriverWait(DRIVER,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.sqdOP.L3NKy.y3zKF"))).click()
		WebDriverWait(DRIVER,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.aOOlW.HoLwm"))).click()
		self.go_to_instagram_target()

	def fb_Login(self):
		DRIVER.get(BASE_FB_URL)
		WebDriverWait(DRIVER,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.inputtext._55r1._6luy[type='text']"))).send_keys(self.username)
		WebDriverWait(DRIVER,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.inputtext._55r1._6luy._9npi[type='password']"))).send_keys(self.password)
		WebDriverWait(DRIVER,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button._42ft._4jy0._6lth._4jy6._4jy1.selected._51sy"))).click()
		time.sleep(5)
		self.go_to_facebook_target()

	def go_to_instagram_target(self):
		profile_url = BASE_IG_URL+'/'+self.target
		DRIVER.get(profile_url)

	def go_to_facebook_target(self):
		profile_url = self.target
		DRIVER.get(profile_url)
	
	def download_IG_img(self):
		timeout = 0
		i = 0
		previous_length = int(len(self.image_list))
		target_total_posts = int(WebDriverWait(DRIVER,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"span.g47SY"))).text.replace(",",""))
		soup = BeautifulSoup(DRIVER.page_source,'html.parser')
		img = soup.findAll('img',attrs={'class':'FFVAD'})
		print("Start scraping")
		for x in img:
			self.image_list.append(x['src'])
		
		if(int(len(self.image_list)) >= target_total_posts):
			return self.save_to_local()
		
		total_scroll = int(target_total_posts) - len(img) // 12
		DRIVER.execute_script('window.scrollTo(0, document.body.scrollHeight);')

		time.sleep(2)
		for x in range(total_scroll):
			try:
				soup = BeautifulSoup(DRIVER.page_source,'html.parser')
				div_to_img = soup.find_all('div',attrs={'class':'KL4Bh'})

				for idx, x in enumerate(div_to_img):
					img_link = x.next['src']
					if img_link not in self.image_list:
						i += 1
						print(i,' images scraped')
						self.image_list.append(img_link)
				new_length = int(len(self.image_list))

				if(int(len(self.image_list)) >= target_total_posts):
					print("Finish scraping")
					return self.save_to_local()
				elif(new_length == previous_length):
					print("Timeout ",timeout)
					time.sleep(60 + timeout * 10)
					timeout += 1
				else:
					previous_length = new_length

				if(timeout >= 15):
					print("Something Happen,returning ",new_length," collected images")
					return self.save_to_local()

				DRIVER.execute_script('window.scrollTo(0, document.body.scrollHeight);')
				time.sleep(5)
			except KeyboardInterrupt:
				return self.save_to_local()
				
		return self.save_to_local()
	
	def download_FB_img(self):
		time.sleep(3)
		DRIVER.execute_script('window.scrollTo(0, document.body.scrollHeight/7);')
		soup = BeautifulSoup(DRIVER.page_source,'html.parser')
		old_img = soup.find('img',attrs={'class':'ji94ytn4 r9f5tntg d2edcug0 r0294ipz'})
		element = DRIVER.find_elements_by_css_selector("a.oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.a8c37x1j.p7hjln8o.kvgmc6g5.cxmmr5t8")
		element[2].click()
		print("Start scraping")
		i = 0
		while(True):
			try:
				soup = BeautifulSoup(DRIVER.page_source,'html.parser')
				new_img = soup.find('img',attrs={'class':'ji94ytn4 r9f5tntg d2edcug0 r0294ipz'})
				if(old_img == new_img):
					continue
				else:
					pass
					if(new_img['src'] not in self.image_list):
						i += 1
						print(i,' images scraped')
						self.image_list.append(new_img['src'])
						old_img = new_img
						# Method 1
						# element = DRIVER.find_elements_by_css_selector("div.oajrlxb2.gs1a9yip.g5ia77u1.mtkw9kbi.tlpljxtp.qensuy8j.ppp5ayq2.goun2846.ccm00jje.s44p3ltw.mk2mc5f4.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.nhd2j8a9.pq6dq46d.mg4g778l.btwxx1t3.pfnyh3mw.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.tgvbjcpo.hpfvmrgz.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.l9j0dhe7.i1ao9s8h.esuyzwwr.f1sip0of.du4w35lb.lzcic4wl.abiwlrkh.p8dawk7l.datstx6m")
						# DRIVER.execute_script("arguments[0][1].click();", element) 
						# Method 2
						# element = DRIVER.find_elements_by_css_selector("i.hu5pjgll.lzf7d6o1")
						# DRIVER.execute_script("arguments[0][4].click();", element) 
						# Method 3
						WebDriverWait(DRIVER,1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body._6s5d._71pn._-kb"))).send_keys(Keys.ARROW_RIGHT)
					else:
						return self.save_to_local()
			except TypeError:
				pass
			except KeyboardInterrupt:
				return self.save_to_local()
		return self.save_to_local()
	
	def download_FB_img_alt(self):
		previous_length = int(len(self.image_list))
		timeout = 0
		i = 0

		try:
			print("Start scraping")
			while(True):
				soup = BeautifulSoup(DRIVER.page_source,'html.parser')
				img = soup.find_all('img')
				for idx, x in enumerate(img):
					img_link = x['src']
					if img_link not in self.image_list:
						self.image_list.append(img_link)
						i += 1
						print(i,' images scraped')
				new_length = int(len(self.image_list))
				if(new_length == previous_length):
					timeout += 1
					print("Timeout ",timeout)
					DRIVER.execute_script('window.scrollTo(document.body.scrollHeight, document.body.scrollHeight/2);')
					time.sleep(60 + timeout * 10)
				else:
					previous_length = new_length

				if(timeout >= 15):
					print("Something Happen or reached end of photos,returning ",new_length," collected images")
					return self.save_to_local()

				DRIVER.execute_script('window.scrollTo(0, document.body.scrollHeight);')
				time.sleep(10)

		except KeyboardInterrupt:
			return self.save_to_local()

	def save_to_local(self):
		DRIVER.	quit()
		folderName = input("Create new folder name :")
		counter = 1
		path = os.getcwd()
		path = os.path.join(path,folderName)
		if os.path.exists(path):
			shutil.rmtree(path)
		os.makedirs(path)
		for idx,x in enumerate(self.image_list):
			print('Downloading image {0} of {1}'.format(idx + 1, len(self.image_list)))
			try:
				save_as = os.path.join(path,folderName + str(counter) +'.jpg')
				with open(save_as,'wb') as f:
					im = requests.get(x)
					f.write(im.content)
				counter += 1
			except:
				print("This image is invalid")