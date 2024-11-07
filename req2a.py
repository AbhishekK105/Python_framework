import re
import csv

# Sample Requirements Input
requirements = {
    'Req1': {'description': 'System weight shall not exceed 10000 kg', 'components': ['motor', 'battery'], 'constraints': {'max_weight': '10000 kg'}},
    'Req2': {'description': 'Motor shall run at 5000 RPM', 'components': ['motor'], 'constraints': {'min_rpm': '5000 RPM'}},
    'Req3': {'description': 'Battery shall provide 2000V', 'components': ['battery'], 'constraints': {'min_voltage': '2000 V'}},
    'Req4': {'description': 'System shall operate in temperatures between -20°C and 50°C', 'components': ['motor', 'battery'], 'constraints': {'min_temp': '-20 °C', 'max_temp': '50 °C'}},
    # Add more requirements as necessary
}

# Define keywords to identify variables and limit types
variable_keywords = {
    'weight': 'weight',               # Total weight, payload, etc.
    'rpm': 'rpm',                     # Revolutions per minute for motors/engines
    'torque': 'torque',               # Torque for motors or other components
    'voltage': 'voltage',             # Voltage requirements, battery voltage, etc.
    'current': 'current',             # Electric current requirements, battery current
    'power': 'power',                 # Power capacity, motor power, battery power
    'capacity': 'capacity',           # Battery capacity, fuel tank capacity
    'temperature': 'temperature',     # Operating temperature, thermal limits
    'altitude': 'altitude',           # Operational altitude limits
    'range': 'range',                 # Range of the aircraft
    'speed': 'speed',                 # Speed constraints, max/min speed
    'efficiency': 'efficiency',       # Efficiency of powertrain, motor, etc.
    'lifespan': 'lifespan',           # Lifespan of battery or motor components
    'charging_time': 'charging_time', # Time required to charge the battery
    'discharge_rate': 'discharge_rate', # Rate at which battery discharges
    'fuel_consumption': 'fuel_consumption', # Fuel consumption rate
    'noise': 'noise',                 # Noise level for regulatory compliance
    'vibration': 'vibration',         # Vibration levels, particularly for sensitive components
    'humidity': 'humidity',           # Operational humidity range
    'pressure': 'pressure',           # Pressure limits, relevant at different altitudes
    'protection_rating': 'protection_rating', # IP rating for dust/water protection
    'cost': 'cost',                   # Cost-related limits
    'thrust': 'thrust',               # Thrust level for propellers/engines
    'drag': 'drag',                   # Aerodynamic drag
    'lift': 'lift',                   # Lift force constraints
    'stability': 'stability',         # Stability margins or related factors
    'control_surface': 'control_surface', # Characteristics of control surfaces (e.g., aileron, rudder)
    'emissions': 'emissions',         # Emission levels for compliance
    'fuel_capacity': 'fuel_capacity', # Capacity of fuel tanks, separate from battery capacity
    'battery_health': 'battery_health', # Health indicators for battery condition
    'redundancy': 'redundancy',       # Redundancy levels in critical systems
    'structural_integrity': 'structural_integrity', # Structural safety limits
    'airflow': 'airflow',             # Airflow requirements over wings or cooling systems
    'cooling_capacity': 'cooling_capacity', # Cooling system capacity
    'reliability': 'reliability',     # Reliability metrics
    'operational_time': 'operational_time', # Duration of continuous operation
    'turn_rate': 'turn_rate',         # Maximum or minimum turn rate
    'fuel_efficiency': 'fuel_efficiency', # Efficiency in fuel usage
    'battery_cycles': 'battery_cycles', # Number of charge cycles for batteries
}

