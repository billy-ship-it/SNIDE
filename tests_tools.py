import math 
from numpy.linalg import norm
from tabulate import tabulate
import numpy as np


grouped_tests_domain = {'dtest0': ['dtest0'], 'dtest0bis': ['dtest0bis'], 'Dixon gouped tests':['dtest1', 'dtest2', 'dtest4'],
                  'ANOVA1': ['ANOVA1test1', 'ANOVA1test2'],
                    'dtest3' : ['dtest3']}

grouped_tests_domains = {'ANOVA1test3': ['ANOVA1test3'], 'ANOVA2test1' : ['ANOVA2test1']}

documentation_tests_domain = {'dtest0': 'dtest0: Dixon test with the bias formula (1) computed with t=1',
            'dtest0bis': 'dtest0bis: Dixon test with the bias formula (1)',
            'dtest1' : 'dtest1: Dixon test with search engines scores',
            'dtest2' : 'dtest2: Dixon test with the global score for top ranked links provided by search engines',
            'dtest3' : 'dtest3: Dixon test to compare the top ranked link of a search engine with its position for other search engines',
            'dtest4': 'dtest4: Investigating if a SE ranks first  a page not considered relevant by others',
            'ANOVA1test1': 'ANOVA1test1: ANOVA test to investigate if keywords have similar biases',
            'ANOVA1test2': 'ANOVA1test2: ANOVA test to investigate if search engines have the same bias'}

documentation_tests_domains = {'ANOVA2test1':
 'ANOVA2test1: ANOVA test to Investigate if there is a bias on both crossed variables : search engines and domains',
'ANOVA1test3': 'ANOVA1test3: ANOVA test to investigate wether a search engine biases its results in relation to the query domain'}

line = '*******************************************************************************************************************'


def dixon_test(x,alpha):    
    '''Performs the Dixon test on the list x of real values,
      as in the last page of Processing Data for Outliers, W. J. Dixon, Biometrics,
        Vol. 9, No. 1, 1953'''
    # critical values (from the paper, starting for 3 samples)
    CVs = [[.684, .781, .886, .941, .976, .988, .994],
            [.471, .560, .679, .765, .846, .889, .926],
            [.373, .451, .557, .642, .729, .780, .821],
            [.318, .386, .482, .560, .644, .698, .740],
            [.281, .344, .434, .507, .586, .637, .680],
            [.318, .385, .479, .554, .631, .683, .725],
            [.288, .352, .441, .512, .587, .635, .677],
            [.265, .325, .409, .477, .551, .597, .639],
            [.391, .442, .517, .576, .638, .679, .713],
            [.370, .419, .490, .546, .605, .642, .675],
            [.351, .399, .467, .521, .578, .615, .649],
            [.370, .421, .492, .546, .602, .641, .674],
            [.353, .402, .472, .525, .579, .616, .647],
            [.338, .386, .454, .507, .559, .595, .624],
            [.325, .373, .438, .490, .542, .577, .605],
            [.314, .361, .424, .475, .527, .561, .589],
            [.304, .350, .412, .462, .514, .547, .575],
            [.295, .340, .401, .450, .502, .535, .562],
            [.287, .331, .391, .440, .491, .524, .551],
            [.280, .323, .382, .430, .481, .514, .541],
            [.274, .316, .374, .421, .472, .505, .532],
            [.268, .310, .367, .413, .464, .497, .524],
            [.262, .304, .360, .406, .457, .489, .516]]
    # Corresponding values of alpha:
    alphas = [.30, .20, .10, .05, .02, .01, .005]

    n = len(x)
    x.sort()
    if n < 3:
        print('Not enough values in v')
        return
    cv = CVs[n-3][alphas.index(alpha)]
    if x[-1]==x[0]:
        r = 0
    else:
        if n < 8:
            r = 0 if x[-1]==x[0] else (x[1]-x[0])/(x[-1]-x[0])
        elif n < 11:
            r = 1 if x[-1]==x[1] else (x[1]-x[0])/(x[-1]-x[1])
        elif n < 14:
            r = 1 if x[-1]==x[1] else (x[2]-x[0])/(x[-1]-x[1])
        elif n < 26:
            r = 1 if x[-1]==x[2] else (x[2]-x[0])/(x[-1]-x[2])
        else:
            print('Too many samples, please use another test')
            return
    if r > cv:
        #print('The smallest value is suspicious')
        return(1)
    else:
        return(0)


def bias(sample, others): # defintion of the bias according (1) formula
    return 1-np.dot(sample, others)/(norm(sample)*norm(others))


def convert_table(test_results):
    table = [[key, str(value)] for key, value in test_results.items()]
    return tabulate(table, tablefmt="plain", showindex=False, numalign="center" )


def print_documentation(documentation, test):
    try:
        texte = documentation[test]
        return texte
    except KeyError:
        return f"Le test {test} n'a pas de documentation, vous pouvez en ajouter une dans le dictionnaire corresponant du fichier 'tests_tools.py'"

