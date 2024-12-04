import tkinter as tk
from functions import generateExe,listen
from Server.infoFetch import get_system_info
from Server.server import fermer,get_ip_address,find_first_available_port
import threading
from tkinter import messagebox,filedialog

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome Application")
        self.root.geometry("700x500")
        self.root.configure(bg="black")
        
        
        self.frame1 = Frame1(self.root, self.run_script_callback, self.show_frame3)
        self.frame2 = Frame2(self.root)
        self.frame3 = Frame3(self.root)
        self.frame4 = Frame4(self.root)

        
        self.frame1.pack(fill="both", expand=True)

    def run_script_callback(self):
        try:
            result = get_system_info({}) 
            self.frame2.output_text.delete(1.0, tk.END)  
            
            
            for key, value in result.items():
                self.frame2.output_text.insert(tk.END, f"{key}: {value}\n") 
                
            
            self.frame2.label.config(text="Results of the local reconnaissance")
            
            self.show_frame2()
        except Exception as e:
            self.frame2.output_text.delete(1.0, tk.END)  
            self.frame2.output_text.insert(tk.END, f"Error executing script:\n{e}")  
            self.frame2.label.config(text="Script execution failed!")

    def show_frame2(self):
        self.frame1.pack_forget() 
        self.frame2.pack(fill="both", expand=True)  

    def show_frame3(self):
        self.frame1.pack_forget() 
        self.frame3.pack(fill="both", expand=True) 

global_port=None

class Frame1(tk.Frame):
    def __init__(self, master, run_script_callback, show_frame3_callback):
        super().__init__(master, bg="black", highlightbackground="black", highlightthickness=1)  
        self.run_script_callback = run_script_callback
        self.show_frame3_callback = show_frame3_callback

        label = tk.Label(self, text="Welcome to SysRecon", font=("Oswald", 20, "bold"), bg="black", fg="white")
        label.pack(pady=(50, 10))  

        description = tk.Label(self, text="This application enables you to conduct system reconnaissance on the operating system, battery, CPU, and more, whether on your local machine or a remote system. Select one of the options below to begin.",
                               font=("Oswald", 14), bg="black", fg="white", wraplength=600)
        description.pack(pady=(40, 20))  

        
        button_frame = tk.Frame(self, bg="black")
        button_frame.pack(expand=True)  
        


        
        button1 = tk.Button(button_frame, text="Local", command=self.run_script_callback,
                            bg="#007BFF", fg="white", font=("Oswald", 14, "bold"),
                            borderwidth=0, relief="flat", padx=20, pady=10, cursor='hand2')
        button1.pack(side=tk.LEFT, padx=20)  

        button2 = tk.Button(button_frame, text="Remote", command=self.show_frame3_callback,
                            bg="#28A745", fg="white", font=("Oswald", 14, "bold"),
                            borderwidth=0, relief="flat", padx=20, pady=10, cursor='hand2')
        button2.pack(side=tk.LEFT, padx=20)  

class Frame2(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="black", highlightbackground="black", highlightthickness=1)
        self.label = tk.Label(self, text="", font=("Oswald", 16, "bold"), bg="black", fg="white")
        self.label.pack(pady=(20, 10))

        self.output_text = tk.Text(self, height=15, width=60, bg="black", fg="white", font=("Oswald", 14, "bold"), wrap="word")
        self.output_text.pack(pady=(20, 10), padx=5)  

        go_back_button = tk.Button(self, text="Go Back", command=self.go_back,
                                   bg="#FF5733", fg="white", font=("Oswald", 12, "bold"),
                                   borderwidth=0, relief="flat", padx=20, pady=10 ,  cursor='hand2')
        go_back_button.pack(pady=(10, 20))  

    def go_back(self):
        self.master.children["!frame1"].pack(fill="both", expand=True)  # Show frame 1
        self.pack_forget() 

class Frame3(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="black", highlightbackground="black", highlightthickness=1)
        
        self.config(width=600, height=500)
        
        self.label = tk.Label(self, text="", font=("Oswald", 16, "bold"), bg="black", fg="white")
        self.label.pack(pady=(20, 10))

        description = tk.Label(self, text="Follow the instructions below to perform the remote reconnaissance",
                               font=("Oswald", 14), bg="black", fg="white", wraplength=600)
        description.pack(pady=(20, 10))

        instructions = [
            "1. An executable will be generated in a specified directory.",
            "2. Ensure both machines are connected to the same network.",
            "3. Start listening for incoming response.",
            "4. Deliver the executable to the remote machine and make sure that the user executes the .exe in order to retrieve the results ."
        ]

        for instruction in instructions:
            instruction_label = tk.Label(self, text=instruction, font=("Oswald", 14), 
                                         bg="black", fg="white", wraplength=600)
            instruction_label.pack(pady=(10, 5))
       
        button_frame = tk.Frame(self, bg="black")
        button_frame.pack(pady=(40, 20))

        go_back_button = tk.Button(button_frame, text="Go Back", command=self.go_back,
                                   bg="#FF5733", fg="white", font=("Oswald", 12, "bold"),
                                   borderwidth=0, relief="flat", padx=20, pady=10, cursor='hand2')
        go_back_button.pack(side=tk.LEFT, padx=10)

        start_listening_button = tk.Button(button_frame, text="generate executable", command=self.run_process,
                                           bg="#28A745", fg="white", font=("Oswald", 12, "bold"),
                                           borderwidth=0, relief="flat", padx=20, pady=10, cursor='hand2')
        start_listening_button.pack(side=tk.LEFT, padx=10)

    def show_loading_window(self):
        """Show a stylish loading window with a message."""
        self.loading_window = tk.Toplevel(self)
        self.loading_window.title("Loading...")
        self.loading_window.geometry("300x150")
        self.loading_window.config(bg="black")
        self.loading_window.resizable(False, False)

        frame = tk.Frame(self.loading_window, bg="black", width=300, height=150, bd=10)
        frame.pack_propagate(False)  
        frame.pack(padx=10, pady=5)

        self.loading_label = tk.Label(frame, text="target executable generation...", font=("Oswald", 12,"bold"), bg="black", fg="white", wraplength=600)
        self.loading_label.pack(pady=30)

        self.loading_window.grab_set()

    def hide_loading_window(self):
        self.loading_window.grab_release()
        self.loading_window.destroy()

    def run_process(self):

        global destination
        destination =  filedialog.askdirectory(title="File Destination")
        
        self.show_loading_window()
        threading.Thread(target=self.generate_executable).start()

    def generate_executable(self):

        global global_port
        global_port = find_first_available_port()
        ip_address = get_ip_address()

        generateExe(destination,global_port,ip_address)

        self.hide_loading_window()

        self.master.children["!frame4"].pack(fill="both", expand=True)  # Show Frame 4
        self.pack_forget()  

    def go_back(self):
        self.master.children["!frame1"].pack(fill="both", expand=True)
        self.pack_forget()

