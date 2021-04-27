import sys
import tfmplus as tfmP   # Import the `tfmplus` module v0.0.12
from tfmplus import *    # and command and paramter defintions
from datetime import datetime
import serial,time
import numpy as np
import matplotlib.pyplot as plt
#
############################
# Serial Functions
############################
#
serialPort = "/dev/ttyAMA0"  # Raspberry Pi normal serial port
serialRate = 115200          # TFMini-Plus default baud rate

# - - - Set and Test serial communication - - - -
print( "Serial port: ", end= '')
if( tfmP.begin( serialPort, serialRate)):
    print( "ready.")
else:
    print( "not ready")
    sys.exit()   #  quit the program if serial not ready

# - - Perform a system reset - - - - - - - -
print( "System reset: ", end= '')
if( tfmP.sendCommand( SYSTEM_RESET, 0)):
    print( "passed.")
else:
    tfmP.printReply()
# - - - - - - - - - - - - - - - - - - - - - - - -
time.sleep(0.5)  # allow 500ms for reset to complete

# - - - - - - - - - - - - - - - - - - - - - - - -

# - - Set the data frame-rate to 20Hz - - - - - - - -
print( "Data-Frame rate: ", end= '')
if( tfmP.sendCommand( SET_FRAME_RATE, FRAME_250)):
    print( str(FRAME_20) + 'Hz')
else:
    tfmP.printReply()
# - - - - - - - - - - - - - - - - - - - - - - - -
time.sleep(0.001)     # Wait half a second.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - -  the main program loop begins here  - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def read_tfluna_data():
    while True:
    #time.sleep(0.001)   # Loop delay 50ms to match the 20Hz data frame rate
        # Use the 'getData' function to get data from device
        if( tfmP.getData()):
            distance = tfmP.dist
            strength = tfmP.flux
            temperature = tfmP.temp
            
            return distance,strength,temperature
            #print( f" Dist: {tfmP.dist:{3}}cm ", end= '')   # display distance,
            #print( " | ", end= '')
            #print(datetime.utcnow().strftime('%H:%M:%S.%f'))
            #print( f"Flux: {tfmP.flux:{4}d} ",   end= '')   # display signal strength/quality,
            #print( " | ", end= '')
            #print( f"Temp: {tfmP.temp:{2}}°C",  )   # display temperature,
        else:                  # If the command fails...
          tfmP.printFrame()    # display the error and HEX data
#
    

##############################################
# Plotting functions
##############################################
#
def plotter():
    ################################################
    # ---- start real-time ranging and strength bar
    ################################################
    #
    plt.style.use('ggplot') # plot formatting
    fig,axs = plt.subplots(1,2,figsize=(12,8),
                        gridspec_kw={'width_ratios': [5,1]}) # create figure
    fig.canvas.set_window_title('TF-Luna Real-Time Ranging')
    fig.subplots_adjust(wspace=0.05)
    # ranging axis formatting
    axs[0].set_xlabel('Sample',fontsize=16)
    axs[0].set_ylabel('Distance',fontsize=16) # Distance label
    axs[0].set_xlim([0.0,plot_pts])
    axs[0].set_ylim([0.0,400]) # set ranging limits
    # signal strength axis formatting
    axs[1].set_xlim([-1.0,1.0]) # strength bar width
    axs[1].set_xticks([]) # remove x-ticks
    axs[1].set_ylim([1.0,2**16]) # set signal strength limits
    axs[1].yaxis.tick_right() # move strength ticks to right
    axs[1].yaxis.set_label_position('right') # label to right
    axs[1].set_ylabel('Signal Strength',fontsize=16,labelpad=6.0)
    axs[1].set_yscale('log') # log scale for better visual
    # draw and background specification
    fig.canvas.draw() # draw initial plot
    ax1_bgnd = fig.canvas.copy_from_bbox(axs[0].bbox) # get background
    ax2_bgnd = fig.canvas.copy_from_bbox(axs[1].bbox) # get background
    line1, = axs[0].plot(np.zeros((plot_pts,)),linewidth=1.0,
                color=plt.cm.Set1(1)) # dummy initial ranging data (zeros)
    bar1,  = axs[1].bar(0.0,1.0,width=1.0,color=plt.cm.Set1(2))
    fig.show() # show plot
    return fig,axs,ax1_bgnd,ax2_bgnd,line1,bar1

def plot_updater():
    ##########################################
    # ---- time series 
    fig.canvas.restore_region(ax1_bgnd) # restore background 1 (for speed)
    fig.canvas.restore_region(ax2_bgnd) # restore background 2
    line1.set_ydata(dist_array) # update channel data
    bar1.set_height(strength) # update signal strength
    if strength<100.0 or strength>30000.0:
        bar1.set_color(plt.cm.Set1(0)) # if invalid strength, make bar red
    else:
        bar1.set_color(plt.cm.Set1(2)) # green bar
    axs[0].draw_artist(line1) # draw line
    axs[1].draw_artist(bar1) # draw signal strength bar
    fig.canvas.blit(axs[0].bbox) # blitting (for speed)
    fig.canvas.blit(axs[1].bbox) # blitting
    fig.canvas.flush_events() # required for blitting
    return line1,bar1
#
############################
# Real-Time Plotter Loop
############################
#
plot_pts = 400 # points for sample rate test
fig,axs,ax1_bgnd,ax2_bgnd,line1,bar1 = plotter() # instantiate figure and plot
dist_array = [] # for updating values
print('Starting Ranging...')
while True:
    distance,strength,temperature = read_tfluna_data() # read values
    dist_array.append(distance) # append to array
    if len(dist_array)>plot_pts:
        dist_array = dist_array[1:] # drop first point (maintain array size)
        line1,bar1 = plot_updater() # update plot
ser.close() # close serial port

