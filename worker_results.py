import requests
import time
from urllib3.exceptions import ConnectTimeoutError
import json
import numpy as np
import webbrowser
import random
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import math

import majjudg_ranking
import fenetres_tk
import conf


class ResultsDomain():
    def __init__(self, domain, only_manual):
        self.domain = domain
        self.keywords = conf.Domains[domain]
        self.snide_information = snide_information(domain, only_manual)
        self.failed_keywords = self.snide_information[1]
        self.information = self.snide_information[0]
        self.complete = True
        self.add_keyword()
        self.complete_snide()
        if self.complete:
            self.update()
            self.save_information()
        else:
            fenetres_tk.print_message(
                motif='Erreur',
                message=f"Les informations pour le domaine : '{self.domain}' ne sont pas complètes.\
        Si vous voulez utiliser les résultats associés à ce domaine, vous devez compléter toutes les informations."
        )


    def complete_snide(self):
        for keyword in self.keywords:
            for i in range(conf.nb_SEs):
                if self.complete:
                    if self.information[keyword]['results'][i]['results'] == {}:
                        self.add_all_pages(i, keyword)
                    elif len(self.information[keyword]['results'][i]['results']) < conf.nb_pages:
                        dernier_lien = \
                            self.information[keyword]['results'][i]['results'][str(len(
                            self.information[keyword]['results'][i]['results']
                            ))]['url']
                        self.add_pages(i,
                                    keyword, 
                                    liste = [l for 
                                                l in range(len(self.information[keyword]['results'][i]['results']) + 1,
                                                            conf.nb_pages + 1)],
                                        dernier_lien=dernier_lien)


    def add_pages(self, indice_se, keyword, liste, dernier_lien):
        webbrowser.open(conf.URLs[indice_se] + keyword)
        results = fenetres_tk.TableauTk(indice_se, liste[0], liste[-1], dernier_lien).informations
        if results == []:
            self.complete = False
        else:
            for k in range(len(liste)):
                url = results[0][k]
                title = results[1][k]
                self.information[keyword]['results'][indice_se]['results'][f'{liste[k]}'] = {
                    'score' : 0 , 'url' : url, 'title' : title
                }


    def add_all_pages(self, indice_se, keyword):
        res = {}
        webbrowser.open(conf.URLs[indice_se] + keyword)
        results = fenetres_tk.TableauTk(indice_se, first_page=1,
                                            last_page=conf.nb_pages, last_link=None).informations
        if results == []:
            self.complete = False
        else:
            for l in range(1, conf.nb_pages + 1):
                url = results[0][l-1]
                title = results[1][l-1]
                score = 0
                res[str(l)] = {'score': score, 'url': url, 'title': title}
            self.information[keyword]['results'][indice_se]['results'] = res


    def add_keyword(self):
        for keyword in self.failed_keywords:
            if self.complete:
                fenetre = tk.Tk()
                fenetre.withdraw()
                fenetre.wm_attributes("-topmost", True)
                fenetre.transient
                reponse = messagebox.askyesno("Problème de collecte des données", 
                f"SNIDE n'a pas pu récupérer les informations concernant la requête : {keyword} \
                \n Voulez-vous rentrer manuellement les informations?")
                if reponse :
                    fenetre.destroy()
                    self.add_place_keyword(keyword)
                    for i in range(conf.nb_SEs):
                        if self.complete:
                            self.add_all_pages(i, keyword)
                else:
                    fenetre.destroy()
                    self.complete = False


    def add_place_keyword(self, keyword):
        self.information[keyword] = {'percent' : 0, 'results' : [0]*conf.nb_SEs ,
                                      'ranking' : {} , 'majjudg' : {},
                                        'dixontestscore' : {}, 'distance' : {}
                                        }
        for i in range(conf.nb_SEs):
            self.information[keyword]['results'][i] = {'results': {}, 'score' : 0,
                                                        'se' : conf.SEs[i], 'status' : 'done'
                                                        }
            dic = {}
            for l in range(1, conf.nb_pages + 1):
                dic[str(l)] = {'score': 0, 'url' : ' ', 'title' :' ' }
            self.information[keyword]['results'][i]['results'] = dic


    def update(self):
        for keyword in self.keywords:
            all_pages_CTR_keyword = {}
            for i in range(conf.nb_SEs):
                for l in range(1, conf.nb_pages + 1):
                    url = self.information[keyword]['results'][i]['results'][str(l)]['url']
                    if url not in all_pages_CTR_keyword.keys():
                        all_pages_CTR_keyword[url] = conf.weights[l-1]
                    else:
                        all_pages_CTR_keyword[url] += conf.weights[l-1]

        # On met à jour le classement des moteurs de recherche et des pages
            for i in range(conf.nb_SEs):
                for l in range(1, conf.nb_pages + 1):
                    url = self.information[keyword]['results'][i]['results'][str(l)]['url']
                    self.information[keyword]['results'][i]['results'][str(l)]['score'] = \
                    all_pages_CTR_keyword[url]/conf.nb_SEs
                self.information[keyword]['results'][i]['score'] = sum(
                    [self.information[keyword]['results'][i]['results'][str(l)]['score']*conf.weights[l-1] for l\
                     in range(1, conf.nb_pages + 1)]
                )

        # On met à jour le classement du consensus
            keys_values = sorted(all_pages_CTR_keyword.items(),
                                 key=lambda x: x[1], reverse=True)[:conf.nb_pages]
            dic_score = dict(keys_values)
            self.information[keyword]['ranking'] = [[key, value/conf.nb_SEs] for key,
                                                      value in dic_score.items()]
    
        # On met à jour les distances d'Hellinger
            dic = {}
            for i in range(conf.nb_SEs):
                results = {}
                for j in range(i+1, conf.nb_SEs):
                    results[conf.SEs[j]] = self.hellinger_distance(i, j, keyword)
                dic[conf.SEs[i]] = results
            self.information[keyword]['distances'] = dic

        # On crée le classement majoritaire
            pages_votes_majjudg = {key: [] for key in all_pages_CTR_keyword.keys()}
            dic_medianes = {}
            for url in all_pages_CTR_keyword.keys():
                for i in range(conf.nb_SEs):
                    liste = [
                        self.information[keyword]['results'][i]['results'][str(l)]['url'] \
                            for l in range(1, conf.nb_pages + 1)]
                    if url in liste:
                        rank = liste.index(url)
                        pages_votes_majjudg[url].append(conf.weights[rank])
                    else:
                        pages_votes_majjudg[url].append(0)
                dic_medianes[url] = majjudg_ranking.mediane(pages_votes_majjudg[url])
            self.information[keyword]['majjudg'] = majjudg_ranking.majjudg_ranking(
                pages_votes_majjudg, dic_medianes)


    def hellinger_distance(self, indice1, indice2, keyword):
        d = 0
        ind = 0
        ind_list = []
        l1 = [self.information[keyword]['results'][indice1]['results'][str(l)]['url'] 
              for l in range(1, conf.nb_pages + 1)]
        l2 = [self.information[keyword]['results'][indice2]['results'][str(l)]['url'] 
              for l in range(1, conf.nb_pages + 1)]
        for link in l1:
            if link in l2:
                ind_list.append(l2.index(link))
                d += math.pow(math.sqrt(conf.weights_normalized[ind])
                            - math.sqrt(conf.weights_normalized[l2.index(link)]), 2)
            else:
                d += math.pow(math.sqrt(conf.weights_normalized[ind]), 2)
            ind += 1
        ind = 0
        for link in l2:
            if link not in l1:
                d += math.pow(math.sqrt(conf.weights_normalized[ind]), 2)
            ind += 1
        return math.sqrt(d) / math.sqrt(2)


    def save_information(self):
        with open(f'SNIDE Results\\campaign_results_{self.domain}.json', 'w') as file:
            json.dump(self.information, file)


