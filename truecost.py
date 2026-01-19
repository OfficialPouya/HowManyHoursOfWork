import sqlite3
from datetime import datetime
import json
from dataclasses import dataclass
from typing import Optional

@dataclass
class CompensationData:
    name: str
    salary: float
    rsu: float
    match_401k: float
    bonus_percent: float
    commute_time_minutes: float
    commute_distance_miles: float
    car_type: str
    fuel_cost: float
    car_cost: float
    car_mileage: float
    daily_hours: float
    gas_mileage: Optional[float] = None
    electric_efficiency: Optional[float] = None

class CompensationAnalyzer:
    def __init__(self, db_name="compensation_data.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Main compensation data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS compensation_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                salary REAL NOT NULL,
                rsu REAL NOT NULL,
                match_401k REAL NOT NULL,
                bonus_percent REAL NOT NULL,
                commute_time_minutes REAL NOT NULL,
                commute_distance_miles REAL NOT NULL,
                car_type TEXT NOT NULL,
                fuel_cost REAL NOT NULL,
                car_cost REAL NOT NULL,
                car_mileage REAL NOT NULL,
                daily_hours REAL NOT NULL,
                gas_mileage REAL,
                electric_efficiency REAL,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                real_hourly_wage REAL
            )
        ''')
        
        # Monthly calculations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monthly_calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id INTEGER,
                month_year TEXT,
                total_compensation REAL,
                commute_cost REAL,
                work_hours REAL,
                real_hourly_wage REAL,
                FOREIGN KEY (record_id) REFERENCES compensation_records (id)
            )
        ''')
        
        self.conn.commit()
    
    def get_user_input(self):
        print("=== Compensation Analysis Tool ===")
        print()
        
        name = input("1. Enter your name: ").strip()
        
        salary = float(input("2. Enter your annual salary ($): "))
        rsu = float(input("3. Enter your RSU value (annual $): "))
        match_401k = float(input("4. Enter 401k match percentage (e.g., 4 for 4%): "))
        bonus_percent = float(input("5. Enter bonus percentage (e.g., 10 for 10%): "))
        
        commute_time_minutes = float(input("6. Enter average daily commute time (minutes): "))
        commute_distance_miles = float(input("7. Enter average daily commute distance (miles): "))
        
        print()
        print("8. Car Type:")
        print("   g - Gas car")
        print("   e - Electric car")
        car_type = input("   Enter your choice (g/e): ").strip().lower()
        
        if car_type == 'g':
            car_type = 'gas'
            fuel_cost = float(input("   Enter average gas price per gallon ($): "))
            gas_mileage = float(input("   Enter your car's gas mileage (miles per gallon): "))
            electric_efficiency = None
        else:
            car_type = 'electric'
            fuel_cost = float(input("   Enter average electricity cost per kWh ($): "))
            electric_efficiency = float(input("   Enter your car's efficiency (miles per kWh): "))
            gas_mileage = None
        
        car_cost_input = input("9. Enter car cost with mileage (format: 'cost,mileage' e.g., '30000,15000'): ")
        car_cost, car_mileage_total = map(float, car_cost_input.split(','))
        
        daily_hours = float(input("10. Enter average hours worked per day: "))
        
        return CompensationData(
            name=name,
            salary=salary,
            rsu=rsu,
            match_401k=match_401k,
            bonus_percent=bonus_percent,
            commute_time_minutes=commute_time_minutes,
            commute_distance_miles=commute_distance_miles,
            car_type=car_type,
            fuel_cost=fuel_cost,
            car_cost=car_cost,
            car_mileage=car_mileage_total,
            daily_hours=daily_hours,
            gas_mileage=gas_mileage,
            electric_efficiency=electric_efficiency
        )
    
    def calculate_commute_cost(self, data: CompensationData, work_days_per_year=260):
        # calc daily commute cost
        daily_distance = data.commute_distance_miles * 2  # round trip
        
        if data.car_type == 'gas':
            # gas car calculation
            daily_gallons = daily_distance / data.gas_mileage
            daily_fuel_cost = daily_gallons * data.fuel_cost
        else:
            # elec car calculation
            daily_kwh = daily_distance / data.electric_efficiency
            daily_fuel_cost = daily_kwh * data.fuel_cost
        
        # add car depreciation
        cost_per_mile = data.car_cost / data.car_mileage
        daily_depreciation = daily_distance * cost_per_mile
        
        daily_total = daily_fuel_cost + daily_depreciation
        annual_commute_cost = daily_total * work_days_per_year
        
        return {
            'daily_fuel': daily_fuel_cost,
            'daily_depreciation': daily_depreciation,
            'daily_total': daily_total,
            'annual_total': annual_commute_cost
        }
    
    def calculate_real_hourly_wage(self, data: CompensationData):
        # standard work parameters
        work_days_per_year = 260  # 52 weeks * 5 days
        weeks_per_year = 52
        
        # calc total annual compensation
        bonus_amount = data.salary * (data.bonus_percent / 100)
        match_401k_amount = data.salary * (data.match_401k / 100)
        total_compensation = data.salary + data.rsu + bonus_amount + match_401k_amount
        
        # calc commute costs
        commute_costs = self.calculate_commute_cost(data, work_days_per_year)
        annual_commute_cost = commute_costs['annual_total']
        
        # total work time (including commute)
        daily_commute_hours = data.commute_time_minutes * 2 / 60  # Round trip in hours
        total_daily_hours = data.daily_hours + daily_commute_hours
        annual_work_hours = total_daily_hours * work_days_per_year
        
        net_compensation = total_compensation - annual_commute_cost
        real_hourly_wage = net_compensation / annual_work_hours
        
        return {
            'total_compensation': total_compensation,
            'net_compensation': net_compensation,
            'annual_commute_cost': annual_commute_cost,
            'annual_work_hours': annual_work_hours,
            'real_hourly_wage': real_hourly_wage,
            'commute_costs': commute_costs,
            'bonus_amount': bonus_amount,
            'match_401k_amount': match_401k_amount
        }
    
    def save_to_database(self, data: CompensationData, calculations: dict):
        cursor = self.conn.cursor()
        
        # Insert main record
        cursor.execute('''
            INSERT INTO compensation_records 
            (name, salary, rsu, match_401k, bonus_percent, commute_time_minutes, 
             commute_distance_miles, car_type, fuel_cost, car_cost, car_mileage, 
             daily_hours, gas_mileage, electric_efficiency, real_hourly_wage)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.name, data.salary, data.rsu, data.match_401k, data.bonus_percent,
            data.commute_time_minutes, data.commute_distance_miles, data.car_type,
            data.fuel_cost, data.car_cost, data.car_mileage, data.daily_hours,
            data.gas_mileage, data.electric_efficiency, calculations['real_hourly_wage']
        ))
        
        record_id = cursor.lastrowid
        
        # Insert monthly calculation (current month)
        current_month = datetime.now().strftime("%Y-%m")
        cursor.execute('''
            INSERT INTO monthly_calculations 
            (record_id, month_year, total_compensation, commute_cost, work_hours, real_hourly_wage)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            record_id, current_month, calculations['total_compensation'],
            calculations['annual_commute_cost'], calculations['annual_work_hours'],
            calculations['real_hourly_wage']
        ))
        
        self.conn.commit()
        return record_id
    
    def display_results(self, data: CompensationData, calculations: dict):
        print()
        print("="*60)
        print("COMPENSATION ANALYSIS RESULTS")
        print("="*60)
        
        print()
        print(f"Employee: {data.name}")
        print(f"Car Type: {data.car_type.upper()}")
        
        print()
        print("COMPENSATION BREAKDOWN:")
        print(f"   Base Salary: ${data.salary:,.2f}")
        print(f"   RSU: ${data.rsu:,.2f}")
        print(f"   Bonus ({data.bonus_percent}%): ${calculations['bonus_amount']:,.2f}")
        print(f"   401k Match ({data.match_401k}%): ${calculations['match_401k_amount']:,.2f}")
        print(f"   ------------------------------------")
        print(f"   TOTAL COMPENSATION: ${calculations['total_compensation']:,.2f}")
        
        print()
        print("COMMUTE COSTS (Annual):")
        print(f"   Daily Fuel: ${calculations['commute_costs']['daily_fuel']:.2f}")
        print(f"   Daily Depreciation: ${calculations['commute_costs']['daily_depreciation']:.2f}")
        print(f"   Daily Total: ${calculations['commute_costs']['daily_total']:.2f}")
        print(f"   Annual Commute Cost: ${calculations['annual_commute_cost']:,.2f}")
        
        print()
        print("TIME ANALYSIS:")
        print(f"   Daily Work Hours: {data.daily_hours:.1f}")
        print(f"   Daily Commute Hours: {data.commute_time_minutes * 2 / 60:.1f}")
        print(f"   Total Daily Hours: {data.daily_hours + (data.commute_time_minutes * 2 / 60):.1f}")
        print(f"   Annual Work Hours: {calculations['annual_work_hours']:,.1f}")
        
        print()
        print("NET ANALYSIS:")
        print(f"   Net Compensation: ${calculations['net_compensation']:,.2f}")
        print(f"   REAL HOURLY WAGE: ${calculations['real_hourly_wage']:.2f}")
        
        # Compare with nominal hourly wage
        nominal_hourly = data.salary / (data.daily_hours * 260)
        difference = calculations['real_hourly_wage'] - nominal_hourly
        difference_percent = (difference / nominal_hourly) * 100
        
        print()
        print("COMPARISON:")
        print(f"   Nominal Hourly Wage: ${nominal_hourly:.2f}")
        print(f"   Difference: ${difference:+.2f} ({difference_percent:+.1f}%)")
        print("="*60)
    
    def view_records(self):
        cursor = self.conn.cursor()
        print()
        print("DATABASE RECORDS")
        print("-" * 80)
        
        cursor.execute('''
            SELECT id, name, created_date, real_hourly_wage, salary, rsu
            FROM compensation_records
            ORDER BY created_date DESC
        ''')
        
        records = cursor.fetchall()
        
        if not records:
            print("No records found in the database.")
            return
        
        for record in records:
            print(f"ID: {record[0]} | Name: {record[1]} | Date: {record[2]} | "
                  f"Real Hourly: ${record[3]:.2f} | Salary: ${record[4]:,.0f} | "
                  f"RSU: ${record[5]:,.0f}")
        
        return records
    
    def update_record(self, record_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM compensation_records WHERE id = ?', (record_id,))
        record = cursor.fetchone()
        
        if not record:
            print(f"Record ID {record_id} not found.")
            return
        
        print()
        print(f"Updating record for {record[1]}")
        print("Leave blank to keep current value.")
        print()
        
        # get updated values
        salary = input(f"Current salary ${record[2]}: ") or record[2]
        rsu = input(f"Current RSU ${record[3]}: ") or record[3]
        daily_hours = input(f"Current daily hours {record[12]}: ") or record[12]
        
        # update the record
        cursor.execute('''
            UPDATE compensation_records 
            SET salary = ?, rsu = ?, daily_hours = ?
            WHERE id = ?
        ''', (float(salary), float(rsu), float(daily_hours), record_id))
        
        # recalc
        data = CompensationData(
            name=record[1],
            salary=float(salary),
            rsu=float(rsu),
            match_401k=record[4],
            bonus_percent=record[5],
            commute_time_minutes=record[6],
            commute_distance_miles=record[7],
            car_type=record[8],
            fuel_cost=record[9],
            car_cost=record[10],
            car_mileage=record[11],
            daily_hours=float(daily_hours),
            gas_mileage=record[13],
            electric_efficiency=record[14]
        )
        
        calculations = self.calculate_real_hourly_wage(data)
        
        # update real hourly wage
        cursor.execute('''
            UPDATE compensation_records 
            SET real_hourly_wage = ?
            WHERE id = ?
        ''', (calculations['real_hourly_wage'], record_id))
        
        # add new monthly calculation
        current_month = datetime.now().strftime("%Y-%m")
        cursor.execute('''
            INSERT INTO monthly_calculations 
            (record_id, month_year, total_compensation, commute_cost, work_hours, real_hourly_wage)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            record_id, current_month, calculations['total_compensation'],
            calculations['annual_commute_cost'], calculations['annual_work_hours'],
            calculations['real_hourly_wage']
        ))
        
        self.conn.commit()
        print()
        print(f"Record {record_id} updated successfully!")
        
        return calculations
    
    def generate_report(self):
        cursor = self.conn.cursor()
        print()
        print("COMPREHENSIVE REPORT")
        print("="*80)

        cursor.execute('''
            SELECT name, MAX(real_hourly_wage) as latest_wage, 
                   AVG(real_hourly_wage) as avg_wage, COUNT(*) as entries
            FROM compensation_records
            GROUP BY name
            ORDER BY latest_wage DESC
        ''')
        
        results = cursor.fetchall()
        print()
        print("REAL HOURLY WAGE SUMMARY:")
        print("-" * 60)
        for name, latest, avg, entries in results:
            print(f"{name:20} Latest: ${latest:7.2f} | Avg: ${avg:7.2f} | Entries: {entries}")
        
        # Get monthly trends for the first person (or specify)
        if results:
            cursor.execute('''
                SELECT c.name, m.month_year, m.real_hourly_wage
                FROM monthly_calculations m
                JOIN compensation_records c ON m.record_id = c.id
                WHERE c.name = ?
                ORDER BY m.month_year
            ''', (results[0][0],))
            
            trends = cursor.fetchall()
            
            if trends:
                print()
                print(f"MONTHLY TREND for {trends[0][0]}:")
                print("-" * 40)
                for name, month, wage in trends:
                    print(f"  {month}: ${wage:.2f}")
        print()
        print("="*80)
    
    def close(self):
        self.conn.close()

def main():
    analyzer = CompensationAnalyzer()
    
    while True:
        print()
        print("="*60)
        print("COMPENSATION ANALYSIS TOOL")
        print("="*60)
        print("1. Enter new compensation data")
        print("2. View all records")
        print("3. Update existing record")
        print("4. Generate report")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            # New entry
            data = analyzer.get_user_input()
            calculations = analyzer.calculate_real_hourly_wage(data)
            record_id = analyzer.save_to_database(data, calculations)
            analyzer.display_results(data, calculations)
            print()
            print(f"Record saved with ID: {record_id}")
            
        elif choice == '2':
            analyzer.view_records()
            
        elif choice == '3':
            records = analyzer.view_records()
            if records:
                try:
                    record_id = int(input("\nEnter record ID to update: "))
                    calculations = analyzer.update_record(record_id)
                    
                    if calculations:
                        show = input("\nShow updated results? (y/n): ").lower()
                        if show == 'y':
                            cursor = analyzer.conn.cursor()
                            cursor.execute('SELECT * FROM compensation_records WHERE id = ?', (record_id,))
                            record = cursor.fetchone()
                            
                            data = CompensationData(
                                name=record[1],
                                salary=record[2],
                                rsu=record[3],
                                match_401k=record[4],
                                bonus_percent=record[5],
                                commute_time_minutes=record[6],
                                commute_distance_miles=record[7],
                                car_type=record[8],
                                fuel_cost=record[9],
                                car_cost=record[10],
                                car_mileage=record[11],
                                daily_hours=record[12],
                                gas_mileage=record[13],
                                electric_efficiency=record[14]
                            )
                            analyzer.display_results(data, calculations)
                except ValueError:
                    print("Invalid record ID.")
                    
        elif choice == '4':
            analyzer.generate_report()
            
        elif choice == '5':
            analyzer.close()
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()