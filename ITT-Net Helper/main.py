from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from idlelib.tooltip import Hovertip
import NetzAdCalc as nac
import Subnetting as sbn

class ITT: #ITT-Helper Main Window

    def __init__(self, master, logo1, logo2, logo3, logo4):

        self.net_logo = logo1
        self.isc_logo = logo2
        self.tsc_logo = logo3
        self.quiz_logo = logo4
        self.filename = "default.csv"

        # Root
        master.title("ITT-NET Helper")
        master.resizable(False, False)

        # Menu
        master.option_add('*tearOff', False)
        menubar = Menu(master)
        master.config(menu=menubar)

        Datei = Menu(menubar)
        Bearbeiten = Menu(menubar)
        Hilfe = Menu(menubar)

        menubar.add_cascade(menu=Datei, label="Datei")
        menubar.add_cascade(menu=Bearbeiten, label="Bearbeiten")
        menubar.add_cascade(menu=Hilfe, label="Hilfe")

        # Maybe use this to force a switch to Quiz tab when a quiz file is opened? Look into it later
        def switchTab(x):
            notebook.select(x)

        def openFile():
            if messagebox.askyesno(title="Quizdatei laden?", message="Dies ist noch nicht implementiert.\n\n Fortfahren?") == True:
                self.filename = filedialog.askopenfile()
                print(filename.name)
            return self.filename

        def errorMessage(errorMessage="Bitte überprüfe deine Eingaben."):
            messagebox.showerror(title="Fehler!", message=errorMessage)

        Datei.add_command(label="Lade Quizdatei", command = openFile)
        Datei.add_command(label="Speichere Quizdatei", command = None)
        Datei.add_separator()
        Datei.add_command(label="Exit", command = lambda: master.destroy())


        # Root -> Notebook
        self.notebook = ttk.Notebook(master)
        self.notebook.pack()

        NAC_tab = ttk.Frame(self.notebook)
        ISC_tab = ttk.Frame(self.notebook)
        TSC_tab = ttk.Frame(self.notebook)
        Quiz_tab = ttk.Frame(self.notebook)

        self.notebook.add(NAC_tab, text="Netzadresse")
        netAddressCalculator = NAC(NAC_tab, self.net_logo)

        self.notebook.add(ISC_tab, text="Bildgröße")
        imageSizeCalculator = ISC(ISC_tab, self.isc_logo)

        self.notebook.add(TSC_tab, text="Datei-Transfer")
        transferSpeedCalculator = TSC(TSC_tab, self.tsc_logo)

        self.notebook.add(Quiz_tab, text="Quiz")
        quiz = Quiz(Quiz_tab, self.quiz_logo)

