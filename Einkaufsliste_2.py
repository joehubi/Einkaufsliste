from colorama import init, Fore, Style

def print_error_message(message):
    init(autoreset=True)  # Initialisiere colorama mit autoreset=True, um Farben zurückzusetzen
    print(Fore.RED + Style.BRIGHT + f"Error: {message}" + Style.RESET_ALL)

def print_green_message(message):
    init(autoreset=True)  # Initialisiere colorama mit autoreset=True, um Farben zurückzusetzen
    print(Fore.GREEN + Style.BRIGHT + f"Info: {message}" + Style.RESET_ALL)

def print_blue_message(message):
    init(autoreset=True)  # Initialisiere colorama mit autoreset=True, um Farben zurückzusetzen
    print(Fore.BLUE + Style.BRIGHT + f"{message}" + Style.RESET_ALL)

def wartestelle():
    print_blue_message("Drücke Enter, um fortzufahren...")
    
def einkauf_hinzufuegen():
    artikel = input("Gib den Artikelnamen ein: ")
    try:
        menge = float(input("Gib die Menge ein (Stück oder Kilogramm): "))  # Kommazahlen für Kilogramm-Artikel
    except ValueError:
        print_error_message("Ungültige Eingabe für die Menge. Bitte gib eine Kommazahl ein.")
        return

    try:
        preis = float(input("Gib den Preis in Euro ein: "))
    except ValueError:
        print_error_message("Ungültige Eingabe für den Preis. Bitte gib eine Dezimalzahl ein.")
        return

    # Berechne das Produkt aus Menge und Preis
    produkt = round(menge * preis, 2)

    with open("einkaufsliste.txt", "a") as file:
        nummer = get_naechste_nummer()
        file.write(f"{nummer};{artikel};{menge};{preis} €;{produkt} €\n")
    print("\n")
    print_green_message("Einkauf erfolgreich hinzugefügt!")
    einkaufsliste_anzeigen()

'''
def einkaufsliste_anzeigen():
    try:
        with open("einkaufsliste.txt", "r") as file:
            einkaufsliste = file.read()
            print("Einkaufsliste:")
            print(einkaufsliste)
    except FileNotFoundError:
        print("Die Einkaufsliste ist noch leer.")
'''

def einkaufsliste_anzeigen():
    try:
        with open("einkaufsliste.txt", "r") as file:
            einkaufsliste = file.readlines()

        if not einkaufsliste:
            print("Die Einkaufsliste ist noch leer.")
            return

        print("\n")
        #print("Einkaufsliste:")
        print("{:<10} {:<20} {:<10} {:<10} {:<10}".format("Nummer", "Artikel", "Menge", "Preis", "Produkt"))
        print("-" * 60)

        for line in einkaufsliste:
            nummer, artikel, menge, preis, produkt = line.strip().split(";")
            print("{:<10} {:<20} {:<10} {:<10} {:<10}".format(nummer, artikel, menge, preis, produkt))

    except FileNotFoundError:
        print("Die Einkaufsliste ist noch leer.")
        

def get_naechste_nummer():
    try:
        with open("einkaufsliste.txt", "r") as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1]
                nummer = int(last_line.split(";")[0].strip())
                return nummer + 1
    except FileNotFoundError:
        pass
    return 1


def einkauf_loeschen():
    nummer = input("Gib die Nummer des Einkaufs ein, den du löschen möchtest: ")
    try:
        with open("einkaufsliste.txt", "r") as file:
            lines = file.readlines()

        with open("einkaufsliste.txt", "w") as file:
            for line in lines:
                if not line.startswith(f"{nummer};"):
                    file.write(line)

        print("Einkauf erfolgreich gelöscht!")
    except FileNotFoundError:
        print("Die Einkaufsliste ist noch leer.")

def gesamtsumme_anzeigen():
    try:
        gesamtsumme = 0.0
        with open("einkaufsliste.txt", "r") as file:
            for line in file:
                produkt = line.split(";")[-1].strip()  # Extrahiere das letzte Element (Produkt) aus der Zeile
                if produkt.endswith("€"):
                    produkt = produkt[:-1]  # Entferne das Euro-Symbol am Ende der Zahl
                gesamtsumme += float(produkt)

        print(f"Gesamtsumme aller Produkte: {gesamtsumme:.2f} €")
    except FileNotFoundError:
        print("Die Einkaufsliste ist noch leer.")
    except ValueError:
        print("Fehler beim Berechnen der Gesamtsumme.")

def get_artikel_preis_by_nummer(nummer):
    try:
        with open("artikel_preis.txt", "r") as file:
            for line in file:
                artikel_num, artikel, preis = line.strip().split(";")
                if int(artikel_num) == nummer:
                    return artikel, float(preis)
    except FileNotFoundError:
        print("Die Datei 'artikel_preis.txt' wurde nicht gefunden.")
    except ValueError:
        print("Fehler beim Lesen der Daten.")

    return None, None


def main():
    print_blue_message("Willkommen zur KOOP-Einkaufsliste!")
    while True:
        print("\n")
        print("\nMenü:")
        print("\n")
        print("1. Einkauf hinzufügen")
        print("2. Artikel und Preise anzeigen")
        print("3. Einkaufsliste anzeigen")
        print("4. Summe bilden")
        print("5. Einkauf löschen")
        print("6. Beenden")

        print("\n")
        auswahl = input("Wähle eine Option (1/2/3/4/5/6): ")

        if auswahl == "1":
            einkauf_hinzufuegen()
        elif auswahl == "2":
            
            nummer = input("Bitte gib' die Nummer des Artikels ein (0 zum Beenden): ")
 
            try:
                nummer = int(nummer)
                artikel, preis = get_artikel_preis_by_nummer(nummer)
                if artikel is not None and preis is not None:
                    print_blue_message(f"Artikel: {artikel}, Preis: {preis:.2f} €")
                else:
                    print_error_message("Artikel nicht gefunden.")
            except ValueError:
                print_error_message("Ungültige Eingabe. Bitte gib eine Ganzzahl ein.")
        
        elif auswahl == "3":
            einkaufsliste_anzeigen()
        elif auswahl == "4":
            gesamtsumme_anzeigen()
        elif auswahl == "5":
            einkauf_loeschen()
        elif auswahl == "6":
            print("Auf Wiedersehen!")
            break
        else:
            print_error_message("Ungültige Eingabe")


if __name__ == "__main__":
    main()
