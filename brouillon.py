import json

campaign_results_Sport = json.load(open('SNIDE results\\campaign_results_Sport.json'))

with open("C:\\Users\\65jlp\\Documents\\Ecole ENSAE\\1A\\Stage 1A\\copie dictionnaires\\campaign_results_Sport.json", 'w') as file:
    json.dump(campaign_results_Sport, file)

with open("C:\\Users\\65jlp\\Documents\\Ecole ENSAE\\1A\\Stage 1A\\copie dictionnaires\\results.txt", 'w') as file:
    with open("Tests Results\\tests_Sport_0.01.txt", 'r') as file2:
        file.write(file2.read())