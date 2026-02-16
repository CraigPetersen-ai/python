import pyvisa

def list_resources():
    # Create a resource manager instance
    rm = pyvisa.ResourceManager()

    # List all available resources
    resources = rm.list_resources()

    if not resources:
        print("No instruments found.")
        return

    print("Instruments Found:")
    for resource in resources:
        print(f"Resource: {resource}")

if __name__ == "__main__":
    list_resources()