class NAC():  # Netzadresse

    def __init__(self, frame, logo):

        self.logo = logo.subsample(5, 5)

        # Frame1 -> Header
        self.frame = frame
        self.frame_header = ttk.Frame(frame)
        self.frame_header.pack()

        # Frame1 -> Logo & Text

        ttk.Label(self.frame_header, image=logo).grid(row=0, column=0, rowspan=2)
        ttk.Label(self.frame_header, text="Netzadressenrechner").grid(row=0, column=1)  # style = "Header.TLabel"
        ttk.Label(self.frame_header, wraplength=600,
                  text="\nBerechnung der Netz-ID, Broadcast-IP, erster und letzter nutzbarer IP und Anzahl der nutzbaren Hosts.\n").grid(
            row=1, column=1)

        # Frame1-Body
        self.frame_content = ttk.Frame(frame)
        self.frame_content.pack()

        # Frame1-Body -> Sub/CIDR + Entry Subframe
        self.frame_content_sub = ttk.Frame(self.frame_content)
        self.frame_content_sub.grid(row=2, column=1)

        # Radiobuttons
        # Subnetz will be set as default, these function allow us to switch which entry is greyed out
        def disableCIDR_enableSub():
            self.spin_CIDR.configure(state=["disabled"])
            self.entry_sub.configure(state=["!disabled"])

        def disableSub_enableCIDR():
            self.entry_sub.configure(state=["disabled"])
            self.spin_CIDR.configure(state=["!disabled"])

        self.v = IntVar()
        self.subRadio = ttk.Radiobutton(self.frame_content_sub, text="Subnetz", variable=self.v, value=1,
                                        command=lambda: disableCIDR_enableSub())
        self.subRadio.grid(row=0, column=0, sticky="w")
        self.CIDRRadio = ttk.Radiobutton(self.frame_content_sub, text="CIDR", variable=self.v, value=2,
                                         command=lambda: disableSub_enableCIDR())
        self.CIDRRadio.grid(row=1, column=0, sticky="w")

        self.entry_sub = ttk.Entry(self.frame_content_sub, width=15)
        self.entry_sub.grid(row=0, column=1)
        self.entry_sub.insert(0, "255.255.255.240")

        self.spin_CIDR = ttk.Spinbox(self.frame_content_sub, from_=1, to=32, width=13)
        self.spin_CIDR.grid(row=1, column=1)
        self.spin_CIDR.insert(0, "28")

        # Set radiobutton default to Subnetz and disable CIDR entry
        self.v.set(1)
        self.spin_CIDR.configure(state=["disabled"])

        self.label_Netzadresse = ttk.Label(self.frame_content, text="Netzadresse")
        self.label_Netzadresse.grid(row=1, column=0)
        self.entry_Netzadresse = ttk.Entry(self.frame_content, width=15)
        self.entry_Netzadresse.grid(row=2, column=0)
        self.entry_Netzadresse.insert(0, "192.168.110.0")
        Hovertip(self.entry_Netzadresse, 'Format: xxx.xxx.xxx.xxx')

        self.ergebnisbox = Text(self.frame_content, width=65, height=16)
        self.ergebnisbox.grid(row=4, column=0)
        self.ergebnisbox.insert("1.0", "Ergebnisbox")
        self.rechenwegbox = Text(self.frame_content, width=65, height=16)
        self.rechenwegbox.grid(row=4, column=1)
        self.rechenwegbox.insert("1.0", "Detaillierter Rechenweg")

        def calc():
            # Clear the text boxes to be filled in
            self.ergebnisbox.delete("1.0", "end")
            self.rechenwegbox.delete("1.0", "end")

            # Get the inputs
            # IP-Address
            inputNetzadresse = self.entry_Netzadresse.get()

            # Subnet, get it from whichever box is currently active
            # From Subnetz
            if self.v.get() == 1:
                inputSub = self.entry_sub.get()  # for text widgets it'd be .get("1.0", "end")
                CIDR = nac.sub_to_CIDR(nac.Sub_split(inputSub))
            # From CIDR
            elif self.v.get() == 2:
                CIDR = int(self.spin_CIDR.get())
                inputSub = nac.CIDR_to_sub(CIDR)

            # Remaining calculations
            binary_IP = nac.IP_split(inputNetzadresse)
            binary_sub = nac.Sub_split(inputSub)
            addition = nac.binary_add(binary_IP, binary_sub)
            network_ID = nac.netzIDlist(addition)
            network_type = nac.network_class(addition)
            octet = nac.oktett(CIDR)
            block_size = nac.block_size(CIDR)
            broadcast_IP, first_IP, last_IP = nac.broadcastIP(network_ID, octet, block_size)
            unmodified_block = 2 ** (32 - CIDR)
            max_usable_hosts = 2 ** (32 - CIDR) - 2
            if max_usable_hosts < 0:
                max_usable_hosts = 0
            max_subnets = 2 ** (30 - CIDR)
            if CIDR > 30:
                max_subnets = 0

            # Outputs Ergebnisbox
            self.ergebnisbox.insert("end", f"IP-Adresse: {inputNetzadresse}\n")
            self.ergebnisbox.insert("end", f"Subnetz:    {inputSub}, CIDR: {CIDR}\n")
            self.ergebnisbox.insert("end", f"\n")
            self.ergebnisbox.insert("end",
                                    f"Netz-ID:    {network_ID[0]}.{network_ID[1]}.{network_ID[2]}.{network_ID[3]}"
                                    f" /{CIDR}, {network_type}\n")
            self.ergebnisbox.insert("end", f"\n")
            self.ergebnisbox.insert("end", f"Broadcast:  {broadcast_IP}\n")
            self.ergebnisbox.insert("end", f"Erste IP:   {first_IP}\n")
            self.ergebnisbox.insert("end", f"Letzte IP:  {last_IP}\n")
            self.ergebnisbox.insert("end", f"\n")
            self.ergebnisbox.insert("end", f"Anzahl nutzbarer Hosts: {max_usable_hosts}\n")
            self.ergebnisbox.insert("end", f"Maximale Anzahl nutzbarer Subnetze: {max_subnets}\n")
            if max_subnets >= 4:
                self.ergebnisbox.insert("end", f"In wie viele Subnets teilen?    ")
                self.subnetting = ttk.Button(self.ergebnisbox, text="Subnet!",
                                             command=lambda: subnetting(network_ID, CIDR))
                self.combo_subnetting = ttk.Combobox(self.ergebnisbox, width=4)
                max_subnets_values = [2 ** x for x in range((30 - CIDR) + 1)]

                # Set some sane limits here
                if len(max_subnets_values) >= 2:  # remove 0 and 1 if there is at least 2 possible subnets
                    max_subnets_values = max_subnets_values[1:]
                if len(max_subnets_values) >= 6:  # remove the ridiculously high subnetting values, they are impractical anyway
                    max_subnets_values = max_subnets_values[:6]  # 10 --> 65536

                self.combo_subnetting.config(values=max_subnets_values)
                self.combo_subnetting.set(max_subnets_values[0])

                self.ergebnisbox.window_create("insert", window=self.combo_subnetting)
                self.ergebnisbox.window_create("insert", window=self.subnetting)
                self.ergebnisbox.insert("end", f"\n\nBitte beachten: Subnetting ist übersichtshalber auf 64 begrenzt    ")

            # Spacing for visualization of the broadcast calculations in Rechenwegbox
            # (.center probably would have worked as well with conversion to str first?)

            if octet == 4:
                pad = 25 * " "
            elif octet == 3:
                pad = 17 * " "
            elif octet == 2:
                pad = 10 * " "
            elif octet == 1:
                pad = 1 * " "
            pad2 = 25 * " "
            bc_spaced = list(broadcast_IP.split("."))

            # Outputs Rechenwegbox
            self.rechenwegbox.insert("end", f"IP-Binär:        {binary_IP}\n")
            self.rechenwegbox.insert("end", f"Subnetz-Binär: + {binary_sub}\n")
            self.rechenwegbox.insert("end", f"Netz-ID(bin):  = {addition}\n")
            self.rechenwegbox.insert("end", f"\n")
            self.rechenwegbox.insert("end",
                                     f"Netz-ID(dez):            {network_ID[0]}  .  {network_ID[1]}  .  {network_ID[2]}  .  {network_ID[3]}\n")
            self.rechenwegbox.insert("end", f"Blockgröße auf {octet}.Oktett{pad}+{block_size}\n")
            self.rechenwegbox.insert("end", f"1 vom 4.Oktett abziehen{pad2}-1 \n")
            self.rechenwegbox.insert("end",
                                     f"Broadcast:             = {bc_spaced[0]}  .  {bc_spaced[1]}  .  {bc_spaced[2]}  .  {bc_spaced[3]}\n")
            self.rechenwegbox.insert("end", f"\n")
            self.rechenwegbox.insert("end", f"Blockgröße: {block_size}")
            if unmodified_block <= 256:
                self.rechenwegbox.insert("end", f"\n")
            elif unmodified_block > 256:
                self.rechenwegbox.insert("end", f" ({unmodified_block}/256")
                while unmodified_block > 256:
                    unmodified_block = unmodified_block // 256
                    if unmodified_block < 256:
                        self.rechenwegbox.insert("end", f" = {unmodified_block})\n")
                    else:
                        self.rechenwegbox.insert("end", f" = {unmodified_block}/256")
            if max_subnets == 0:
                self.rechenwegbox.insert("end", f"CIDR darf nicht größer als 30 sein.")
            else:
                self.rechenwegbox.insert("end",
                                         f"30 Bit - {CIDR} Bit = {30 - CIDR} Bit = {2 ** (30 - CIDR)} (2^{30 - CIDR})")
                self.rechenwegbox.insert("end",
                                         f"\n\nSubnetze gibt es immer nur in Zweierpotenzschritten. Falls eine \nandere gesucht wird (z.B. '7'), dann muss die nächsthöhere in der\nListe gewählt werden ('8').")

        ttk.Button(self.frame_content, text="Berechnen", command=lambda: calc()).grid(row=5, column=0, columnspan=2)

        def subnetting(network_ID, CIDR):
            num_of_subnets = int(self.combo_subnetting.get())
            if num_of_subnets == 1:
                return
            elif num_of_subnets not in sbn.CIDR_dict.keys():
                print("something")
                return

            list_of_net_IDs = sbn.subnet_net_IDs(network_ID, CIDR, num_of_subnets)

            list_of_first_IPs = sbn.subnet_first_IPs(list_of_net_IDs)

            list_of_bc_IPs = sbn.subnet_bc_IPs(list_of_net_IDs)

            # list_of_bc_IPs = list_of_bc_IPs[1:]
            list_of_last_IPs = sbn.subnet_last_IPs(list_of_bc_IPs)

            # list_of_net_IDs = list_of_net_IDs[:-1]
            # list_of_first_IPs = list_of_first_IPs[:-1]

            # FORMATTING & STYLE
            fg1 = "#195c03"  # dark green
            fg2 = "#030f73"  # dark blue
            boldfont = "Verdana 14 bold"

            # Creating the window
            subnet = Tk()
            subnet.title(
                f"Subnetting {list_of_net_IDs[0][0]}.{list_of_net_IDs[0][1]}.{list_of_net_IDs[0][2]}.{list_of_net_IDs[0][3]}/{CIDR} in {num_of_subnets} Netze")

            ttk.Label(subnet, text="#", font=boldfont).grid(row=0, column=0, padx=10)
            ttk.Label(subnet, text="Netz-ID", font=boldfont).grid(row=0, column=1, padx=30)
            ttk.Label(subnet, text="Erste IP", font=boldfont).grid(row=0, column=2, padx=30)
            ttk.Label(subnet, text="Letzte IP", font=boldfont).grid(row=0, column=3, padx=30)
            ttk.Label(subnet, text="Broadcast IP", font=boldfont).grid(row=0, column=4, padx=30)

            if num_of_subnets > 32:
                ttk.Label(subnet, text="|", font=boldfont).grid(row=0, column=5, padx=30)
                ttk.Label(subnet, text="#", font=boldfont).grid(row=0, column=6, padx=10)
                ttk.Label(subnet, text="Netz-ID", font=boldfont).grid(row=0, column=7, padx=30)
                ttk.Label(subnet, text="Erste IP", font=boldfont).grid(row=0, column=8, padx=30)
                ttk.Label(subnet, text="Letzte IP", font=boldfont).grid(row=0, column=9, padx=30)
                ttk.Label(subnet, text="Broadcast IP", font=boldfont).grid(row=0, column=10, padx=30)

            for i in range(len(list_of_net_IDs)):
                if i >= 32:
                    if i % 2:
                        fg = fg1
                    else:
                        fg = fg2
                    ttk.Label(subnet, text="|").grid(row=i - 31, column=5, padx=30)
                    ttk.Label(subnet, text=f"{i + 1}. Netz", foreground=fg).grid(row=i - 31, column=6, padx=5)
                    ttk.Label(subnet,
                              text=f"{list_of_net_IDs[i][0]}.{list_of_net_IDs[i][1]}.{list_of_net_IDs[i][2]}.{list_of_net_IDs[i][3]}  /{CIDR + sbn.CIDR_dict[num_of_subnets]}",
                              foreground=fg).grid(
                        row=i - 31, column=7,
                        padx=27)
                    ttk.Label(subnet,
                              text=f"{list_of_first_IPs[i][0]}.{list_of_first_IPs[i][1]}.{list_of_first_IPs[i][2]}.{list_of_first_IPs[i][3]}",
                              foreground=fg).grid(
                        row=i - 31,
                        column=8,
                        padx=30)
                    ttk.Label(subnet,
                              text=f"{list_of_last_IPs[i][0]}.{list_of_last_IPs[i][1]}.{list_of_last_IPs[i][2]}.{list_of_last_IPs[i][3]}",
                              foreground=fg).grid(
                        row=i - 31, column=9,
                        padx=30)
                    ttk.Label(subnet,
                              text=f"{list_of_bc_IPs[i][0]}.{list_of_bc_IPs[i][1]}.{list_of_bc_IPs[i][2]}.{list_of_bc_IPs[i][3]}",
                              foreground=fg).grid(
                        row=i - 31, column=10,
                        padx=30)
                else:
                    if i % 2:
                        fg = fg1
                    else:
                        fg = fg2
                    ttk.Label(subnet, text=f"{i + 1}. Netz", foreground=fg).grid(row=i + 1, column=0, padx=5)
                    ttk.Label(subnet,
                              text=f"{list_of_net_IDs[i][0]}.{list_of_net_IDs[i][1]}.{list_of_net_IDs[i][2]}.{list_of_net_IDs[i][3]}  /{CIDR + sbn.CIDR_dict[num_of_subnets]}",
                              foreground=fg).grid(row=i + 1, column=1,
                                                  padx=27)
                    ttk.Label(subnet,
                              text=f"{list_of_first_IPs[i][0]}.{list_of_first_IPs[i][1]}.{list_of_first_IPs[i][2]}.{list_of_first_IPs[i][3]}",
                              foreground=fg).grid(row=i + 1,
                                                  column=2,
                                                  padx=30)
                    ttk.Label(subnet,
                              text=f"{list_of_last_IPs[i][0]}.{list_of_last_IPs[i][1]}.{list_of_last_IPs[i][2]}.{list_of_last_IPs[i][3]}",
                              foreground=fg).grid(row=i + 1, column=3,
                                                  padx=30)
                    ttk.Label(subnet,
                              text=f"{list_of_bc_IPs[i][0]}.{list_of_bc_IPs[i][1]}.{list_of_bc_IPs[i][2]}.{list_of_bc_IPs[i][3]}",
                              foreground=fg).grid(row=i + 1, column=4,
                                                  padx=30)

            """print("Net-IDs", list_of_net_IDs)
            print("First IPs", list_of_first_IPs)
            print("Last IPs", list_of_last_IPs)
            print("Broadcasts", list_of_bc_IPs)
            print("  Start Address  |   End Address  |  Network Address  |  Broadcast Address ")
            for i in range(len(list_of_net_IDs)):
                print(list_of_first_IPs[i], "|", list_of_last_IPs[i], "|", list_of_net_IDs[i], "|", list_of_bc_IPs[i])"""

