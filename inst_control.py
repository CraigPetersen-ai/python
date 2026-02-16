import pyvisa
import matplotlib.pyplot as plt
import time
from tqdm import tqdm

# Initialize the GPIB interface
rm = pyvisa.ResourceManager()
resources = rm.list_resources()

def menu():
    print("\nGPIB Instrument Interface Menu:")
    print("1. List Instruments")
    print("2. Select Instrument")
    print("3. Read Instrument Once")
    print("4. Multiple Reads Plot Results")
    print("5. Send Command to Instrument")
    print("6. Query Instrument")
    print("7. Multiple Queries Plot Results")
    print("8. Exit")
    return input("Choose an option: ")

def list_instruments():
    for resource in resources:
        print(resource)

def select_instrument():
    print("Available instruments:")
    for i, resource in enumerate(resources):
        print(f"{i+1}. {resource}")
    choice = int(input("Enter the number of the instrument to select: ")) - 1
    return rm.open_resource(resources[choice])

def read_once(instrument):
    try:
        response = instrument.query("")
        print(f"Response from instrument: {response.strip()}")
    except pyvisa.VisaIOError as e:
        print(f"Error reading from the instrument: {e}")

def multiple_reads(instrument):
    readings = []
    count = int(input("Enter number of readings: "))
    delay = float(input("Enter delay between reads in seconds: "))

    with tqdm(total=count, desc="Reading", unit="read") as pbar:
        for i in range(count):
            try:
                reading = instrument.query("")
                readings.append(float(reading.strip()))
                if i < count - 1:
                    time.sleep(delay)
                pbar.update(1)
            except (pyvisa.VisaIOError, ValueError) as e:
                print(f"Error reading from the instrument: {e}. Stopping.")
                break

    plt.plot(readings)
    plt.title("Instrument Readings")
    plt.xlabel("Reading Number")
    plt.ylabel("Value")
    plt.show()

def send_command(instrument):
    command = input("Enter command to send to the instrument: ")
    try:
        response = instrument.query(command)
        print(f"Response from instrument: {response.strip()}")
    except pyvisa.VisaIOError as e:
        print(f"Error sending command or receiving response: {e}")

def query_instrument(instrument):
    query = input("Enter the query command: ")
    try:
        response = instrument.query(query)
        print(f"Response from instrument: {response.strip()}")
    except pyvisa.VisaIOError as e:
        print(f"Error querying the instrument: {e}")

def multiple_queries(instrument):
    responses = []
    query = input("Enter the query command to send: ")
    count = int(input("Enter number of queries: "))
    delay = float(input("Enter delay between queries in seconds: "))

    with tqdm(total=count, desc="Querying", unit="query") as pbar:
        for i in range(count):
            try:
                response = instrument.query(query)
                responses.append(float(response.strip()))
                if i < count - 1:
                    time.sleep(delay)
                pbar.update(1)
            except (pyvisa.VisaIOError, ValueError) as e:
                print(f"Error querying the instrument: {e}. Stopping.")
                break

    plt.plot(responses)
    plt.title("Instrument Query Responses")
    plt.xlabel("Query Number")
    plt.ylabel("Response Value")
    plt.show()

def main():
    instrument = None
    while True:
        choice = menu()

        if choice == '1':
            list_instruments()
        elif choice == '2':
            instrument = select_instrument()
            print(f"Selected: {instrument.resource_name}")
        elif choice == '3':
            if instrument:
                read_once(instrument)
            else:
                print("Please select an instrument first.")
        elif choice == '4':
            if instrument:
                multiple_reads(instrument)
            else:
                print("Please select an instrument first.")
        elif choice == '5':
            if instrument:
                send_command(instrument)
            else:
                print("Please select an instrument first.")
        elif choice == '6':
            if instrument:
                query_instrument(instrument)
            else:
                print("Please select an instrument first.")
        elif choice == '7':
            if instrument:
                multiple_queries(instrument)
            else:
                print("Please select an instrument first.")
        elif choice == '8':
            break
        else:
            print("Invalid option, please try again.")

    if instrument:
        instrument.close()
    rm.close()

if __name__ == "__main__":
    main()

