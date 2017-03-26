import csv, os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime

Version="1.2"
email="alexvac@hotmail.it"

#INIZIALIZZO LE LISTE E LE VARIABILI
b=0
t=0
numero_dark=0
numero_tsv=0
unisci=0
dark_value_sum=0

dark_list=[]
wl_list=[]
wld_list=[]
en_list=[]
da_list=[]
MATRICE=[]
MATRICED=[]
namefile_list=[]

#INTRO__________________________________________________________________________
print "Welcome to VaccaOptics " + Version + "\n@: " + email
print "____________________________\nAn STS tsv converter to txt" + "\n" + "for proper exportation"+ "\n" + "and calibration" + "\n____________________________\n"

##DOMANDA DI RICHIESTA DARK DATA__________________________________________
if raw_input("Do you have dark data? [Si/No]") in ["Si","SI","si","sI"]:
    print "\n|D A R K   S I G N A L   A V E R A G E"
    print "|Please place your dark.tsv files in the /DARK directory"
    dark_bool=1
else:
    dark_bool=0

##LETTURA E MEDIA DEI DARK______________________________________________________

if dark_bool==1:

    print ("|\n|Searching for dark.tsv files in" + str(os.path.dirname(os.path.realpath(__file__)) + "\DARK"))

    for file in os.listdir(str(os.path.dirname(os.path.realpath(__file__)) + "\DARK")):
        if file.endswith(".tsv"):
            numero_dark+=1
    if numero_dark>0:
        print "|Found " + str(numero_dark) + " *.tsv dark files\n|"
    else:
        print "|No dark files found."

    #LOOP PER ACQUISIZIONE DARK E MEDIA DEI SEGNALI
    for file in os.listdir(str(os.path.dirname(os.path.realpath(__file__)) + "\DARK")):

        #SE IL FILE TERMINA PER *tsv LO SCRIPT VA AVANTI ED ESEGUE IL POPOLAMENTO DELLA MATRICED
        if file.endswith(".tsv"):

            print ("|%d/%d - Working...")%(t+1, numero_dark)

            dark_open=open(str("DARK/" + file),'rb')

            for i in range(0,5):
                next(dark_open)

            dark_aperto=csv.reader(dark_open, delimiter='\t')

            for rigad in dark_aperto:
                wld=float(rigad[0])
                da=float(rigad[1])
                if t==0:
                    wld_list.append(wld)
                da_list.append(da)
            t+=1

            dark_open.close()

            if len(MATRICED)==0:
                MATRICED.append(wld_list)

            MATRICED.append(da_list)

            da_list=[]

    print "|\n|Dark list done!"

    #MEDIA DEI DARK__________________________________________

    print "|\n|Starting dark data averaging..."
    
    for colonna in range(0,len(MATRICED[0])):
        for riga in range(0+1,len(MATRICED)):
            dark_value_sum+=MATRICED[riga][colonna]
        dark_value=dark_value_sum/(len(MATRICED)-1)
        dark_list.append(dark_value)
        dark_value_sum=0

    #AGGIUNZIONE DELLA LISTA DEGLI AVERAGE ALLA MATRICED
    MATRICED.append(dark_list)

    ##SCRITTURA____________________________________________________________________

    #APRO IL FILE DI OUTPUT
    outputd=open("DARK/Dark.txt","w")

    outputd.write("WL" + "\t")

    for i in range(0,len(MATRICED)-1):
        outputd.write(str(i) + "\t")
    outputd.write("\n")

    #TRASPONGO LA MATRICE DARK FINALE
    MATRICEDt=map(list,zip(*MATRICED))

    #SCRIVO PER RIGHE LE COLONNE
    for colonne in MATRICEDt:
        for item in colonne:
            outputd.write(str(item).replace(".",",") + "\t")
        outputd.write("\n")
        
    outputd.close()

    print "|Dark averaging done!\n"
        

##LETTURA_______________________________________________________________________

print "Searching for tsv files in " + os.path.dirname(os.path.realpath(__file__))

#RICERCA DEL NUMERO DI FILE TSV NELLA CARTELLA
for file in os.listdir(os.path.dirname(os.path.realpath(__file__))):
    if file.endswith(".tsv"):
        numero_tsv+=1

#COSA SUCCEDE SE NUMERO TSV=0
if numero_tsv==0:
    print "No *.tsv found inside the directory."

print "Found " + str(numero_tsv) + " tsv files \n"

#LOOP CON I FILE ALL'INTERNO DELLA CARTELLA DELLO SCRIPT
for file in os.listdir(os.path.dirname(os.path.realpath(__file__))):
        
    #SE IL FILE TERMINA PER *tsv VA AVANTI
    if file.endswith(".tsv"):

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