class ISC:  # Bildgröße

    def __init__(self, frame, logo):
        self.logo = logo
        self.frame = frame

        # Frame2 -> Header
        self.frame_header = ttk.Frame(frame)
        self.frame_header.pack()

        #s = ttk.Style()
        #s.configure("TFrame", background="orange")

        # Frame2 -> Logo & Text
        ttk.Label(self.frame_header, image=logo).grid(row=0, column=0, rowspan=2)
        ttk.Label(self.frame_header, text="Bild- und Videodateigrößenrechner").grid(row=0, column=1)  # style = "Header.TLabel"
        ttk.Label(self.frame_header, wraplength=600, text="\n Berechnung der Größe von Bild und Videodateien.\n\n""Bitte nur Zahlen ohne Einheiten eintippen\n").grid(row=1, column=1)

        # Frame2-Body
        self.frame_content = ttk.Frame(frame)
        self.frame_content.pack()

        # Frame2-Body -> Image Dimensions & Video Data
        self.frame_content_dimensions = ttk.Frame(self.frame_content)
        self.frame_content_dimensions.grid(row=0, column=0)

        self.frame_video_check = ttk.Frame(self.frame_content)
        self.frame_video_check.grid(row=1, column=1, sticky="n")

        self.frame_content_video = ttk.Frame(self.frame_content)
        self.frame_content_video.grid(row=0, column=1, sticky="n")


        # Radiobuttons
        # Pixel will be enabled by default, Video-Checkbox and DPI will be disabled from the get-go
        def disableDPI_enablePX():
            self.dpiWidthEntry.configure(state=["disabled"])
            self.dpiHeightEntry.configure(state=["disabled"])
            self.dpiEntry.configure(state=["disabled"])
            self.pxWidthEntry.configure(state=["!disabled"])
            self.pxHeightEntry.configure(state=["!disabled"])

        def disablePX_enableDPI():
            self.dpiWidthEntry.configure(state=["!disabled"])
            self.dpiHeightEntry.configure(state=["!disabled"])
            self.dpiEntry.configure(state=["!disabled"])
            self.pxWidthEntry.configure(state=["disabled"])
            self.pxHeightEntry.configure(state=["disabled"])

        def enableVideoFrame():
            for widget in self.frame_content_video.winfo_children():
                widget.configure(state=["!disabled"])

        def disableVideoFrame():
            for widget in self.frame_content_video.winfo_children():
                widget.configure(state=["disabled"])


        self.boolvar = BooleanVar()
        self.boolvar.set(False)
        self.checkbtnVideo = ttk.Checkbutton(self.frame_video_check, variable=self.boolvar, text="Video?", command=lambda: enableVideoFrame() if self.boolvar.get()==True else disableVideoFrame())
        self.checkbtnVideo.grid(row=0, column=0, padx=0, pady=0)
        self.PXorDPI = IntVar()
        self.pxRadio = ttk.Radiobutton(self.frame_content_dimensions,text="Pixel [Px]", variable=self.PXorDPI, value=1, command=lambda: disableDPI_enablePX())
        self.pxRadio.grid(row=0, column=0)
        self.pxHeightEntry = ttk.Entry(self.frame_content_dimensions, justify="center", width=5)
        self.pxHeightEntry.grid(row=0, column=1, padx=0, pady=0, sticky="w")
        self.pxHeightEntry.insert(0, "3200")
        ttk.Label(self.frame_content_dimensions, text="x    ").grid(row=0, column=2, padx=0, pady=0)
        self.pxWidthEntry = ttk.Entry(self.frame_content_dimensions, justify="center", width=5)
        self.pxWidthEntry.grid(row=0, column=3, sticky="w")
        self.pxWidthEntry.insert(0, "1800")

        self.dpiRadio = ttk.Radiobutton(self.frame_content_dimensions, text="DPI [cm]", variable=self.PXorDPI, value=2, command=lambda: disablePX_enableDPI())
        self.dpiRadio.grid(row=1, column=0)
        self.dpiHeightEntry = ttk.Entry(self.frame_content_dimensions, justify="center", width=5)
        self.dpiHeightEntry.grid(row=1, column=1, sticky="w")
        self.dpiHeightEntry.insert(0, "29.7")
        ttk.Label(self.frame_content_dimensions, text="x", width=1).grid(row=1, column=2, sticky="w", padx=0)
        self.dpiWidthEntry = ttk.Entry(self.frame_content_dimensions, justify="center", width=5)
        self.dpiWidthEntry.grid(row=1, column=3, sticky="w")
        self.dpiWidthEntry.insert(0, "21.0")
        ttk.Label(self.frame_content_dimensions, text="DPI:",width=4, borderwidth=0).grid(row=1, column=4, padx=0, pady=0, sticky="w")
        self.dpiEntry = ttk.Entry(self.frame_content_dimensions, justify="center", width=4)
        self.dpiEntry.grid(row=1, column=5, sticky="w")
        self.dpiEntry.insert(0, "300")

        self.compressionLabel = ttk.Label(self.frame_content_dimensions, text="Kompression [%]", justify="center")
        self.compressionPercent = ttk.Spinbox(self.frame_content_dimensions, justify="center", width=3, from_=0, to=99, increment=5)
        self.compressionLabel.grid(row=5, column=0)
        self.compressionPercent.grid(row=5, column=1)
        self.compressionPercent.insert(0, "50")

        self.colorDepthLabel = ttk.Label(self.frame_content_dimensions, text="Farbtiefe:", justify="center")
        self.colorDepthEntry = ttk.Entry(self.frame_content_dimensions, justify="center", width=4)
        self.colorDepthLabel.grid(row=5, column=4)
        self.colorDepthEntry.grid(row=5, column=5)
        self.colorDepthEntry.insert(0, "8")

        self.videoFPS = ttk.Entry(self.frame_content_video, width=4)
        self.videoFPS.insert(0, "24")

        self.videoLengthHours = ttk.Entry(self.frame_content_video, width=4)
        self.videoLengthHours.insert(0, "2")

        self.videoLengthMinutes = ttk.Entry(self.frame_content_video, width=4)
        self.videoLengthMinutes.insert(0, "56")

        self.videoLengthSeconds = ttk.Entry(self.frame_content_video, width=4)
        self.videoLengthSeconds.insert(0, "37")

        self.videoFPSLabel = ttk.Label(self.frame_content_video, text="Bilder/Sek", justify="center")
        self.videoLengthHoursLabel = ttk.Label(self.frame_content_video, text="Std", justify="center")
        self.videoLengthMinutesLabel = ttk.Label(self.frame_content_video, text="Min", justify="center")
        self.videoLengthSecondsLabel = ttk.Label(self.frame_content_video, text="Sek", justify="center")


        self.videoFPSLabel.grid(row=0, column=0, padx=5, pady=0)
        self.videoFPS.grid(row=1, column=0, padx=5, pady=0)

        self.videoLengthHoursLabel.grid(row=0, column=1, padx=5, pady=0)
        self.videoLengthHours.grid(row=1, column=1, padx=5, pady=0)

        self.videoLengthMinutesLabel.grid(row=0, column=2, padx=5, pady=0)
        self.videoLengthMinutes.grid(row=1, column=2, padx=5, pady=0)

        self.videoLengthSecondsLabel.grid(row=0, column=3, padx=5, pady=0)
        self.videoLengthSeconds.grid(row=1, column=3, padx=5, pady=0)

        unitList = ["Bit", "Byte", "KB", "MB", "GB", "TB", "KiB", "MiB", "GiB", "TiB"]

        self.unitsLabel = ttk.Label(self.frame_content_dimensions, text="Umrechnung in?", justify="center")
        self.unitsLabel.grid(row=6, column=0)
        self.units = ttk.Combobox(self.frame_content_dimensions, values=unitList, width=5, justify="center")
        self.units.insert(0, "MiB")
        self.units.configure(state="readonly")
        self.units.grid(row=6, column=1)

        # Set radiobutton default to PX, disable DPI entry, disable Video
        self.PXorDPI.set(1)
        disableDPI_enablePX()

        self.rechenwegbox = Text(self.frame_content, width=130, height=12)
        self.rechenwegbox.grid(row=4, column=0, columnspan=2)
        self.rechenwegbox.insert("1.0", "Detaillierter Rechenweg")

        # Start with Video Frame disabled
        disableVideoFrame()

        def calc():
            video = False
            unitDict = {"Bit": 1, "Byte": 1 / 8, "KB": 1 / 1000, "MB": 1 / (1000 ** 2), "GB": 1 / (1000 ** 3),
                        "TB": 1 / (1000 ** 4),
                        "KiB": 1 / 1024, "MiB": 1 / (1024 ** 2), "GiB": 1 / (1024 ** 3), "TiB": 1 / (1024 ** 4)}

            self.rechenwegbox.delete("1.0", "end")

            # Height/Width from either PX or DPI
            if self.PXorDPI.get() == 1:
                height = int(self.pxHeightEntry.get())
                width = int(self.pxWidthEntry.get())
            elif self.PXorDPI.get() == 2:
                dpi = int(self.dpiEntry.get())
                height = int(float(self.dpiHeightEntry.get()) / 2.54 * dpi)
                width = int(float(self.dpiWidthEntry.get()) / 2.54 * dpi)
            colordepth = int(self.colorDepthEntry.get())
            compression = (100 - int(self.compressionPercent.get())) / 100

            # These calculation always need to happen to proceed
            imageSizeBit = height * width * colordepth * compression

            unit = self.units.get()
            if unit not in ("Bit", "Byte"):  # divide by 8 here instead of adding it to each case in the Dictionary
                unitConversion = unitDict[unit] / 8
            else:
                unitConversion = unitDict[unit]

            imageSize = imageSizeBit * unitConversion

            # If it is a video, we continue:
            if self.boolvar.get():
                video = True
                h = int(self.videoLengthHours.get())
                m = int(self.videoLengthMinutes.get())
                s = int(self.videoLengthSeconds.get())
                fps = int(self.videoFPS.get())
                videoDuration = h * 3600 + m * 60 + s
                videoSize = imageSizeBit * fps * videoDuration * unitConversion
                self.rechenwegbox.insert("end", f"Die Dateigröße des Videos beträgt: {videoSize:.2f} {unit}.\n")
            else:
                self.rechenwegbox.insert("end", f"Die Dateigröße des Bildes beträgt: {imageSize:.2f} {unit}.\n")

            self.rechenwegbox.insert("end", "\nDie Berechnung der Bildgröße folgt dieser Formel: \n\n"
                                            "[Höhe in Pixel] * [Breite in Pixel] * [Farbtiefe in Bit] * [Kompression in %] = [Bildgröße in Bit]\n")
            if self.PXorDPI.get() == 2:
                self.rechenwegbox.insert("end",
                                         "In diesem Fall haben wir die Pixelwerte noch nicht, können es aber recht einfach umrechnen: \n"
                                         "Höhe in Pixel = Höhe in cm * DPI / 2,54  bzw. Breite in Pixel = Breite in cm * DPI / 2,54\n")
            # self.rechenwegbox.insert("end", "So kommt man dann auf das Teilergebnis bevor Einheitenumwandlung: ")
            self.rechenwegbox.insert("end",
                                     f"     {height}       *       {width}        *           {colordepth}        *        {compression}         =   {imageSizeBit} Bit\n\n")
            # just for a fun: a needlessly convoluted method of making the conversion more explicit by reusing the unitDict-Dictionary:
            conversionString = "/8 (Byte) "

            if unit == "Byte":
                self.rechenwegbox.insert("end",
                                         f"Umrechnung in {unit}: {imageSizeBit} Bit /8 = {imageSize:.2f} {unit}:\n\n")
            elif unit != "Bit":
                try:
                    count = list(unitDict.keys())[2:6].index(unit)# Check if unit is in the decimal portion
                    for i in range(count+1):
                        conversionString += f"/1000 ({list(unitDict.keys())[2:6][i]}) "
                except ValueError:  # if it is not, ignore the error and check for it in the binary portion
                    count = list(unitDict.keys())[6:].index(unit)
                    for i in range(count+1):
                        conversionString += f"/1024 ({list(unitDict.keys())[6:][i]}) "

                self.rechenwegbox.insert("end", f"Umrechnung in {unit}: {imageSizeBit} Bit {conversionString}= {imageSize:.2f} {unit}:\n\n")

            if video:
                self.rechenwegbox.insert("end",
                                         f"Videos sind eine Abfolge von Bildern pro x Sekunden, darüber wird dann die Videogröße berechnet:\n")
                self.rechenwegbox.insert("end",
                                         f"{imageSize:.2f} {unit} * {fps} Bilder pro Sekunde * {videoDuration} Sekunden = {videoSize:.2f} {unit}")

        ttk.Button(self.frame_content, text="Berechnen", command=lambda: calc()).grid(row=5, column=0, columnspan=2)

