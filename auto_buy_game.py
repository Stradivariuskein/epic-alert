import time
import webbrowser
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, Playwright

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
URL = 'https://store.epicgames.com/en-US/'
STORE_URL = 'https://store.epicgames.com'
# Etiquetas para el filtrado y las keys par el diccionario
FREE_NOW = 'free now'
COMING_SOON = 'coming soon'


class FreeGame():
    '''Data game'''
    def __init__(self, link, expiration, title_game, img_src):
        self.title_game = title_game
        self.img_src = img_src
        self.link = link
        self.expiration = expiration
        
    def open_in_store(self):
        webbrowser.open(STORE_URL + self.link)

    def __str__(self) -> str:
        return f"Title: {self.title_game}\tlink: {self.link}\texpiration: {self.expiration}\timg_src: {self.img_src}\n"
    

        

class ApiFreeGame():
    '''Manager and detect fre games of store'''
    def __init__(self, playwright_param: Playwright):
        
        if isinstance(playwright_param, Playwright):
            self.playwright = playwright_param
        self.games = []

    
    # obtenemos el link para comprarlo, la fecha de caducidad, link de la imagen y titulo del juego
    def _get_attributes_from_html(self, elem, mach_key) -> FreeGame:
        '''Get attributes from element and return free games'''
        
        # Obtenemos el link
        a_element = elem.find('a')
        if a_element:
            a_href = a_element.get('href')
            if mach_key == FREE_NOW:
                a_aria_label = a_element.get('aria-label').lower().split(',')[-3:-1]
                expiration = a_aria_label[1].split('-')[-1]
            elif mach_key == COMING_SOON:
                a_aria_label = a_element.get('aria-label').lower().split(',')[-2:]
                expiration ='Coming soon ' + a_aria_label[1].split('free')[-1].strip()
            else:
                raise ValueError("mach_key invalida value. Use global variable COMING_SOON or FREE_NOW") 
            title_game = a_aria_label[0]
            
            # Encuentra la etiqueta de la imagen dentro del elemento actual
            img_element = elem.find('img')
            if img_element:
                #obtenemos el link de la imagen
                img_src = img_element.get('data-image')
            else:
                img_src = ''
            # Creamos el juego y lo retornamos
            game = FreeGame(a_href, expiration, title_game, img_src)
            return game
        
        print("error no data game")
        return None
        
    # Obtiene los juegos gratis ahora y los q vendrá pronto. Retorna un diccionario con 2 listas 
    def get_free_games(self) -> dict[str]:
        '''Get free games and return dic with 2 list free now and coming soon '''

        # Abrimos el navegador
        chromium = self.playwright.chromium
        browser = chromium.launch(headless=True)
        page = browser.new_page(user_agent=USER_AGENT )

        # Abre la tienda de epic
        page.goto(URL)

        # Espera a que la página se cargue completamente
        page.wait_for_load_state("load")


        # Obtiene el contenido HTML con Playwright
        page_content = page.content()

        # Analiza el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(page_content, 'html.parser')

        # Encuentra todos los elementos con la clase 'css-1ukp34s'
        elements = soup.find_all(class_='css-1ukp34s')
        for elem in elements:
            # Obtiene el HTML interno del elemento
            inner_html = elem.decode_contents()
            if FREE_NOW in inner_html.lower():
                # obtenemos el link para comprarlo y la fecha de caducidad, link de la imagen y titulo del juego
                game = self._get_attributes_from_html(elem, FREE_NOW)
            elif COMING_SOON in inner_html.lower():
                game = self._get_attributes_from_html(elem, COMING_SOON)
            try:
                if not game is None :
                    self.games.append(game)
                    game = None
            except:
                time.sleep(300)
                return self.get_free_games()

        browser.close()
        return self.games



if __name__ == "__main__":
    with sync_playwright() as playwright:
        games = ApiFreeGame(playwright).get_free_games()



