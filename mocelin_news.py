from scraping_sites.site import *
import os  
from threading import Thread  # colocar uma funçao para atualizar 
import time
from datetime import datetime
import sys
import pickle
import webbrowser
from math import ceil

from pytimedinput import timedInput  # tive que instalar 



class MocelinNews:
    def __init__(self):
        self.dict_sites = {}
        self.all_sites = [ 'veja', 'r7', 'globo']
        
        self.screan = 0
        self.kill = False
        
        self.page = 1
        
        self.news = self._read_file('news') if 'news' in os.listdir() else []
        self._update_file(self.news, 'news')
        self.sites = self._read_file('sites') if 'sites' in os.listdir() else []
        self._update_file(self.sites, 'sites')
    
        for site in self.all_sites:
            self.dict_sites[site] = Site(site)

        ###################
        self.news_thread = Thread(target=self.update_news)
        self.news_thread.setDaemon(True)
        self.news_thread.start()
        ###################
        
        
    def _update_file(self, lista, mode='news'):
        with open(mode, 'wb') as fp:
            pickle.dump(lista, fp)

    def _read_file(self, mode='news'):
        with open(mode, 'rb') as fp:
            n_list = pickle.load(fp)
            return n_list


    def _receive_command(self, valid_commands, timeout=30):
        command, timed = timedInput('>>', timeout)
        while command.lower() not in valid_commands and not timed:
            print('Comando inválido. Digite novamente\n')
            command, timed = timedInput('>>', timeout)
        command = 0 if command == '' else command
    
    def main_loop(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
        
            match self.screan:
                case 0:
                    print('SEJA BEM VINDO AO MOCELIN NEWS')
                    print('Por favor escolha algum item do menu')
                    print('')
                    print("1. Ultimas noticias\n2. Adicionar site\n3. Remover site\n4. Fechar programa")
                    
                    self.screan = int(self._receive_command([ '1', '2', '3'], 5))
                    
                case 1:
                    self.display_news()
                    command = self._receive_command(['p', 'a', 'l', 'v'], 500)
                case 2:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print('Digite o numero do site que deseja adicinar para lista de sites ativios.\nPrecione 0 para voltar para o menu')
                    print('\tSITES ATIVOS==========\n')
                    for i in self.sites:
                        print('\t', i)

                    print('\tSITES INATIVOS==========\n')
                    offiline_sites = [i for i in self.all_sites if i not in self.sites]
                    for i in range(len(offiline_sites)):
                        print(f'\t{i+1}. {offiline_sites[i]}')
                    site = int(self._receive_command([str(i) for i in range(len(offiline_sites)+1)], 50))
                    
                    if site == 0:
                        self.screan=0
                        continue
                    self.sites += [offiline_sites[site-1]]
                    self._update_file(self.sites, 'sites')
                    
                    
                case 3:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print('Digite o numero do site para remove-lo. Caso queira voltar para o menu, digite0\n')
                    for i in range(len(self.sites)):
                        print(f'\t{i+1}. {self.sites[i]}')
                    site = int(self._receive_command([str(i) for i in range(len(self.sites)+1)], 50))
                    
                    if site == 0:
                        self.screan=0
                        continue
                    
                    del self.sites[site-1]
                    self._update_file(self.sites, 'sites')
                    
                    
                case 4:
                    self.kill = True
                    sys.exit()
        
    def display_news(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Último update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.filtered_news = [ i for i in self.news if i["fonte"] in self.sites]
        self.max_page = ceil(len(self.filtered_news) / 20)
        
        if self.page > self.max_page: self.page = 1
        
        constante = (self.page - 1) * 10
        
        for i, article in enumerate(self.filtered_news[constante:constante+10]):
            print(f'{constante+i}. {article['data'].strftime('%Y-%m-%d %H:%M:%S')} - {article['fonte'].upper()} - {article['materia']}')
        print(f'Page {self.page}/{self.max_page}')
        
        print('===========================================================================')
        print('Comandos')
        print('P - Poxima Pagína | A - Pagna Anterior | L - Abrir material no navegador | V - Voltar  ')
        
    def update_news(self):
        while not self.kill:
            for site in self.all_sites:
                self.dict_sites[site].update_news()

                for key, value in self.dict_sites[site].news.items():
                    dict_aux = {}
                    dict_aux['data'] = datetime.now()
                    dict_aux['fonte'] = site
                    dict_aux['materia'] = key
                    dict_aux['link'] = value
                    
                    if len(self.news) == 0:
                        self.news.insert(0, dict_aux)
                        continue
                    
                    add_news = True
                    for news in self.news:
                        if dict_aux['materia'] == news['materia'] and dict_aux['fonte'] == news['fonte']:
                            add_news = False
                            break
                    
                    if add_news:
                        self.news.insert(0, dict_aux)
            self.news = sorted(self.news, key=lambda d: d['data'], reverse=True)
            self._update_file(self.news, 'news')
            time.sleep(10)
            
self = MocelinNews()
