import os

extensions = {"Bilder": ["jpg", "png", "ico", "bmp", "gif", "PNG", "jpeg", "cur", "ani", "jfif", "svg"],
          "Videos": ["mp4", "mov"],
          "Audios": ["mp3"],
          "ausführbare Dateien": ["exe", "jar", "msi", "whl"],
          "PDFs": ["pdf"], "Archive": ["zip", "7z", "rar", "gz", "bz2", "tgz", "tar", "gz", "xz"],
          "Textdateien": ["txt", "log", "epub", "ttf", "otf", "pf2"],
          "Isos": ["iso"],
          "Ordner": "",
          "unbestimmt": ""}


folders_txt = "path.txt"  # Datei, in der Pfad angegeben wird (z.B. /home/user/Downloads)


# -----------------------------------------------------FUNKTIONEN-----------------------------------------------------
def read_txt(txtpath):
    """Liest txtpath und gibt eine Liste mit jeder Zeile zurück, also jedem Pfad, der gereinigt werden soll"""
    try:
        with open(txtpath, "r") as file:
            content = file.readlines()
        content = [line.strip() for line in content]  # Entfernt \n am Ende jedes Strings
        return content

    except FileNotFoundError:
        # existiert die Datei nicht, wird der in txtpath angegebene Pfad erstellt
        print(f"{txtpath} existiert nicht, wurde erstellt")
        open(txtpath, "w")  # Wird eine Datei im Schreibmodus geöffnet, wird sie automatisch erstellt
        exit()


# ---------Erstellung der Hauptordner---------
def create_folder_structure(directory, extensions):
    """Alle Ordner in extensions werden in directory erstellt und es wird geprüft, ob directory existiert"""
    try:
        create_folders(directory, extensions)
        return True  # directory existiert und Ordner wurden erfolgreich erstellt
    except FileNotFoundError:
        print(f"-Pfad '{directory}' existiert nicht")
        return False  # directory wurde nicht gefunden


def create_folders(path, folders):
    """Es werden alle in folders übergebenen Ordner in dem Pfad erstellt, sofern sie nicht schon existieren"""
    for folder in folders.keys():  # Hierzu werden alle Schlüssel des Dictionarys durchlaufen (siehe Oben)
        try:
            os.mkdir(f"{path}/{folder}")
        except FileExistsError:
            pass


# ---------Rückgabe der Dateien---------
def get_files(path):
    """Gibt eine Liste mit allen Dateien und eine Liste mit allen Ordnern zurück"""
    file_list = os.listdir(path)
    folder_list = filter_folders(file_list)
    return file_list, folder_list


def filter_folders(file_list):
    """Sortiert Elemente mit einem '.' im Name in die Liste Dateien und den Rest in die Liste Ordner"""
    folders = []
    for file in file_list:
        if "." not in file:
            # Ist kein "." in dem Element, sprich es ist vermutlich keine Datei, wird es zu der Liste Ordner hinzugefügt
            folders.append(file)

    for folder in folders:
        file_list.remove(folder)  # Es werden alle Ordner aus der Dateiliste entfernt

    return folders  # Die Liste file_list wurde schon bearbeitet, wir geben daher nur die neue Ordnerliste zurück


# ---------Verschieben der Dateien---------
def move_file_in_folder(directory, extensions, file):
    """Eine Datei wird in den Ordner, der ihrer Dateiendung entspricht, verschoben"""
    extension = get_extension(file)
    for filetype, extns_list in extensions.items():  # Filetype = "Videos"    extns_list = ["mp4", "mov"]
        if extension in extns_list:
            move_file(directory, filetype, file)
            break

        elif filetype == "unbestimmt":
            # Ist man bei filetype="unbestimmt", dem letzten Element, angelangt, ist die Dateiendung nicht im Dictionary
            print(f"Dateityp von {file} unbekannt, verschoben nach unbestimmt")
            move_file(directory, filetype, file)


def get_extension(file):
    """Gibt Dateiendung zurück"""
    extension = file.split(".")[-1]  # Die Datei wird an jedem Punkt getrennt, das letzte Element ist die Endung
    return extension


def move_file(path, folder, file):
    """Verschiebt die Datei in den übergenenen Ordner und benennt sie um, wenn sie schon bereits existiert"""
    old_path = f"{path}/{file}"           # Wo die Datei war
    new_path = f"{path}/{folder}/{file}"  # Wohin die Datei verschoben wird

    if os.path.isfile(new_path):
        # Existiert die Datei wird sie umbenannt und es wird move_file() für die neu benannte Datei aufgerufen
        file = rename_file(path, file)
        move_file(path, folder, file)
    else:
        # Ansonsten wird sie verschoben
        os.rename(old_path, new_path)


def rename_file(path, file):
    """Es wird ein '_kopie' an den Dateinamen angehangen und sie wird dann umbenannt"""
    # Die Datei wird an dem "." getrennt, sodass man mit new_file[-2] nur den Dateinamen ändert und nicht die Endung
    new_file = file.split(".")
    new_file[-2] += "_kopie"
    new_file = ".".join(new_file)

    os.rename(f"{path}/{file}", f"{path}/{new_file}")
    return new_file


# -----------------------------------------------------HAUPTTEIL-----------------------------------------------------
directorys = read_txt(folders_txt)  # directorys ist Liste mit in folders_txt angegebenen Pfaden, die gereinigt werden
for directory in directorys:

    # For-Schleife wird nur fortgesetzt, wenn directory existiert
    if not create_folder_structure(directory, extensions):
        continue

    files, folders = get_files(directory)  # Liste mit Dateien und Liste mit den Ordnern

    for file in files:
        move_file_in_folder(directory, extensions, file)

    for folder in folders:
        if folder not in extensions.keys():  # Ist folder keiner der Hauptordner, wird er nach "Ordner" verschoben
            move_file(directory, "Ordner", folder)

    print(f"-Pfad '{directory}' sortiert")
