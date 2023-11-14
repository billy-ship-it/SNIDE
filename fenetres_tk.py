import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

import conf

class TableauTk():
    def __init__(self , indice_se, first_page, last_page, last_link):
        self.indice_se = indice_se
        self.first_page = first_page
        self.last_page = last_page
        self.last_link = last_link
        self.informations = []
        self.url_saisies = []
        self.titre_saisies = []
        self.root = tk.Tk()
        self.main()


    def enregistrer_informations(self):
        urls = [url_saisie.get() for url_saisie in self.url_saisies]
        titres = [titre_saisie.get() for titre_saisie in self.titre_saisies]
        result = messagebox.askyesno("Enregistrement",
                            "Voulez-vous enregistrez les informations?")
        if result == True:
            self.root.destroy()
        self.informations.extend([urls, titres])


    def quitter(self):
        reponse = messagebox.askyesno("Confirmation",
                                       "Etes-vous sûr de vouloir quitter la fenêtre?")
        if reponse == True:
            self.root.destroy()
    

    def main(self):
        self.root.wm_attributes("-topmost", True) # pour placer la fenêtre au premier plan
        self.root.transient # pour que la fenêtre reste affichée même si on clique à côté

        # mise en page
        consigne = tk.Label(self.root,
        text=f"Remplissez les informations pour le moteur de recherche : {conf.SEs[self.indice_se]}\n \
            l'url de la dernière page enregistrée est : {self.last_link}")
        consigne["fg"] = "blue"  # pour mettre en bleu le texte
        position_page = tk.Label(self.root, text="Position de la page")
        url = tk.Label(self.root, text="url de la page")
        titre_page = tk.Label(self.root, text="Titre de la page")
        espace1 = tk.Label(self.root, text="   ")

        # première ligne
        consigne.grid(row=0, columnspan=3)
        espace1.grid(row=0, column=3)
        # deuxième ligne
        position_page.grid(row=1, column=0)
        url.grid(row=1, column=1)
        titre_page.grid(row=1, column=2)

        for k in range(self.first_page, self.last_page + 1):
            numero = tk.Label(self.root, text=f"{k}")
            numero.grid(row=2+k, column=0)

            url_saisie = tk.StringVar()
            url_saisie_entry = ttk.Entry(self.root, width=60, 
                                        textvariable=url_saisie)
            url_saisie_entry.grid(row=2+k, column=1)
            self.url_saisies.append(url_saisie_entry)

            titre_saisie = tk.StringVar()
            titre_saisie_entry = ttk.Entry(self.root, width=60, 
                                        textvariable=titre_saisie)
            titre_saisie_entry.grid(row=2+k, column=2)
            self.titre_saisies.append(titre_saisie_entry)

            # Associer la fonction d'enregistrement aux événements \
            # de pression de la touche "Return"
            url_saisie_entry.bind("<Return>", 
                                lambda event: self.enregistrer_informations())

        bouton_valider = tk.Button(self.root, text="  Valider  ", 
                                command=self.enregistrer_informations)
        bouton_valider.grid(row=4+self.last_page, column=1, sticky=tk.E)
        bouton_fermer = tk.Button(self.root, text="  Fermer  ", command=self.quitter)
        bouton_fermer.grid(row=4+self.last_page, column=2, sticky=tk.E)
        self.root.title(f"Tableau pour le moteur de recherche {conf.SEs[self.indice_se]}")
        self.root.mainloop()


def print_message(motif, message):
    root = tk.Tk()
    root.wm_attributes("-topmost", True)
    root.title(motif)
    texte = tk.Message(root, text=message, width=400)
    texte.pack()
    root.mainloop()