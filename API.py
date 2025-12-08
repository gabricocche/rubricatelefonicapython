#importo le funzioni di controllo e salvataggio
from funzioni.aggiungiContatto import stringaErrata,save
import webview
import os


#creo la classe secondaria che si occupa delle sottoschede
class Api_form:

    #costruttore della classe
    def __init__(self,rubrica,finestra_principale):
        self.rubrica=rubrica #mantengo il riferimento alla lista del main
        self.finestra_principale=finestra_principale
        self.finestra=None
        self.numero_da_modificare=None

    #metodo che crea la finestra le sotto_finestre
    def crea_finestra(self, tipo:str, numero_da_modificare:int=None):
        cartella_corrente = os.path.dirname(__file__)
        if tipo=='f':
            file_path = os.path.join(cartella_corrente, "form.html")
            window_form=webview.create_window('Aggiunta contatto', f'file://{file_path}',js_api=self, width=500, height=550, resizable=False) #creo la finestra
            self.finestra=window_form
        elif tipo=='m':
            self.numero_da_modificare=numero_da_modificare
            file_path = os.path.join(cartella_corrente, "modifica.html")
            window_mod=webview.create_window('modifica', f'file://{file_path}',js_api=self, width=700, height=550, resizable=False) #creo la finestra
            self.finestra=window_mod

    #metodo che ritorna a js il contatto da modificare
    def get_contatto_da_modificare(self):
        for i in self.rubrica:
            # telefono in rubrica è salvato come stringa: normalizziamo il confronto
            if str(i['telefono']) == str(self.numero_da_modificare):
                return i
        return 5
    
    #metodo prova di funzionamento
    def saluta(self):
        return 'ciao'

    #Funzione per gestire l'aggiunta di un nuovo contatto nella rubrica e il suo salvataggio su un file in locale
    def aggiungiContatto(self,contatto): #parametro contatto che viene passato da js

        errori = [] #salvo eventuali errori in una lista

         #se c'è un errore lo appendo alla lista
        if stringaErrata(contatto['nome'], 's'):
            errori.append("il nome può essere costituito solo da caratteri.")
        if stringaErrata(contatto['cognome'], 's'):
            errori.append("il cognome può essere costituito solo da caratteri.")
        if stringaErrata(contatto['telefono'], 'n',self.rubrica):
            errori.append("Telefono non valido (deve essere 10 cifre).")
        if stringaErrata(contatto['email'], 'e'):
            errori.append("Email deve contenere la @ e un dominio esistente.")

        if errori:
            return errori

        #aggiungo il contatto alla rubrica passata come parametro
        self.rubrica.append(contatto)

        #aggiungo il contatto al file locale ('contatti.csv')
        save(contatto)

        return True

    #metodo per aggiornare la grafica della finestra
    def aggiorna(self):
        self.finestra_principale.evaluate_js("caricaContatti();")

    #metodo per chiudere in automatico la finestra
    def chiudi(self):
        self.finestra.destroy()

    #metodo che fa il controllo degli errori su eventuali modifiche e se corretti li salva nella rubrica tempornea e in locale
    def modificaContatto(self, nuovo: dict):
        """Aggiorna il contatto selezionato (self.numero_da_modificare) con i campi in `nuovo`.

        Restituisce True se OK oppure una lista di messaggi di errore.
        """
        errori = []

        # Validazioni base (riutilizziamo stringaErrata quando possibile)
        if stringaErrata(nuovo.get('nome',''), 's'):
            errori.append("il nome può essere costituito solo da caratteri.")
        if stringaErrata(nuovo.get('cognome',''), 's'):
            errori.append("il cognome può essere costituito solo da caratteri.")
        if stringaErrata(nuovo.get('email',''), 'e'):
            errori.append("Email deve contenere la @ e un dominio esistente.")

        if errori:
            return errori

        # Trova il contatto da modificare
        for contatto in self.rubrica:
            if contatto['telefono'] == str(self.numero_da_modificare):
                contatto['nome'] = nuovo['nome']
                contatto['cognome'] = nuovo['cognome']
                contatto['email'] = nuovo['email']
                break

        # Riscrivo l'intero file contatti.csv in modo consistente
        with open('contatti.csv', 'w', newline='') as file:
            for i in self.rubrica:
                formattazione = (
                    i.get('nome','') + ';' + i.get('cognome','') + ';' + str(i.get('telefono','')) + ';' + i.get('email','') + '\n'
                )
                file.write(formattazione)

        return True

#classe Api che gestisce la finestra principale
class Api:
    #costruttore della classe
    def __init__(self,rubrica:list):
        self.rubrica=rubrica #mantengo il riferimento alla lista del main
        self.finestra=None

    #metodo che crea graficamente la finestra
    def crea_finestra_principale (self):
        cartella_corrente = os.path.dirname(__file__)
        file_path = os.path.join(cartella_corrente, "index.html")
        window = webview.create_window("Rubricapy", f"file://{file_path}", js_api=self, width=1200, height=600, resizable=True)
        self.finestra=window

    #metodo che passa a js i contatti(dizionari) per poterli inserire nell'html dinamicamente
    def get_contatti(self):
        return self.rubrica #funzione adibita al passaggio a js dei contatti in modo che vengano mostrati a schermo

    def form_aggiunta(self): #funzione che serve per aprire una seconda scheda che corrisponde al form per l'aggiunta di un nuovo contatto
        api_form=Api_form(self.rubrica,self.finestra)
        api_form.crea_finestra('f')

    def mod_aggiunta(self,numero_da_modificare:int): #funzione che serve per aprire una seconda scheda che corrisponde al form per l'aggiunta di un nuovo contatto
        api_form=Api_form(self.rubrica,self.finestra)
        api_form.crea_finestra('m',numero_da_modificare)

    #funzione per eliminare un contatto sia dalla rubrica(lista) che dal file salvato in locale
    #riceve come parametro il numero di telefono del contatto da eliminare
    def eliminaContatto (self,numero:int):

        contatore=0 #inizializzo un contatore che servirà per il pop, in quanto i è un dizionario e non un valore numerico
        for i in self.rubrica:
            if i['telefono']==numero:
                self.rubrica.pop(contatore) #rimuovo il contatto
                self.finestra.evaluate_js("caricaContatti();")
                break
            contatore+=1

        with open('contatti.csv', 'w', newline='') as file:
            for i in self.rubrica:
                formattazione = (
                    i['nome'] + ';' + i['cognome'] + ';' + str(i['telefono']) + ';' + i['email'] + '\n'
                )
                file.write(formattazione)

    #metodo che ritorna i contatti che soddisfano i requisit di ricerca
    def cercaContatto (self,valore_ricercato:str):
        valore_ricercato=valore_ricercato.split(' ')
        aggiunti=set()
        corrispondenze=[]
        for i in self.rubrica:
            for ricerca in valore_ricercato:
                flag=True
                if ricerca.lower() not in i['nome'].lower() and ricerca.lower() not in i['cognome'].lower() and ricerca.lower() not in i['email'].lower() and ricerca not in str(i['telefono']):
                    flag=False
                    break
        
            if i['telefono'] not in aggiunti and flag==True:
                        corrispondenze.append(i)
                        aggiunti.add(i['telefono'])
        return corrispondenze