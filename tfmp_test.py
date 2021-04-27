
try:
    while True:
        #time.sleep(0.001)   # Loop delay 50ms to match the 20Hz data frame rate
        # Use the 'getData' function to get data from device
        if( tfmP.getData()):
            print( f" Dist: {tfmP.dist:{3}}cm ", end= '')   # display distance,
            print( " | ", end= '')
            print(datetime.utcnow().strftime('%H:%M:%S.%f'))
            #print( f"Flux: {tfmP.flux:{4}d} ",   end= '')   # display signal strength/quality,
            #print( " | ", end= '')
            #print( f"Temp: {tfmP.temp:{2}}°C",  )   # display temperature,
        else:                  # If the command fails...
          tfmP.printFrame()    # display the error and HEX data
#
except KeyboardInterrupt:
    print( 'Keyboard Interrupt')
#    
except: # catch all other exceptions
    eType = sys.exc_info()[0]  # return exception type
    print( eType)
#
finally:
    print( "That's all folks!")
    sys.exit()                   # clean up the OS and exit
#
# - - - - - -  the main program sequence ends here  - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
