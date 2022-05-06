#########################################
# Magic Mirror
# 5/5/22
# Calvin Grant, Umang Gurung, Darmir Rios
#
#########################################
# importing libraries
from tkinter import *
from tkinter import ttk
from time import sleep, time
import requests
from time import sleep
import RPi.GPIO as GPIO
from time import strftime

# initializing variables
DEBUG = False
hour = None
SETTLE_TIME = 2		# seconds to let the sensor settle
CALIBRATIONS = 5	# number of calibration measurements to take
CALIBRATION_DELAY = 1	# seconds to delay in between calibration measurements
TRIGGER_TIME = 0.00001	# seconds needed to trigger the sensor (to get a measurement)
SPEED_OF_SOUND = 343	# speed of sound in m/s
# and the variable is set to our desired API
api_address = 'https://api.openweathermap.org/data/2.5/weather?appid=6d4e77cb2731a3554b3755e4245ec0e9&q='



# Class of a Tk Frame 
class GUI(Frame):
    # initializing class attributes
    def __init__(self, parent):
        Frame.__init__(self, parent, bg="black")
        parent.attributes("-fullscreen", True) # so the GUI will cover the whole Pi screen
        self.setup()
        self.pack(fill=BOTH, expand=1)
        self._hidden = True
        self._walked_away = False
        self._12H()   # the code beings by showing a 12 hour clock even before a button has been pressed
        self.after(100, self.process)
    
    # displaying the weather (in test form)
    def myClick(self):
        # calling an instance of the function 'function' after getting and input from myInput
        hello= "weather:  " +   self.function(self._myInput.get())
        # configuring our label to the standard of this mirror
        # passing in the variable hello as input 
        self._weatherText.config(text=hello, font = ('times new roman', 25), background = 'black', foreground = 'green')
        self._weatherText.pack()
        
    # displaying the 12 hour time of the clock     
    def _12H(self):
        # calling a global variable
        global hour
        # calling an imported library and assigning it to a variable 
        string = strftime('%I:%M:%S %p %a')
        # configuring the clock that will be presented 
        self._myClock.config(text = string)
        # allowing for the ability to change between 12 hour and 24 hour clock settings
        if (hour):
            self._myClock.after_cancel(hour)
        hour = self._myClock.after(1000, self._12H)
    
    # displaying the 24 hour clock 
    def _24H(self):
        # calling a global variable 
        global hour
        # calling an imported library and assigning it to a variable 
        string = strftime('%H:%M:%S %p %a')
        # configuring the clock that will be presented 
        self._myClock.config(text = string)
        # allowing for the ability to change between 12 hour and 24 hour clock settings
        if (hour):
            self._myClock.after_cancel(hour)
        hour = self._myClock.after(1000, self._24H)
    
    
    
    # this is the setup for the widgets and the API
    # to be presented on the Tk frame
    def setup(self):
        # using pack_forget() to allow for the screen to apear blank 
        self._cityLabel= Label(self, text = "CITY", font = ('times new roman', 25, 'bold'), background = 'black', foreground = 'green')
        self._cityLabel.pack_forget()
        
        self._weatherBu= Button(self, text = "Show weather",font = ('times new roman', 25, 'bold'), background = 'black', foreground = 'green' ,command = self.myClick)
        self._weatherBu.pack_forget()
      
        
        
        self._img= PhotoImage(file="plain.gif")
        self._imageLabel=Label(self, image=self._img)
        self._imageLabel.image= self._img
        self._imageLabel.pack_forget()
        
        
        self._myInput = Entry(self)
        # initializing the entry as Tampa
        self._myInput.insert(0, "Tampa")
        self._myInput.config(font = ('times new roman', 25), background = 'black', foreground = 'green')
        self._myInput.pack_forget()
        
        
        self._myClock = Label(self, font = ('times new roman', 50, 'bold'), background = 'black', foreground = 'green')
        self._myClock.pack_forget()
        
        self._24Button = Button(self, text = "24 Hours",font = ('times new roman', 25), background = 'black', foreground = 'green' ,command = self._24H)
        self._24Button.pack_forget()
        
        self._12Button = Button(self, text = "12 Hours",font = ('times new roman', 25), background = 'black', foreground = 'green' ,command = self._12H)
        self._12Button.pack_forget()
        
    
        self._closeButton = Button(self, text = "Close", font = ('times new roman', 10), background = 'black', foreground = 'green',command = exit)
        self._closeButton.pack_forget()
        
        self._weatherText = Label(self, text="")
        self._weatherText.pack_forget()
    
    # the function to process the API
    # and present the correct data as well as image onto the frame 
    def function(self, city):    
        url = api_address + city

        json_data = requests.get(url).json()

        formatted_data = json_data['weather'][0]['main']
        # Allowing for different pictures to be passed in for different weather readings
        if (formatted_data == "Clouds"):
            self._img= PhotoImage(file="clouds.gif")
            self._imageLabel.config(image=self._img)
            self._imageLabel.image= self._img
            
            return formatted_data
        elif (formatted_data == "Haze"):
            self._img= PhotoImage(file="haze.gif")
            self._imageLabel.config(image=self._img)
            self._imageLabel.image= self._img
            
            return formatted_data
        elif (formatted_data == "Clear"):
            self._img= PhotoImage(file="clear.gif")
            self._imageLabel.config(image=self._img)
            self._imageLabel.image= self._img
            
            return formatted_data
        elif (formatted_data == "Rain"):
            self._img= PhotoImage(file="rain.gif")
            self._imageLabel.config(image=self._img)
            self._imageLabel.image= self._img
            
            return formatted_data
        else:
            self._img= PhotoImage(file="rain.gif")
            self._imageLabel.config(image=self._img)
            self._imageLabel.image= self._img
            
            return formatted_data
    # Allowing for widgets to be presented and taken off of a Tkinter Frame
    # using Ultrasonic sensor and the ultrasonic sort 
    def process(self):
        distance = getDistance() * correction_factor
        sleep(0.1)
        # using .pack() to present the widgets and API on the frame 
        if (distance <= 5.0):
            if (self._hidden):
                self.config(bg="black")
                self._cityLabel.pack(side=TOP)
                self._myInput.pack(side=TOP)
                self._weatherBu.pack(side=TOP)
                self._myClock.pack(side=BOTTOM, expand=True)
                self._24Button.pack(side=TOP, anchor=W)
                self._12Button.pack(side=LEFT, anchor=W)                
                self._imageLabel.pack(side=RIGHT, anchor=E)
                self._weatherText.pack(side=TOP)
                self._closeButton.pack(side=TOP)
                self._hidden = not self._hidden
                self._weatherBu.invoke()
                sleep(0.1)
        else:
            # if the screen is not hidden and the person is not close to the sensor
            # after 4 seconds hide the widgets 
            if (not self._hidden):
                if (not self._walked_away):
                    self._walked_away = True
                    self.after(4000, self.process)
                    return
                # using .pack_forget() make the widgets disapear and only present the current time
                # either 12 or 24 hour
                else:
                    self.config(bg="black")
                    self._weatherBu.pack_forget()
                    self._cityLabel.pack_forget()
                    self._imageLabel.pack_forget()
                    self._myInput.pack_forget()
                    self._24Button.pack_forget()
                    self._12Button.pack_forget()
                    self._closeButton.pack_forget()
                    self._weatherText.pack_forget()
                    self._walked_away = not self._walked_away
                    self._hidden = not self._hidden
        self.after(100, self.process)
        
