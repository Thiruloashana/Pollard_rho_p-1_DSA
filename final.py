from tkinter import ttk
import tkinter as tk
import random


global s1_entry
global s2_entry
global e2_entry



# Pollard Rho Factorization window
def rho():
    #function to go back to the main menu
    def go_back_to_menu():
        window.destroy()
        main_menu()

    # Pollard Rho algorithm for factorization
    def pollard_rho(n, B):
        x = 2
        y = 2
        c = 1
        d = 1
        values = []  # A list to store the intermediate values for visualization
        while d == 1 and len(values) < B:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = gcd(abs(x - y), n)
            values.append((x, y, c, d))
        if d == n:
            return None, values  # Factor not found
        else:
            return d, values

    # Calculate the greatest common divisor (GCD)
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    # Function to perform factorization
    def factorize():
        n = int(entry.get())  # Get the input number from the entry field
        B = 100  # Maximum number of iterations
        factor, values = pollard_rho(n, B)  # Call the Pollard Rho algorithm

        if factor is None:
            result_label.config(text="Could not factorize further.")
        else:
            result_label.config(text=f"Factors: {factor}")

        # Display the intermediate values in the GUI
        values_text.config(text="Iteration   |   f(x)   |   f(f(x))   |   c   |   d\n" + "\n".join(
            f"{i+1:10} | {x:8} | {y:11} | {c:5} | {d:5}" for i, (x, y, c, d) in enumerate(values)))

    # main tkinter window
    window = tk.Tk()
    window.title("Pollard Rho Factorization")

    # Create and place GUI elements on the window
    label = ttk.Label(window, text="Enter a number to factorize:")
    label.grid(row=0, column=0)

    entry = ttk.Entry(window)
    entry.grid(row=0, column=1)

    factor_button = ttk.Button(window, text="Factorize", command=factorize)
    factor_button.grid(row=1, column=0, columnspan=2)

    result_label = ttk.Label(window, text="")
    result_label.grid(row=2, column=0, columnspan=2)

    values_text = ttk.Label(window, text="")
    values_text.grid(row=3, column=0, columnspan=2)

    # Create a Back button to return to the menu
    back_button = ttk.Button(
        window, text="Back to Menu", command=go_back_to_menu)
    back_button.grid(row=4, column=0, columnspan=2)

    # Start the main GUI event loop
    window.mainloop()


# Define a function to create the Pollard's p-1 Factorization window
def p_1():

    # Define a function to go back to the main menu
    def go_back_to_menu():
        window.destroy()
        main_menu()

    # Pollard's p-1 algorithm for factorization
    def pollard_p_minus_1(n, B):
        a = 2
        p = 2
        factors = []
        while p < B:
            a = pow(a, p, n)
            d = gcd(a - 1, n)
            if d > 1:
                factors.append(d)
                while n % d == 0:
                    n //= d
            if n == 1:
                return factors
            p += 1
        return factors

    # Calculate the greatest common divisor (GCD)
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    # Function to perform factorization
    def factorize():
        n = int(entry.get())  # Get the input number from the entry field
        B = 100  # Maximum number of iterations
        factors = pollard_p_minus_1(n, B)  # Call the Pollard's p-1 algorithm

        if len(factors) == 0:
            result_label.config(text="Could not factorize further.")
        else:
            result_label.config(text="Factors: " + " ".join(map(str, factors)))

    # Create the main tkinter window
    window = tk.Tk()
    window.title("Pollard's p-1 Factorization")

    # Create and place GUI elements on the window
    label = ttk.Label(window, text="Enter a number to factorize:")
    label.grid(row=0, column=0)

    entry = ttk.Entry(window)
    entry.grid(row=0, column=1)

    factor_button = ttk.Button(window, text="Factorize", command=factorize)
    factor_button.grid(row=1, column=0, columnspan=2)

    result_label = ttk.Label(window, text="")
    result_label.grid(row=2, column=0, columnspan=2)

    # Create a Back button to return to the menu
    back_button = ttk.Button(
        window, text="Back to Menu", command=go_back_to_menu)
    back_button.grid(row=4, column=0, columnspan=2)

    # Start the main GUI event loop
    window.mainloop()



# Function to calculate the multiplicative inverse of r modulo q
def calc_inv(r, q):
    for i in range(1, q):  # Iterate through numbers 1 to q
        if (r * i) % q == 1:  # Check if (r * i) modulo q is equal to 1
            return i  # Return i as the multiplicative inverse of r modulo q



