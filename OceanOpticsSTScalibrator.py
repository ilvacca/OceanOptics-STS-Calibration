import csv, os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime

Version="1.1"
email="alexvac@hotmail.it"

#INIZIALIZZO LE LISTE E LE VARIABILI
b=0
numero_tsv=0
unisci=0

wl_list=[]
en_list=[]
MATRICE=[]
namefile_list=[]

#INTRO__________________________________________________________________________
print "Welcome to OceanVacca " + Version + "\n@: " + email
print "____________________________\nAn STS tsv converter to txt" + "\n" + "for proper exportation" + "\n____________________________\n"

##LETTURA_______________________________________________________________________

print "Searching for tsv files in " + os.path.dirname(os.path.realpath(__file__))

#RICERCA DEL NUMERO DI FILE TSV NELLA CARTELLA
for file in os.listdir(os.path.dirname(os.path.realpath(__file__))):
    if file.endswith(".tsv"):
        numero_tsv+=1

print "Found " + str(numero_tsv) + " tsv files \n"

#LOOP CON I FILE ALL'INTERNO DELLA CARTELLA DELLO SCRIPT
for file in os.listdir(os.path.dirname(os.path.realpath(__file__))):
        
    #SE IL FILE TERMINA PER *tsv VA AVANTI
    if file.endswith(".tsv"):

        if (b+1)%10==0:
            print ("%d/%d - Working...")%(b+1, numero_tsv)

        #PRENDO IL NOME DEL PRIMO FILE PER DECIDERE IL NOME DELL'OUTPUT
        nome_file_output=file[:-8]

        #AGGIUNGO IL NOME (TRONCANDOLO) DEL FILE ALLA LISTA namefile_list
        namefile_list.append(file[-8:][:4])

        #APRO IL FILE DI INPUT
        file_open=open(file,'rb')

        #SALTO L'HEADER DI 7 RIGHE
        for i in range(0,6):
            next(file_open)

        #LEGGO IL FILE DI INPUT SEPARANDO LE TABULAZIONI
        file_aperto=csv.reader(file_open, delimiter='\t')

        #LETTURA E POPOLAMENTO DELLE DUE LISTE
        for riga in file_aperto:
            wl=float(riga[0])
            en=float(riga[1])
            if b==0:
                wl_list.append(wl)
            en_list.append(en)
        b+=1

        #CHIUDO IL FILE DI INPUT
        file_open.close()

        #SE LA MATRICE FINALE E' VUOTA ALLORA INSERISCO LE WAVELENGTH NELLA 1 RIGA
        if len(MATRICE)==0:
            MATRICE.append(wl_list)

        #AGGIUNGO ALLA MATRICE FINALE LA RIGA DELLE MISURE
        MATRICE.append(en_list)

        #RIINIZIALIZZO LA LISTA DELLE MISURE
        en_list=[]

print "\nDone\n"


##SCRITTURA____________________________________________________________________

#APRO IL FILE DI OUTPUT
output=open(nome_file_output + ".txt","w")
output.write("WL" + "\t")

for i in range(0,len(MATRICE)-1):
    output.write(str(namefile_list[i]) + "\t")
output.write("\n")

#TRASPONGO LA MATRICE FINALE
MATRICEt=map(list,zip(*MATRICE))

#SCRIVO PER RIGHE LE COLONNE
for colonne in MATRICEt:
    for item in colonne:
        output.write(str(item).replace(".",",") + "\t")
    output.write("\n")


output.close()


##PLOT_________________________________________________________________________

if raw_input("Do you want to export spectrum images? [Si/No] ") in  ["Si","SI","si","sI"]:
    fig=plt.subplots()

    hournamepath=str(datetime.now().strftime('%Y%m%d%H%M%S'))
    os.mkdir("IMG_" + hournamepath)
    
    for d in range(0,len(MATRICE)-1):
        plt.axis([630,1130,0,16384])
        plt.ylabel('DN')
        plt.xlabel('Wavelength [nm]')
        plt.plot(MATRICE[0],MATRICE[d+1])
        plt.savefig("IMG_" + hournamepath + "/" + nome_file_output + "_IMG" + str(d) + ".jpg", dpi=150)
        plt.cla()
        
    for d in range(0,len(MATRICE)-1):
        plt.axis([630,1130,0,16384])
        plt.ylabel('DN')
        plt.xlabel('Wavelength [nm]')
        plt.plot(MATRICE[0],MATRICE[d+1])
    plt.savefig("IMG_" + hournamepath + "/" + nome_file_output + "_IMG_STACK.jpg", dpi=150)
        
plt.close()

print "\nDone\nBye!"