limit_keywords = {
    'max': 'upper',            # Maximum allowed level (e.g., max_speed, max_weight)
    'min': 'lower',            # Minimum required level (e.g., min_voltage, min_range)
    'upper': 'upper',          # Upper limit for ranges
    'lower': 'lower',          # Lower limit for ranges
    'threshold': 'upper',      # Often refers to a maximum threshold (e.g., noise_threshold)
    'critical_max': 'upper',   # Critical maximum level, especially for safety parameters
    'critical_min': 'lower',   # Critical minimum level
    'high': 'upper',           # Can denote high values in operational parameters
    'low': 'lower',            # Can denote low values in operational parameters
    'limit': 'upper',          # General term for an upper boundary, depending on context
    'floor': 'lower',          # The lowest acceptable limit (often for financial or capacity metrics)
    'ceiling': 'upper',        # The highest acceptable limit, sometimes for cost or emissions
    'safe_max': 'upper',       # Safety maximum (e.g., max safe temperature)
    'safe_min': 'lower',       # Safety minimum (e.g., minimum safe RPM)
    'peak': 'upper',           # Peak allowable value, especially for power or thrust
    'baseline': 'lower',       # Baseline value, often denotes a minimum benchmark
    'target': 'upper',         # Can refer to an ideal upper target value for optimization
    'optimum_high': 'upper',   # Optimal upper range, especially in operational contexts
    'optimum_low': 'lower',    # Optimal lower range, particularly for environmental or efficiency metrics
    'upper_bound': 'upper',    # Explicit upper bound
    'lower_bound': 'lower',    # Explicit lower bound
}

# Regular expression to find numerical values and units
value_unit_pattern = re.compile(r"(-?\d+\.?\d*)\s*([a-zA-Z%°]*)")

# Function to parse each requirement description
def parse_requirement(description):
    components = []
    constraints = {}

    # Check for any component in the description from the components list
    for component in components:
        if component.lower() in description.lower():
            components.append(component)

    # Search for variable and limit keywords in description
    for variable, var_key in variable_keywords.items():
        if variable in description.lower():
            for limit, limit_type in limit_keywords.items():
                if limit in description.lower():
                    # Find value and unit using regex
                    match = value_unit_pattern.search(description)
                    if match:
                        value = match.group(1)
                        unit = match.group(2) or None
                        constraint_key = f"{limit}_{var_key}"
                        constraints[constraint_key] = f"{value} {unit}".strip()
    return components, constraints

# Function to convert requirements list to numbered dictionary with parsed components and constraints
def generate_requirements_dict(requirements_list):
    requirements_dict = {}
    for i, req in enumerate(requirements_list, start=1):
        req_id = f"Req{i}"
        components, constraints = parse_requirement(req['description'])
        requirements_dict[req_id] = {
            'description': req['description'],
            'components': components,
            'constraints': constraints
        }
    return requirements_dict

# Function to parse constraints and identify variable, limit, value, and units
def extract_constraints_details(constraints):
    parsed_constraints = []
    for constraint, value in constraints.items():
        # Split constraint key to identify variable and limit type
        parts = constraint.split('_')
        variable = next((variable_keywords.get(p) for p in parts if p in variable_keywords), None)
        limit_type = next((limit_keywords.get(p) for p in parts if p in limit_keywords), None)

        # Extract numerical value and units from the constraint's value string
        match = value_unit_pattern.search(value)
        if match:
            num_value = float(match.group(1))
            unit = match.group(2) or None  # Assign None if no unit is found

            # Append the parsed data
            parsed_constraints.append({
                'variable': variable,
                'limit_type': limit_type,
                'value': num_value,
                'unit': unit
            })
    return parsed_constraints


# Function to parse all requirements
def extract_requirements_data(requirements):
    parsed_requirements = []
    for req_id, details in requirements.items():
        # Parse each constraint and store it with requirement context
        constraints = extract_constraints_details(details['constraints'])
        for constraint in constraints:
            parsed_requirements.append({
                'requirement_id': req_id,
                'description': details['description'],
                'component': ', '.join(details['components']),
                **constraint
            })
    return parsed_requirements

# Function to save parsed data to CSV
def save_to_csv(parsed_data, filename='parsed_requirements.csv'):
    # Define CSV column headers
    headers = ['requirement_id', 'description', 'component', 'variable', 'limit_type', 'value', 'unit']
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for data in parsed_data:
            writer.writerow(data)

# Parse the requirements and save to CSV
parsed_data = parse_requirement(requirements)
save_to_csv(parsed_data)

print("Parsed requirements have been saved to 'parsed_requirements.csv'")
