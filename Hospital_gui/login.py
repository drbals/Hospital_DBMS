from tkinter import*
root = Tk()
#root.geometry('500x500')
root.state('zoomed')
root.title("Appalamma Hospitals")

self=Frame(root,width=500, height=500,pady=200)

label_0 = tk.Label(self, text="Login/Signup",width=20,font=("bold", 20))
label_0.place(x=90,y=10)

var = IntVar()
tk.Radiobutton(self, text="Patient", padx=5, variable=var, value=1, font=("bold", 10)).place(x=150, y=80)
tk.Radiobutton(self, text="Doctor", padx=5, variable=var, value=2, font=("bold", 10)).place(x=220, y=80)
tk.Radiobutton(self, text="Staff", padx=5, variable=var, value=3, font=("bold", 10)).place(x=290, y=80)



label_1 = tk.Label(self, text="Email ID",width=20,font=("bold", 10))
label_1.place(x=80,y=130)

entry_1 = tk.Entry(self)
entry_1.place(x=240,y=130)

label_2 = tk.Label(self, text="Password",width=20,font=("bold", 10))
label_2.place(x=68,y=180)

entry_2 = tk.Entry(self,show='*')
entry_2.place(x=240,y=180)

#This function is called after Login Button is clicked
def login():
    if(var.get()==0 or entry_1.get()=="" or entry_2.get()==""):
        print("Check")
        #Warn using a pop Up
    else :
        print("Check")
        #Hash the Password
        #send the request to API for validation of credentials
        #Get the response and based on the response Load the logged in frame

#This function is called after signup Button is clicked
def signup():
    if(var.get()==0):
        print("Check")
        #warn to select who he/she is. So that corresponding signup page can be loaded!
    else :
        print("Check")
        #based on the value from var.get() load the corresponding Signup Page!

tk.Button(self, text='  Login  ',bg='brown',fg='white',command=login).place(x=250,y=250)

tk.Button(self, text='Sign Up',command=signup).place(x=170,y=250)

self.pack()

root.mainloop()
