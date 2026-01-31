def validate_input(prompt, input_type=float, min_value=None, max_value=None, allow_zero=False):
    """Validate user input with optional range checking"""
    while True:
        try:
            value = input_type(input(prompt))
            
            if min_value is not None and value < min_value:
                print(f"Value must be at least {min_value}")
                continue
                
            if max_value is not None and value > max_value:
                print(f"Value must be at most {max_value}")
                continue
                
            if not allow_zero and value == 0:
                print("Value cannot be zero")
                continue
                
            return value
            
        except ValueError:
            print(f"Please enter a valid {input_type.__name__}")


def calculate_true_hourly_wage():
    """Calculate true hourly wage - one time calculation"""
    print("\n" + "="*60)
    print("TRUE HOURLY WAGE CALCULATOR")
    print("="*60)
    print("\nCalculate your actual hourly wage including commute time and costs")
    
    print("\n--- Pay Information ---")
    print("How often do you get paid?")
    print("1. Daily")
    print("2. Weekly")
    print("3. Bi-weekly")
    print("4. Semi-monthly*")
    print("5. Monthly")
    
    pay_frequency_choice = input("\nEnter choice (1-5): ")
    pay_frequency_map = {
        '1': 'daily', '2': 'weekly', '3': 'biweekly', 
        '4': 'semi_monthly', '5': 'monthly'
    }
    pay_frequency = pay_frequency_map.get(pay_frequency_choice, 'biweekly')
    
    paycheck_amount = validate_input("Enter your take-home paycheck amount: $", float, min_value=0.01)
    
    # Time inputs with sensible checks
    print("\n--- Work Schedule ---")
    daily_work_hours = validate_input("Daily work hours: ", float, min_value=0.1, max_value=24)
    work_days_per_week = validate_input("Number of days in week worked: ", float, min_value=0.1, max_value=7)
    
    print("\n--- Commute Details ---")
    # Check: minutes per day should be reasonable
    daily_commute_minutes = validate_input("One-way commute time in minutes: ", float, min_value=0, max_value=1440)
    
    # Convert minutes to hours for sanity check
    daily_commute_hours_one_way = daily_commute_minutes / 60
    if daily_commute_hours_one_way > 24:
        print(f"Warning: Your one-way commute of {daily_commute_hours_one_way:.1f} hours seems unrealistic!")
        proceed = input("Do you want to continue anyway? (yes/no): ").lower()
        if proceed != 'yes':
            daily_commute_minutes = validate_input("Your one-way commute time in minutes: ", float, min_value=0, max_value=1440)
    
    # TRANSPORTATION TYPE SELECTION
    print("\n--- Transportation Type ---")
    print("Select your transportation type:")
    print("1. Driving (Gasoline)")
    print("2. Public Transportation")
    print("3. Electric Vehicle (EV)")
    print("4. Biking")
    print("5. Walking")
    
    transport_choice = input("Enter choice: ")
    
    # Initialize variables for all transport types
    transport_type = ""
    daily_commute_miles = 0
    gas_mileage = 0
    gas_price = 0
    ev_efficiency = 0
    electricity_price = 0
    daily_public_transport_cost = 0
    monthly_pass_cost = 0
    
    if transport_choice == '2':  # Public Transport
        transport_type = "public_transport"
        print("\n--- Public Transport Details ---")
        print("Enter your public transport costs:")
        print("Option A: Daily cost")
        print("Option B: Monthly pass")
        cost_choice = input("Choose option (A or B): ").upper()
        
        if cost_choice == 'A':
            daily_public_transport_cost = validate_input(
                "Daily round-trip cost for public transport: $", 
                float, min_value=0
            )
            # No need for monthly pass cost
        else:
            monthly_pass_cost = validate_input(
                "Monthly pass cost: $", 
                float, min_value=0
            )
            # Calculate daily cost from monthly pass
            daily_public_transport_cost = monthly_pass_cost / (work_days_per_week * 4.33)  # Average weeks per month
        
        print("\n--- Additional Public Transport Details ---")
        daily_walking_minutes = validate_input(
            "Daily walking time to/from stations/stops (minutes): ", 
            float, min_value=0
        )
        # Add walking time to commute time
        daily_commute_minutes += daily_walking_minutes
        
    elif transport_choice == '3':  # EV
        transport_type = "ev"
        print("\n--- EV Details ---")
        daily_commute_miles = validate_input("One-way commute distance in miles: ", float, min_value=0)
        ev_efficiency = validate_input("EV efficiency (miles per kWh): ", float, min_value=0.1)
        electricity_price = validate_input("Electricity price ($ per kWh): $", float, min_value=0.01)
    
    elif transport_choice == '4':  # Biking
        transport_type = "biking"
        print("\n--- Biking Details ---")
        daily_commute_miles = validate_input("One-way commute distance in miles: ", float, min_value=0)
        
    elif transport_choice == '5':  # Walking
        transport_type = "walking"
        print("\n--- Walking Details ---")
        daily_commute_miles = validate_input("One-way commute distance in miles: ", float, min_value=0)
        
    else:
        transport_type = "car"
        print("\n--- Car Details ---")
        daily_commute_miles = validate_input("One-way commute distance in miles: ", float, min_value=0)
        gas_mileage = validate_input("Car's MPG: ", float, min_value=0.1)
        gas_price = validate_input("Gas price per gallon: $", float, min_value=0.01)
    
    # additional costs
    print("\n--- Additional Commuting Costs ---")
    if transport_type in ["biking", "walking"]:
        print("Additional daily commuting costs (maintenance, etc.)")
    else:
        print("Additional daily commuting costs (tolls, etc.)")
    daily_other_costs = validate_input("Additional daily commuting costs: $", float, min_value=0, allow_zero=True)
    
    # Calculate annual income based on pay frequency
    print("\n" + "="*60)
    
    if pay_frequency == 'daily':
        annual_income = paycheck_amount * work_days_per_week * 50
        pay_description = f"${paycheck_amount:.2f} per day"
    elif pay_frequency == 'weekly':
        annual_income = paycheck_amount * 50
        pay_description = f"${paycheck_amount:.2f} per week"
    elif pay_frequency == 'biweekly':
        annual_income = paycheck_amount * 26
        pay_description = f"${paycheck_amount:.2f} bi-weekly"
    elif pay_frequency == 'semi_monthly':
        annual_income = paycheck_amount * 24
        pay_description = f"${paycheck_amount:.2f} semi-monthly"
    else:  # monthly
        annual_income = paycheck_amount * 12
        pay_description = f"${paycheck_amount:.2f} per month"
    
    # Calculate commute costs and time
    daily_commute_hours = (daily_commute_minutes * 2) / 60  # Round trip
    
    # Calculate daily commute costs based on transport type
    daily_commute_cost = 0
    cost_details = ""
    
    if transport_type == "car":
        round_trip_miles = daily_commute_miles * 2
        if gas_mileage > 0:
            daily_fuel_cost = (round_trip_miles / gas_mileage) * gas_price
        daily_commute_cost = daily_fuel_cost + daily_other_costs
        cost_details = f"Fuel: ${daily_fuel_cost:.2f}"
        if daily_other_costs > 0:
            cost_details += f" + Other: ${daily_other_costs:.2f}"
        
    elif transport_type == "ev":
        round_trip_miles = daily_commute_miles * 2
        if ev_efficiency > 0:
            daily_electricity_cost = (round_trip_miles / ev_efficiency) * electricity_price
        daily_commute_cost = daily_electricity_cost + daily_other_costs
        cost_details = f"Electricity: ${daily_electricity_cost:.2f}"
        if daily_other_costs > 0:
            cost_details += f" + Other: ${daily_other_costs:.2f}"
        
    elif transport_type == "public_transport":
        daily_commute_cost = daily_public_transport_cost + daily_other_costs
        cost_details = f"Transport fare: ${daily_public_transport_cost:.2f}"
        if monthly_pass_cost > 0:
            cost_details += f" (from ${monthly_pass_cost:.2f}/month pass)"
        if daily_other_costs > 0:
            cost_details += f" + Other: ${daily_other_costs:.2f}"
    
    elif transport_type == "biking":
        daily_commute_cost = daily_other_costs
        cost_details = "No fuel/transportation costs"
        if daily_other_costs > 0:
            cost_details = f"Maintenance/gear: ${daily_other_costs:.2f}"
    
    elif transport_type == "walking":
        daily_commute_cost = daily_other_costs
        cost_details = "No fuel/transportation costs"
        if daily_other_costs > 0:
            cost_details = f"Gear/other: ${daily_other_costs:.2f}"
    
    # Yearly calculations
    weekly_work_hours = daily_work_hours * work_days_per_week
    weekly_commute_hours = daily_commute_hours * work_days_per_week
    weekly_commute_costs = daily_commute_cost * work_days_per_week
    
    work_weeks_per_year = 50
    yearly_work_hours = weekly_work_hours * work_weeks_per_year
    yearly_commute_hours = weekly_commute_hours * work_weeks_per_year
    yearly_commute_costs = weekly_commute_costs * work_weeks_per_year
    
    # Wage calculations
    if yearly_work_hours > 0:
        traditional_wage = annual_income / yearly_work_hours
    else:
        traditional_wage = 0
    
    net_yearly_income = annual_income - yearly_commute_costs
    total_committed_hours = yearly_work_hours + yearly_commute_hours
    
    if total_committed_hours > 0:
        true_wage = net_yearly_income / total_committed_hours
    else:
        true_wage = 0
    
    # Display results
    print("\n" + "="*60)
    print("RESULTS")
    print("="*60)
    print(f"Pay Frequency: {pay_description}")
    
    # Display transport type
    if transport_type == "car":
        print(f"Transportation: Driving (Gas Vehicle)")
    elif transport_type == "ev":
        print(f"Transportation: Electric Vehicle")
    elif transport_type == "public_transport":
        print(f"Transportation: Public Transport")
    elif transport_type == "biking":
        print(f"Transportation: Biking")
    elif transport_type == "walking":
        print(f"Transportation: Walking")
    
    print(f"\n" + "-"*60)
    print("WAGE ANALYSIS")
    print("-"*60)
    print(f"Traditional hourly wage: ${traditional_wage:.2f}")
    print(f"True hourly wage: ${true_wage:.2f}")
    print(f"Difference: ${traditional_wage - true_wage:.2f}")
    
    print(f"\n" + "-"*60)
    print("TIME BREAKDOWN")
    print("-"*60)
    print(f"Work hours per day: {daily_work_hours} hours")
    print(f"Work days per week: {work_days_per_week} days")
    print(f"Daily commute time: {daily_commute_hours:.1f} hours ({daily_commute_minutes*2:.0f} min total)")
    print(f"Weekly work hours: {weekly_work_hours:.1f} hours")
    print(f"Weekly commute hours: {weekly_commute_hours:.1f} hours")
    print(f"Yearly work hours: {yearly_work_hours:.0f} hours")
    print(f"Yearly commute hours: {yearly_commute_hours:.0f} hours")
    print(f"Total committed time per year: {total_committed_hours:.0f} hours")
    
    print(f"\n" + "-"*60)
    print("COST BREAKDOWN")
    print("-"*60)
    
    if transport_type in ["car", "ev", "biking", "walking"]:
        round_trip_miles = daily_commute_miles * 2
        print(f"Round trip distance: {round_trip_miles:.1f} miles")
        
        if transport_type == "car":
            print(f"Vehicle efficiency: {gas_mileage:.1f} MPG")
            print(f"Gas price: ${gas_price:.2f} per gallon")
        elif transport_type == "ev":
            print(f"Vehicle efficiency: {ev_efficiency:.1f} mi/kWh")
            print(f"Electricity price: ${electricity_price:.2f} per kWh")
    
    print(f"Daily commute cost breakdown: {cost_details}")
    print(f"Total daily commute cost: ${daily_commute_cost:.2f}")
    print(f"Yearly commute cost: ${yearly_commute_costs:,.2f}")
    print(f"Yearly take-home pay: ${annual_income:,.2f}")
    print(f"Yearly disposable income (after commute): ${net_yearly_income:,.2f}")
    
    if annual_income > 0:
        cost_percentage = (yearly_commute_costs / annual_income) * 100
        print(f"\nCommute costs consume {cost_percentage:.1f}% of your take-home pay")
    
    # Per paycheck perspective for common frequencies
    print(f"\n" + "-"*60)
    print("PAYCHECK PERSPECTIVE")
    print("-"*60)
    
    if pay_frequency == 'biweekly':
        biweekly_commute_cost = daily_commute_cost * work_days_per_week * 2
        biweekly_commute_hours = daily_commute_hours * work_days_per_week * 2
        print(f"Per Bi-weekly Paycheck:")
        print(f"  Take-home: ${paycheck_amount:.2f}")
        print(f"  Commute costs: ${biweekly_commute_cost:.2f}")
        print(f"  Commute time: {biweekly_commute_hours:.1f} hours")
        print(f"  Effective take-home: ${paycheck_amount - biweekly_commute_cost:.2f}")
        print(f"  Commute eats {biweekly_commute_cost/paycheck_amount*100:.1f}% of your paycheck")
    
    elif pay_frequency == 'weekly':
        weekly_commute_cost = daily_commute_cost * work_days_per_week
        weekly_commute_hours = daily_commute_hours * work_days_per_week
        print(f"Per Weekly Paycheck:")
        print(f"  Take-home: ${paycheck_amount:.2f}")
        print(f"  Commute costs: ${weekly_commute_cost:.2f}")
        print(f"  Effective take-home: ${paycheck_amount - weekly_commute_cost:.2f}")
    
    print(f"\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Your true hourly wage is ${true_wage:.2f}, which is ${traditional_wage - true_wage:.2f}")
    print(f"less than your traditional wage of ${traditional_wage:.2f}.")
    
    if true_wage < traditional_wage:
        print(f"\nYour commute reduces your effective wage by:")
        print(f"  ${(traditional_wage - true_wage):.2f} per hour")
        print(f"  ${(traditional_wage - true_wage) * yearly_work_hours:,.2f} per year")
    
    return true_wage


def main():
    """Main program"""
    print("Calculate your actual hourly wage including commute time and costs")
    
    while True:
        try:
            # Run the calculator
            calculate_true_hourly_wage()
            
            # Ask if user wants to calculate again
            print("\n" + "="*60)
            again = input("\nCalculate again? (yes/no): ").lower()
            
            if again != 'yes':
                break
                
        except KeyboardInterrupt:
            print("\n\nProgram interrupted")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()