#======================================================================
# Pico Punk Console
# A simple programmable 8 step tone sequencer, ported from the Arduino Punk Console by dano/beavisaudio.com
# http://beavisaudio.com/projects/arduinopunkconsole/
#======================================================================

import time
import board
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range
import pwmio

# assign pots to variables
AnalogInFrequency = AnalogIn(board.A0)
AnalogInDuration = AnalogIn(board.A1)
AnalogInTempo = AnalogIn(board.A2)

# assign buttons + LED to variables
DigitalInSwitch0 = DigitalInOut(board.GP7)
DigitalInSwitch1 = DigitalInOut(board.GP6)
DigitalInSwitch2 = DigitalInOut(board.GP5)
DigitalInSwitch3 = DigitalInOut(board.GP4)
DigitalInSwitch4 = DigitalInOut(board.GP3)
DigitalInSwitch5 = DigitalInOut(board.GP2)
DigitalInSwitch6 = DigitalInOut(board.GP1)
DigitalInSwitch7 = DigitalInOut(board.GP0) 
DigitalInStartStop = DigitalInOut(board.GP9)
DigitalOutLED = DigitalInOut(board.GP8)

# assign audio output to variable
sound = pwmio.PWMOut(board.GP14, frequency=440, duty_cycle=0, variable_frequency=True)

# set button pins to inputs and LED pin to output
DigitalInSwitch0.direction = Direction.INPUT
DigitalInSwitch1.direction = Direction.INPUT
DigitalInSwitch2.direction = Direction.INPUT
DigitalInSwitch3.direction = Direction.INPUT
DigitalInSwitch4.direction = Direction.INPUT
DigitalInSwitch5.direction = Direction.INPUT
DigitalInSwitch6.direction = Direction.INPUT
DigitalInSwitch7.direction = Direction.INPUT
DigitalInStartStop.direction = Direction.INPUT
DigitalOutLED.direction = Direction.OUTPUT

# set up the array for each step
steps = [100,120,140,160,180,200,220,240]
num = len(steps)

# initial values for other variables
duration = 50
mapD = 50
pitchval = 1
lastPushedStep = -1
tempo = 100
mapT = 100
mapF = 100

# check switch 0 > if pressed, save the current freq into step 0 > repeat for each button
def readSwitches():
    lastPushedStep = -1
    
    if DigitalInSwitch0.value:
      steps[0] = mapF
      lastPushedStep = 1
      print("switch 1")
  
    elif DigitalInSwitch1.value:
      steps[1] = mapF
      lastPushedStep = 2
      print("switch 2")

    elif DigitalInSwitch2.value:
      steps[2] = mapF
      lastPushedStep = 3
      print("switch 3")

    elif DigitalInSwitch3.value:
      steps[3] = mapF
      lastPushedStep = 4
      print("switch 4")
 
    elif DigitalInSwitch4.value:
      steps[4] = mapF
      lastPushedStep = 5
      print("switch 5")

    elif DigitalInSwitch5.value:
      steps[5] = mapF
      lastPushedStep = 6
      print("switch 6")

    elif DigitalInSwitch6.value:
      steps[6] = mapF
      lastPushedStep = 7
      print("switch 7")

    elif DigitalInSwitch7.value:
      steps[7] = mapF
      lastPushedStep = 8
      print("switch 8")


# main loop
while True:
  for i in range(num): # for each step in the sequence
    if DigitalInStartStop.value: # wait until Play button is pressed

      DigitalOutLED.value = True # turn LED on
 
      readSwitches() # check if any buttons are pressed

      # read values from pots 1 + 3 and remap from 0-65535 to 0-255
      mapF = int(AnalogInFrequency.value/257)
      mapT = int(AnalogInTempo.value/257)

      tempo = mapT * 1.9 # set tempo according to pot 3 value; adjust multiplier to suit the range you need

      sound.frequency = steps[i] # set frequency of the current step
      sound.duty_cycle = AnalogInDuration.value # set duty cycle according to pot 2 value

      
      DigitalOutLED.value = False # turn LED off 
      time.sleep(tempo/1000) # pause for a beat
   
    else:
        sound.duty_cycle = 0 # mute audio if button is not pressed
