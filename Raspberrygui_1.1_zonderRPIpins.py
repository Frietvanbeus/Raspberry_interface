from tkinter import *
from tkinter import ttk
import tkinter as tk
import os
import time
import decimal
import myconfig
#from gpiozero import LED
#import RPi.GPIO as GPIO
from time import sleep


#versie waar alle GPIO pins met een hashtag (#) vooraf gaat is bedoeld om te testen op de pc.
# Voor het testen op de Raspberry PI goed checken of al deze hashtags weg zijn gehaald!
# GPIO 26 is opvoerband(vullen) GPIO 19 is waterventiel (schrappen) GPIO 13 is luchtventiel(wachten).





class RaspberryGui(object):
    def __init__(self):
        self.root = Tk()
        self.root.title("Schrappen interface")
        self.mainframe = ttk.Frame(self.root, padding="100 30 100 100")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        InfoSchrapperLabel = ttk.Label(self.mainframe, text="Schrapper automaat aanzetten: ").grid(column=0, row=0, sticky=W)
        LegeLabel = ttk.Label(self.mainframe, text="               ").grid(column=0, row=1, sticky=W)
        Legelabel_2 = ttk.Label(self.mainframe, text="                    ").grid(column=0, row=6, sticky=W)
        #Voor handmatige bediening de status van deze apparaten definieren:
        self.Opvoerbandstatus = False
        self.Waterklepstatus = False
        self.Luchtklepstatus = False


        global running
        running = True

        #Standaard tekst labels
        VulTijdLabel = ttk.Label(self.mainframe, text="Vultijd: ").grid(column=0, row=8, sticky=W)
        SchrapTijdLabel = ttk.Label(self.mainframe, text="Schraptijd: ").grid(column=0, row=9, sticky=W)
        SchrapTijdLabel_2 = ttk.Label(self.mainframe, text="Schraptijd middel: ").grid(column=0, row=10, sticky=W)
        SchrapTijdLabel_3 = ttk.Label(self.mainframe, text="Schraptijd lang: ").grid(column=0, row=11, sticky=W)
        WachtTijdLabel = ttk.Label(self.mainframe, text="Wachttijd: ").grid(column=0, row=12, sticky=W)


        #Tijdlabels, hierbij wordt de tijd van de sliders weergegeven. De slider functie past de label aan
        self.VultijdSecondeLabel = ttk.Label(self.mainframe, text=str(myconfig.vullen_standaard_tijd) + " sec.", width=10)
        self.VultijdSecondeLabel.grid(column=2, row=8, sticky=W)
        self.SchraptijdSecondeLabel = ttk.Label(self.mainframe, text=str(myconfig.kort_schrappen_standaard_tijd) + " sec.", width=10)
        self.SchraptijdSecondeLabel.grid(column=2, row=9, sticky=W)
        self.WachttijdSecondeLabel = ttk.Label(self.mainframe, text=str(myconfig.wachttijd_standaard_tijd) + " sec.", width=10)
        self.WachttijdSecondeLabel.grid(column=2, row=12, sticky=W)
        self.SchraptijdSecondeLabel_2 = ttk.Label(self.mainframe, text=str(myconfig.middel_schrappen_standaard_tijd) + " sec.", width=10)
        self.SchraptijdSecondeLabel_2.grid(column=2, row=10, sticky=W)
        self.SchraptijdSecondeLabel_3 = ttk.Label(self.mainframe, text=str(myconfig.lang_schrappen_standaard_tijd) + " sec.", width=10)
        self.SchraptijdSecondeLabel_3.grid(column=2, row=11, sticky=W)

        #tijdschalen om met een slider de tijden van het betreffende proces te bepalen
        VullenTijdSchaal = ttk.Scale(self.mainframe, orient='horizontal', length=300, from_=0, to=10, variable=myconfig.vullen_standaard_tijd, command=self.print_tijd_vullen)
        VullenTijdSchaal.grid(column=1, row=8, sticky=W, pady=10)
        SchrappenTijdSchaal = ttk.Scale(self.mainframe, orient='horizontal', length=300, from_=0, to=10, variable=myconfig.kort_schrappen_standaard_tijd, command=self.print_tijd_schrappen)
        SchrappenTijdSchaal.grid(column=1, row=9, sticky=W, pady=10)
        SchrappenTijdSchaal_2 = ttk.Scale(self.mainframe, orient='horizontal', length=300, from_=0, to=40, variable=myconfig.middel_schrappen_standaard_tijd, command=self.print_tijd_schrappen_2)
        SchrappenTijdSchaal_2.grid(column=1, row=10, sticky=W, pady=10)
        SchrappenTijdSchaal_3 = ttk.Scale(self.mainframe, orient='horizontal', length=300, from_=0, to=120, variable=myconfig.lang_schrappen_standaard_tijd, command=self.print_tijd_schrappen_3)
        SchrappenTijdSchaal_3.grid(column=1, row=11, sticky=W, pady=10)
        WachtTijdSchaal = ttk.Scale(self.mainframe, orient='horizontal', length=300, from_=0, to=600, variable=myconfig.wachttijd_standaard_tijd, command=self.print_tijd_wachten)
        WachtTijdSchaal.grid(column=1, row=12, sticky=W, pady=12)


        self.StartSchrappenButton = ttk.Button(self.mainframe, text="Start schrappen ", command=self.starten)
        self.StartSchrappenButton.grid(column=0, row=5, sticky=W)
        StopSchrappenButton = ttk.Button(self.mainframe, text="Stop schrappen + open HANDBEDIEND", command=self.StopSchrappen).grid(column=0, row=7, sticky=W)

        self.OpvoerbandButton = Button(self.mainframe, text="(HAND) Opvoerband ", command=self.Opvoerband, width=30, bg="green")
        self.OpvoerbandButton.grid(column=3, row=1, sticky=W, pady=5, ipadx=30)
        self.WaterAanButton = Button(self.mainframe, text="(HAND) Water aan", command=self.WaterAan, bg="green", width=30)
        self.WaterAanButton.grid(column=3, row=2, sticky=W, pady=5, ipadx=30)
        self.KlepOpenButton = Button(self.mainframe, text="(HAND) Klep open ", command=self.KlepOpen, bg="green", width=30)
        self.KlepOpenButton.grid(column=3, row=3, sticky=W, pady=5, ipadx=30)
        bepaal_schrap_standaard_button_1 = ttk.Button(self.mainframe, text="Kort schrappen ", command=self.bepaal_schrap_standaard_1).grid(column=3, row=9, sticky=W)
        bepaal_schrap_standaard_button_2 = ttk.Button(self.mainframe, text="Middel schrappen ", command=self.bepaal_schrap_standaard_2).grid(column=3, row=10, sticky=W)
        bepaal_schrap_standaard_button_3 = ttk.Button(self.mainframe, text="Lang schrappen ", command=self.bepaal_schrap_standaard_3).grid(column=3, row=11, sticky=W)


        #Met een pijl wordt aangeduid of er voor kort, middel of lang schrappen gekozen is.
        self.wijzer_label = ttk.Label(self.mainframe, text="<-----------")
        self.wijzer_label.grid(column=4, row=(8 + myconfig.schrap_standaard), sticky=W)

        #Statuslabel om aan te geven waar in het proces de loop zich bevindt.
        self.Status_text = Text(self.mainframe, height=1, width = 40, bg = "red")
        self.Status_text.insert(INSERT, " ---  STATUS BEGINSTAND ---")
        self.Status_text.grid(column=1, row=2, sticky=W)

        #RPI instellingen definiëren:

        #GPIO.setwarnings(False)
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(26, GPIO.OUT)
        #GPIO.setup(19, GPIO.OUT)
        #GPIO.setup(13, GPIO.OUT)
        #GPIO.output(26, GPIO.HIGH)
        #GPIO.output(19, GPIO.HIGH)
        #GPIO.output(13, GPIO.HIGH)



    def run(self):
        self.root.mainloop()


    def starten(self):
        #Bij het starten staan alle functies onbediend, zodat handmatig ingrijpen ook eventueel wordt gereset.
        #GPIO.output(26, GPIO.HIGH)
        #GPIO.output(19, GPIO.HIGH)
        #GPIO.output(13, GPIO.HIGH)
        self.Opvoerbandstatus = False
        self.Waterklepstatus = False
        self.Luchtklepstatus = False
        self.OpvoerbandButton.grid_forget()
        self.WaterAanButton.grid_forget()
        self.KlepOpenButton.grid_forget()
        global running
        running = True
        self.Status_text = Text(self.mainframe, height=1, width=40, bg="Green")
        self.Status_text.insert(INSERT, " ---  STATUS OPSTART ---")
        self.Status_text.grid(column=1, row=2, sticky=W)

        self.root.after(2300, self.Vullen)

    def Vullen(self):
        self.StartSchrappenButton.grid_forget()
        try:
            global running
            #running = True
            if running:
                        self.Status_text = Text(self.mainframe, height=1, width=40, bg="Green")
                        self.Status_text.insert(INSERT, " ---  STATUS VULLEND ---")
                        self.Status_text.grid(column=1, row=2, sticky=W)
                        #GPIO.output(26, GPIO.LOW)
                        #GPIO.output(19, GPIO.LOW)
                        self.root.after((myconfig.vullen_standaard_tijd*1000), self.CheckSchrapStatus)

        except ValueError:
            print("Error met het vullen")
