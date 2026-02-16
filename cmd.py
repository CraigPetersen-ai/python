import sys
import pyvisa as visa

def send_command_to_instrument(gpib_address, command):
    # Initialize the resource manager
    rm = visa.ResourceManager()
    
    # List all available resources and print them
    print("Available resources:", rm.list_resources())
    
    try:
        # Open a connection to the specified GPIB instrument
        instrument = rm.open_resource(f"GPIB0::{gpib_address}::INSTR")
        
        # Send the command
        instrument.write(command)
        
        # Optionally, you can read the response if needed
        response = instrument.read()
        print("Response from instrument:", response)
        
    except visa.VisaIOError as e:
        print(f"Failed to communicate with the instrument: {e}")
    
    finally:
        # Close the connection when done
        instrument.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: program.py <GPIB_address> '<command>'")
        sys.exit(1)
    
    gpib_address = sys.argv[1]
    command = sys.argv[2]
    
    send_command_to_instrument(gpib_address, command)

