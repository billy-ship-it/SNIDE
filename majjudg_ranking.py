import itertools
import conf

def mediane(liste):
    n = len(liste)
    liste.sort()
    if n%2==1:
        return liste[n//2]
    else:
        return liste[n//2-1]


def iteratif(dic_votes, median, group_medianes, results):
    new_medianes = {}
    for url in group_medianes[median]: # ce sont les urls\
        # qui ont la même médiane
        if len(dic_votes[url]) == 1:
            for element in group_medianes[median]:
                results.append([element])
            break
        else:
            dic_votes[url].remove(median)
            new_medianes[url] = mediane(dic_votes[url]) \
                  # on met à jour les médianes avec la valeur enlevée

    group_medianes  = {} # on regroupe les clés entre elles\
    #si elles ont la même médiane
    for cle, valeur in new_medianes.items():
        if valeur not in group_medianes.keys():
            group_medianes[valeur] = [cle]
        else:
            group_medianes[valeur].append(cle)
    group_medianes = {cle: group_medianes[cle] for cle in \
                      sorted(group_medianes.keys(), reverse=True)}

    for median in group_medianes.keys():
        if len(group_medianes[median])>1: # si on a deux urls \
            #qui ont la même médiane, on recommence le processus
            return iteratif(dic_votes, median, group_medianes, results)
        else:
            results.append(group_medianes[median])
    

def majjudg_ranking(dic_votes, dic_medianes):  
    group_medianes = {}
    results = []
    for cle, valeur in dic_medianes.items(): # on regroupe les urls qui ont \
        #la même médiane
        if valeur not in group_medianes.keys():
            group_medianes[valeur] = [cle]
        else:
            group_medianes[valeur].append(cle)
    group_medianes = {cle: group_medianes[cle] for cle in 
                      sorted(group_medianes.keys(), reverse=True)}
    group_medianes = dict(itertools.islice(group_medianes.items(), conf.nb_pages))
    for cle in group_medianes.keys():
        if len(group_medianes[cle])>1:
            iteratif(dic_votes, cle, group_medianes, results)
        else:
            results.append(group_medianes[cle])
    return results[:conf.nb_pages]
