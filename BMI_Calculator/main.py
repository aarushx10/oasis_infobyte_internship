import customtkinter as ctk
from tkinter import messagebox

def output():
    try:
        height = float(height_placeholder.get())
        weight = float(weight_placeholder.get())
        if variable2.get()=="ft":
            height = height * 30.48
        if variable1.get()=="lbs":
            weight *= 0.453592
        bmi = weight / ((height/100) ** 2)
        result_label.configure(text=f"Your BMI is {bmi}")
    except ValueError:
        messagebox.showerror("Error","Enter a valid number")
    except ZeroDivisionError:
        messagebox.showerror("Error","Height cannot be 0")

def clear():
    weight_placeholder.delete(0,ctk.END)
    height_placeholder.delete(0,ctk.END)

if __name__ == "__main__":
    root = ctk.CTk()
    
    root._set_appearance_mode("system")
    root.iconbitmap("calculator.ico")
    root.title("BMI CALCULATOR")
    variable1 = ctk.StringVar()
    variable2= ctk.StringVar()

    
    height_label = ctk.CTkLabel(master=root,text="Height",font=("Helvetica",15))
    height_label.grid(row=0,column=0)

    age_label= ctk.CTkLabel(master=root,text="Ages: 2-120",font=("Helvetica",15))
    age_label.grid(row=0,column=1)

    height_placeholder = ctk.CTkEntry(master=root,placeholder_text="enter height",font=("Helvetica",15))
    height_placeholder.grid(row=1,column=0)

    height_dropdown = ctk.CTkComboBox(master=root,values=["cm","ft"],variable= variable2)
    height_dropdown.grid(row=1,column=1)
    height_dropdown.set("cm") 
    
    
    weight_label = ctk.CTkLabel(master=root,text="Weight",font=("Helvetica",15))
    weight_label.grid(row=2,column=0)

    weight_placeholder = ctk.CTkEntry(master=root,placeholder_text="Enter weight",font=("Helvetica",15))
    weight_placeholder.grid(row=3,column=0,pady=5)
    
    weight_dropdown = ctk.CTkComboBox(master=root,values=["kg","lbs"],variable=variable1)
    weight_dropdown.grid(row=3,column=1)
    weight_dropdown.set("kg")
    
  

    submit_button = ctk.CTkButton(master=root,text="Calculate",command=output)
    submit_button.grid(row=4,column=0,padx=20,pady=5)
    
    clear_button = ctk.CTkButton(master=root,text="Clear",command=clear)
    clear_button.grid(row=4,column=1,padx=5)
    
    result_label = ctk.CTkLabel(master=root,text="",font=("Helvetica",15))
    result_label.grid(row=5,column=0)

    root.mainloop()
