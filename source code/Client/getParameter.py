import sys

# l'aquise des paramettres (addresse ip et port) en entree
def update_parameters():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'set-parameter':
            try:
                address = sys.argv[2]
                port = sys.argv[3]  
            except IndexError as e:
                print(f"Missing arguments for set-parameter: {e}")
            except Exception as e:
                print(f"Unexpected error during parameter set: {e}")

    return (address, int(port))