# Function to create the DSA implementation window
def dsa():
    # Function to go back to the main menu
    def go_back_to_menu():
        window.destroy()  # Close the current DSA window
        main_menu()  # Return to the main menu

    # Function to generate DSA key pair
    def generate_key():
        global e2_entry  # Access e2_entry as a global variable
        p = int(p_entry.get())  
        q = int(q_entry.get())  
        d = int(d_entry.get())  
        e0 = random.randint(2, p - 2)  # Generate a random e0
        e1 = int(e1_entry.get())  # Get the value of e1 from the input field
        e2 = e1 ** d  # Calculate e2
        e2 = e2 % p  # Take e2 modulo p
        public_key.set(f"Public Key: (e1={e1}, e2={e2}, p={p}, q={q})")  # Set the public key label
        private_key.set(f"Private Key: d={d}")  # Set the private key label
        e2_entry = e2  # Set e2_entry to the calculated e2

    # Function to sign a message using DSA        
    def sign():
        global e2_entry, s1_entry, s2_entry
        p = int(p_entry.get())
        q = int(q_entry.get())
        e1 = int(e1_entry.get())
        d = int(d_entry.get())
        r = int(r_entry.get())
        h_m = int(h_m_entry.get())

        s1 = (pow(e1, r) % p) % q
        r_inv = calc_inv(r, q) # Calculate the multiplicative inverse of r
        print("k_inv", r_inv)
        s2 = ((h_m + (d * s1)) * r_inv) % q # Calculate s2
        print("s2", s2)
        signature.set(f"Signature: (s1={s1}, s2={s2})")
        s1_entry = s1  # Set s1_entry to the calculated s1
        s2_entry = s2  # Set s2_entry to the calculated s2



    # Function to verify a DSA signature
    def verify():
        global e2_entry, s1_entry, s2_entry  # Access these variables as global
        e1 = int(e1_entry.get())  
        e2 = e2_entry  # Access the value of e2 as a global variable
        s1 = s1_entry  # Access the value of s1 as a global variable
        p = int(p_entry.get())  
        q = int(q_entry.get())  
        s2 = s2_entry  # Access the value of s2 as a global variable
        h_m = int(h_m_entry.get())  
        v = ((pow(e1, (h_m * calc_inv(s2, q)) % q) *
             pow(e2, (s1 * calc_inv(s2, q)) % q)) % p) % q  # Calculate v
        if 0 < s1 < q and 0 < s2 < q:  # Check if s1 and s2 are within valid ranges
            if v == s1:  # Check if v matches s1
                output_text.set("Signature verified successfully.") 
            else:
                output_text.set("Signature verification failed.")  
        else:
            output_text.set("Invalid values for s1 or s2")  # Set an error message

    # Create the main window
    window = tk.Tk()
    window.title("DSA Implementation")  

    # Create and place input fields and labels
    p_label = tk.Label(window, text="Enter p:")
    p_label.pack()
    p_entry = tk.Entry(window)
    p_entry.pack()

    q_label = tk.Label(window, text="Enter q:")
    q_label.pack()
    q_entry = tk.Entry(window)
    q_entry.pack()

    e1_label = tk.Label(window, text="Enter e1:")
    e1_label.pack()
    e1_entry = tk.Entry(window)
    e1_entry.pack()

    d_label = tk.Label(window, text="Enter d:")
    d_label.pack()
    d_entry = tk.Entry(window)
    d_entry.pack()

    r_label = tk.Label(window, text="Enter r:")
    r_label.pack()
    r_entry = tk.Entry(window)
    r_entry.pack()

    h_m_label = tk.Label(window, text="Enter h_m:")
    h_m_label.pack()
    h_m_entry = tk.Entry(window)
    h_m_entry.pack()

    # Create and place buttons
    keygen_button = tk.Button(
        window, text="Generate Key Pair", command=generate_key)
    keygen_button.pack()

    sign_button = tk.Button(window, text="Sign", command=sign)
    sign_button.pack()

    verify_button = tk.Button(window, text="Verify", command=verify)
    verify_button.pack()

    # Create and place output labels
    public_key = tk.StringVar()
    private_key = tk.StringVar()
    signature = tk.StringVar()
    output_text = tk.StringVar()

    public_key_label = tk.Label(window, textvariable=public_key)
    public_key_label.pack()

    private_key_label = tk.Label(window, textvariable=private_key)
    private_key_label.pack()

    signature_label = tk.Label(window, textvariable=signature)
    signature_label.pack()

    output_label = tk.Label(window, textvariable=output_text)
    output_label.pack()

    back_button = tk.Button(window, text="Back to Menu",
                            command=go_back_to_menu)
    back_button.pack()

    window.mainloop()


def main_menu():
    window = tk.Tk()
    window.title("Menu")

    
    window.geometry("400x200")

    
    title_label = ttk.Label(window, text="MENU", font=("Helvetica", 16))
    title_label.pack(pady=10)

    def open_rho():
        window.destroy()
        rho()

    def open_p_1():
        window.destroy()
        p_1()

    def open_dsa():
        window.destroy()
        dsa()

    
    button_frame = ttk.Frame(window)
    button_frame.pack(expand=True)

    rho_button = ttk.Button(button_frame, text="Pollard Rho", command=open_rho)
    rho_button.pack(side=tk.LEFT, padx=10, pady=10)

    p_1_button = ttk.Button(
        button_frame, text="Pollard's p-1", command=open_p_1)
    p_1_button.pack(side=tk.LEFT, padx=10, pady=10)

    dsa_button = ttk.Button(button_frame, text="DSA", command=open_dsa)
    dsa_button.pack(side=tk.LEFT, padx=10, pady=10)

    window.mainloop()



main_menu()