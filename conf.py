# Configuration of parameters

Domains = {'Sport' : ['soccer world cup', 'Olymic game', 'NBA', 'NCAA final four', 'Golf US Open'],\
            'Grammaire' : ['fish plural', 'irregular verbs', 'subjonctive', 'grammar corrector', 'when to use the'],\
                'Cuisine' : ['home-made sushi', 'pizza recipe', 'mojito', 'cooking advice', 'scrambled eggs'],\
                    'Voyages' : ['visit Paris', 'event Las Vegas', 'plane ticket', 'stay in Rome', 'best travel agency']}

SEs = ['AllTheInternet', 'AOL', 'Ask', 'Bing', 'DirectHit', 'Duckduckgo',\
       'Ecosia', 'Google', 'Lilo', 'Lycos', 'Qwant', 'Startpage', 'Yahoo', 'Yandex']

URLs = ['https://www.alltheinternet.com/?q=', 'https://search.aol.com/aol/search?query=', 'https://www.ask.com/web?q=',\
        'https://www.bing.com/search?q=', 'https://www.directhit.com/web?o=778997&l=dir&qo=homepageSearchBox&q=',\
            'https://duckduckgo.com/html/?q=', 'https://www.ecosia.org/search?q=', 'https://www.google.com/search?q=',\
                'https://search.lilo.org/searchweb.php?q=', 'https://search1.lycos.com/web/?q=', 'https://www.qwant.com/?q=',\
                    'https://www.startpage.com/do/search?query=', 'https://search.yahoo.com/search?p=',\
                        'https://yandex.com/search/?text=']

nb_SEs = len(SEs)

nb_pages = 10 # on peut faire varier le nombre de pages

weights = [.364,.125,.095,.079,.061,.041,.038,.035,.03,.022] + [0]*(nb_pages-10) if nb_pages>10 else [.364,.125,.095,.079,.061,.041,.038,.035,.03,.022]

weights_normalized = [elt/sum([weigh for weigh in weights]) for elt in weights]
