import customtkinter as ctk
from tkinter import messagebox, filedialog
import os 


def get_ticket_price(age: int) -> int:


    if age < 3:
        return 0    
    elif 3 <= age <= 12:
        return 10   
    else: 
        return 15   

def calculate_group_cost(ages: list[int]) -> tuple[float, float, float]:
   
    group_size = len(ages)
    total_cost_before_discount = sum(get_ticket_price(age) for age in ages)
    
    discount_rate = 0.0
    if group_size >= 5:
       
        discount_rate = 0.10 
        
    discount_amount = total_cost_before_discount * discount_rate
    final_cost = total_cost_before_discount - discount_amount
    
    return final_cost, discount_amount, total_cost_before_discount


class CinemaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("🎬 Cinemax Ticket Calculator")
        self.geometry("650x550")
        ctk.set_appearance_mode("Dark") 
        ctk.set_default_color_theme("blue")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) 

        
        try:
            image_path = os.path.join(os.path.dirname(__file__), "cinema_icon.png")
            self.cinema_icon = ctk.CTkImage(light_image=None, dark_image=Image.open(image_path), size=(50, 50))
        except FileNotFoundError:
            self.cinema_icon = None

        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=0, pady=20, sticky="ew")
        title_frame.grid_columnconfigure(0, weight=1)

        if self.cinema_icon:
             ctk.CTkLabel(title_frame, image=self.cinema_icon, text="").grid(row=0, column=0, padx=10, sticky="w")
             
        ctk.CTkLabel(title_frame, text="CINEMAX PRICE CALCULATOR", 
                     font=ctk.CTkFont(size=26, weight="bold", family="Arial")).grid(row=0, column=0, pady=0)
        
        # --- Mode Selection Buttons ---
        self.button_frame = ctk.CTkFrame(self, border_width=2, border_color="#F1C40F") # Yellow border for attention
        self.button_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Single Mode Button (Red/Maroon theme)
        ctk.CTkButton(self.button_frame, text="SINGLE TICKET (TICKET)", command=self.show_single_mode, 
                      fg_color="#C0392B", hover_color="#A93226").grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Group Mode Button (Blue/Teal theme)
        ctk.CTkButton(self.button_frame, text="GROUP PURCHASE (POP-CORN)", command=self.show_group_mode, 
                      fg_color="#2980B9", hover_color="#2471A3").grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # --- Main Calculation Frame (Dynamic content) ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Initial display
        self.show_single_mode()

    # --- Mode Switching Logic ---

    def clear_main_frame(self):
        """Removes all widgets from the main_frame for switching modes."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_single_mode(self):
        self.clear_main_frame()
        
        # Input Label and Field
        ctk.CTkLabel(self.main_frame, text="PERSON'S AGE:", font=ctk.CTkFont(size=18)).grid(row=0, column=0, pady=(40, 10))
        self.age_entry = ctk.CTkEntry(self.main_frame, width=250, placeholder_text="Age (e.g., 25, 8, 2)")
        self.age_entry.grid(row=1, column=0, pady=10)
        
        # Calculate Button
        ctk.CTkButton(self.main_frame, text="CALCULATE PRICE", command=self.calculate_single).grid(row=2, column=0, pady=25)
        
        # Result Label
        self.result_label = ctk.CTkLabel(self.main_frame, text="Price: $0.00", font=ctk.CTkFont(size=30, weight="bold"))
        self.result_label.grid(row=3, column=0, pady=10)

    def calculate_single(self):
        """Calculates and displays the single ticket price."""
        try:
            age = int(self.age_entry.get())
            if age < 0:
                messagebox.showerror("Error", "Age must be non-negative.")
                return
            
            price = get_ticket_price(age)
            
            if price == 0:
                # Free ticket: set text to green/special
                self.result_label.configure(text_color="#2ECC71", text="Price: **FREE!** (Under 3)") 
            else:
                # Paid ticket: set text to yellow/gold
                self.result_label.configure(text_color="#F1C40F", text=f"Price: **${price}.00**")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer for age.")
            
    def show_group_mode(self):
        self.clear_main_frame()

        # Instruction Label
        ctk.CTkLabel(self.main_frame, text="ENTER AGES (COMMA-SEPARATED):", font=ctk.CTkFont(size=18)).grid(row=0, column=0, pady=(40, 10))
        
        # Ages Input Field
        self.ages_entry = ctk.CTkEntry(self.main_frame, width=400, placeholder_text="e.g., 10, 15, 4, 30, 45, 50, 7")
        self.ages_entry.grid(row=1, column=0, pady=10)
        
        # Calculate Button
        ctk.CTkButton(self.main_frame, text="CALCULATE GROUP COST", command=self.calculate_group).grid(row=2, column=0, pady=25)
        
        # Result Labels for Group
        self.cost_label = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=14))
        self.cost_label.grid(row=3, column=0, pady=2)
        
        self.discount_label = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=16, weight="bold"))
        self.discount_label.grid(row=4, column=0, pady=2)
        
        self.final_label = ctk.CTkLabel(self.main_frame, text="Final Cost: $0.00", font=ctk.CTkFont(size=30, weight="bold"), text_color="#3498DB")
        self.final_label.grid(row=5, column=0, pady=15)

    def calculate_group(self):
        """Calculates and displays the group ticket cost with discount."""
        ages_str = self.ages_entry.get().replace(" ", "")
        
        try:
            # Parse comma-separated string into a list of integers
            ages = [int(age) for age in ages_str.split(',') if age.strip() and age.isdigit()]
            
            if not ages:
                messagebox.showerror("Error", "Please enter at least one valid age.")
                return
            
            final_cost, discount_amount, pre_discount_cost = calculate_group_cost(ages)
            
            # Update GUI Labels
            self.cost_label.configure(text=f"Total Pre-Discount Cost: ${pre_discount_cost:.2f}")
            self.final_label.configure(text=f"Final Cost: **${final_cost:.2f}**")
            
            if discount_amount > 0:
                # Discount applied: show celebratory message
                self.discount_label.configure(text=f"🎉 10% GROUP DISCOUNT APPLIED! SAVED: ${discount_amount:.2f}", text_color="#2ECC71")
            else:
                # No discount applied
                self.discount_label.configure(text=f"No Discount (Group Size: {len(ages)}. Need 5+)", text_color="#E74C3C")
            
        except Exception:
            messagebox.showerror("Error", "Input format error. Ensure ages are numbers separated by commas.")


if __name__ == "__main__":
    # Import Image only if needed (for ctk.CTkImage)
    try:
        from PIL import Image
    except ImportError:
        # User needs to install Pillow for images
        pass 
        
    app = CinemaApp()
    app.mainloop()