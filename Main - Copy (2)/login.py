import tkinter as tk

def login():
    
    username = username_entry.get()
    password = password_entry.get()


    if username == "1" and password == "1":
        
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

        
        login_frame.pack_forget()
        import main_menu
    else:
        
        error_label.config(text="Invalid username or password")
        
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)


window = tk.Tk()
window.title("Criminal Recognition System")


login_frame = tk.Frame(window)

username_label = tk.Label(login_frame, text="Username:")
username_label.pack()

username_entry = tk.Entry(login_frame)
username_entry.pack()

password_label = tk.Label(login_frame, text="Password:")
password_label.pack()

password_entry = tk.Entry(login_frame, show="*")
password_entry.pack()

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.pack()

error_label = tk.Label(login_frame, fg="red")
error_label.pack()

login_frame.pack()


window.mainloop()
