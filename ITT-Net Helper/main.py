from tkinter import *
from tkinter import ttk
from idlelib.tooltip import Hovertip
import NetzAdCalc as nac

class ITT:

    def __init__(self, master):
        # Root
        master.title("ITT-NET Helper")
        #master.resizable(False, False)
        #master.geometry("600x400")
        
        # Style stuff, leave for later
        """self.bg = "#7393B3"
        self.font = ("Verdana", 12)
        self.font_header = ("Verdana", 18, "bold")
        
        master.configure(background=self.bg)
        
        self.style=ttk.Style()
        
        self.style.configure("TFrame", background = self.bg)
        self.style.configure("TButton", background=self.bg)
        self.style.configure("TLabel", background=self.bg, font=self.font,)
        self.style.configure("Header.TLabel", background=self.bg, font=self.font_header)"""

        # Root -> Notebook
        self.notebook = ttk.Notebook(master)
        self.notebook.pack()

        frame1 = ttk.Frame(self.notebook)
        frame2 = ttk.Frame(self.notebook)
        frame3 = ttk.Frame(self.notebook)

        self.notebook.add(frame1, text="Netzadresse")
        self.notebook.add(frame2, text="Bildgröße")
        self.notebook.add(frame3, text="Datei-Transfer")

        # Root -> Header
        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()

        # Header -> Logo & Text
        self.logo = PhotoImage(file = "testlogo.png")
        ttk.Label(self.frame_header, image = self.logo).grid(row = 0, column = 0, rowspan = 2, stick="w") # no variables because they will not change, change for easter egg
        ttk.Label(self.frame_header, text="Netzadressenrechner").grid(row = 0, column = 1) # style = "Header.TLabel"
        ttk.Label(self.frame_header, wraplength= 400, text="\nBerechnung der Netz-ID, Broadcast-IP, erster und letzter nutzbarer IP und Anzahl der nutzbaren Hosts.\n").grid(row = 1, column = 1)

        # Body
        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()

        # Body -> Sub/CIDR + Entry Subframe
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
        self.subRadio = ttk.Radiobutton(self.frame_content_sub, text="Subnetz", variable=self.v, value=1, command=lambda: disableCIDR_enableSub())
        self.subRadio.grid(row=0, column=0, sticky="w")
        self.CIDRRadio = ttk.Radiobutton(self.frame_content_sub, text="CIDR", variable=self.v, value=2, command=lambda: disableSub_enableCIDR())
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
        self.entry_Netzadresse = ttk.Entry(self.frame_content, width = 15)
        self.entry_Netzadresse.grid(row=2, column=0)
        self.entry_Netzadresse.insert(0, "192.168.110.0")
        Hovertip(self.entry_Netzadresse, 'Format: xxx.xxx.xxx.xxx')

        self.ergebnisbox = self.text_ergebnis = Text(self.frame_content, width = 55, height = 10)
        self.ergebnisbox.grid(row=4, column=0)
        self.ergebnisbox.insert("1.0", "Ergebnisbox")
        self.rechenwegbox = Text(self.frame_content, width=70, height=10)
        self.rechenwegbox.grid(row=4, column=1)
        self.rechenwegbox.insert("1.0", "Detaillierter Rechenweg")

        #rechenwegbox.config(state="normal")
        #rechenwegbox.config(state="disabled")
        #rechenwegbox.delete("1.0", "end")

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
                inputSub = self.entry_sub.get() #for text widgets it'd be .get("1.0", "end")
                CIDR = nac.sub_to_CIDR(nac.Sub_split(inputSub))
            # From CIDR
            elif self.v.get() == 2:
                inputCIDR = int(self.spin_CIDR.get())
                inputSub = nac.CIDR_to_sub(inputCIDR)
                CIDR = int(self.spin_CIDR.get())
            
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

            # Outputs Ergebnisbox
            self.ergebnisbox.insert("end", f"IP-Adresse: {inputNetzadresse}\n")
            self.ergebnisbox.insert("end", f"Subnetz:    {inputSub}, CIDR: {CIDR}\n")
            self.ergebnisbox.insert("end", f"\n")
            self.ergebnisbox.insert("end", f"Netz-ID:    {network_ID[0]}.{network_ID[1]}.{network_ID[2]}.{network_ID[3]}"
                                    f" /{CIDR}, {network_type}\n")
            self.ergebnisbox.insert("end", f"\n")
            self.ergebnisbox.insert("end", f"Broadcast:  {broadcast_IP}\n")
            self.ergebnisbox.insert("end", f"Erste IP:   {first_IP}\n")
            self.ergebnisbox.insert("end", f"Letzte IP:  {last_IP}\n")
            self.ergebnisbox.insert("end", f"\n")
            self.ergebnisbox.insert("end", f"Anzahl nutzbarer Hosts: {2**(32-CIDR)-2}\n")
            
            # Spacing for visualization of the broadcast calculations in Rechenwegbox
                       
            if octet == 4:
                pad = 25*" "
            elif octet == 3:
                pad = 17*" "
            elif octet == 2:
                pad = 10*" "
            elif octet == 1:
                pad = 1*" "
            pad2 = 25*" "
            bc_spaced = list(broadcast_IP.split("."))
            
            # Outputs Rechenwegbox
            self.rechenwegbox.insert("end", f"IP-Binär:        {binary_IP}\n")
            self.rechenwegbox.insert("end", f"Subnetz-Binär: + {binary_sub}\n")
            self.rechenwegbox.insert("end", f"Netz-ID(bin):  = {addition}\n")
            self.rechenwegbox.insert("end", f"\n")
            self.rechenwegbox.insert("end", f"Netz-ID(dez):            {network_ID[0]}  .  {network_ID[1]}  .  {network_ID[2]}  .  {network_ID[3]}\n")
            self.rechenwegbox.insert("end", f"Blockgröße auf {octet}.Oktett{pad}+{block_size}\n")
            self.rechenwegbox.insert("end", f"1 vom 4.Oktett abziehen{pad2}-1 \n")
            self.rechenwegbox.insert("end", f"Broadcast:             = {bc_spaced[0]}  .  {bc_spaced[1]}  .  {bc_spaced[2]}  .  {bc_spaced[3]}\n")
            self.rechenwegbox.insert("end", f"\n")
            self.rechenwegbox.insert("end", f"Blockgröße: {block_size}")
            if unmodified_block <= 256:
                self.rechenwegbox.insert("end", f"\n")
            elif unmodified_block > 256:
                self.rechenwegbox.insert("end", f" ({unmodified_block}/256")
                while unmodified_block > 256:
                    unmodified_block=unmodified_block//256
                    if unmodified_block < 256:
                        self.rechenwegbox.insert("end", f" = {unmodified_block})")
                    else:
                        self.rechenwegbox.insert("end", f" = {unmodified_block}/256")


        def clear():
            self.spin_CIDR.delete(0, "end")
            self.entry_sub.delete(0, "end")
            self.entry_Netzadresse.delete(0, "end")
            self.ergebnisbox.delete("1.0", "end")
            self.rechenwegbox.delete("1.0", "end")

        ttk.Button(self.frame_content, text ="Berechnen", command=lambda: calc()).grid(row=5, column=0, columnspan=2)

def main():

    root = Tk()
    itt = ITT(root)
    root.mainloop()

if __name__ == "__main__":
    main()

