import json
import numpy as np
from numpy.linalg import norm
import scipy.stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from tabulate import tabulate
import pandas as pd

import conf
import tests_tools

alpha = 0.01

class TestsDomain():
    def __init__(self, domain, alpha):
        self.domain = domain
        self.keywords = conf.Domains[domain]
        self.alpha = alpha
        self.information = json.load(open(f"SNIDE Results\\campaign_results_{self.domain}.json"))
        self.grouped_tests_domain = tests_tools.grouped_tests_domain
        self.documentation = tests_tools.documentation_tests_domain
        self.results_tests = {}
        self.execution = {'dtest0': self.dtest0(), 'dtest0bis': self.dtest0bis(), 'dtest1': self.dtest1(),
                 'dtest2': self.dtest2(), 'dtest4': self.dtest4(), 'ANOVA1test1': self.ANOVA1test1(),
                 'ANOVA1test2': self.ANOVA1test2()} 
        self.save_results()


    def dtest0(self): # Test with the bias formula (1) for t=1
        res = {}
        for keyword in self.keywords:
            tests = {}
            all_pages_bias = {}
            all_pages_Mosh = {}
            SEs_links = {se: 
                         [self.information[keyword]['results'][conf.SEs.index(se)]['results'][str(l)]['url'] 
                              for l in range(1, conf.nb_pages + 1)] for se in conf.SEs}
            
            for i in range(conf.nb_SEs):
                for l in range(1, conf.nb_pages + 1):
                    url = self.information[keyword]['results'][i]['results'][str(l)]['url']
                    all_pages_bias[url] = self.information[keyword]['results'][i]['results'][str(l)]['score']
                    if url not in all_pages_Mosh.keys():
                        all_pages_Mosh[url] = 1
                    else:
                        all_pages_Mosh[url] += 1
            
            SEs_bias = {se: {key: all_pages_bias[key] if key in 
                                SEs_links[se] else 0 for key in all_pages_bias.keys()} 
                                for se in conf.SEs}
            SEs_Mosh = {se: {key: 1 if key in 
                                SEs_links[se] else 0 for key in all_pages_Mosh.keys()} 
                                for se in conf.SEs}
            
            dic_bias = {se: tests_tools.bias(list(SEs_bias[se].values()), list(all_pages_bias.values())) for se in conf.SEs}
            dic_Mosh = {se: tests_tools.bias(list(SEs_Mosh[se].values()), list(all_pages_Mosh.values())) for se in conf.SEs}
            dic_score = {se: self.information[keyword]['results'][conf.SEs.index(se)]['score'] 
                         for se in conf.SEs}
            
            tests['Dixon tests bias'] = tests_tools.dixon_test(list(dic_bias.values()),self.alpha)
            tests['Dixon tests Mosh'] = tests_tools.dixon_test(list(dic_Mosh.values()), self.alpha)
            tests['Dixon tests score'] = tests_tools.dixon_test(list(dic_score.values()), self.alpha)
            res[keyword] = tests
        self.results_tests['dtest0'] = res
    

    def dtest0bis(self):
        res = {}
        urls = {}
        SEs_vilk_bias = {} # correspond aux vilk
        SEs_vilk_Mosh = {}
        SEs_vil_bias = {}
        SEs_vil_Mosh = {}
        urls_bias = {}
        urls_Mosh = {}
        for keyword in self.keywords: # on recense toutes les urls pour les différentes requêtes
            for i in range(conf.nb_SEs):
                for l in range(1, conf.nb_pages + 1):
                    url = self.information[keyword]['results'][i]['results'][str(l)]['url']
                    urls[url] = 0
        for i in range(conf.nb_SEs):
            dic_urls_bias = {}
            dic_urls_Mosh = {}
            for url in urls.keys():
                dic_keywords_bias = {}
                dic_keywords_Mosh = {}
                for keyword in self.keywords:
                    dic = self.information[keyword]['results'][i]['results']
                    if url in [dic[str(l)]['url'] for l in range(1, conf.nb_pages + 1)]:
                        index = [dic[str(l)]['url'] for l in range(1, conf.nb_pages + 1)].index(url)
                        dic_keywords_bias[keyword] = conf.weights[index] # pour la métrique CTR
                        dic_keywords_Mosh[keyword] = 1 # pour la métrique Mosh
                    else:
                        dic_keywords_bias[keyword] = 0
                        dic_keywords_Mosh[keyword] = 0
                dic_urls_bias[url] = dic_keywords_bias
                dic_urls_Mosh[url] = dic_keywords_Mosh
            SEs_vilk_bias[conf.SEs[i]] = dic_urls_bias
            SEs_vilk_Mosh[conf.SEs[i]] = dic_urls_Mosh
        for i in range(conf.nb_SEs):
            dic_urls_bias = {}
            dic_urls_Mosh = {}
            for url in urls.keys():
                dic_urls_bias[url] = sum([SEs_vilk_bias[conf.SEs[i]][url][k] for k in self.keywords])
                dic_urls_Mosh[url] = sum([SEs_vilk_Mosh[conf.SEs[i]][url][k] for k in self.keywords])
            SEs_vil_bias[conf.SEs[i]] = dic_urls_bias
            SEs_vil_Mosh[conf.SEs[i]] = dic_urls_Mosh
        for url in urls.keys():
            urls_bias[url] = sum([SEs_vil_bias[conf.SEs[i]][url] for i in range(conf.nb_SEs)])
            urls_Mosh[url] = sum([SEs_vil_Mosh[conf.SEs[i]][url] for i in range(conf.nb_SEs)])
        SEs_bias = {se : tests_tools.bias(list(SEs_vil_bias[se].values()), list(urls_bias.values())) for se in conf.SEs}
        SEs_Mosh = {se : tests_tools.bias(list(SEs_vil_Mosh[se].values()), list(urls_Mosh.values())) for se in conf.SEs}
        res['Dixon test bias'] = tests_tools.dixon_test(list(SEs_bias.values()), alpha)
        res['Dixon test Mosh'] = tests_tools.dixon_test(list(SEs_Mosh.values()), alpha)
        self.results_tests['dtest0bis'] = res    


    def dtest1(self): # Abnormal SE score for a given research
        res = {}
        for keyword in self.keywords:
            test = {}
            SEs_score = {se: self.information[keyword]['results'][conf.SEs.index(se)]['score']
                         for se in conf.SEs}
        
            test['Dixon test score'] = tests_tools.dixon_test(list(SEs_score.values()), self.alpha)
            res[keyword] = test
        self.results_tests['dtest1'] = res


    def dtest2(self): # Investigation SEs disregarding the most visible link
        res = {}
        for keyword in self.keywords:
            test = {}
            most_visible_link, score_most_visible_link = \
            self.information[keyword]['ranking'][0]
            SEs_scores = {}
            for i in range(conf.nb_SEs):
                results_se = self.information[keyword]['results'][i]['results']
                ranking = [key for key, value in results_se.items() if value['url'] == most_visible_link]
                if ranking != []:
                    SEs_scores[conf.SEs[i]] = conf.weights[int(ranking[0])-1]
                else:
                    SEs_scores[conf.SEs[i]] = 0
            test['Dixon test score most visible link'] = tests_tools.dixon_test(list(SEs_scores.values()), self.alpha)
            res[keyword] = test
        self.results_tests['dtest2'] = res


    def dtest3(self, indice_se): # Investigating if the top-ranked page of one\
        # particular SE is also visible at other SEs
        res = {}
        for keyword in self.keywords:
            test = {}
            top_pages_se = self.information[keyword]['results'][indice_se]['results']['1']['url']
            SEs_scores = {}
            for i in range(conf.nb_SEs):
                results_se = self.information[keyword]['results'][i]['results']
                ranking = [key for key, value in results_se.items() if value['url'] == top_pages_se]
                if ranking != []:
                    SEs_scores[conf.SEs[i]] = conf.weights[int(ranking[0])-1]
                else:
                    SEs_scores[conf.SEs[i]] = 0
            test[f'Dixon test top ranked link {conf.SEs[indice_se]}'] = tests_tools.dixon_test(list(SEs_scores.values()),
                                                                                   self.alpha)
            res[keyword] = test
        self.results_tests['dtest3'] = res

    def dtest4(self): # Investigating if a SE ranks first  a page not considered relevant by others
        res = {}
        for keyword in self.keywords:
            test = {}
            SEs_score = {se: self.information[keyword]['results'][conf.SEs.index(se)]['results']['1']['score']
                         for se in conf.SEs}
            test['Dixon test top ranked pages'] = tests_tools.dixon_test(list(SEs_score.values()), self.alpha)
            res[keyword] = test
        self.results_tests['dtest4'] = res


    def ANOVA1test1(self): #  Investigating if keywords have similar biases
        res = {}
        request_bias = []
        request_Mosh = []
        request_score = []
        for keyword in self.keywords:
            all_pages_bias = {}
            all_pages_Mosh = {}
            SEs_links = {se: 
                         [self.information[keyword]['results'][conf.SEs.index(se)]['results'][str(l)]['url'] 
                              for l in range(1, conf.nb_pages + 1)] for se in conf.SEs}
            for i in range(conf.nb_SEs):
                for l in range(1, conf.nb_pages + 1):
                    url = self.information[keyword]['results'][i]['results'][str(l)]['url']
                    all_pages_bias[url] = self.information[keyword]['results'][i]['results'][str(l)]['score']
                    if url not in all_pages_Mosh.keys():
                        all_pages_Mosh[url] = 1
                    else:
                        all_pages_Mosh[url] += 1
            SEs_bias = {se: {key: all_pages_bias[key] if key in 
                                SEs_links[se] else 0 for key in all_pages_bias.keys()} 
                                for se in conf.SEs}
            SEs_Mosh = {se: {key: 1 if key in 
                                SEs_links[se] else 0 for key in all_pages_Mosh.keys()} 
                                for se in conf.SEs}
            liste_bias, liste_Mosh, liste_score = [], [], []
            for i in range(conf.nb_SEs):
                liste_bias.append(tests_tools.bias(list(SEs_bias[conf.SEs[i]].values()), list(all_pages_bias.values())))
                liste_Mosh.append(tests_tools.bias(list(SEs_Mosh[conf.SEs[i]].values()), list(all_pages_Mosh.values())))
                liste_score.append(self.information[keyword]['results'][i]['score'])
            request_bias.append(liste_bias)
            request_Mosh.append(liste_Mosh)
            request_score.append(liste_score)
        res['Anova1 test bias'] = scipy.stats.f_oneway(*request_bias)[1]<self.alpha
        res['Anova1 test Mosh'] = scipy.stats.f_oneway(*request_Mosh)[1]<self.alpha
        res['Anova1 test score'] = scipy.stats.f_oneway(*request_score)[1]<self.alpha
        self.results_tests['ANOVA1test1'] = res


    def ANOVA1test2(self): # Investigating if SEs have the same bias
        res = {}
        request_score = [[0]*len(self.keywords) for i in range(conf.nb_SEs)]
        request_bias = [[0]*len(self.keywords) for i in range(conf.nb_SEs)]
        request_Mosh = [[0]*len(self.keywords) for i in range(conf.nb_SEs)]
        for keyword in self.keywords:
            all_pages_bias = {}
            all_pages_Mosh = {}
            SEs_links = {se: 
                         [self.information[keyword]['results'][conf.SEs.index(se)]['results'][str(l)]['url'] 
                              for l in range(1, conf.nb_pages + 1)] for se in conf.SEs}
            for i in range(conf.nb_SEs):
                for l in range(1, conf.nb_pages + 1):
                    url = self.information[keyword]['results'][i]['results'][str(l)]['url']
                    all_pages_bias[url] = self.information[keyword]['results'][i]['results'][str(l)]['score']
                    if url not in all_pages_Mosh.keys():
                        all_pages_Mosh[url] = 1
                    else:
                        all_pages_Mosh[url] += 1
            SEs_bias = {se: {key: all_pages_bias[key] if key in 
                                SEs_links[se] else 0 for key in all_pages_bias.keys()} 
                                for se in conf.SEs}
            SEs_Mosh = {se: {key: 1 if key in 
                                SEs_links[se] else 0 for key in all_pages_Mosh.keys()} 
                                for se in conf.SEs}
            dic_bias = {se: tests_tools.bias(list(SEs_bias[se].values()), list(all_pages_bias.values())) for se in conf.SEs}
            dic_Mosh = {se: tests_tools.bias(list(SEs_Mosh[se].values()), list(all_pages_Mosh.values())) for se in conf.SEs}
            dic_score = {se: self.information[keyword]['results'][conf.SEs.index(se)]['score'] for se in conf.SEs}
            ind = 0
            for i in range(conf.nb_SEs):
                request_bias[i][ind] = dic_bias[conf.SEs[i]]
                request_Mosh[i][ind] = dic_Mosh[conf.SEs[i]]
                request_score[i][ind] = dic_score[conf.SEs[i]]
        res['Anova1 test bias'] = scipy.stats.f_oneway(*request_bias)[1]<self.alpha
        res['Anova1 test Mosh'] = scipy.stats.f_oneway(*request_Mosh)[1]<self.alpha
        res['Anova1 test score'] = scipy.stats.f_oneway(*request_score)[1]<self.alpha
        self.results_tests['ANOVA1test2'] =  res
        

    def save_results(self):
        with open(f'Tests Results\\tests_{self.domain}_{self.alpha}.txt', 'w') as file:
            file.write(f'Fichier des resultats des tests statistiques effectues pour le domaine :{self.domain}\n')
            file.write(f'Les tests sont de niveau alpha : {self.alpha}\n')
            file.write('\n')
            file.write(tests_tools.line)
            file.write('\n')

            for tests in self.grouped_tests_domain:
                if tests == 'dtest0':
                    self.execution[tests]
                    table = []
                    first_line = ['keywords'] + list(self.results_tests[tests][self.keywords[0]].keys())
                    for k in range(len(self.keywords)):
                        table.append([self.keywords[k]] + list(self.results_tests[tests][self.keywords[k]].values()))
                    file.write(tests +'\n')
                    file.write('\n')
                    file.write(tabulate(table, headers=first_line, tablefmt="plain",
                                        showindex=False, numalign="center") + '\n')
                    file.write('\n')
                    file.write('\n')
                    for test in self.grouped_tests_domain[tests]:
                        file.write(tests_tools.print_documentation(self.documentation, test) + '\n')
                    file.write('\n')
                    file.write(tests_tools.line)
                    file.write('\n')
                
                elif tests == 'dtest0bis':
                    for test in self.grouped_tests_domain[tests]:
                        self.execution[test]
                    file.write(tests +'\n')
                    file.write('\n')
                    file.write(tests_tools.convert_table(self.results_tests[tests]) +'\n')
                    file.write('\n')
                    for test in self.grouped_tests_domain[tests]:
                        file.write(tests_tools.print_documentation(self.documentation, test) + '\n')
                    file.write('\n')
                    file.write(tests_tools.line)
                    file.write('\n')

                elif tests == 'ANOVA1':
                    for test in self.grouped_tests_domain[tests]:
                        self.execution[test]
                    file.write(f'Results for {tests}\n')
                    file.write('\n')
                    table = [[1 for i in range(len(self.grouped_tests_domain[tests])+1)]
                              for j in range(3)]
                    first_line = ['metrics']
                    ind = 1
                    for test in self.grouped_tests_domain[tests]:
                        first_line.append(test)
                        metrics = list(self.results_tests[test].keys())
                        for k in range(len(metrics)):
                            table[k][ind] = str(self.results_tests[test][metrics[k]])
                        ind += 1
                    for k in range(len(metrics)):
                        table[k][0] = metrics[k]
                    file.write(tabulate(table, headers=first_line, tablefmt="plain",
                                            showindex=False, numalign="center") + '\n')
                    file.write('\n')
                    for test in self.grouped_tests_domain[tests]:
                        file.write(tests_tools.print_documentation(self.documentation, test) + '\n')
                    file.write('\n')
                    file.write(tests_tools.line)
                    file.write('\n')

                elif tests == 'Dixon gouped tests':
                    for test in self.grouped_tests_domain[tests]:
                        self.execution[test]
                    file.write(f'Results for {tests}\n')
                    file.write('\n')
                    table = [[1 for i in range(4)] for j in range(len(self.keywords))]
                    first_line = ['keywords']
                    for k in range(len(self.keywords)):
                        table[k][0] = self.keywords[k]
                    ind = 1
                    for test in self.grouped_tests_domain[tests]:
                        first_line.append(test)
                        for k in range(len(self.keywords)):
                            value = self.results_tests[test][self.keywords[k]].values()
                            table[k][ind] = list(value)[0]
                        ind += 1
                    file.write(tabulate(table, headers=first_line, tablefmt="plain",
                                            showindex=False, numalign="center") +'\n')
                    file.write('\n')
                    for test in self.grouped_tests_domain[tests]:
                        file.write(tests_tools.print_documentation(self.documentation, test) + '\n')
                    file.write('\n')
                    file.write(tests_tools.line)
                    file.write('\n')
                
                elif tests == 'dtest3':
                    file.write(f'Results for {tests}\n')
                    table = [[1 for i in range(conf.nb_SEs + 1)] for j in range(len(self.keywords))]
                    first_line = ['keywords']
                    for k in range(len(self.keywords)):
                        table[k][0] = self.keywords[k]
                    for i in range(conf.nb_SEs):
                        self.dtest3(indice_se=i)
                        first_line.append(conf.SEs[i])
                        for k in range(len(self.keywords)):
                            table[k][i+1] = \
                            self.results_tests['dtest3'][self.keywords[k]][f'Dixon test top ranked link {conf.SEs[i]}']
                    table.insert(0, first_line)
                    file.write('\n')
                    file.write(tabulate(table, tablefmt="plain",
                                            showindex=False, numalign="center") + '\n')
                    file.write('\n')
                    for test in self.grouped_tests_domain[tests]:
                        file.write(tests_tools.print_documentation(self.documentation, test) + '\n')
                    file.write('\n')
                    file.write(tests_tools.line)
                    file.write('\n')

                else:
                    file.write(f'Results for {tests} do not exist\n')
                    file.write('\n')
                                                 

