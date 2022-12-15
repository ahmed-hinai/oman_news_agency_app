import os, certifi
os.environ['SSL_CERT_FILE'] = certifi.where()
import ssl
try:
	_create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
	# Legacy Python that doesn't verify HTTPS certificates by default
	pass
else:
	# Handle target environment that doesn't support HTTPS verification
	ssl._create_default_https_context = _create_unverified_https_context
os.environ['KIVY_IMAGE'] = 'pil,sdl2'
from kivy.config import Config
Config.read('ONA.ini')
Config.set('kivy', 'exit_on_escape', '0')
Config.setdefault('widgets', 'dark_switch.active', '0')
Config.setdefault('widgets', 'image_switch.active', '0')
Config.setdefault('widgets', 'english_switch.active', '0')
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.recycleview import RecycleView
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.base import EventLoop
from kivy.loader import Loader
from kivymd.utils import asynckivy
from kivy.config import Config
class LoadingGif(FloatLayout):
	text = StringProperty()


class infocard(ScrollView):
	text = StringProperty()
	def __init__(self, **kwargs):
		(super(infocard, self).__init__)(**kwargs)
		self.layout_content.bind(minimum_height=(self.layout_content.setter('height')))
class contactcard(ScrollView):
	text = StringProperty()
	def __init__(self, **kwargs):
		(super(contactcard, self).__init__)(**kwargs)
		self.layout_content.bind(minimum_height=(self.layout_content.setter('height')))


class DarkMode(FloatLayout):
	text = StringProperty()


class ConnectionError(BoxLayout):
	text = StringProperty()


class ContentNavigationDrawer(BoxLayout):
	screen_manager = ObjectProperty()
	nav_drawer = ObjectProperty()




class NewsCard(BoxLayout):
	content= ObjectProperty()
	text = StringProperty()
	secondary_text = StringProperty()
	link = StringProperty()
	title = StringProperty()

class NewsArticle(RecycleView):
	text = StringProperty()
	text1 = StringProperty()
	text2 = StringProperty()
	text3 = StringProperty()
	text4 = StringProperty()
	text5 = StringProperty()
	title = StringProperty()
	date = StringProperty()
	author = StringProperty()
	link = StringProperty()
	scroll_timeout = NumericProperty('250')

	def __init__(self, **kwargs):
		(super(NewsArticle, self).__init__)(**kwargs)
		self.layout_content.bind(minimum_height=(self.layout_content.setter('height')))


class NewsArticleWithImage(RecycleView):
	text = StringProperty()
	text1 = StringProperty()
	text2 = StringProperty()
	text3 = StringProperty()
	text4 = StringProperty()
	text5 = StringProperty()
	title = StringProperty()
	date = StringProperty()
	author = StringProperty()
	scroll_timeout = NumericProperty('250')
	image = StringProperty()
	link = StringProperty()

	def __init__(self, **kwargs):
		(super(NewsArticleWithImage, self).__init__)(**kwargs)
		self.layout_content.bind(minimum_height=(self.layout_content.setter('height')))