#

##
    def Schrappen(self):
        global running

        #running = True
        #GPIO.output(26, GPIO.HIGH)
        if running:
            try:
                self.Status_text = Text(self.mainframe, height=1, width=40, bg="Green")
                self.Status_text.insert(INSERT, " ---  STATUS DRAAIEND ---")
                self.Status_text.grid(column=1, row=2, sticky=W)

                if myconfig.schrap_standaard == 1:
                    self.root.after((myconfig.kort_schrappen_standaard_tijd*1000), self.Wachttijd)

                if myconfig.schrap_standaard == 2:
                    self.root.after((myconfig.middel_schrappen_standaard_tijd * 1000), self.Wachttijd)

                if myconfig.schrap_standaard == 3:
                    self.root.after((myconfig.lang_schrappen_standaard_tijd * 1000), self.Wachttijd)


            except ValueError:
                print("Error bij het Schrappen")
#

    #Loop gaat wachttijd in om opnieuw op te kunnen starten
    def Wachttijd(self):
        #GPIO.output(19, GPIO.HIGH)
        try:
            global running
            if running:
                self.Status_text = Text(self.mainframe, height= 1, width=40, bg="Red")
                self.Status_text.insert(INSERT, " ---  STATUS WACHTTIJD  ---")
                self.Status_text.grid(column=1, row=2, sticky=W)
                #GPIO.output(13, GPIO.LOW)
                self.root.after((myconfig.wachttijd_standaard_tijd*1000), self.CheckVulStatus)
            else:
                self.StopSchrappen()

        except ValueError:
            print("Iets ging fout bij de wachttijd")





    def CheckSchrapStatus(self):
        global running
        if running:
            self.Schrappen()
        else:
            self.StopSchrappen()



    def CheckVulStatus(self):
        #GPIO.output(13, GPIO.HIGH)
        global running
        if running:
            self.Vullen()
        else:
            self.StopSchrappen()


    def StopSchrappen(self):
        #GPIO.output(26, GPIO.HIGH)
        #GPIO.output(19, GPIO.HIGH)
        #GPIO.output(13, GPIO.HIGH)
        global running
        running = False
        self.Status_text = Text(self.mainframe, height=1, width=40, bg="red")
        self.Status_text.insert(INSERT, " ---  STATUS GESTOPT   ---")
        self.Status_text.grid(column=1, row=2, sticky=W)
        self.StartSchrappenButton.grid(column=0, row=5, sticky=W)
        self.root.destroy()






    #volgende 3 functies om handmatig bij het indrukken van de buttons de functies te bedienen:
    def Opvoerband(self):
        # GPIO.output(26, GPIO.HIGH)
        # GPIO.output(19, GPIO.HIGH)
        # GPIO.output(13, GPIO.HIGH)
        global running
        running = False
        self.Status_text = Text(self.mainframe, height=1, width=40, bg="red")
        self.Status_text.insert(INSERT, " ---  STATUS AUTOMAAT GESTOPT   ---")
        self.Status_text.grid(column=1, row=2, sticky=W)
        if self.Opvoerbandstatus == False:
            #GPIO.output(26, GPIO.LOW)
            self.OpvoerbandButton = Button(self.mainframe, text="(HAND) Opvoerband ", command=self.Opvoerband, bg="Red", width=30).grid(column=3, row=1, sticky=W, pady=5, ipadx=30)

            self.Opvoerbandstatus = True
        else:
            #GPIO.output(26, GPIO.HIGH)
            self.OpvoerbandButton = Button(self.mainframe, text="(HAND) Opvoerband ", command=self.Opvoerband, bg="Green", width=30).grid(column=3, row=1, sticky=W, pady=5, ipadx=30)
            self.Opvoerbandstatus = False

        print("Opvoerbandddd")


    def WaterAan(self):
        # GPIO.output(26, GPIO.HIGH)
        # GPIO.output(19, GPIO.HIGH)
        # GPIO.output(13, GPIO.HIGH)
        global running
        running = False
        self.Status_text = Text(self.mainframe, height=1, width=40, bg="red")
        self.Status_text.insert(INSERT, " ---  STATUS AUTOMAAT GESTOPT   ---")
        self.Status_text.grid(column=1, row=2, sticky=W)
        if self.Waterklepstatus == False:
            #GPIO.output(19, GPIO.LOW)
            self.WaterAanButton = Button(self.mainframe, text="(HAND) Water aan ", command=self.WaterAan, bg="Red", width=30).grid(column=3, row=2, sticky=W, pady=5, ipadx=30)

            self.Waterklepstatus = True
        else:
            #GPIO.output(19, GPIO.HIGH)
            self.WaterAanButton = Button(self.mainframe, text="(HAND) Water aan ", command=self.WaterAan, bg="Green", width=30).grid(column=3, row=2, sticky=W, pady=5, ipadx=30)
            self.Waterklepstatus = False

        print("WATERRR")



    def KlepOpen(self):
        # GPIO.output(26, GPIO.HIGH)
        # GPIO.output(19, GPIO.HIGH)
        # GPIO.output(13, GPIO.HIGH)
        global running
        running = False
        self.Status_text = Text(self.mainframe, height=1, width=40, bg="red")
        self.Status_text.insert(INSERT, " ---  STATUS AUTOMAAT GESTOPT   ---")
        self.Status_text.grid(column=1, row=2, sticky=W)
        if self.Luchtklepstatus == False:
            #GPIO.output(13, GPIO.LOW)
            self.KlepOpenButton = Button(self.mainframe, text="(HAND) Klep open ", command=self.KlepOpen, bg="Red", width=30).grid(column=3, row=3, sticky=W, pady=5, ipadx=30)
            self.Luchtklepstatus = True
        else:
            #GPIO.output(13, GPIO.HIGH)
            self.KlepOpenButton = Button(self.mainframe, text="(HAND) Klep open ", command=self.KlepOpen, bg="Green", width=30).grid(column=3, row=3, sticky=W, pady=5, ipadx=30)
            self.Luchtklepstatus = False
        print("Luchtleppp")



    def print_tijd_vullen(self, variabele_vullen):
        x = decimal.Decimal(variabele_vullen)
        variabele_vullen = int(round(x, 0))
        self.VultijdSecondeLabel.config(text=str(variabele_vullen) + " sec.")
        myconfig.vullen_standaard_tijd = variabele_vullen
        return myconfig.vullen_standaard_tijd



    def print_tijd_schrappen(self, variabele_schraptijd):
        x = decimal.Decimal(variabele_schraptijd)
        variabele_schraptijd = int(round(x, 0))
        self.SchraptijdSecondeLabel.config(text=str(variabele_schraptijd) + " sec.")
        myconfig.kort_schrappen_standaard_tijd = variabele_schraptijd
        return myconfig.kort_schrappen_standaard_tijd


    def print_tijd_schrappen_2(self, variabele_schraptijd_2):
        y = decimal.Decimal(variabele_schraptijd_2)
        variabele_schraptijd_2 = int(round(y, 0))
        self.SchraptijdSecondeLabel_2.config(text=str(variabele_schraptijd_2) + " sec.")
        myconfig.middel_schrappen_standaard_tijd = variabele_schraptijd_2
        return myconfig.middel_schrappen_standaard_tijd


    def print_tijd_schrappen_3(self, variabele_schraptijd_3):
        z = decimal.Decimal(variabele_schraptijd_3)
        variabele_schraptijd_3 = int(round(z, 0))
        self.SchraptijdSecondeLabel_3.config(text=str(variabele_schraptijd_3) + " sec.")
        myconfig.lang_schrappen_standaard_tijd = variabele_schraptijd_3
        return myconfig.lang_schrappen_standaard_tijd


    def bepaal_schrap_standaard_1(self):
        self.wijzer_label.grid(column=4, row=9, sticky=W)
        myconfig.schrap_standaard = 1


    def bepaal_schrap_standaard_2(self):
        self.wijzer_label.grid(column=4, row=10, sticky=W)
        myconfig.schrap_standaard = 2


    def bepaal_schrap_standaard_3(self):
        self.wijzer_label.grid(column=4, row=11, sticky=W)
        myconfig.schrap_standaard = 3



    def print_tijd_wachten(self, variabele_wachttijd):
        x = decimal.Decimal(variabele_wachttijd)
        variabele_wachttijd = int(round(x, 0))
        self.WachttijdSecondeLabel.config(text=str(variabele_wachttijd) + " sec.")
        myconfig.wachttijd_standaard_tijd = variabele_wachttijd
        return myconfig.wachttijd_standaard_tijd


def HerhaalInterface():
    p = RaspberryGui()
    p.run()

herhaal = True
while herhaal:
   HerhaalInterface()