class TSC: #Datei-Transfer

    def __init__(self, frame, logo):

        self.logo = logo

        # Frame3 -> Header
        self.frame_header = ttk.Frame(frame)
        self.frame_header.pack()

        # Frame3 -> Logo & Text
        #self.logo = PhotoImage(file="testlogo.png")
        ttk.Label(self.frame_header, image=self.logo).grid(row=0, column=0, rowspan=2, stick="w")
        ttk.Label(self.frame_header, text="Netzadressenrechner").grid(row=0, column=1)  # style = "Header.TLabel"
        ttk.Label(self.frame_header, wraplength=400,
                  text="\nBerechnung der Netz-ID, Broadcast-IP, erster und letzter nutzbarer IP und Anzahl der nutzbaren Hosts.\n").grid(
            row=1, column=1)

        # Frame3-Body
        self.frame_content = ttk.Frame(frame)
        self.frame_content.pack()

class Quiz():  # Quiz

    def __init__(self, frame, logo):

        self.logo = logo

        # Frame4 -> Header
        self.frame = frame
        self.frame_header = ttk.Frame(frame)
        self.frame_header.pack()

        # Frame4 -> Logo & Text
        ttk.Label(self.frame_header, image=logo).grid(row=0, column=0, rowspan=2)
        ttk.Label(self.frame_header, text="Quiz").grid(row=0, column=1)  # style = "Header.TLabel"
        ttk.Label(self.frame_header, wraplength=600,
                  text="\n__Quiz__ NYI.\n").grid(
            row=1, column=1)

        # Frame4-Body
        self.frame_content = ttk.Frame(frame)
        self.frame_content.pack()