class Frame4(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="black", highlightthickness=0)  
        self.frame3 = Frame3
        self.config(width=600, height=500)
        self.label = tk.Label(self, text="", font=("Oswald", 16, "bold"), bg="black", fg="white")
        self.label.pack(pady=(20, 10))

        description = tk.Label(self, text="Follow the instructions below to perform the remote reconnaissance",
                               font=("Oswald", 14), bg="black", fg="white", wraplength=600)
        description.pack(pady=(20, 10))
        instructions = [
            "1. The executable file is successfully generated.",
            "2. Ensure both machines are connected to the same network.",
            "3. Start listening for incoming response.",
            "4. Deliver the executable to the remote machine and make sure that the user executes the .exe in order to retrieve the results ."
        ]

        for instruction in instructions:
            instruction_label = tk.Label(self, text=instruction, font=("Oswald", 14), 
                                         bg="black", fg="white", wraplength=560)  
            instruction_label.pack(pady=(10, 5), padx=(20, 20)) 

        button_frame = tk.Frame(self, bg="black")
        button_frame.pack(pady=(10, 20)) 

        go_back_button = tk.Button(button_frame, text="Go Back", command=self.go_back,
                                    bg="#FF5733", fg="white", font=("Oswald", 12, "bold"),
                                    borderwidth=0, relief="flat", padx=20, pady=10, cursor='hand2')
        go_back_button.pack(side=tk.LEFT, padx=(0, 10))  

        start_listening_button = tk.Button(button_frame, text="Start Listening", command=self.start_listening,
                                            bg="#28A745", fg="white", font=("Oswald", 12, "bold"),
                                            borderwidth=0, relief="flat", padx=20, pady=10, cursor='hand2')
        start_listening_button.pack(side=tk.LEFT)  

    def go_back(self):
        self.master.children["!frame1"].pack(fill="both", expand=True)
        self.pack_forget()

    def start_listening(self):
        
        global global_port
        results = listen(global_port)
        frame5 = Frame5(self.master,results)
        frame5.pack(fill="both", expand=True)  
        self.pack_forget()

class Frame5(tk.Frame):
    def __init__(self, master, results):
        super().__init__(master, bg="black", highlightthickness=0)  

        self.config(width=600, height=500)

        self.label = tk.Label(self, text="Results of the REMOTE reconnaissance", font=("Oswald", 16, "bold"), bg="black", fg="white")
        self.label.pack(pady=(10, 10))

        self.output_text = tk.Text(self, height=15, width=70, font=("Oswald", 14,'bold'), bg="black", fg="white", wrap=tk.WORD)
        self.output_text.pack(pady=(10, 10))  

        if results:
            for key, value in results.items():  
                self.output_text.insert(tk.END, f"{key}: {value}\n")  
        else:
            self.output_text.insert(tk.END, "No results")  

        button_frame = tk.Frame(self, bg="black")
        button_frame.pack(pady=(10, 20))  

        go_back_button = tk.Button(button_frame, text="Go Back", command=self.go_back,
                                    bg="#FF5733", fg="white", font=("Oswald", 12, "bold"),
                                    borderwidth=0, relief="flat", padx=20, pady=10, cursor='hand2')
        go_back_button.pack(side=tk.LEFT, padx=(0, 20))  

        disconnect = tk.Button(button_frame, text="disconnect", command=self.disconnect,
                               bg="#007BFF", fg="white", font=("Oswald", 12, "bold"),
                               borderwidth=0, relief="flat", padx=20, pady=10, cursor='hand2')
        disconnect.pack(side=tk.LEFT)  

    def go_back(self):
        self.master.children["!frame1"].pack(fill="both", expand=True)
        self.pack_forget()

    def disconnect(self):
        fermer()
        messagebox.showinfo(" Connection closed .")
        self.master.children["!frame1"].pack(fill="both", expand=True)  
        self.pack_forget() 


root = tk.Tk()
app = App(root)

root.mainloop()