class MainApp(MDApp):
	x = NumericProperty(0)
	y = NumericProperty(0)

	def __init__(self, **kwargs):
		(super().__init__)(**kwargs)
		Loader.loading_image = 'loading.png'
		self.screen_list = ['scr 0', 'scr 1']
		EventLoop.window.bind(on_keyboard=(self.hook_keyboard))
	def build(self):
		self.screen = Builder.load_file('what.kv')
		return self.screen

	def on_start(self):
		self.refresh_callback()
		if self.screen.ids.dark_switch.active == True:
			self.theme_cls.theme_style = 'Dark'
			self.theme_cls.primary_palette = 'Red'
			self.theme_cls.primary_hue = '600'
			Config.set('widgets', 'dark_switch.active', '1')
		else:
			self.theme_cls.theme_style = 'Light'
			self.theme_cls.primary_palette = 'Red'
			self.theme_cls.primary_hue = '600'
			Config.set('widgets', 'dark_switch.active', '0')

	def on_pause(self):
		return True

	def on_resume(self):
		pass

	def amiactive(self):
		if Config.getint('widgets', 'dark_switch.active') == 1:
			return True
		return False

	def on_start_image(self):
		if self.screen.ids.image_switch.active == True:
			Config.set('widgets', 'image_switch.active', '1')
		else:
			Config.set('widgets', 'image_switch.active', '0')

	def amiactive_image(self):
		if Config.getint('widgets', 'image_switch.active') == 1:
			return True
		return False



	def screen_manager(self, name):
		ScreenManager = self.screen.ids.screen_manager
		self.screen_list.append(name)
		ScreenManager.current = name

	def to_screen1(self, *args):

		def to_screen1(interval):
			self.screen_manager('scr 1')

		Clock.schedule_once(to_screen1, 1)

	def hook_keyboard(self, window, key, *largs):
		if key == 27:
			if self.screen.ids.screen_manager.current == 'scr 0':
				MDApp.get_running_app().stop()
			else:
				if self.screen_list[-1] != 'scr 1' and self.screen_list[-1] != 'info' and self.screen_list[-1] != 'contact' and self.screen_list[-1]!= "settings":
					self.screen_manager(self.screen_list[-2])
				else:
					if self.screen_list[-1] == 'settings':
						self.screen_manager("scr 1")
					else:
						if self.screen_list[-1] == 'info' or self.screen_list[-1] == 'contact':
							self.screen_manager("settings")
						else:
							if self.screen.ids.nav_drawer.state == 'open':
								self.screen.ids.nav_drawer.set_state('closed')
							else:
								self.screen_manager('scr 0')

		else:
			pass

	def fix_text(self, text):
		import bidi.algorithm, arabic_reshaper, textwrap
		reshaped = arabic_reshaper.reshape(text)
		fixed_text = bidi.algorithm.get_display(reshaped)
		return fixed_text

	def fix__headline(self, text):
		import bidi.algorithm, arabic_reshaper, textwrap
		reshaped = arabic_reshaper.reshape(text)
		wrapper = textwrap.TextWrapper(drop_whitespace=True)
		if Window.height / Window.width <= 1.3333333333333333:
			wrapped = textwrap.fill(reshaped, width=79)
		else:
			wrapped = textwrap.fill(reshaped, width=33)
		return bidi.algorithm.get_display(wrapped)

	def fix__copyrighttext(self, text):
		import bidi.algorithm, arabic_reshaper, textwrap
		reshaped = arabic_reshaper.reshape(text)
		wrapper = textwrap.TextWrapper(drop_whitespace=True)
		if Window.height / Window.width <= 1.3333333333333333:
			wrapped = textwrap.fill(reshaped, width=33)
		else:
			wrapped = textwrap.fill(reshaped, width=33)
		return bidi.algorithm.get_display(wrapped)

	def fix__article(self, text):
		import bidi.algorithm, arabic_reshaper, textwrap, re
		if 'ا' or 'و' or 'ي' or 'ل' or 'م' or 'س' or 'ع' or 'ف' or 'ث' or 'ص' or 'ج' or 'د' or 'ك' or 'ط' or 'ن' or 'ب' or 'ش' or 'ر' or 'ى' or 'ز' or 'ظ' or 'ح' or 'خ' or 'ه' or 'ق' or 'ض' or 'ء' in text:
			reshaped = arabic_reshaper.reshape(text)
		else:
			reshaped = text
		flipped_text = reshaped.replace('\xa0', ' ')
		flipped_text = flipped_text.replace('\n', ' ')
		def dots_duplicates(seq, item):
			start_at = -1
			locs = []
			while True:
				try:
					loc = seq.index(item, start_at + 1)
				except ValueError:
					break
				else:
					locs.append(loc)
					start_at = loc

			return locs

		dots = dots_duplicates(flipped_text, '.')
		try:
			its_a_digit = []
			its_a_digit_left = []
			its_an_upper_case = []
			its_a_letter = []
			for dot in dots:
				its_a_digit.append(flipped_text[dot + 1].isdigit())
				its_a_digit_left.append(flipped_text[dot-1].isdigit())
				its_an_upper_case.append(flipped_text[dot + 1].isupper())
				its_a_letter.append(flipped_text[dot + 1].isalpha())

			if any((x == True for x in its_a_digit)) or any((y == True for y in its_an_upper_case)) or  any((x == True for x in its_a_digit_left)):
				pass
			else:
				flipped_text = flipped_text.replace('.', '. ')
		except IndexError as exception:
			try:
				pass
			finally:
				exception = None
				del exception

		flipped_text = flipped_text.replace('  ', ' ')
		flipped_text = flipped_text.replace('Dr.', 'Dr')
		flipped_text = flipped_text.replace('د.', 'د')
		try:
			if flipped_text[flipped_text.find('م.') - 1].isdigit() == True:
				pass
			else:
				flipped_text = flipped_text.replace('م.', 'م')
		except IndexError as exception:
			try:
				pass
			finally:
				exception = None
				del exception
		flipped_text = flipped_text.replace('No.', 'No')
		flipped_text = flipped_text.replace('Eng.', 'Eng')
		flipped_text = flipped_text.replace('أ.', 'أ')
		flipped_text = flipped_text.replace('Mr.', 'Mr')
		flipped_text = flipped_text.replace('Mrs.', 'Mrs')
		flipped_text = flipped_text.replace('Miss.', 'Miss')
		flipped_text = flipped_text.replace(' .', '.')
		flipped_text = flipped_text.replace('....', '،')
		flipped_text = flipped_text.replace('..', '،')
		flipped_text = flipped_text.replace('...', '،')
		flipped_text = flipped_text.replace('. ', '. \n')
		split_text = flipped_text.split('\n')
		wrapper = textwrap.TextWrapper()
		wrapped_lines = []
		for line in split_text:
			if Window.height / Window.width <= 1.3333333333333333:
				line = line.strip()
				if 'ا' or 'و' or 'ي' or 'ل' or 'م' or 'س' or 'ع' or 'ف' or 'ث' or 'ص' or 'ج' or 'د' or 'ك' or 'ط' or 'ن' or 'ب' or 'ش' or 'ر' or 'ى' or 'ز' or 'ظ' or 'ح' or 'خ' or 'ه' or 'ق' or 'ض' or 'ء' in line:
					wrapped = bidi.algorithm.get_display(textwrap.fill(line, width=85))
				else:
					wrapped = textwrap.fill(line, width=85)
				wrapped_lines.append(wrapped)
			else:
				line = line.strip()
				if 'ا' or 'و' or 'ي' or 'ل' or 'م' or 'س' or 'ع' or 'ف' or 'ث' or 'ص' or 'ج' or 'د' or 'ك' or 'ط' or 'ن' or 'ب' or 'ش' or 'ر' or 'ى' or 'ز' or 'ظ' or 'ح' or 'خ' or 'ه' or 'ق' or 'ض' or 'ء' in line:
					wrapped = bidi.algorithm.get_display(textwrap.fill(line, width=39))
				else:
					wrapped = textwrap.fill(line, width=39)
				wrapped_lines.append(wrapped)

		return '\n\n'.join(wrapped_lines)

	def fix__paragraphs(self, text):
		import textwrap, re
		reshaped = text
		flipped_text = reshaped.replace('\xa0', ' ')
		flipped_text = flipped_text.replace('\n', ' ')
		def dots_duplicates(seq, item):
			start_at = -1
			locs = []
			while True:
				try:
					loc = seq.index(item, start_at + 1)
				except ValueError:
					break
				else:
					locs.append(loc)
					start_at = loc

			return locs

		dots = dots_duplicates(flipped_text, '.')
		try:
			its_a_digit = []
			its_a_digit_left = []
			its_an_upper_case = []
			its_a_letter = []
			for dot in dots:
				its_a_digit.append(flipped_text[dot + 1].isdigit())
				its_a_digit_left.append(flipped_text[dot-1].isdigit())
				its_an_upper_case.append(flipped_text[dot + 1].isupper())
				its_a_letter.append(flipped_text[dot + 1].isalpha())

			if any((x == True for x in its_a_digit)) or any((y == True for y in its_an_upper_case)) or  any((x == True for x in its_a_digit_left)):
				pass
			else:
				flipped_text = flipped_text.replace('.', '. ')
		except IndexError as exception:
			try:
				pass
			finally:
				exception = None
				del exception

		flipped_text = flipped_text.replace('  ', ' ')
		flipped_text = flipped_text.replace('Dr.', 'Dr')
		flipped_text = flipped_text.replace('د.', 'د')
		try:
			if flipped_text[flipped_text.find('م.') - 1].isdigit() == True:
				pass
			else:
				flipped_text = flipped_text.replace('م.', 'م')
		except IndexError as exception:
			try:
				pass
			finally:
				exception = None
				del exception
		flipped_text = flipped_text.replace('No.', 'No')
		flipped_text = flipped_text.replace('Eng.', 'Eng')
		flipped_text = flipped_text.replace('أ.', 'أ')
		flipped_text = flipped_text.replace('Mr.', 'Mr')
		flipped_text = flipped_text.replace('Mrs.', 'Mrs')
		flipped_text = flipped_text.replace('Miss.', 'Miss')
		flipped_text = flipped_text.replace(' .', '.')
		flipped_text = flipped_text.replace('....', '،')
		flipped_text = flipped_text.replace('..', '،')
		flipped_text = flipped_text.replace('...', '،')
		flipped_text = flipped_text.replace('. ', '. \n')
		split_text = flipped_text.split('\n')
		wrapper = textwrap.TextWrapper()
		wrapped_lines = []
		for line in split_text:
			if Window.height / Window.width <= 1.3333333333333333:
				line = line.strip()
				wrapped = textwrap.fill(line, width=85)
				wrapped_lines.append(wrapped)
			else:
				line = line.strip()
				wrapped = textwrap.fill(line, width=39)
				wrapped_lines.append(wrapped)

		return '\n\n'.join(wrapped_lines)

	def set_info(self):
		if self.screen_list[-1] == 'info':
			self.screen.ids.info_box.add_widget(infocard())
	def set_contact(self):
		if self.screen_list[-1] == 'contact':
			self.screen.ids.contact_box.add_widget(contactcard())

	def set_list(self, *args):

		def set_list(interval):

			latest = 'https://omannews.gov.om/rss.ona'
			self.latest_headlines = []
			self.latest_headlines_datetime = []
			self.latest_headlines_links = []
			self.latest_images = []
			from bs4 import BeautifulSoup
			import requests
			from urllib3.exceptions import InsecureRequestWarning
			from urllib3 import disable_warnings
			disable_warnings(InsecureRequestWarning)
			try:
				resp_latest = requests.get(latest,verify=False, timeout=15)
				soup_latest = BeautifulSoup((resp_latest.content), features='xml')
				items_latest = soup_latest.findAll('item')
				for item in items_latest:
					self.latest_headlines.append(item.title.text)
					self.latest_headlines_datetime.append(item.pubDate.text)
					self.latest_headlines_links.append(item.link.text)

				if self.screen_list[-1] == 'scr 1':
					for i in range(len(self.latest_headlines)-82):
						self.screen.ids.md_list1.add_widget(NewsCard(link = (self.latest_headlines_links[i]), text=(self.fix__headline(self.latest_headlines[i])), secondary_text=(self.latest_headlines_datetime[i])))
				else:
					pass
			except (requests.ConnectionError, requests.Timeout) as exception:
				try:
					self.screen.ids.md_list1.add_widget(ConnectionError())
				finally:
					exception = None
					del exception

		Clock.schedule_once(set_list, 0.5)



	def print_article_on_press_latest(self, key, title, datea):

		def print_article_on_press_latest(interval):
			from bs4 import BeautifulSoup
			import requests
			from readability import Document
			try:
				link = requests.get((key),verify=False, timeout=60)

				doc = Document(link.text)
				clean_doc = BeautifulSoup(doc.summary(), 'lxml').text
				clean_title = title
				clean_authoer = clean_doc.partition("/ العمانية /")[2]
				if clean_title in clean_doc:
					clean_doc = clean_doc.replace(clean_title, '')
				else:
					pass
				try:
					paragraphs = self.fix__paragraphs(clean_doc).split("\n\n")
					seg1 = []
					seg2 = []
					seg3 = []
					seg4 = []
					seg5 = []
					seg6 = []
					for i in range(len(paragraphs)):

						if i <= 5:
							seg1.append(paragraphs[i])
						if i > 5 and i <= 10:
							seg2.append(paragraphs[i])
						if i > 10 and i <=15:
							seg3.append(paragraphs[i])
						if i > 15 and i <=20:
							seg4.append(paragraphs[i])
						if i > 20 and i <=25:
							seg5.append(paragraphs[i])
						if i > 25 and i <=30:
							seg6.append(paragraphs[i])
						else:
							pass
						
					segment1 = self.fix__article(" ".join(seg1))
					segment2 = self.fix__article(" ".join(seg2))
					segment3 = self.fix__article(" ".join(seg3))
					segment4 = self.fix__article(" ".join(seg4))
					segment5 = self.fix__article(" ".join(seg5))
					segment6 = self.fix__article(" ".join(seg6))
				except IndexError:
					segment1 = self.fix__article(clean_doc)
					segment2 = ""
					segment3 = ""
				if self.screen.ids.image_switch.active == False:

					self.screen.ids.article_box.add_widget(NewsArticle(author = clean_doc.split("/", -1)[-1], text=segment1, text1=segment2, text2=segment3,text3=segment4, text4=segment5, text5=segment6, title=((clean_title)), date=(datea), link=(key)))

				else:
					if self.screen.ids.image_switch.active == True:
						latest_images = BeautifulSoup((link.content), features='lxml').find('meta', property='og:image')
						try:
							self.screen.ids.article_box.add_widget(NewsArticleWithImage(author = clean_doc.split("/", -1)[-1],text=segment1, text1=segment2, text2=segment3,text3=segment4, text4=segment5, text5=segment6, title=(title), date=(datea), image=(str(latest_images['content'])), link=(key)))
						except TypeError:
							self.screen.ids.article_box.add_widget(NewsArticle(author = clean_doc.split("/", -1)[-1],text=segment1, text1=segment2, text2=segment3,text3=segment4, text4=segment5, text5=segment6, title=(title), date=(datea), link=(key)))


			except (requests.ConnectionError, requests.Timeout) as exception:
				try:
					self.screen.ids.article_box.add_widget(ConnectionError())
				finally:
					exception = None
					del exception


		Clock.schedule_once(print_article_on_press_latest, 0.5)


	def loading_callback(self, *args):
		self.loading_gif = LoadingGif()

		async def loading_callback():
			if self.screen_list[-1] == 'scr 1':
				self.screen.ids.scr1.add_widget(self.loading_gif)
				self.set_list()
				await asynckivy.sleep(0.5)
				self.screen.ids.scr1.remove_widget(self.loading_gif)

		asynckivy.start(loading_callback())

	def loading_callback_latest(self,key,title,datea, *args):
		self.loading_gif = LoadingGif()

		async def loading_callback_article():
			if self.screen_list[-1] == 'article_screen':
				self.screen.ids.artscr.add_widget(self.loading_gif)
				self.print_article_on_press_latest(key, title, datea)
				await asynckivy.sleep(0.5)
				self.screen.ids.artscr.remove_widget(self.loading_gif)
		asynckivy.start(loading_callback_article())



	def refresh_callback(self, *args):

		def refresh_callback(interval):
			if self.screen_list[-1] == 'scr 1':
				self.screen.ids.md_list1.clear_widgets()
			if self.x == 0:
				self.x, self.y = (10, 20)
			else:
				self.x, self.y = (0, 10)
			self.screen.ids.article_box.clear_widgets()
			self.loading_callback()
			self.screen.ids.refresh_layout1.refresh_done()


		Clock.schedule_once(refresh_callback, 0.5)


if __name__ == '__main__':
	MainApp().run()
Config.write()