"""
Unused stuff for now

        # Style stuff, leave for later
        self.bg = "#7393B3"
        self.font = ("Verdana", 12)
        self.font_header = ("Verdana", 18, "bold")
        
        master.configure(background=self.bg)
        
        self.style=ttk.Style()
        
        self.style.configure("TFrame", background = self.bg)
        self.style.configure("TButton", background=self.bg)
        self.style.configure("TLabel", background=self.bg, font=self.font,)
        self.style.configure("Header.TLabel", background=self.bg, font=self.font_header)

Clear button
        def clear():
            self.spin_CIDR.delete(0, "end")
            self.entry_sub.delete(0, "end")
            self.entry_Netzadresse.delete(0, "end")
            self.ergebnisbox.delete("1.0", "end")
            self.rechenwegbox.delete("1.0", "end")

Enable/Disable boxes to prevent writing
        # rechenwegbox.config(state="normal")
        # rechenwegbox.config(state="disabled")
        # rechenwegbox.delete("1.0", "end")
"""

def main():

    # Create the main window
    root = Tk()

    # Turns out we have to create the images here or they won't show up in the Class for all but the first tab
    logo1 = PhotoImage(file="Logo_Net.png")
    logo2 = PhotoImage(file="Logo_Transfer.png")
    logo3 = PhotoImage(file="Logo_Image.png")
    logo4 = PhotoImage(file="Logo_Quiz.png")
    itt = ITT(root, logo1, logo2, logo3, logo4)

    # Start the GUI
    root.mainloop()

# Making sure that this only runs if it is the main file
if __name__ == "__main__":
    main()