class TestsDomains():
    def __init__(self, alpha):
        self.alpha = alpha
        self.Domains = conf.Domains
        self.domains = list(self.Domains.keys())
        self.grouped_tests_domains = tests_tools.grouped_tests_domains
        self.documentation = tests_tools.documentation_tests_domains
        self.information = {}
        self.results_tests = {}
        for domain in self.Domains:
            self.information[domain] = json.load(open(f"SNIDE Results\\campaign_results_{domain}.json"))
        with open("SNIDE Results\\Domains_results.json", 'w') as file:
            json.dump(self.information, file)
        self.execution = {'ANOVA2test1': self.ANOVA2test1()}
        self.save_results()


    def ANOVA2test1(self):
        res = {}
        df = df = pd.DataFrame(columns=["Domain", "SE", "Score"])

        for domain in self.Domains:
            campaign_results = self.information[domain]
            for keyword in list(campaign_results.keys()):
                for i in range(conf.nb_SEs):
                    a_line = {"Domain" : domain, "SE" : i, "Score" : campaign_results[keyword]['results'][i]['score']}
                    df.loc[len(df)] = a_line
        model = ols('Score ~ Domain*SE', data=df).fit()
        Anova_Score = sm.stats.anova_lm(model, typ=2)

        res['ANOVA2 Score Domain'] = Anova_Score.loc['Domain']['PR(>F)']<alpha
        res['ANOVA2 Score SE'] = Anova_Score.loc['SE']['PR(>F)']<alpha
        self.results_tests['ANOVA2test1'] = res


    def ANOVA1test3(self, indice_se):
        res = {}
        request_score = []
        request_bias = []
        request_Mosh = []

        for domain in self.domains:
            list_domain_score, list_domain_bias, list_domain_Mosh = [], [], []
            for keyword in self.Domains[domain]:
                pages_bias_score = {}
                pages_Mosh = {}
                SE_dic = {se : {value['url'] : value['score']
                            for value in self.information[domain][keyword]['results'][conf.SEs.index(se)]['results'].values()}
                              for se in conf.SEs}
                for i in range(conf.nb_SEs):
                    for value in self.information[domain][keyword]['results'][i]['results'].values():
                        url = value['url']
                        score = value['score']
                        pages_bias_score[url] = score
                        if url not in pages_Mosh.keys():
                            pages_Mosh[url] = 1 
                        else:
                            pages_Mosh[url] += 1

                se_bias = {key : pages_bias_score[key] if key in SE_dic[conf.SEs[indice_se]] 
                           else 0 for key in pages_bias_score.keys()}
                se_Mosh = {key : 1 if key in SE_dic[conf.SEs[indice_se]] else 0 for key in pages_Mosh.keys()}
                se_score = self.information[domain][keyword]['results'][indice_se]['score']

                list_domain_bias.append(tests_tools.bias(list(se_bias.values()), list(pages_bias_score.values())))
                list_domain_Mosh.append(tests_tools.bias(list(se_Mosh.values()), list(pages_Mosh.values())))
                list_domain_score.append(se_score)

            request_bias.append(list_domain_bias)
            request_Mosh.append(list_domain_Mosh)
            request_score.append(list_domain_score)

        res['ANOVA1 test bias'] = scipy.stats.f_oneway(*request_bias)[1]<self.alpha
        res['ANOVA1 test Mosh'] = scipy.stats.f_oneway(*request_Mosh)[1]<self.alpha
        res['ANOVA1 test score'] = scipy.stats.f_oneway(*request_score)[1]<self.alpha

        self.results_tests['ANOVA1test3'] = res

    
    def save_results(self):
            for tests in self.grouped_tests_domains:
                if tests == 'ANOVA2test1':
                    for test in self.grouped_tests_domains[tests]:
                        self.execution[test]
                    for domain in self.Domains:
                        with open(f'Tests Results\\tests_{domain}_{self.alpha}.txt', 'a') as file:
                            file.write(f'Results for {tests}\n')
                            file.write('\n')
                            file.write(tabulate([[key, str(value)] for key, value in self.results_tests['ANOVA2test1'].items()],
                                                    tablefmt="plain", showindex=False, numalign="center" ) + '\n')
                            file.write('\n')
                            file.write(tests_tools.print_documentation(self.documentation, tests) +'\n')
                            file.write('\n')
                            file.write(tests_tools.line)
                            file.write('\n')

                elif tests == 'ANOVA1test3':
                    for domain in self.Domains:
                        with open(f'Tests Results\\tests_{domain}_{self.alpha}.txt', 'a') as file:
                            file.write(f'Results for {tests}\n')
                            table = [[1 for i in range(conf.nb_SEs + 1)] for j in range(3)]
                            first_line = ['metrics']
                            metrics = ['ANOVA1 test bias', 'ANOVA1 test Mosh', 'ANOVA1 test score']
                            ind = 0
                            for metric in metrics:
                                table[ind][0] = metric
                                ind += 1
                            for i in range(conf.nb_SEs):
                                self.ANOVA1test3(indice_se=i)
                                first_line.append(conf.SEs[i])
                                ind = 0
                                for metric in metrics:
                                    table[ind][i+1] = \
                                    str(self.results_tests['ANOVA1test3'][metric])
                                    ind += 1
                            file.write('\n')
                            file.write(tabulate(table, headers=first_line, tablefmt="plain",
                                                    showindex=False, numalign="center") + '\n')
                            file.write('\n')
                            for test in self.grouped_tests_domains[tests]:
                                file.write(tests_tools.print_documentation(self.documentation, test) + '\n')
                            file.write('\n')
                            file.write(tests_tools.line)
                            file.write('\n')


def main():
    for domain in conf.Domains:
        test_domain = TestsDomain(domain, alpha)
    test_domains = TestsDomains(alpha)

if __name__ == '__main__':
    main()
