import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class TrueHourlyWageCalculator:
    def __init__(self, root):
        self.font_family = "Segoe UI"
        self.title_font = (self.font_family, 24, 'bold')
        self.heading_font = (self.font_family, 16, 'bold')
        self.subheading_font = (self.font_family, 14, 'bold')
        self.body_font = (self.font_family, 12)
        self.detail_font = (self.font_family, 13)
        self.small_font = (self.font_family, 11)

        self.root = root
        self.root.title("True Hourly Wage Calculator")
        self.root.geometry("1500x1000")
        self.root.configure(bg='#f0f0f0')
        
        # main vars
        self.paycheck_var = tk.DoubleVar(value=2000)
        self.daily_hours_var = tk.DoubleVar(value=8)
        self.work_days_var = tk.DoubleVar(value=5)
        self.commute_minutes_var = tk.DoubleVar(value=30)
        self.daily_miles_var = tk.DoubleVar(value=10)
        self.gas_price_var = tk.DoubleVar(value=3.50)
        self.mpg_var = tk.DoubleVar(value=25)
        self.daily_costs_var = tk.DoubleVar(value=5)
        self.wfh_days_var = tk.DoubleVar(value=0)  # WFH days
        
        # transport vars
        self.transport_type = tk.StringVar(value="car")
        self.ev_efficiency_var = tk.DoubleVar(value=4.0)
        self.electricity_price_var = tk.DoubleVar(value=0.15)
        self.public_daily_cost_var = tk.DoubleVar(value=5.50)
        self.public_monthly_cost_var = tk.DoubleVar(value=100)
        self.public_walking_minutes_var = tk.DoubleVar(value=10)
        self.use_monthly_pass = tk.BooleanVar(value=False)
        
        # comparison vars (initialized to match current, can be modified)
        self.comp_transport_type = tk.StringVar(value="car")
        self.comp_commute_minutes_var = tk.DoubleVar(value=30)
        self.comp_daily_miles_var = tk.DoubleVar(value=10)
        self.comp_gas_price_var = tk.DoubleVar(value=3.50)
        self.comp_mpg_var = tk.DoubleVar(value=25)
        self.comp_daily_costs_var = tk.DoubleVar(value=5)
        self.comp_ev_efficiency_var = tk.DoubleVar(value=4.0)
        self.comp_electricity_price_var = tk.DoubleVar(value=0.15)
        self.comp_public_daily_cost_var = tk.DoubleVar(value=5.50)
        self.comp_public_monthly_cost_var = tk.DoubleVar(value=100)
        self.comp_public_walking_minutes_var = tk.DoubleVar(value=10)
        self.comp_use_monthly_pass = tk.BooleanVar(value=False)
        
        self.pay_frequency = tk.StringVar(value="biweekly")
        
        self.setup_ui()

    def exit_app(self):
        try:
            if hasattr(self, 'results'):
                plt.close('all')
            self.root.quit()
        except:
            self.root.destroy()

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        exit_button = ttk.Button(self.root, text="Exit", command=self.exit_app)
        exit_button.place(relx=0.99, rely=0.99, anchor='se') 
        style = ttk.Style()
        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TNotebook.Tab', background='#f0f0f0')
        
        # tabs
        self.main_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text="Calculator")
        
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="Results")
        
        self.comparison_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.comparison_frame, text="Compare Commutes")
        
        self.setup_calculator_tab()
        self.setup_results_tab()
        self.setup_comparison_tab()
        
    def setup_calculator_tab(self):
        main_container = ttk.Frame(self.main_frame)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        title_label = ttk.Label(main_container, text="True Hourly Wage Calculator", font=self.title_font)
        title_label.pack(pady=(0, 30))
        
        description = """How much are you actually getting paid?"""
        desc_label = ttk.Label(main_container, text=description, font=self.subheading_font, wraplength=800, justify='center')
        desc_label.pack(pady=(0, 30))
        
        inputs_frame = ttk.Frame(main_container)
        inputs_frame.pack(fill='both', expand=True)
        
        left_column = ttk.Frame(inputs_frame)
        left_column.pack(side='left', fill='both', expand=True, padx=10)
        
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
        
        # work schedule
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
        
        # WFH days
        ttk.Label(work_frame, text="WFH Days per Week:", font=self.body_font).grid(row=2, column=0, sticky='w', pady=8)
        wfh_scale = ttk.Scale(work_frame, from_=0, to=7, variable=self.wfh_days_var, orient='horizontal', length=200)
        wfh_scale.grid(row=2, column=1, padx=10, pady=8, sticky='w')
        self.wfh_label = ttk.Label(work_frame, text=f"{self.wfh_days_var.get():.0f} days", font=self.body_font)
        self.wfh_label.grid(row=2, column=2, padx=5, pady=8)
        
        self.daily_hours_var.trace('w', lambda *args: self.hours_label.config(text=f"{self.daily_hours_var.get():.1f} hrs"))
        self.work_days_var.trace('w', lambda *args: self.days_label.config(text=f"{self.work_days_var.get():.0f} days"))
        self.wfh_days_var.trace('w', lambda *args: self.wfh_label.config(text=f"{self.wfh_days_var.get():.0f} days"))
        
        # additional costs
        costs_frame = ttk.LabelFrame(left_column, text="Additional Costs", padding=15)
        costs_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(costs_frame, text="Additional Daily Costs:", font=self.body_font).grid(row=0, column=0, sticky='w', pady=8)
        ttk.Entry(costs_frame, textvariable=self.daily_costs_var, width=20, font=self.body_font).grid(row=0, column=1, padx=10, pady=8, sticky='w')
        ttk.Label(costs_frame, text="$", font=self.body_font).grid(row=0, column=2, sticky='w', pady=8)
        ttk.Label(costs_frame, text="parking, tolls, etc.", font=self.body_font, foreground='gray').grid(row=1, column=0, columnspan=3, sticky='w', pady=(0, 5))
        
        ttk.Button(left_column, text="Calculate True Hourly Wage", 
                  command=self.calculate, style='Accent.TButton').pack(pady=30)
        
        # commute time - editable entry
        commute_time_frame = ttk.LabelFrame(right_column, text="Commute Time", padding=15)
        commute_time_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(commute_time_frame, text="One-way Commute Time:", font=self.body_font).grid(row=0, column=0, sticky='w', pady=8)
        ttk.Entry(commute_time_frame, textvariable=self.commute_minutes_var, width=15, font=self.body_font).grid(row=0, column=1, padx=10, pady=8, sticky='w')
        ttk.Label(commute_time_frame, text="minutes", font=self.body_font).grid(row=0, column=2, sticky='w', pady=8)
        
        # transportation type
        transport_frame = ttk.LabelFrame(right_column, text="Transportation Type", padding=15)
        transport_frame.pack(fill='x', pady=(0, 20))
        
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
        
        self.transport_details_frame = ttk.LabelFrame(right_column, text="Transport Details", padding=15)
        self.transport_details_frame.pack(fill='x', pady=(0, 20))
        self.setup_transport_details()
        
    def setup_transport_details(self, is_comparison=False):
        # determine which frame and vars to use
        if is_comparison:
            frame = self.comp_transport_details_frame
            transport_type = self.comp_transport_type.get()
            daily_miles_var = self.comp_daily_miles_var
            gas_price_var = self.comp_gas_price_var
            mpg_var = self.comp_mpg_var
            ev_efficiency_var = self.comp_ev_efficiency_var
            electricity_price_var = self.comp_electricity_price_var
            public_daily_cost_var = self.comp_public_daily_cost_var
            public_monthly_cost_var = self.comp_public_monthly_cost_var
            public_walking_minutes_var = self.comp_public_walking_minutes_var
            use_monthly_pass = self.comp_use_monthly_pass
        else:
            frame = self.transport_details_frame
            transport_type = self.transport_type.get()
            daily_miles_var = self.daily_miles_var
            gas_price_var = self.gas_price_var
            mpg_var = self.mpg_var
            ev_efficiency_var = self.ev_efficiency_var
            electricity_price_var = self.electricity_price_var
            public_daily_cost_var = self.public_daily_cost_var
            public_monthly_cost_var = self.public_monthly_cost_var
            public_walking_minutes_var = self.public_walking_minutes_var
            use_monthly_pass = self.use_monthly_pass
        
        for widget in frame.winfo_children():
            widget.destroy()
        
        frame.config(text=f"{transport_type.title()} Details")
        
        if transport_type == "car":
            ttk.Label(frame, text="One-way Distance:", font=self.body_font).grid(row=0, column=0, sticky='w', pady=8)
            ttk.Entry(frame, textvariable=daily_miles_var, width=15, font=self.body_font).grid(row=0, column=1, padx=10, pady=8)
            ttk.Label(frame, text="miles", font=self.body_font).grid(row=0, column=2, sticky='w', pady=8)
            
            ttk.Label(frame, text="Gas Price:", font=self.body_font).grid(row=1, column=0, sticky='w', pady=8)
            ttk.Entry(frame, textvariable=gas_price_var, width=15, font=self.body_font).grid(row=1, column=1, padx=10, pady=8)
            ttk.Label(frame, text="$/gallon", font=self.body_font).grid(row=1, column=2, sticky='w', pady=8)
            
            ttk.Label(frame, text="MPG:", font=self.body_font).grid(row=2, column=0, sticky='w', pady=8)
            ttk.Entry(frame, textvariable=mpg_var, width=15, font=self.body_font).grid(row=2, column=1, padx=10, pady=8)
            ttk.Label(frame, text="miles/gallon", font=self.body_font).grid(row=2, column=2, sticky='w', pady=8)
            
        elif transport_type == "ev":
            ttk.Label(frame, text="One-way Distance:", font=self.body_font).grid(row=0, column=0, sticky='w', pady=8)
            ttk.Entry(frame, textvariable=daily_miles_var, width=15, font=self.body_font).grid(row=0, column=1, padx=10, pady=8)
            ttk.Label(frame, text="miles", font=self.body_font).grid(row=0, column=2, sticky='w', pady=8)
            
            ttk.Label(frame, text="EV Efficiency:", font=self.body_font).grid(row=1, column=0, sticky='w', pady=8)
            ttk.Entry(frame, textvariable=ev_efficiency_var, width=15, font=self.body_font).grid(row=1, column=1, padx=10, pady=8)
            ttk.Label(frame, text="mi/kWh", font=self.body_font).grid(row=1, column=2, sticky='w', pady=8)
            
            ttk.Label(frame, text="Electricity Price:", font=self.body_font).grid(row=2, column=0, sticky='w', pady=8)
            ttk.Entry(frame, textvariable=electricity_price_var, width=15, font=self.body_font).grid(row=2, column=1, padx=10, pady=8)
            ttk.Label(frame, text="$/kWh", font=self.body_font).grid(row=2, column=2, sticky='w', pady=8)
            
        elif transport_type == "public":
            ttk.Radiobutton(frame, text="Daily Cost", variable=use_monthly_pass, value=False, 
                          command=lambda: self.on_public_cost_change(is_comparison)).grid(row=0, column=0, sticky='w', pady=8, padx=10)
            ttk.Radiobutton(frame, text="Monthly Pass", variable=use_monthly_pass, value=True, 
                          command=lambda: self.on_public_cost_change(is_comparison)).grid(row=0, column=1, sticky='w', pady=8, padx=10)
            
            cost_label_attr = 'comp_public_cost_label' if is_comparison else 'public_cost_label'
            cost_entry_attr = 'comp_public_cost_entry' if is_comparison else 'public_cost_entry'
            
            setattr(self, cost_label_attr, ttk.Label(frame, text="Daily Cost:", font=self.body_font))
            getattr(self, cost_label_attr).grid(row=1, column=0, sticky='w', pady=8)
            setattr(self, cost_entry_attr, ttk.Entry(frame, textvariable=public_daily_cost_var, width=15, font=self.body_font))
            getattr(self, cost_entry_attr).grid(row=1, column=1, padx=10, pady=8)
            ttk.Label(frame, text="$", font=self.body_font).grid(row=1, column=2, sticky='w', pady=8)
            
            ttk.Label(frame, text="Walking Time to/from Stations:", font=self.body_font).grid(row=2, column=0, sticky='w', pady=8)
            ttk.Entry(frame, textvariable=public_walking_minutes_var, width=15, font=self.body_font).grid(row=2, column=1, padx=10, pady=8)
            ttk.Label(frame, text="minutes", font=self.body_font).grid(row=2, column=2, sticky='w', pady=8)
            
        elif transport_type in ["biking", "walking"]:
            ttk.Label(frame, text="One-way Distance:", font=self.body_font).grid(row=0, column=0, sticky='w', pady=8)
            ttk.Entry(frame, textvariable=daily_miles_var, width=15, font=self.body_font).grid(row=0, column=1, padx=10, pady=8)
            ttk.Label(frame, text="miles", font=self.body_font).grid(row=0, column=2, sticky='w', pady=8)
            
    def on_transport_change(self, is_comparison=False):
        self.setup_transport_details(is_comparison)
        
    def on_public_cost_change(self, is_comparison=False):
        if is_comparison:
            if hasattr(self, 'comp_public_cost_label') and hasattr(self, 'comp_public_cost_entry'):
                if self.comp_use_monthly_pass.get():
                    self.comp_public_cost_label.config(text="Monthly Pass Cost:")
                    self.comp_public_cost_entry.config(textvariable=self.comp_public_monthly_cost_var)
                else:
                    self.comp_public_cost_label.config(text="Daily Cost:")
                    self.comp_public_cost_entry.config(textvariable=self.comp_public_daily_cost_var)
        else:
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
        self.results_canvas = tk.Canvas(self.results_frame, bg='#f0f0f0', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", 
                                    command=self.results_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.results_canvas)
        self.results_canvas.bind('<Configure>', self.update_canvas_width)
        
        style = ttk.Style()
        style.configure('Results.TFrame', background='#f0f0f0')
        self.scrollable_frame.configure(style='Results.TFrame')
        
        self.results_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", 
                                        width=self.results_canvas.winfo_reqwidth())
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all"))
        )
        
        self.results_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.results_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
    
    def setup_comparison_tab(self):
        # create scrollable canvas
        self.comparison_canvas = tk.Canvas(self.comparison_frame, bg='#f0f0f0', highlightthickness=0)
        self.comparison_scrollbar = ttk.Scrollbar(self.comparison_frame, orient="vertical", 
                                                 command=self.comparison_canvas.yview)
        self.comparison_scrollable_frame = ttk.Frame(self.comparison_canvas)
        
        self.comparison_canvas.bind('<Configure>', 
                                   lambda e: self.comparison_canvas.itemconfig(1, width=e.width))
        
        style = ttk.Style()
        style.configure('Comparison.TFrame', background='#f0f0f0')
        self.comparison_scrollable_frame.configure(style='Comparison.TFrame')
        
        self.comparison_canvas.create_window((0, 0), window=self.comparison_scrollable_frame, 
                                            anchor="nw", width=self.comparison_canvas.winfo_reqwidth())
        
        self.comparison_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.comparison_canvas.configure(scrollregion=self.comparison_canvas.bbox("all"))
        )
        
        self.comparison_canvas.configure(yscrollcommand=self.comparison_scrollbar.set)
        
        self.comparison_canvas.pack(side="left", fill="both", expand=True)
        self.comparison_scrollbar.pack(side="right", fill="y")
        
        # content
        main_container = ttk.Frame(self.comparison_scrollable_frame)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        title_label = ttk.Label(main_container, text="Compare Two Commute Options", font=self.title_font)
        title_label.pack(pady=(0, 30))
        
        # two columns for comparison
        columns_frame = ttk.Frame(main_container)
        columns_frame.pack(fill='both', expand=True)
        
        # current commute column
        current_column = ttk.Frame(columns_frame)
        current_column.pack(side='left', fill='both', expand=True, padx=10)
        
        ttk.Label(current_column, text="Current Commute", font=self.heading_font).pack(pady=10)
        ttk.Label(current_column, text="(from Calculator tab)", font=self.small_font, foreground='gray').pack(pady=5)
        
        # alternative commute column
        alt_column = ttk.Frame(columns_frame)
        alt_column.pack(side='right', fill='both', expand=True, padx=10)
        
        ttk.Label(alt_column, text="Alternative Commute", font=self.heading_font).pack(pady=10)
        
        # button to sync values
        ttk.Button(alt_column, text="Copy from Current Commute", 
                  command=self.sync_comparison_values).pack(pady=10)
        
        # alternative commute inputs
        comp_commute_frame = ttk.LabelFrame(alt_column, text="Commute Time", padding=15)
        comp_commute_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(comp_commute_frame, text="One-way Commute Time:", font=self.body_font).grid(row=0, column=0, sticky='w', pady=8)
        ttk.Entry(comp_commute_frame, textvariable=self.comp_commute_minutes_var, width=15, font=self.body_font).grid(row=0, column=1, padx=10, pady=8, sticky='w')
        ttk.Label(comp_commute_frame, text="minutes", font=self.body_font).grid(row=0, column=2, sticky='w', pady=8)
        
        comp_transport_frame = ttk.LabelFrame(alt_column, text="Transportation Type", padding=15)
        comp_transport_frame.pack(fill='x', pady=(0, 20))
        
        transport_types = [
            ("Car", "car"),
            ("Electric Vehicle", "ev"),
            ("Public Transport", "public"),
            ("Biking", "biking"),
            ("Walking", "walking")
        ]
        
        for i, (text, value) in enumerate(transport_types):
            rb = ttk.Radiobutton(comp_transport_frame, text=text, variable=self.comp_transport_type, value=value, 
                               command=lambda: self.on_transport_change(is_comparison=True))
            rb.grid(row=i//2, column=i%2, sticky='w', pady=5, padx=10)
        
        self.comp_transport_details_frame = ttk.LabelFrame(alt_column, text="Transport Details", padding=15)
        self.comp_transport_details_frame.pack(fill='x', pady=(0, 20))
        self.setup_transport_details(is_comparison=True)
        
        comp_costs_frame = ttk.LabelFrame(alt_column, text="Additional Costs", padding=15)
        comp_costs_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(comp_costs_frame, text="Additional Daily Costs:", font=self.body_font).grid(row=0, column=0, sticky='w', pady=8)
        ttk.Entry(comp_costs_frame, textvariable=self.comp_daily_costs_var, width=20, font=self.body_font).grid(row=0, column=1, padx=10, pady=8, sticky='w')
        ttk.Label(comp_costs_frame, text="$", font=self.body_font).grid(row=0, column=2, sticky='w', pady=8)
        
        ttk.Button(main_container, text="Compare Commutes", 
                  command=self.compare_commutes, style='Accent.TButton').pack(pady=30)
        
        # comparison results area
        self.comparison_results_frame = ttk.Frame(main_container)
        self.comparison_results_frame.pack(fill='both', expand=True, pady=20)
    
    def sync_comparison_values(self):
        # copy current commute values to comparison
        self.comp_commute_minutes_var.set(self.commute_minutes_var.get())
        self.comp_transport_type.set(self.transport_type.get())
        self.comp_daily_miles_var.set(self.daily_miles_var.get())
        self.comp_gas_price_var.set(self.gas_price_var.get())
        self.comp_mpg_var.set(self.mpg_var.get())
        self.comp_daily_costs_var.set(self.daily_costs_var.get())
        self.comp_ev_efficiency_var.set(self.ev_efficiency_var.get())
        self.comp_electricity_price_var.set(self.electricity_price_var.get())
        self.comp_public_daily_cost_var.set(self.public_daily_cost_var.get())
        self.comp_public_monthly_cost_var.set(self.public_monthly_cost_var.get())
        self.comp_public_walking_minutes_var.set(self.public_walking_minutes_var.get())
        self.comp_use_monthly_pass.set(self.use_monthly_pass.get())
        
        # refresh the transport details frame
        self.setup_transport_details(is_comparison=True)
    
    def calculate_commute_metrics(self, transport_type, commute_minutes, daily_miles, gas_price, mpg, 
                                  ev_efficiency, electricity_price, public_daily_cost, public_monthly_cost,
                                  public_walking_minutes, use_monthly_pass, daily_costs):
        # calculate costs and time for a given commute scenario
        work_days = self.work_days_var.get()
        wfh_days = self.wfh_days_var.get()
        commute_days = work_days - wfh_days  # only commute on non-WFH days
        
        if transport_type == "public":
            commute_minutes += public_walking_minutes
        
        daily_commute_hours = (commute_minutes * 2) / 60
        daily_commute_cost = daily_costs
        cost_breakdown = ""
        
        if transport_type == "car":
            round_trip_miles = daily_miles * 2
            daily_fuel_cost = (round_trip_miles / mpg) * gas_price if mpg > 0 else 0
            daily_commute_cost += daily_fuel_cost
            cost_breakdown = f"Fuel: ${daily_fuel_cost:.2f}"
            
        elif transport_type == "ev":
            round_trip_miles = daily_miles * 2
            daily_electricity_cost = (round_trip_miles / ev_efficiency) * electricity_price if ev_efficiency > 0 else 0
            daily_commute_cost += daily_electricity_cost
            cost_breakdown = f"Electricity: ${daily_electricity_cost:.2f}"
            
        elif transport_type == "public":
            if use_monthly_pass:
                monthly_pass = public_monthly_cost
                daily_transport_cost = monthly_pass / (commute_days * 4.33)
            else:
                daily_transport_cost = public_daily_cost
            daily_commute_cost += daily_transport_cost
            cost_breakdown = f"Transport: ${daily_transport_cost:.2f}"
        
        elif transport_type in ["biking", "walking"]:
            cost_breakdown = "No fuel/transportation costs"
            if daily_costs > 0:
                cost_breakdown = f"Gear/Maintenance: ${daily_costs:.2f}"
        
        # account for WFH days
        weekly_commute_hours = daily_commute_hours * commute_days
        weekly_commute_costs = daily_commute_cost * commute_days
        
        work_weeks_per_year = 50
        yearly_commute_hours = weekly_commute_hours * work_weeks_per_year
        yearly_commute_costs = weekly_commute_costs * work_weeks_per_year
        
        return {
            'daily_commute_hours': daily_commute_hours,
            'daily_commute_cost': daily_commute_cost,
            'yearly_commute_hours': yearly_commute_hours,
            'yearly_commute_costs': yearly_commute_costs,
            'cost_breakdown': cost_breakdown,
            'commute_days': commute_days
        }
    
    def calculate(self):
        try:
            paycheck = self.paycheck_var.get()
            daily_hours = self.daily_hours_var.get()
            work_days = self.work_days_var.get()
            wfh_days = self.wfh_days_var.get()
            
            if wfh_days > work_days:
                messagebox.showerror("Input Error", "WFH days cannot exceed work days per week")
                return
            
            pay_freq = self.pay_frequency.get()
            if pay_freq == 'daily':
                annual_income = paycheck * work_days * 50
            elif pay_freq == 'weekly':
                annual_income = paycheck * 50
            elif pay_freq == 'biweekly':
                annual_income = paycheck * 26
            elif pay_freq == 'semi_monthly':
                annual_income = paycheck * 24
            else:
                annual_income = paycheck * 12
            
            metrics = self.calculate_commute_metrics(
                self.transport_type.get(), self.commute_minutes_var.get(), self.daily_miles_var.get(),
                self.gas_price_var.get(), self.mpg_var.get(), self.ev_efficiency_var.get(),
                self.electricity_price_var.get(), self.public_daily_cost_var.get(),
                self.public_monthly_cost_var.get(), self.public_walking_minutes_var.get(),
                self.use_monthly_pass.get(), self.daily_costs_var.get()
            )
            
            weekly_work_hours = daily_hours * work_days
            work_weeks_per_year = 50
            yearly_work_hours = weekly_work_hours * work_weeks_per_year
            
            traditional_wage = annual_income / yearly_work_hours if yearly_work_hours > 0 else 0
            net_yearly_income = annual_income - metrics['yearly_commute_costs']
            total_committed_hours = yearly_work_hours + metrics['yearly_commute_hours']
            true_wage = net_yearly_income / total_committed_hours if total_committed_hours > 0 else 0
            
            self.results = {
                'traditional_wage': traditional_wage,
                'true_wage': true_wage,
                'annual_income': annual_income,
                'yearly_commute_costs': metrics['yearly_commute_costs'],
                'net_yearly_income': net_yearly_income,
                'yearly_work_hours': yearly_work_hours,
                'yearly_commute_hours': metrics['yearly_commute_hours'],
                'total_committed_hours': total_committed_hours,
                'daily_commute_cost': metrics['daily_commute_cost'],
                'daily_commute_hours': metrics['daily_commute_hours'],
                'cost_breakdown': metrics['cost_breakdown'],
                'transport_type': self.transport_type.get(),
                'daily_miles': self.daily_miles_var.get(),
                'commute_days': metrics['commute_days'],
                'wfh_days': wfh_days
            }
            
            self.notebook.select(1)
            self.display_results()
            
            # auto-sync comparison values
            self.sync_comparison_values()
            
        except Exception as e:
            messagebox.showerror("Calculation Error", f"An error occurred: {str(e)}")
    
    def compare_commutes(self):
        try:
            if not hasattr(self, 'results'):
                messagebox.showinfo("Calculate First", "Please calculate your current commute first in the Calculator tab")
                return
            
            # calculate alternative commute
            alt_metrics = self.calculate_commute_metrics(
                self.comp_transport_type.get(), self.comp_commute_minutes_var.get(), 
                self.comp_daily_miles_var.get(), self.comp_gas_price_var.get(), self.comp_mpg_var.get(),
                self.comp_ev_efficiency_var.get(), self.comp_electricity_price_var.get(),
                self.comp_public_daily_cost_var.get(), self.comp_public_monthly_cost_var.get(),
                self.comp_public_walking_minutes_var.get(), self.comp_use_monthly_pass.get(),
                self.comp_daily_costs_var.get()
            )
            
            # clear previous results
            for widget in self.comparison_results_frame.winfo_children():
                widget.destroy()
            
            # display comparison
            ttk.Label(self.comparison_results_frame, text="Comparison Results", 
                     font=self.heading_font).pack(pady=20)
            
            # create comparison table
            comparison_frame = ttk.Frame(self.comparison_results_frame)
            comparison_frame.pack(fill='x', padx=20, pady=10)
            
            headers = ["Metric", "Current Commute", "Alternative Commute", "Difference"]
            for col, header in enumerate(headers):
                ttk.Label(comparison_frame, text=header, font=self.subheading_font).grid(
                    row=0, column=col, padx=10, pady=10, sticky='w')
            
            # comparison metrics
            current = self.results
            alt_annual_income = current['annual_income']
            alt_net_income = alt_annual_income - alt_metrics['yearly_commute_costs']
            alt_total_hours = current['yearly_work_hours'] + alt_metrics['yearly_commute_hours']
            alt_true_wage = alt_net_income / alt_total_hours if alt_total_hours > 0 else 0
            
            comparisons = [
                ("Daily Commute Time", f"{current['daily_commute_hours']:.1f} hrs", 
                 f"{alt_metrics['daily_commute_hours']:.1f} hrs",
                 f"{current['daily_commute_hours'] - alt_metrics['daily_commute_hours']:+.1f} hrs"),
                ("Daily Commute Cost", f"${current['daily_commute_cost']:.2f}",
                 f"${alt_metrics['daily_commute_cost']:.2f}",
                 f"${current['daily_commute_cost'] - alt_metrics['daily_commute_cost']:+.2f}"),
                ("Yearly Commute Hours", f"{current['yearly_commute_hours']:.0f} hrs",
                 f"{alt_metrics['yearly_commute_hours']:.0f} hrs",
                 f"{current['yearly_commute_hours'] - alt_metrics['yearly_commute_hours']:+.0f} hrs"),
                ("Yearly Commute Costs", f"${current['yearly_commute_costs']:,.2f}",
                 f"${alt_metrics['yearly_commute_costs']:,.2f}",
                 f"${current['yearly_commute_costs'] - alt_metrics['yearly_commute_costs']:+,.2f}"),
                ("True Hourly Wage", f"${current['true_wage']:.2f}",
                 f"${alt_true_wage:.2f}",
                 f"${alt_true_wage - current['true_wage']:+.2f}")
            ]
            
            for row, (metric, curr, alt, diff) in enumerate(comparisons, start=1):
                ttk.Label(comparison_frame, text=metric, font=self.detail_font).grid(
                    row=row, column=0, padx=10, pady=5, sticky='w')
                ttk.Label(comparison_frame, text=curr, font=self.detail_font).grid(
                    row=row, column=1, padx=10, pady=5, sticky='w')
                ttk.Label(comparison_frame, text=alt, font=self.detail_font).grid(
                    row=row, column=2, padx=10, pady=5, sticky='w')
                
                # color code difference
                color = '#27ae60' if '-' not in diff or diff.startswith('$+') or diff.endswith('+.2f}') else '#c0392b'
                if metric == "True Hourly Wage":
                    color = '#27ae60' if '+' in diff else '#c0392b'
                ttk.Label(comparison_frame, text=diff, font=self.detail_font, foreground=color).grid(
                    row=row, column=3, padx=10, pady=5, sticky='w')
            
            # visualization
            self.create_comparison_visualization(current, alt_metrics, alt_true_wage)
            
        except Exception as e:
            messagebox.showerror("Comparison Error", f"An error occurred: {str(e)}")
    
    def create_comparison_visualization(self, current, alt_metrics, alt_true_wage):
        vis_frame = ttk.LabelFrame(self.comparison_results_frame, text="Visual Comparison", padding=15)
        vis_frame.pack(fill='x', padx=20, pady=20)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.patch.set_facecolor('#f0f0f0')
        
        # wage comparison
        labels = ['Current\nTrue Wage', 'Alternative\nTrue Wage']
        values = [current['true_wage'], alt_true_wage]
        colors = ['#3498db', '#27ae60']
        
        bars = ax1.bar(labels, values, color=colors)
        ax1.set_ylabel('True Hourly Wage ($)', fontsize=11)
        ax1.set_title('True Wage Comparison', fontsize=12, fontweight='bold')
        
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'${value:.2f}', ha='center', va='bottom', fontsize=10)
        
        # yearly cost comparison
        x = np.arange(2)
        width = 0.35
        
        current_costs = current['yearly_commute_costs']
        alt_costs = alt_metrics['yearly_commute_costs']
        
        ax2.bar(x[0], current_costs, width, label='Current', color='#e74c3c')
        ax2.bar(x[1], alt_costs, width, label='Alternative', color='#2ecc71')
        
        ax2.set_ylabel('Yearly Commute Costs ($)', fontsize=11)
        ax2.set_title('Annual Commute Cost Comparison', fontsize=12, fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(['Current', 'Alternative'])
        ax2.legend()
        
        for i, (cost, label) in enumerate([(current_costs, 'Current'), (alt_costs, 'Alternative')]):
            ax2.text(i, cost + 100, f'${cost:,.0f}', ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=vis_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def display_results(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        r = self.results
    
        header_frame = ttk.Frame(self.scrollable_frame)
        header_frame.pack(fill='x', padx=20, pady=20)
        
        # wage comparison
        wage_frame = ttk.LabelFrame(self.scrollable_frame, text="Wage Analysis", padding=15)
        wage_frame.pack(fill='x', padx=20, pady=10)

        wage_frame.grid_columnconfigure(0, weight=1)
        wage_frame.grid_columnconfigure(1, weight=1)
        wage_frame.grid_columnconfigure(2, weight=1)

        ttk.Label(wage_frame, text="Traditional Hourly Wage:", 
                font=self.heading_font).grid(row=0, column=0, sticky='w', padx=10, pady=5)
        ttk.Label(wage_frame, text=f"${r['traditional_wage']:.2f}", 
                font=self.heading_font, foreground='#2c3e50').grid(row=1, column=0, sticky='w', padx=10, pady=5)

        diff = r['traditional_wage'] - r['true_wage']
        ttk.Label(wage_frame, text="Difference:", 
                font=self.heading_font).grid(row=0, column=1, sticky='w', padx=10, pady=5)
        ttk.Label(wage_frame, text=f"${diff:.2f} per hour", 
                font=self.heading_font).grid(row=1, column=1, sticky='w', padx=10, pady=5)

        ttk.Label(wage_frame, text="True Hourly Wage:", 
                font=self.heading_font).grid(row=0, column=2, sticky='w', padx=10, pady=5)
        ttk.Label(wage_frame, text=f"${r['true_wage']:.2f}", 
                font=self.heading_font, foreground='#27ae60').grid(row=1, column=2, sticky='w', padx=10, pady=5)

        if diff > 0:
            ttk.Label(wage_frame, 
                    text=f"Commute reduces wage by ${diff:.2f}/hr",
                    font=self.subheading_font, foreground='#c0392b').grid(row=2, column=0, columnspan=3, sticky='w', padx=10, pady=(10, 0))
        
        # time breakdown
        time_frame = ttk.LabelFrame(self.scrollable_frame, text="Time Breakdown", padding=15)
        time_frame.pack(fill='x', padx=20, pady=10)
        
        metrics = [
            ("Daily Work Hours", f"{self.daily_hours_var.get():.1f} hrs"),
            ("Daily Commute Time", f"{r['daily_commute_hours']:.1f} hrs"),
            ("Commute Days per Week", f"{r['commute_days']:.0f} days"),
            ("WFH Days per Week", f"{r['wfh_days']:.0f} days"),
            ("Weekly Work Hours", f"{self.daily_hours_var.get() * self.work_days_var.get():.1f} hrs"),
            ("Weekly Commute Hours", f"{r['daily_commute_hours'] * r['commute_days']:.1f} hrs"),
            ("Yearly Work Hours", f"{r['yearly_work_hours']:.0f} hrs"),
            ("Yearly Commute Hours", f"{r['yearly_commute_hours']:.0f} hrs"),
            ("Total Committed Hours/Year", f"{r['total_committed_hours']:.0f} hrs")
        ]
        
        for i, (label, value) in enumerate(metrics):
            row = i // 2
            col = (i % 2) * 2
            
            ttk.Label(time_frame, text=label, font=self.detail_font).grid(row=row, column=col, 
                                                                      sticky='w', padx=10, pady=5)
            ttk.Label(time_frame, text=value, font=self.detail_font).grid(row=row, 
                                                                              column=col+1, 
                                                                              sticky='w', 
                                                                              padx=10, pady=5)
        
        # cost breakdown
        cost_frame = ttk.LabelFrame(self.scrollable_frame, text="Cost Breakdown", padding=15)
        cost_frame.pack(fill='x', padx=20, pady=10)
        
        transport_names = {
            'car': 'Car (Gas)',
            'ev': 'Electric Vehicle',
            'public': 'Public Transport',
            'biking': 'Biking',
            'walking': 'Walking'
        }
        
        ttk.Label(cost_frame, text=f"Transportation: {transport_names.get(r['transport_type'], r['transport_type'])}",
                 font=self.detail_font).pack(anchor='w', pady=5)
        
        if r['transport_type'] in ['car', 'ev', 'biking', 'walking']:
            ttk.Label(cost_frame, text=f"Round Trip Distance: {r['daily_miles'] * 2:.1f} miles",
                     font=self.detail_font).pack(anchor='w', pady=2)
        
        ttk.Label(cost_frame, text=f"Daily Cost Breakdown: {r['cost_breakdown']}",
                 font=self.detail_font).pack(anchor='w', pady=2)
        
        if self.daily_costs_var.get() > 0 and r['transport_type'] not in ['biking', 'walking']:
            ttk.Label(cost_frame, text=f"+ Additional Costs: ${self.daily_costs_var.get():.2f}",
                     font=self.detail_font).pack(anchor='w', pady=2)
        
        ttk.Label(cost_frame, text=f"Total Daily Commute Cost: ${r['daily_commute_cost']:.2f}",
                 font=self.detail_font).pack(anchor='w', pady=5)
        
        yearly_cost_frame = ttk.Frame(cost_frame)
        yearly_cost_frame.pack(fill='x', pady=10)
        
        ttk.Label(yearly_cost_frame, text="Yearly Take-home Pay:", 
                 font=self.detail_font).pack(side='left', padx=20)
        ttk.Label(yearly_cost_frame, text=f"${r['annual_income']:,.2f}", 
                 font=self.detail_font).pack(side='left', padx=10)
        
        ttk.Label(yearly_cost_frame, text="Yearly Commute Costs:", 
                 font=self.detail_font).pack(side='left', padx=20)
        ttk.Label(yearly_cost_frame, text=f"${r['yearly_commute_costs']:,.2f}", 
                 font=self.detail_font, foreground='#c0392b').pack(side='left', padx=10)
        
        ttk.Label(yearly_cost_frame, text="Net Yearly Income:", 
                 font=self.detail_font).pack(side='left', padx=20)
        ttk.Label(yearly_cost_frame, text=f"${r['net_yearly_income']:,.2f}", 
                 font=self.detail_font, foreground='#27ae60').pack(side='left', padx=10)
        
        if r['annual_income'] > 0:
            cost_percentage = (r['yearly_commute_costs'] / r['annual_income']) * 100
            ttk.Label(cost_frame, 
                     text=f"Commute costs consume {cost_percentage:.1f}% of your take-home pay",
                     font=self.detail_font).pack(anchor='w', pady=5)
        
        # paycheck perspective
        paycheck_frame = ttk.LabelFrame(self.scrollable_frame, text="Paycheck Perspective", padding=15)
        paycheck_frame.pack(fill='x', padx=20, pady=10)
        
        pay_freq = self.pay_frequency.get()
        paycheck = self.paycheck_var.get()
        
        if pay_freq == 'biweekly':
            biweekly_commute_cost = r['daily_commute_cost'] * r['commute_days'] * 2
            biweekly_commute_hours = r['daily_commute_hours'] * r['commute_days'] * 2
            percentage = (biweekly_commute_cost / paycheck) * 100 if paycheck > 0 else 0
            
            ttk.Label(paycheck_frame, text="Per Bi-weekly Paycheck:", 
                     font=self.detail_font).pack(anchor='w', pady=5)
            
            ttk.Label(paycheck_frame, 
                     text=f"Take-home: ${paycheck:.2f} | Commute costs: ${biweekly_commute_cost:.2f} | Effective: ${paycheck - biweekly_commute_cost:.2f}",
                     font=self.detail_font).pack(anchor='w', pady=2)
            
            ttk.Label(paycheck_frame, 
                     text=f"Commute time: {biweekly_commute_hours:.1f} hours | Commute eats {percentage:.1f}% of your paycheck",
                     font=self.detail_font).pack(anchor='w', pady=2)
        
        self.create_visualization()
        ttk.Button(self.scrollable_frame, text="← Back to Calculator", 
                  command=lambda: self.notebook.select(0)).pack(pady=20)
    
    def create_visualization(self):
        vis_frame = ttk.LabelFrame(self.scrollable_frame, text="Wage Comparison", padding=15)
        vis_frame.pack(fill='x', padx=20, pady=10)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))
        fig.patch.set_facecolor('#f0f0f0')
        
        labels = ['Traditional Wage', 'True Hourly Wage']
        values = [self.results['traditional_wage'], self.results['true_wage']]
        colors = ['#3498db', '#27ae60']
        
        bars = ax1.bar(labels, values, color=colors)
        ax1.set_ylabel('Hourly Wage ($)')
        ax1.set_title('Wage Comparison')
        
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'${value:.2f}', ha='center', va='bottom')
        
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
    style.configure('Accent.TButton', font=('Segoe UI', 12, 'bold'))  
    style.map('Accent.TButton', background=[('active', '#2980b9'), ('pressed', '#1c638e')])
    
    app = TrueHourlyWageCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()