# set the RPi to the Broadcom pin layout
GPIO.setmode(GPIO.BCM)

# GPIO pins
TRIG = 18			# the sensor's TRIG pin
ECHO = 27			# the sensor's ECHO pin

GPIO.setup(TRIG, GPIO.OUT)	# TRIG is an output
GPIO.setup(ECHO, GPIO.IN)	# ECHO is an input

# calibrates the sensor
# technically, it returns a correction factor to use in our calculations
def calibrate():
    print("Calibrating...")
    # prompt the user for an object's known distance
    print("-Place the sensor a measured distance away from an object.")
    known_distance = float(input("-What is the measured distance (cm)? "))

    # measure the distance to the object with the sensor
    # do this several times and get an average
    print("-Getting calibration measurements...")
    distance_avg = 0
    for i in range(CALIBRATIONS):
        distance = getDistance()
        if (DEBUG):
            print("--Got {}cm".format(distance))
        # keep a running sum
        distance_avg += distance
        # delay a short time before using the sensor again
        sleep(CALIBRATION_DELAY)
    # calculate the average of the distances
    distance_avg /= CALIBRATIONS
    if (DEBUG):
        print("--Average is {}cm".format(distance_avg))

    # calculate the correction factor
    correction_factor = known_distance / distance_avg
    if (DEBUG):
        print("--Correction factor is {}".format(correction_factor))

    print("Done.")
    sleep(1)
    print()

    return correction_factor

# uses the sensor to calculate the distance to an object
def getDistance():
    # trigger the sensor by setting it high for a short time and then setting it low
    GPIO.output(TRIG, GPIO.HIGH)
    sleep(TRIGGER_TIME)
    GPIO.output(TRIG, GPIO.LOW)

    # wait for the ECHO pin to read high
    # once the ECHO pin is high, the start time is set
    # once the ECHO pin is low again, the end time is set
    while (GPIO.input(ECHO) == GPIO.LOW):
        start = time()
    while (GPIO.input(ECHO) == GPIO.HIGH):
        end = time()

    # calculate the duration that the ECHO pin was high
    # this is how long the pulse took to get from the sensor to the object -- and back again
    duration = end - start
    # calculate the total distance that the pulse traveled by factoring in the speed of sound (m/s)
    distance = duration * SPEED_OF_SOUND
    # the distance from the sensor to the object is half of the total distance traveled
    distance /= 2
    # convert from meters to centimeters
    distance *= 100

    return distance

GPIO.output(TRIG, GPIO.LOW)
sleep(SETTLE_TIME)
correction_factor = calibrate()

# presenting a window in Tk 
window = Tk()
gui = GUI(window)
gui.mainloop()

print("Done.")
GPIO.cleanup()




