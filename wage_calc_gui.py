import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class TrueHourlyWageCalculator:
    def __init__(self, root):
        #font tuple
        self.font_family = "Segoe UI"  #hotswap fonts
        self.title_font = (self.font_family, 24, 'bold')
        self.heading_font = (self.font_family, 16, 'bold')
        self.subheading_font = (self.font_family, 12, 'bold')
        self.body_font = (self.font_family, 10)
        self.small_font = (self.font_family, 9)

        self.root = root
        self.root.title("True Hourly Wage Calculator")
        self.root.geometry("1500x1000")
        self.root.configure(bg='#f0f0f0')
        
        # vars
        self.paycheck_var = tk.DoubleVar(value=2000)
        self.daily_hours_var = tk.DoubleVar(value=8)
        self.work_days_var = tk.DoubleVar(value=5)
        self.commute_minutes_var = tk.DoubleVar(value=30)
        self.daily_miles_var = tk.DoubleVar(value=10)
        self.gas_price_var = tk.DoubleVar(value=3.50)
        self.mpg_var = tk.DoubleVar(value=25)
        self.daily_costs_var = tk.DoubleVar(value=5)
        
        # Transport vars
        self.transport_type = tk.StringVar(value="car")
        self.ev_efficiency_var = tk.DoubleVar(value=4.0)
        self.electricity_price_var = tk.DoubleVar(value=0.15)
        self.public_daily_cost_var = tk.DoubleVar(value=5.50)
        self.public_monthly_cost_var = tk.DoubleVar(value=100)
        self.public_walking_minutes_var = tk.DoubleVar(value=10)
        self.use_monthly_pass = tk.BooleanVar(value=False)
        
        # frequency of pay
        self.pay_frequency = tk.StringVar(value="biweekly")
        
        self.setup_ui()
        
    def setup_ui(self):
        #notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        style = ttk.Style()
        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TNotebook.Tab', background='#f0f0f0')
        
        # main page
        self.main_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text="Calculator")
        
        # results
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="Results")
        
        self.setup_calculator_tab()
        self.setup_results_tab()
        
    def setup_calculator_tab(self):
        # Create a main container for calculator inputs
        main_container = ttk.Frame(self.main_frame)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_container, text="True Hourly Wage Calculator", font=self.title_font)
        title_label.pack(pady=(0, 30))
        
        #description
        description = """How much are you actaully getting paid?"""
        desc_label = ttk.Label(main_container, text=description, font=self.subheading_font, wraplength=800, justify='center')
        desc_label.pack(pady=(0, 30))
        
        # all input sections
        inputs_frame = ttk.Frame(main_container)
        inputs_frame.pack(fill='both', expand=True)
        
        # left column for pay and work schedule
        left_column = ttk.Frame(inputs_frame)
        left_column.pack(side='left', fill='both', expand=True, padx=10)
        
        # right column for commute and transport
        right_column = ttk.Frame(inputs_frame)
        right_column.pack(side='right', fill='both', expand=True, padx=10)
        
        # pay info
        pay_frame = ttk.LabelFrame(left_column, text="Pay Information", padding=15)
        pay_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(pay_frame, text="Pay Frequency:", font=self.body_font).grid(row=0, column=0, sticky='w', pady=8)
        freq_combo = ttk.Combobox(pay_frame, textvariable=self.pay_frequency,
                                 values=["daily", "weekly", "biweekly", "semi_monthly", "monthly"],
                                 state="readonly", width=20, font=self.body_font)
        freq_combo.grid(row=0, column=1, padx=10, pady=8, sticky='w')
        
        ttk.Label(pay_frame, text="Take-home Pay:", font=self.body_font).grid(row=1, column=0, sticky='w', pady=8)
        pay_entry = ttk.Entry(pay_frame, textvariable=self.paycheck_var, width=20, font=self.body_font)
        pay_entry.grid(row=1, column=1, padx=10, pady=8, sticky='w')
        ttk.Label(pay_frame, text="$", font=self.body_font).grid(row=1, column=2, sticky='w', pady=8)
        
        # Work Schedule Section
        work_frame = ttk.LabelFrame(left_column, text="Work Schedule", padding=15)
        work_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(work_frame, text="Daily Work Hours:", font=self.body_font).grid(row=0, column=0, sticky='w', pady=8)
        hours_scale = ttk.Scale(work_frame, from_=1, to=12, variable=self.daily_hours_var, 
                               orient='horizontal', length=200)
        hours_scale.grid(row=0, column=1, padx=10, pady=8, sticky='w')
        self.hours_label = ttk.Label(work_frame, text=f"{self.daily_hours_var.get():.1f} hrs", font=self.body_font)
        self.hours_label.grid(row=0, column=2, padx=5, pady=8)
        
        ttk.Label(work_frame, text="Work Days per Week:", font=self.body_font).grid(row=1, column=0, sticky='w', pady=8)
        days_scale = ttk.Scale(work_frame, from_=1, to=7, variable=self.work_days_var, orient='horizontal', length=200)
        days_scale.grid(row=1, column=1, padx=10, pady=8, sticky='w')
        self.days_label = ttk.Label(work_frame, text=f"{self.work_days_var.get():.0f} days", font=self.body_font)
        self.days_label.grid(row=1, column=2, padx=5, pady=8)
        
        # ui scaling
        self.daily_hours_var.trace('w', lambda *args: self.hours_label.config(text=f"{self.daily_hours_var.get():.1f} hrs"))
        self.work_days_var.trace('w', lambda *args: self.days_label.config(text=f"{self.work_days_var.get():.0f} days"))
        
        # other costs
        costs_frame = ttk.LabelFrame(left_column, text="Additional Costs", padding=15)
        costs_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(costs_frame, text="Additional Daily Costs:", font=self.body_font).grid(row=0, column=0, sticky='w', pady=8)
        ttk.Entry(costs_frame, textvariable=self.daily_costs_var, width=20, font=self.body_font).grid(row=0, column=1, padx=10, pady=8, sticky='w')
        ttk.Label(costs_frame, text="$", font=self.body_font).grid(row=0, column=2, sticky='w', pady=8)
        ttk.Label(costs_frame, text="parking, tolls, etc.", font=self.body_font, foreground='gray').grid(row=1, column=0, columnspan=3, sticky='w', pady=(0, 5))
        
        #calc button 
        ttk.Button(left_column, text="Calculate True Hourly Wage", 
                  command=self.calculate, style='Accent.TButton').pack(pady=30)
        
        # commute times 
        commute_time_frame = ttk.LabelFrame(right_column, text="Commute Time", padding=15)
        commute_time_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(commute_time_frame, text="One-way Commute Time:", font=self.body_font).grid(row=0, column=0, sticky='w', pady=8)
        commute_scale = ttk.Scale(commute_time_frame, from_=0, to=180, variable=self.commute_minutes_var,
                                 orient='horizontal', length=200)
        commute_scale.grid(row=0, column=1, padx=10, pady=8, sticky='w')
        self.commute_label = ttk.Label(commute_time_frame, text=f"{self.commute_minutes_var.get():.0f} min", font=self.body_font)
        self.commute_label.grid(row=0, column=2, padx=5, pady=8)
        
        # commute label when scale changes
        self.commute_minutes_var.trace('w', lambda *args: self.commute_label.config(text=f"{self.commute_minutes_var.get():.0f} min"))
        
        # transportation type 
        transport_frame = ttk.LabelFrame(right_column, text="Transportation Type", padding=15)
        transport_frame.pack(fill='x', pady=(0, 20))
        
        # Transport type buttons
        transport_types = [
            ("Car", "car"),
            ("Electric Vehicle", "ev"),
            ("Public Transport", "public"),
            ("Biking", "biking"),
            ("Walking", "walking")
        ]
        
        for i, (text, value) in enumerate(transport_types):
            rb = ttk.Radiobutton(transport_frame, text=text, variable=self.transport_type, value=value, command=self.on_transport_change)
            rb.grid(row=i//2, column=i%2, sticky='w', pady=5, padx=10)
        
        # update ui based on transport details 
        self.transport_details_frame = ttk.LabelFrame(right_column, text="Transport Details", padding=15)
        self.transport_details_frame.pack(fill='x', pady=(0, 20))
        self.setup_transport_details()
        
    def setup_transport_details(self):
        # clear all existing widgets
        for widget in self.transport_details_frame.winfo_children():
            widget.destroy()
        
        transport_type = self.transport_type.get()
        self.transport_details_frame.config(text=f"{transport_type.title()} Details")
        
        if transport_type == "car":
            ttk.Label(self.transport_details_frame, text="One-way Distance:", font=self.body_font).grid(row=0, column=0, sticky='w', pady=8)
            ttk.Entry(self.transport_details_frame, textvariable=self.daily_miles_var, width=15, font=self.body_font).grid(row=0, column=1, padx=10, pady=8)
            ttk.Label(self.transport_details_frame, text="miles", font=self.body_font).grid(row=0, column=2, sticky='w', pady=8)
            
            ttk.Label(self.transport_details_frame, text="Gas Price:", font=self.body_font).grid(row=1, column=0, sticky='w', pady=8)
            ttk.Entry(self.transport_details_frame, textvariable=self.gas_price_var, width=15, font=self.body_font).grid(row=1, column=1, padx=10, pady=8)
            ttk.Label(self.transport_details_frame, text="$/gallon", font=self.body_font).grid(row=1, column=2, sticky='w', pady=8)
            
            ttk.Label(self.transport_details_frame, text="MPG:", font=self.body_font).grid(row=2, column=0, sticky='w', pady=8)
            ttk.Entry(self.transport_details_frame, textvariable=self.mpg_var, width=15, font=self.body_font).grid(row=2, column=1, padx=10, pady=8)
            ttk.Label(self.transport_details_frame, text="miles/gallon", font=self.body_font).grid(row=2, column=2, sticky='w', pady=8)
            
        elif transport_type == "ev":
            ttk.Label(self.transport_details_frame, text="One-way Distance:", font=self.body_font).grid(row=0, column=0, sticky='w', pady=8)
            ttk.Entry(self.transport_details_frame, textvariable=self.daily_miles_var, width=15, font=self.body_font).grid(row=0, column=1, padx=10, pady=8)
            ttk.Label(self.transport_details_frame, text="miles", font=self.body_font).grid(row=0, column=2, sticky='w', pady=8)
            
            ttk.Label(self.transport_details_frame, text="EV Efficiency:", font=self.body_font).grid(row=1, column=0, sticky='w', pady=8)
            ttk.Entry(self.transport_details_frame, textvariable=self.ev_efficiency_var, width=15, font=self.body_font).grid(row=1, column=1, padx=10, pady=8)
            ttk.Label(self.transport_details_frame, text="mi/kWh", font=self.body_font).grid(row=1, column=2, sticky='w', pady=8)
            
            ttk.Label(self.transport_details_frame, text="Electricity Price:", font=self.body_font).grid(row=2, column=0, sticky='w', pady=8)
            ttk.Entry(self.transport_details_frame, textvariable=self.electricity_price_var, width=15, font=self.body_font).grid(row=2, column=1, padx=10, pady=8)
            ttk.Label(self.transport_details_frame, text="$/kWh", font=self.body_font).grid(row=2, column=2, sticky='w', pady=8)
            
        elif transport_type == "public":
            ttk.Radiobutton(self.transport_details_frame, text="Daily Cost", variable=self.use_monthly_pass, value=False, command=self.on_public_cost_change).grid(row=0, column=0, sticky='w', pady=8, padx=10)
            ttk.Radiobutton(self.transport_details_frame, text="Monthly Pass", variable=self.use_monthly_pass, value=True, command=self.on_public_cost_change).grid(row=0, column=1, sticky='w', pady=8, padx=10)
            self.public_cost_label = ttk.Label(self.transport_details_frame, text="Daily Cost:", font=self.body_font)
            self.public_cost_label.grid(row=1, column=0, sticky='w', pady=8)
            self.public_cost_entry = ttk.Entry(self.transport_details_frame, textvariable=self.public_daily_cost_var, width=15, font=self.body_font)
            self.public_cost_entry.grid(row=1, column=1, padx=10, pady=8)
            ttk.Label(self.transport_details_frame, text="$", font=self.body_font).grid(row=1, column=2, sticky='w', pady=8)
            ttk.Label(self.transport_details_frame, text="Walking Time to/from Stations:", font=self.body_font).grid(row=2, column=0, sticky='w', pady=8)
            ttk.Entry(self.transport_details_frame, textvariable=self.public_walking_minutes_var, width=15, font=self.body_font).grid(row=2, column=1, padx=10, pady=8)
            ttk.Label(self.transport_details_frame, text="minutes", font=self.body_font).grid(row=2, column=2, sticky='w', pady=8)
            
        elif transport_type in ["biking", "walking"]:
            ttk.Label(self.transport_details_frame, text="One-way Distance:", font=self.body_font).grid(row=0, column=0, sticky='w', pady=8)
            ttk.Entry(self.transport_details_frame, textvariable=self.daily_miles_var, width=15, font=self.body_font).grid(row=0, column=1, padx=10, pady=8)
            ttk.Label(self.transport_details_frame, text="miles", font=self.body_font).grid(row=0, column=2, sticky='w', pady=8)
            
    def on_transport_change(self):
        self.setup_transport_details()
        
    def on_public_cost_change(self):
        if hasattr(self, 'public_cost_label') and hasattr(self, 'public_cost_entry'):
            if self.use_monthly_pass.get():
                self.public_cost_label.config(text="Monthly Pass Cost:")
                self.public_cost_entry.config(textvariable=self.public_monthly_cost_var)
            else:
                self.public_cost_label.config(text="Daily Cost:")
                self.public_cost_entry.config(textvariable=self.public_daily_cost_var)
    
    
    def update_canvas_width(self, event):
        self.results_canvas.itemconfig(1, width=event.width)

    def setup_results_tab(self):
        # This will be populated after calculation
        self.results_canvas = tk.Canvas(self.results_frame, bg='#f0f0f0', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", 
                                    command=self.results_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.results_canvas)
        self.results_canvas.bind('<Configure>', self.update_canvas_width)
        # config the scrollable frame to have the same background
        style = ttk.Style()
        style.configure('Results.TFrame', background='#f0f0f0')
        self.scrollable_frame.configure(style='Results.TFrame')
        
        # make the window expand to fill width
        self.results_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", 
                                        width=self.results_canvas.winfo_reqwidth())
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all"))
        )
        
        self.results_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.results_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
    
    def calculate(self):
        try:
            paycheck = self.paycheck_var.get()
            daily_hours = self.daily_hours_var.get()
            work_days = self.work_days_var.get()
            commute_minutes = self.commute_minutes_var.get()
            daily_miles = self.daily_miles_var.get()
            daily_costs = self.daily_costs_var.get()
            transport_type = self.transport_type.get()

            pay_freq = self.pay_frequency.get()
            if pay_freq == 'daily':
                annual_income = paycheck * work_days * 50
            elif pay_freq == 'weekly':
                annual_income = paycheck * 50
            elif pay_freq == 'biweekly':
                annual_income = paycheck * 26
            elif pay_freq == 'semi_monthly':
                annual_income = paycheck * 24
            else:  # monthly
                annual_income = paycheck * 12

            if transport_type == "public":
                commute_minutes += self.public_walking_minutes_var.get()
            
            daily_commute_hours = (commute_minutes * 2) / 60

            daily_commute_cost = daily_costs
            cost_breakdown = ""
            
            if transport_type == "car":
                round_trip_miles = daily_miles * 2
                gas_mileage = self.mpg_var.get()
                gas_price = self.gas_price_var.get()
                daily_fuel_cost = (round_trip_miles / gas_mileage) * gas_price if gas_mileage > 0 else 0
                daily_commute_cost += daily_fuel_cost
                cost_breakdown = f"Fuel: ${daily_fuel_cost:.2f}"
                
            elif transport_type == "ev":
                round_trip_miles = daily_miles * 2
                ev_efficiency = self.ev_efficiency_var.get()
                electricity_price = self.electricity_price_var.get()
                daily_electricity_cost = (round_trip_miles / ev_efficiency) * electricity_price if ev_efficiency > 0 else 0
                daily_commute_cost += daily_electricity_cost
                cost_breakdown = f"Electricity: ${daily_electricity_cost:.2f}"
                
            elif transport_type == "public":
                if self.use_monthly_pass.get():
                    monthly_pass = self.public_monthly_cost_var.get()
                    daily_transport_cost = monthly_pass / (work_days * 4.33)  # avg weeks per month
                else:
                    daily_transport_cost = self.public_daily_cost_var.get()
                daily_commute_cost += daily_transport_cost
                cost_breakdown = f"Transport: ${daily_transport_cost:.2f}"
            
            elif transport_type in ["biking", "walking"]:
                cost_breakdown = "No fuel/transportation costs"
                if daily_costs > 0:
                    cost_breakdown = f"Gear/Maintenance: ${daily_costs:.2f}"
            
            # yearly
            weekly_work_hours = daily_hours * work_days
            weekly_commute_hours = daily_commute_hours * work_days
            weekly_commute_costs = daily_commute_cost * work_days
            
            work_weeks_per_year = 50
            yearly_work_hours = weekly_work_hours * work_weeks_per_year
            yearly_commute_hours = weekly_commute_hours * work_weeks_per_year
            yearly_commute_costs = weekly_commute_costs * work_weeks_per_year
            
            # wage calculations
            traditional_wage = annual_income / yearly_work_hours if yearly_work_hours > 0 else 0
            net_yearly_income = annual_income - yearly_commute_costs
            total_committed_hours = yearly_work_hours + yearly_commute_hours
            true_wage = net_yearly_income / total_committed_hours if total_committed_hours > 0 else 0
            
            # savee results
            self.results = {
                'traditional_wage': traditional_wage,
                'true_wage': true_wage,
                'annual_income': annual_income,
                'yearly_commute_costs': yearly_commute_costs,
                'net_yearly_income': net_yearly_income,
                'yearly_work_hours': yearly_work_hours,
                'yearly_commute_hours': yearly_commute_hours,
                'total_committed_hours': total_committed_hours,
                'daily_commute_cost': daily_commute_cost,
                'daily_commute_hours': daily_commute_hours,
                'cost_breakdown': cost_breakdown,
                'transport_type': transport_type,
                'daily_miles': daily_miles
            }
            
            # switcching 
            self.notebook.select(1)
            self.display_results()
            
        except Exception as e:
            messagebox.showerror("Calculation Error", f"An error occurred: {str(e)}")
    
    def display_results(self):
        # clear results 
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        r = self.results
    
        header_frame = ttk.Frame(self.scrollable_frame)
        header_frame.pack(fill='x', padx=20, pady=20)
        
        ttk.Label(self.transport_details_frame, text="$/kWh", font=self.body_font).grid(row=2, column=2, sticky='w', pady=8)
        
        # wage Comparison
        wage_frame = ttk.LabelFrame(self.scrollable_frame, text="Wage Analysis", padding=15)
        wage_frame.pack(fill='x', padx=20, pady=10)

        # grid layout inside wage_frame
        wage_frame.grid_columnconfigure(0, weight=1)  # Left column
        wage_frame.grid_columnconfigure(1, weight=1)  # Middle column  
        wage_frame.grid_columnconfigure(2, weight=1)  # Right column

        # trad wage
        ttk.Label(wage_frame, text="Traditional Hourly Wage:", 
                font=self.heading_font).grid(row=0, column=0, sticky='w', padx=10, pady=5)
        ttk.Label(wage_frame, text=f"${r['traditional_wage']:.2f}", 
                font=self.heading_font, foreground='#2c3e50').grid(row=1, column=0, sticky='w', padx=10, pady=5)

        # diff
        diff = r['traditional_wage'] - r['true_wage']
        ttk.Label(wage_frame, text="Difference:", 
                font=self.heading_font).grid(row=0, column=1, sticky='w', padx=10, pady=5)
        ttk.Label(wage_frame, text=f"${diff:.2f} per hour", 
                font=self.heading_font).grid(row=1, column=1, sticky='w', padx=10, pady=5)

        # true wage
        ttk.Label(wage_frame, text="True Hourly Wage:", 
                font=self.heading_font).grid(row=0, column=2, sticky='w', padx=10, pady=5)
        ttk.Label(wage_frame, text=f"${r['true_wage']:.2f}", 
                font=self.heading_font, foreground='#27ae60').grid(row=1, column=2, sticky='w', padx=10, pady=5)

        if diff > 0:
            ttk.Label(wage_frame, 
                    text=f"Commute reduces wage by ${diff:.2f}/hr",
                    font=self.subheading_font, foreground='#c0392b').grid(row=2, column=0, columnspan=3, sticky='w', padx=10, pady=(10, 0))
        
        time_frame = ttk.LabelFrame(self.scrollable_frame, text="Time Breakdown", padding=15)
        time_frame.pack(fill='x', padx=20, pady=10)
        
        # time metrics
        metrics = [
            ("Daily Work Hours", f"{self.daily_hours_var.get():.1f} hrs"),
            ("Daily Commute Time", f"{r['daily_commute_hours']:.1f} hrs"),
            ("Weekly Work Hours", f"{self.daily_hours_var.get() * self.work_days_var.get():.1f} hrs"),
            ("Weekly Commute Hours", f"{r['daily_commute_hours'] * self.work_days_var.get():.1f} hrs"),
            ("Yearly Work Hours", f"{r['yearly_work_hours']:.0f} hrs"),
            ("Yearly Commute Hours", f"{r['yearly_commute_hours']:.0f} hrs"),
            ("Total Committed Hours/Year", f"{r['total_committed_hours']:.0f} hrs")
        ]
        
        for i, (label, value) in enumerate(metrics):
            row = i // 2
            col = (i % 2) * 2
            
            ttk.Label(time_frame, text=label, font=self.body_font).grid(row=row, column=col, 
                                                                      sticky='w', padx=10, pady=5)
            ttk.Label(time_frame, text=value, font=self.body_font).grid(row=row, 
                                                                              column=col+1, 
                                                                              sticky='w', 
                                                                              padx=10, pady=5)
        
        # breakdown for cost
        cost_frame = ttk.LabelFrame(self.scrollable_frame, text="Cost Breakdown", padding=15)
        cost_frame.pack(fill='x', padx=20, pady=10)
        
        # Transport type
        transport_names = {
            'car': 'Car (Gas)',
            'ev': 'Electric Vehicle',
            'public': 'Public Transport',
            'biking': 'Biking',
            'walking': 'Walking'
        }
        
        ttk.Label(cost_frame, text=f"Transportation: {transport_names.get(r['transport_type'], r['transport_type'])}",
                 font=self.body_font).pack(anchor='w', pady=5)
        
        if r['transport_type'] in ['car', 'ev', 'biking', 'walking']:
            ttk.Label(cost_frame, text=f"Round Trip Distance: {r['daily_miles'] * 2:.1f} miles",
                     font=self.body_font).pack(anchor='w', pady=2)
        
        ttk.Label(cost_frame, text=f"Daily Cost Breakdown: {r['cost_breakdown']}",
                 font=self.body_font).pack(anchor='w', pady=2)
        
        if self.daily_costs_var.get() > 0 and r['transport_type'] not in ['biking', 'walking']:
            ttk.Label(cost_frame, text=f"+ Additional Costs: ${self.daily_costs_var.get():.2f}",
                     font=self.body_font).pack(anchor='w', pady=2)
        
        ttk.Label(cost_frame, text=f"Total Daily Commute Cost: ${r['daily_commute_cost']:.2f}",
                 font=self.body_font).pack(anchor='w', pady=5)
        
        # yearly costs
        yearly_cost_frame = ttk.Frame(cost_frame)
        yearly_cost_frame.pack(fill='x', pady=10)
        
        ttk.Label(yearly_cost_frame, text="Yearly Take-home Pay:", 
                 font=self.body_font).pack(side='left', padx=20)
        ttk.Label(yearly_cost_frame, text=f"${r['annual_income']:,.2f}", 
                 font=self.body_font).pack(side='left', padx=10)
        
        ttk.Label(yearly_cost_frame, text="Yearly Commute Costs:", 
                 font=self.body_font).pack(side='left', padx=20)
        ttk.Label(yearly_cost_frame, text=f"${r['yearly_commute_costs']:,.2f}", 
                 font=self.body_font, foreground='#c0392b').pack(side='left', padx=10)
        
        ttk.Label(yearly_cost_frame, text="Net Yearly Income:", 
                 font=self.body_font).pack(side='left', padx=20)
        ttk.Label(yearly_cost_frame, text=f"${r['net_yearly_income']:,.2f}", 
                 font=self.body_font, foreground='#27ae60').pack(side='left', padx=10)
        
        # % of income spent on commute
        if r['annual_income'] > 0:
            cost_percentage = (r['yearly_commute_costs'] / r['annual_income']) * 100
            ttk.Label(cost_frame, 
                     text=f"Commute costs consume {cost_percentage:.1f}% of your take-home pay",
                     font=self.body_font).pack(anchor='w', pady=5)
        
        # paycheck
        paycheck_frame = ttk.LabelFrame(self.scrollable_frame, text="Paycheck Perspective", padding=15)
        paycheck_frame.pack(fill='x', padx=20, pady=10)
        
        pay_freq = self.pay_frequency.get()
        paycheck = self.paycheck_var.get()
        
        if pay_freq == 'biweekly':
            biweekly_commute_cost = r['daily_commute_cost'] * self.work_days_var.get() * 2
            biweekly_commute_hours = r['daily_commute_hours'] * self.work_days_var.get() * 2
            percentage = (biweekly_commute_cost / paycheck) * 100 if paycheck > 0 else 0
            
            ttk.Label(paycheck_frame, text="Per Bi-weekly Paycheck:", 
                     font=self.body_font).pack(anchor='w', pady=5)
            
            ttk.Label(paycheck_frame, 
                     text=f"Take-home: ${paycheck:.2f} | Commute costs: ${biweekly_commute_cost:.2f} | Effective: ${paycheck - biweekly_commute_cost:.2f}",
                     font=self.body_font).pack(anchor='w', pady=2)
            
            ttk.Label(paycheck_frame, 
                     text=f"Commute time: {biweekly_commute_hours:.1f} hours | Commute eats {percentage:.1f}% of your paycheck",
                     font=self.body_font).pack(anchor='w', pady=2)
        
        # visualization
        self.create_visualization()
        ttk.Button(self.scrollable_frame, text="← Back to Calculator", 
                  command=lambda: self.notebook.select(0)).pack(pady=20)
    
    def create_visualization(self):
        # bar graph comparing wages
        vis_frame = ttk.LabelFrame(self.scrollable_frame, text="Wage Comparison", padding=15)
        vis_frame.pack(fill='x', padx=20, pady=10)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))
        fig.patch.set_facecolor('#f0f0f0')
        
        # bar graph for wages
        labels = ['Traditional Wage', 'True Hourly Wage']
        values = [self.results['traditional_wage'], self.results['true_wage']]
        colors = ['#3498db', '#27ae60']
        
        bars = ax1.bar(labels, values, color=colors)
        ax1.set_ylabel('Hourly Wage ($)')
        ax1.set_title('Wage Comparison')
        
        # value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'${value:.2f}', ha='center', va='bottom')
        
        # Pie chart
        work_hours = self.results['yearly_work_hours']
        commute_hours = self.results['yearly_commute_hours']
        
        if work_hours + commute_hours > 0:
            sizes = [work_hours, commute_hours]
            labels_pie = ['Work Hours', 'Commute Hours']
            colors_pie = ['#3498db', '#e74c3c']
            
            ax2.pie(sizes, labels=labels_pie, colors=colors_pie, autopct='%1.1f%%',
                   startangle=90)
            ax2.set_title('Yearly Time Allocation')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=vis_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

def main():
    root = tk.Tk()
    style = ttk.Style()
    style.configure('TFrame', background='#f0f0f0')
    style.configure('TLabelFrame', background='#f0f0f0')
    style.configure('TLabelframe.Label', background='#f0f0f0')
    style.configure('TNotebook', background='#f0f0f0')
    style.configure('TNotebook.Tab', background='#f0f0f0', foreground='black')
    style.map('TNotebook.Tab', 
          background=[('selected', '#f0f0f0')],
          foreground=[('selected', 'black')])
    # config colors
    style.configure('Accent.TButton', font=('Segoe UI', 12, 'bold'))  
    style.map('Accent.TButton', background=[('active', '#2980b9'), ('pressed', '#1c638e')])
    
    app = TrueHourlyWageCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()