def snide_information(domain, only_manual):
    campaign_results = {}
    failed_keywords = []
    for keyword in conf.Domains[domain]:
        print(f"request for keywords = {keyword}")
        result,status = search_request(keyword, only_manual)
        print(f"status for this request = {status}")
        if status == 'finish':
            campaign_results[keyword]=result
        else:
            failed_keywords.append(keyword)
        wait_time= 0 if only_manual else random.randint(10,30)
        print(f"wait before next request {wait_time} seconds")
        time.sleep(wait_time)
    return campaign_results, failed_keywords


def search_request(keywords, only_manual, url_base="https://snide.irisa.fr", verify=True,
                    timeout = 10.0, update_period=0.2):
    data = {
        "keywords": keywords.replace(" ","+")
    }
    output = {}
    if only_manual == True:
        return output, 'manual'
    else:
        try:
            r = requests.post(f"{url_base}/search",
                            data=data,
                            verify='snide-inria-fr-chain.pem')
            assert(r.status_code == 200)
            t_start = time.time()

            while time.time()-t_start < timeout :
                time.sleep(update_period)
                r = requests.post(f"{url_base}/update", data=data,
                                verify='snide-inria-fr-chain.pem')
                assert(r.status_code == 200)
                output = r.json()
                if output['percent'] == 100.0 :
                    return output,'finish'
                if output['results']:
                    status = {o['status']=='done' for o in output['results']}
                    if status.isdisjoint(set([False])):
                        return output,'finish'
            return output,'timeout'
        except ConnectTimeoutError:
            return output, 'timeout'
        except requests.exceptions.ConnectTimeout:
            return output, 'timeout'
        except requests.exceptions.ReadTimeout:
            return output, 'timeout'
        except requests.exceptions.Timeout:
            return output, 'timeout'


def main():
    for domain in ['Sport']:
        campaign_results = ResultsDomain(domain, only_manual=False)

if __name__ == '__main__':
    main()
