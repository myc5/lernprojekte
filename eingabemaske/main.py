from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime
import json

class Person:
    def __init__(self, id_, fName, lName, birthday, eMail, gender):
        self.id_ = id_
        self.fName = fName
        self.lName = lName
        self.birthday = birthday
        self.eMail = eMail
        self.gender = gender
    
    def getAllValues(self): # This isn't used anywhere, was just for testing
        allValues = {"id": self.id_, "Vorname":self.fName, "Nachname":self.lName, "Geburtstag (Alter)": self.birthday, "E-Mail": self.eMail, "Geschlecht": self.gender}
        return allValues

class GUI:
    def __init__(self, master):
        self.mainWindow = master

        self.mainWindow.title("Eingabemaske")

        self.mainWindow.option_add('*tearOff', False)

        self.menubar = Menu(self.mainWindow)
        self.mainWindow.config(menu=self.menubar)

        self.file = Menu(self.menubar)
        self.edit = Menu(self.menubar)
        self.help = Menu(self.menubar)

        self.menubar.add_cascade(menu=self.file, label="Datei")
        self.menubar.add_cascade(menu=self.edit, label="Bearbeiten")
        
        # Not implemented
        #self.menubar.add_cascade(menu=self.help, label="Hilfe")

        self.file.add_command(label="Datei laden", command=lambda: loadFile())
        self.file.add_command(label="Datei speichern", command=lambda: saveFile())
        self.file.add_command(label="Datei speichern unter", command=lambda: saveFileAs())
        self.file.add_separator()
        self.file.add_command(label="Exit", command=lambda: self.mainWindow.destroy())

        self.edit.add_command(label="Optionen", command=lambda: optionsWindow())

        # Config
        # General config
        self.treeViewConfig = ["id", "Vorname", "Nachname", "Geburtstag (Alter)", "E-Mail", "Geschlecht"]
        self.personList = []
        self.idList = []
        self.loadFileName = ""
        self.saveFileAsName = ""
        self.idCounter = 0

        # Name config
        self.allowedNameLength = [2, 30]
        self.useNamesBlacklist = False;
        self.blacklistedWords = ["Fritz"]
        self.autoCorrectExceptions = []

        # Email config
        self.useEmailBlacklist = False;
        self.eMailBlacklist = ["hotmail.com"]  # This is meant to be for domains, i.e. "google.com"
        self.useEmailWhitelist = False;
        self.eMailWhitelist = ["google.com"]  # not full addresses (though it can work for them as well)

        # Birthday config
        self.allowedAgeRange = [13, 100]
        self.currentDate = datetime.now().strftime("%d.%m.%Y")
        self.currentDay, self.currentMonth, self.currentYear = int(self.currentDate.split(".")[0]), int(
            self.currentDate.split(".")[1]), int(self.currentDate.split(".")[2])
        self.oldestAllowedBirthdate = [self.currentDay, self.currentMonth, self.currentYear - self.allowedAgeRange[1]]
        self.youngestAllowedBirthdate = [self.currentDay, self.currentMonth, self.currentYear - self.allowedAgeRange[0]]

        # Gender options
        self.genders = ["m", "w", "d", "keine Angabe"]

        # Create the Tree window
        self.tree = ttk.Treeview(self.mainWindow, height=20, selectmode="browse")
        self.tree.grid(row=1, column=1, columnspan=6, padx=20, pady=20, sticky="ns")
        self.tree.grid_rowconfigure(1, weight=1)
        self.tree.grid_columnconfigure(1, weight=1)

        self.tree["columns"] = [x + 1 for x in range(len(self.treeViewConfig))]
        self.tree["show"] = "headings"

        for i in range(len(self.treeViewConfig)):
            self.tree.column(i + 1, anchor="c")
            self.tree.heading(i + 1, text=self.treeViewConfig[i])
            

        # Labels & Entries
        # Note: while the text can be changed, the variable names are fixed;
        # there is probably a way to autogenerate variable names via local/global, but might be overdoing things

        self.idLabel = Label(self.mainWindow, text=self.treeViewConfig[0])
        self.idEntry = Entry(self.mainWindow)
        self.var1 = IntVar()
        self.var1.set(1)
        self.idEntry.configure(state="disabled")
        self.idCheckBtn = Checkbutton(self.mainWindow, text="Auto ID", var=self.var1, command=lambda: toggleIdSelect())

        self.fNameLabel = Label(self.mainWindow, text=self.treeViewConfig[1])
        self.fNameEntry = Entry(self.mainWindow)
        self.fNameEntry.insert(0, "Max")

        self.lNameLabel = Label(self.mainWindow, text=self.treeViewConfig[2])
        self.lNameEntry = Entry(self.mainWindow)
        self.lNameEntry.insert(0, "Mustermann")

        self.birthdayLabel = Label(self.mainWindow, text=self.treeViewConfig[3])
        self.birthdayEntry = Entry(self.mainWindow)
        self.birthdayEntry.insert(0, "12.12.1990")

        self.eMailLabel = Label(self.mainWindow, text=self.treeViewConfig[4])
        self.eMailEntry = Entry(self.mainWindow)
        self.eMailEntry.insert(0, "EMail@Beispiel.de")

        self.genderLabel = Label(self.mainWindow, text=self.treeViewConfig[5])
        self.genderCombo = ttk.Combobox(self.mainWindow, values=self.genders)
        self.genderCombo.insert(0, self.genders[3])
        self.genderCombo.configure(state="readonly")

        self.idLabel.grid(row=2, column=1)
        self.idEntry.grid(row=3, column=1)
        self.idCheckBtn.grid(row=4, column=1)

        self.fNameLabel.grid(row=2, column=2)
        self.fNameEntry.grid(row=3, column=2)

        self.lNameLabel.grid(row=2, column=3)
        self.lNameEntry.grid(row=3, column=3)

        self.birthdayLabel.grid(row=2, column=4)
        self.birthdayEntry.grid(row=3, column=4)

        self.eMailLabel.grid(row=2, column=5)
        self.eMailEntry.grid(row=3, column=5)

        self.genderLabel.grid(row=2, column=6)
        self.genderCombo.grid(row=3, column=6)

        self.addEntryBtn = Button(self.mainWindow, text="Hinzufügen", command=lambda: addEntry())
        self.rmvEntryBtn = Button(self.mainWindow, text="Löschen", command=lambda: removeEntry())
        self.saveBtn = Button(self.mainWindow, text="Alle Einträge löschen", command=lambda: deleteAllEntries())

        self.addEntryBtn.grid(row=5, column=2)
        self.rmvEntryBtn.grid(row=5, column=4)
        self.saveBtn.grid(row=5, column=6)
        # testValues
        # insert(parent, index, iid=None, **kw)

        # self.testValues = ("Test", "Vorname", "Nachname", "23.08.2000 (23)" , "example@gmail.com", "m")
        # self.tree.insert("", "end", values=self.testValues)
        
        # All the functions 
        
        def toggleIdSelect():
            if self.var1.get() == 1:
                self.idEntry.configure(state="disabled")
            else:
                self.idEntry.configure(state="normal")

        
        def infoMessage(title="Dialogbox", dialogueMessage="Text hier"):
            messagebox.showinfo(title=title, message=dialogueMessage)

        def questionMessage(title="Frage", questionMessage="Ja oder Nein?"):
            answer = messagebox.askquestion(title=title, message=questionMessage)
            return answer

        def yesnocancelMessage(title="Frage", questionMessage="Ja, Nein, oder Abbrechen?"):
            answer = messagebox.askyesnocancel(title=title, message=questionMessage)
            return answer

        def errorMessage(title="Fehler!", errorMessage="Bitte überprüfe deine Eingaben."):
            messagebox.showerror(title, message=errorMessage)

        def checkFName(nameString):
            originalNameString = nameString

            # Formatting:
            # Remove leading and trailing white spaces:
            nameString = nameString.strip()

            # Attempt to fix capitalization and replace spaces in between with "-", with the assumption that it was meant to be a double name
            nameString = nameString.lower()
            tempString = ""
            tempString2 = ""
            for i in nameString.split(" "):
                tempString += i.capitalize()
                try:
                    if tempString[-1] != "-":
                        tempString += "-"
                except IndexError:
                    pass
            # Unfortunately, this breaks capitalization of properly entered double names "Max-Mil" --> "Max-mil", so we fix it like this
            for i in tempString.split("-"):
                tempString2 += i.capitalize()
                tempString2 += "-"
            while tempString2[-1] == "-":
                tempString2 = tempString2[:-1]
            nameString = tempString2

            # Check if blacklist is enabled and whether the name is in it
            if self.useNamesBlacklist:
                if nameString in self.blacklistedWords:
                    errorMessage("Unzulässiger Name", f"Der Name ist nicht erlaubt.")
                    self.fNameLabel.configure(fg="red")
                    return False

            # Check  name for length after removing the spaces
            if len(nameString) > self.allowedNameLength[1]:
                errorMessage("Vorname zu lang",
                             f"Vorname ist zu lang. Es dürfen maximal {self.allowedNameLength[1]} Buchstaben benutzt werden.")
                self.fNameLabel.configure(fg="red")
                return False
            if len(nameString) < self.allowedNameLength[0]:
                errorMessage("Vorname zu kurz",
                             f"Vorname ist zu kurz. Es müssen mindestens {self.allowedNameLength[0]} Buchstaben benutzt werden.")
                self.fNameLabel.configure(fg="red")
                return False
            # isalnum() can detect non-letters; unfortunately it also detects hyphens which are necessary for double names
            # if no hypens are in the string but special characters or digits are, we stop
            if not nameString.isalnum() and "-" not in nameString:
                errorMessage("Vorname beinhaltet unzulässige Sonderzeichen",
                             f"Vorname beinhaltet unzulässige Sonderzeichen oder Leerzeichen. Benutzen Sie '-' für Doppelnamen.")
                self.fNameLabel.configure(fg="red")
                return False
            # if there are as many non-letters as hyphens, we proceed; otherwise it means there are non-hypen special characters and we abort
            countHyphen, countNonChars = 0, 0
            for i in nameString:
                if i == "-":
                    countHyphen = + 1
            for i in nameString:
                if i.isalnum() == False:
                    countNonChars = + 1
            if countNonChars > countHyphen:
                errorMessage("Vorname beinhaltet unzulässige Sonderzeichen",
                             f"Vorname beinhaltet unzulässige Sonderzeichen oder Leerzeichen. Benutzen Sie '-' für Doppelnamen.")
                self.fNameLabel.configure(fg="red")
                return False
            # Check for numbers
            for i in nameString:
                if i.isdigit() == True:
                    errorMessage("Vorname beinhaltet unzulässige Sonderzeichen",
                                 f"Nachname beinhaltet unzulässige Sonderzeichen oder Leerzeichen. Benutzen Sie '-' für Doppelnamen.")
                    self.fNameLabel.configure(fg="red")
                    return False
                    # Attempt auto-correct
            if originalNameString != nameString and originalNameString not in self.autoCorrectExceptions:
                question = yesnocancelMessage("Vornamen-Korrektur",
                                              f"Vorname wurde autokorrigiert.\n\n{originalNameString} --> {nameString}\n\nZum Fortfahren mit korrigierten Name mit 'Yes' bestätigen, für den ursprünglichen Namen mit 'No' speichern, und 'Cancel' um per Hand zu korrigieren\n\n(Falls 'No' ausgewählt wird, wird dieser Name nicht mehr korrigiert)")
                if question == True:
                    self.fName = nameString
                    self.fNameEntry.delete(0, "end")
                    self.fNameEntry.insert(0, nameString)
                elif question == False:
                    self.fName = originalNameString
                    self.autoCorrectExceptions.append(self.fName)
                else:
                    self.fNameLabel.configure(fg="red")
                    return False
            return True

        def checkLName(nameString):
            originalNameString = nameString

            # Formatting:
            # Remove leading and trailing white spaces:
            nameString = nameString.strip()

            # Attempt to fix capitalization and replace spaces in between with "-", with the assumption that it was meant to be a double name
            nameString = nameString.lower()
            tempString = ""
            tempString2 = ""
            for i in nameString.split(" "):
                tempString += i.capitalize()
                try:
                    if tempString[-1] != "-":
                        tempString += "-"
                except IndexError:
                    pass
            for i in tempString.split("-"):
                tempString2 += i.capitalize()
                tempString2 += "-"
            while tempString2[-1] == "-":
                tempString2 = tempString2[:-1]
            nameString = tempString2

            # Check if blacklist is enabled and whether the name is in it
            if self.useNamesBlacklist:
                if nameString in self.blacklistedWords:
                    errorMessage("Unzulässiger Name", f"Der Name ist nicht erlaubt.")
                    self.lNameLabel.configure(fg="red")
                    return False

            # Check  name for length after removing the spaces
            if len(nameString) > self.allowedNameLength[1]:
                errorMessage("Nachname zu lang",
                             f"Nachname ist zu lang. Es dürfen maximal {self.allowedNameLength[1]} Buchstaben benutzt werden.")
                self.lNameLabel.configure(fg="red")
                return False
            if len(nameString) < self.allowedNameLength[0]:
                errorMessage("Nachname zu kurz",
                             f"Nachname ist zu kurz. Es müssen mindestens {self.allowedNameLength[0]} Buchstaben benutzt werden.")
                self.lNameLabel.configure(fg="red")
                return False
            # isalnum() can detect non-letters (but not numbers); unfortunately it also detects hyphens which are necessary for double names
            # if no hypens are in the string but special characters or digits are, we stop
            if not nameString.isalnum() and "-" not in nameString:
                errorMessage("Nachname beinhaltet unzulässige Sonderzeichen",
                             f"Nachname beinhaltet unzulässige Sonderzeichen oder Leerzeichen. Benutzen Sie '-' für Doppelnamen.")
                self.lNameLabel.configure(fg="red")
                return False
            # if there are as many non-letters as hyphens, we proceed; otherwise it means there are non-hypen special characters and we abort
            countHyphen, countNonChars = 0, 0
            for i in nameString:
                if i == "-":
                    countHyphen = + 1
            for i in nameString:
                if i.isalnum() == False:
                    countNonChars = + 1
            if countNonChars > countHyphen:
                errorMessage("Nachname beinhaltet unzulässige Sonderzeichen",
                             f"Nachname beinhaltet unzulässige Sonderzeichen oder Leerzeichen. Benutzen Sie '-' für Doppelnamen.")
                self.lNameLabel.configure(fg="red")
                return False
            # Check for numbers
            for i in nameString:
                if i.isdigit() == True:
                    errorMessage("Nachname beinhaltet unzulässige Sonderzeichen",
                                 f"Nachname beinhaltet unzulässige Sonderzeichen oder Leerzeichen. Benutzen Sie '-' für Doppelnamen.")
                    self.lNameLabel.configure(fg="red")
                    return False
                    # Attempt auto-correct
            if originalNameString != nameString and originalNameString not in self.autoCorrectExceptions:
                question = yesnocancelMessage("Nachnamen-Korrektur",
                                              f"Nachname wurde autokorrigiert.\n\n{originalNameString} --> {nameString}\n\nZum Fortfahren mit korrigierten Name mit 'Yes' bestätigen, für den ursprünglichen Namen mit 'No' speichern, und 'Cancel' um per Hand zu korrigieren\n\n(Falls 'No' ausgewählt wird, wird dieser Name nicht mehr korrigiert)")
                if question == True:
                    self.lName = nameString
                    self.lNameEntry.delete(0, "end")
                    self.lNameEntry.insert(0, nameString)
                elif question == False:
                    self.lName = originalNameString
                    self.autoCorrectExceptions.append(self.lName)
                else:
                    self.lNameLabel.configure(fg="red")
                    return False
            return True

        def isLeapYear(year):
            year = int(year)
            if year % 100 == 0:
                if year % 400 == 0:
                    return True
            elif year % 4 == 0:
                return True
            return False

        def getAge(birthday):
            day = int(birthday.split(".")[0])
            month = int(birthday.split(".")[1])
            year = int(birthday.split(".")[2])
            self.age = self.currentYear - year - 1
            if month < self.currentMonth:
                self.age += 1
            elif month == self.currentMonth and day <= self.currentDay:
                self.age += 1
            return self.age

        def checkBirthday(birthday):
            # First check: Were only numbers entered, seperated by a "."?
            try:
                intDay = int(birthday.split(".")[0])
                intMonth = int(birthday.split(".")[1])
                intYear = int(birthday.split(".")[2])
                if intDay < 0:
                    self.birthdayLabel.configure(fg="red")
                    errorMessage("Ungültiger Geburtstag", "Bitte keine negativen Zahlen eingeben.")
                    return False
                # Negative values for month and year should not be possible, since
                # a) year has to be 4 digits and in a given range
                # b) month is checked for specifically in below
            except (ValueError, IndexError):
                self.birthdayLabel.configure(fg="red")
                errorMessage("Ungültiger Geburtstag", "Bitte nur Zahlen in diesem Format eingeben:\n\ndd.mm.yyyy")
                return False
            day = birthday.split(".")[0]
            if len(day) == 1:
                day = "0" + day
            month = birthday.split(".")[1]
            if len(month) == 1:
                month = "0" + month
            year = birthday.split(".")[2]
            if len(day) == 2 and len(month) == 2 and len(year) == 4:
                pass
            else:
                self.birthdayLabel.configure(fg="red")
                errorMessage("Ungültiger Geburtstag",
                             "Tag und Monate dürfen nur 1 oder 2 Ziffern enthalten, das Jahr muss jedoch 4 beinhalten.")
                return False
            if month not in ("01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"):
                self.birthdayLabel.configure(fg="red")
                errorMessage("Ungültiger Geburtstag", "Ungültiger Monat.")
                return False
            if month == "02" and day > "28" and not isLeapYear(year):
                self.birthdayLabel.configure(fg="red")
                errorMessage("Ungültiger Geburtstag", "Dieser Februar hat nur 28 Tage.")
                return False
            elif month == "02" and day > "29" and isLeapYear(year):
                self.birthdayLabel.configure(fg="red")
                errorMessage("Ungültiger Geburtstag", "Dieser Februar hat nur 29 Tage.")
                return False
            elif month in ("04", "06", "09", "11") and day > "30":
                self.birthdayLabel.configure(fg="red")
                errorMessage("Ungültiger Geburtstag", "Dieser Monat hat nur 30 Tage.")
                return False
            elif month not in ("04", "06", "09", "11") and day > "31":
                self.birthdayLabel.configure(fg="red")
                errorMessage("Ungültiger Geburtstag", "Dieser Monat hat nur 31 Tage.")
                return False
            if getAge(birthday) > self.allowedAgeRange[1] or getAge(birthday) < self.allowedAgeRange[0]:
                self.birthdayLabel.configure(fg="red")
                self.oldestAllowedBirthdate = [self.currentDay, self.currentMonth, self.currentYear - self.allowedAgeRange[1]]

                self.youngestAllowedBirthdate = [self.currentDay, self.currentMonth, self.currentYear - self.allowedAgeRange[0]]
                range1 = str(self.oldestAllowedBirthdate[0]) + "." + str(self.oldestAllowedBirthdate[1]) + "." + str(
                    self.oldestAllowedBirthdate[2])
                range2 = str(self.youngestAllowedBirthdate[0]) + "." + str(
                    self.youngestAllowedBirthdate[1]) + "." + str(self.youngestAllowedBirthdate[2])
                errorMessage("Ungültiger Geburtstag",
                             f"Das eingegebene Datum ist nicht im erlaubten Bereich.\n\n (Erlaubter Bereich: {range1} bis {range2})")
                return False
            # if every check passes, return the (potentially) red color back to black and continue on
            self.birthdayLabel.configure(fg="black")
            self.birthday = day + "." + month + "." + year
            return True

        def checkEMail(eMail):
            # Fortunately, e-mails addresses are not case sensitive so we can capitalization
            # E-Mails should consist of two strings, seperated by the @. If there are more, the input was invalid.
            if len(eMail.split("@")) != 2:
                self.eMailLabel.configure(fg="red")
                errorMessage("Ungültiges E-Mail Format",
                             "E-Mails dürfen nur in diesem Format eingegeben werden:\n\n'beispielname@beispieldomain.de'\n\nZum Beispiel: 'Frosch123@gmail.com'")
                return False
            else:
                accountName = eMail.split("@")[0]
                domainName = eMail.split("@")[1]
            # Check whether Blacklist ist enabled and whether the E-Mail we are checking is using that domain
            if (self.useEmailBlacklist and domainName in self.eMailBlacklist) or (
                    self.useEmailWhitelist and domainName not in self.eMailWhitelist):
                self.eMailLabel.configure(fg="red")
                errorMessage("Ungültige E-Mail", "Diese E-Mail ist nicht erlaubt.")
                return False

            # accountName should be at least one character, domain name at least 4 (i.e. "x.de").
            if len(accountName) >= 1 and len(domainName) >= 4:
                pass
            else:
                self.eMailLabel.configure(fg="red")
                errorMessage("Ungültige E-Mail", "Die E-Mail ist zu kurz.")
                return False
            # domainName should have it's final . before at least two letters (.de, .com etc)
            # We expect to find a . at index -3 or -4, but no more . in the last 2 or 3 letters. (exclude i.e. ".d.e")
            if not (domainName[-3] == "." or domainName[-4] == "."): # .de / .com
                self.eMailLabel.configure(fg="red")
                errorMessage("Ungültige E-Mail", "Fehler im Domain-Namen.")
                return False
            if "." in domainName[-2:] and "." in domainName[-3:]:
                self.eMailLabel.configure(fg="red")
                errorMessage("Ungültige E-Mail", "Fehler im Domain-Namen.")
                return False
            # All ASCII chars should be allowed for accountName and domainName. Python can encode a string in ASCII, if the original string is the same as the ASCII Encoded one we know the original string was 100% ASCII compliant
            # Same thing with white spaces: attempt to remove white spaces, then compare lengths
            # Finally, check both for non-repeating "."; they are allowed in the name but not if following another "."
            if (len(accountName) == len(accountName.encode("ascii"))) and (len(accountName) == len(accountName.replace(" ", ""))):
                if "" not in accountName.split("."):  #Two . in a row would create a list with an empty space
                    pass
            else:
                self.eMailLabel.configure(fg="red")
                errorMessage("Ungültige E-Mail", "Der Account-Name enthält nicht erlaubte Zeichen oder Leerzeichen.")
                return False
            if (len(domainName) == len(domainName.encode("ascii"))) and (len(domainName) == len(domainName.replace(" ", ""))):
                pass
            else:
                self.eMailLabel.configure(fg="red")
                errorMessage("Ungültige E-Mail", "Der Domain-Name enthält nicht erlaubte Zeichen oder Leerzeichen.")
                return False
            # This will allow (potentially) nonsensical domains like ".du", ".bo" but not sure how to solve that without knowing every single acceptable domain ending.
            return True

        def incrementID():
            self.idCounter += 1
            return str(self.idCounter)

        def addEntry():
            if self.idEntry.cget("state") == "disabled":
                self.id_ = incrementID()

                while self.id_ in self.idList:
                    self.id_ = incrementID()

            else:
                self.id_ = self.idEntry.get()
                if self.id_ == "":
                    self.idLabel.configure(fg="red")
                    errorMessage("Ungültige ID", "ID darf nicht leer sein.")
                    return
            self.fName = self.fNameEntry.get()
            if checkFName(self.fName):
                self.fNameLabel.configure(fg="black")
            else:
                return
            self.lName = self.lNameEntry.get()
            if checkLName(self.lName):
                self.lNameLabel.configure(fg="black")
            else:
                return
            self.birthday = self.birthdayEntry.get()
            if checkBirthday(self.birthday):
                self.age = f" ({getAge(self.birthday)})"
            else:
                return
            self.eMail = self.eMailEntry.get()
            if checkEMail(self.eMail):
                self.eMailLabel.configure(fg="black")
            else:
                return
            self.gender = self.genderCombo.get()
            if self.id_ in self.idList:
                self.idLabel.configure(fg="red")
                errorMessage("Ungültige ID", "ID existiert bereits.")
                return
            else:
                self.idLabel.configure(fg="black")
                self.tree.insert("", "end", values=(
                self.id_, self.fName, self.lName, self.birthday + self.age, self.eMail, self.gender))
                self.idList.append(self.id_)

        def removeEntry():
            try:
                self.selectedEntry = self.tree.selection()[0]
                self.tree.delete(self.selectedEntry)
            except (IndexError, AttributeError): #if you try to delete without having anything selected
                pass
            try:  # If I try to remove the last row, it will always attempt to remove the one that doesn't exist yet. It is off by +1, it works for all other rows.
                self.idList.remove(self.selectedEntry)
            except ValueError:  # Therefore, if the normal deletion fails, we pop the last item from the list. It's not elegant though.
                self.idList.pop()
            except AttributeError: # Don't throw an error if nothing was selected
                pass

        # Save and Loading
        
        def loadFile():
            file = filedialog.askopenfile()
            try: # If user closes the window before choosing a file to load
                self.loadFileName = file.name
            except AttributeError:
                pass 
            
            if not file:
                return
            # Clean up the displayed table, empty the idList:
                self.idList = []
                
            for child in self.tree.get_children():
                self.tree.delete(child)
            
            # Open, read contents and close file
            f = open (file.name, "r")
            data = json.loads(f.read())
            f.close()
            
            # Input the loaded data into the table
            for i in range(len(data)):
                self.id_ = data[i]["id_"]
                self.fName = data[i]["fName"]
                self.lName = data[i]["lName"]
                self.birthday = data[i]["birthday"]
                self.eMail = data[i]["eMail"]
                self.gender = data[i]["gender"]
                self.tree.insert("", "end", values=(self.id_, self.fName, self.lName, self.birthday, self.eMail, self.gender))
                self.idList.append(str(self.id_))

            
            
        def saveFileAs():
            file = filedialog.askopenfile()
            try: # If user closes the window before choosing a file to save
                self.saveFileAsName = file.name
            except AttributeError:
                pass 
            if not file:
                errorMessage("Speichern fehlgeschlagen", "Keine Datei ausgewählt")
                return
            
            # Read each row of displayed entries
            for child in self.tree.get_children():
                
                # Create the Person objects and store them in a list
                self.personList.append(Person(self.tree.item(child)["values"][0], self.tree.item(child)["values"][1], self.tree.item(child)["values"][2], self.tree.item(child)["values"][3], self.tree.item(child)["values"][4], self.tree.item(child)["values"][5]))
            
            json_string = json.dumps([ob.__dict__ for ob in self.personList])
            f = open(self.saveFileAsName, "w")
            f.write(json_string)
            f.close()
            
            infoMessage("Datei gespeichert", f"Datei erfolgreich unter {file.name} gespeichert")
            return 

       
        def saveFile():
            if not self.saveFileAsName == "":
                # Read each row of displayed entries
                for child in self.tree.get_children():
                    
                    # Create the Person objects and store them in a list
                    self.personList.append(Person(self.tree.item(child)["values"][0], self.tree.item(child)["values"][1], self.tree.item(child)["values"][2], self.tree.item(child)["values"][3], self.tree.item(child)["values"][4], self.tree.item(child)["values"][5]))
                
                json_string = json.dumps([ob.__dict__ for ob in self.personList])
                f = open(self.saveFileAsName, "w")
                f.write(json_string)
                f.close()
                
                #for i in range(len(json_string)):
                #    print(json_string[i])
                infoMessage("Datei gespeichert", f"Datei erfolgreich unter {self.saveFileAsName} gespeichert")
                return 
            else:
                saveFileAs()
            
        def deleteAllEntries():
            # Confirmation check:
            if questionMessage("Alle Einträge löschen?", "Wirklich alle Einträge löschen? Ungespeicherte Daten gehen verloren!") == "yes":
                
                # Clean up the displayed table, empty the idList and reset the auto-increment counter:
                self.idList = []
                self.idCounter = 0
                
                for child in self.tree.get_children():
                    self.tree.delete(child)            
                return
            else:
                return
        
        def updateSettings():
            self.allowedNameLength = [int(self.minNameLengthEntry.get()), int(self.maxNameLengthEntry.get())]
            self.allowedAgeRange = [int(self.minAgeEntry.get()), int(self.maxAgeEntry.get())]

            if self.nameBlackListCombo.get() == "nein":
                self.useNamesBlacklist = False

            if self.nameBlackListCombo.get() == "ja":
                self.useNamesBlacklist = True

            if self.eMailBlackListCombo.get() == "keine":
                self.useEmailBlacklist = False
                self.useEmailWhitelist = False
                self.eMailBlackListCombo.insert(0, "keine")

            elif self.eMailBlackListCombo.get() == "Blacklist":
                self.useEmailBlacklist = True
                self.useEmailWhitelist = False
                self.eMailBlackListCombo.insert(0, "Blacklist")

            elif self.eMailBlackListCombo.get() == "Whitelist":
                self.useEmailBlacklist = False
                self.useEmailWhitelist = True
                self.eMailBlackListCombo.insert(0, "Whitelist")


        def optionsWindow():
            optionsWindow = Tk()
            optionsWindow.title("Optionen")
            
            # Create the entries and labels
            self.minNameLengthLabel = Label(optionsWindow, text="Mindestlänge für Vor-/Nachname")
            self.minNameLengthEntry = Entry(optionsWindow, width=3)
            self.minNameLengthEntry.insert(0, self.allowedNameLength[0])

            self.maxNameLengthLabel = Label(optionsWindow, text="Maximallänge für Vor-/Nachname")
            self.maxNameLengthEntry = Entry(optionsWindow, width=3)
            self.maxNameLengthEntry.insert(0, self.allowedNameLength[1])

            self.minAgeLabel = Label(optionsWindow, text="Kleinstes erlaubtes Alter")
            self.minAgeEntry = Entry(optionsWindow, width=3)
            self.minAgeEntry.insert(0, self.allowedAgeRange[0])

            self.maxAgeLabel = Label(optionsWindow, text="Hochstes erlaubtes Alter")
            self.maxAgeEntry = Entry(optionsWindow, width=3)
            self.maxAgeEntry.insert(0, self.allowedAgeRange[1])

            self.nameBlackListLabel = Label(optionsWindow, text="Blacklist für Namen?")
            self.nameBlackListCombo = ttk.Combobox(optionsWindow, values=("ja", "nein"), width=7)
            self.nameBlackListCombo.insert(0, "nein")
            self.nameBlackListCombo.configure(state="readonly")

            self.eMailBlacklistLabel = Label(optionsWindow, text="Status der E-Mail Black- bzw. Whitelist")
            self.eMailBlackListCombo = ttk.Combobox(optionsWindow, values=("keine", "Blacklist", "Whitelist"), width=7)
            self.eMailBlackListCombo.insert(0, "keine")
            self.eMailBlackListCombo.configure(state="readonly")

            self.saveButton = Button(optionsWindow, text="Speichern", command = updateSettings)

            self.minNameLengthLabel.grid(column=0, row=0)
            self.minNameLengthEntry.grid(column=1, row=0)

            self.maxNameLengthLabel.grid(column=0, row=1)
            self.maxNameLengthEntry.grid(column=1, row=1)

            self.minAgeLabel.grid(column=0, row=2)
            self.minAgeEntry.grid(column=1, row=2)

            self.maxAgeLabel.grid(column=0, row=3)
            self.maxAgeEntry.grid(column=1, row=3)

            self.nameBlackListLabel.grid(column=0, row=4)
            self.nameBlackListCombo.grid(column=1, row=4)

            self.eMailBlacklistLabel.grid(column=0, row=5)
            self.eMailBlackListCombo.grid(column=1, row=5)

            self.saveButton.grid(column=0, row=6, columnspan=2)




            



def main():
    # Create the main window
    root = Tk()

    gui = GUI(root)

    # Start the GUI
    root.mainloop()


# Making sure that this only runs if it is the main file
if __name__ == "__main__":
    main()
