import re

# Define variable and limit keywords dictionaries (from previous setup)
variable_keywords = {
    'weight': 'weight', 'rpm': 'rpm', 'torque': 'torque', 'voltage': 'voltage',
    'current': 'current', 'power': 'power', 'capacity': 'capacity', 'temperature': 'temperature',
    'altitude': 'altitude', 'range': 'range', 'speed': 'speed', 'efficiency': 'efficiency',
    'lifespan': 'lifespan', 'charging_time': 'charging_time', 'discharge_rate': 'discharge_rate',
    'fuel_consumption': 'fuel_consumption', 'noise': 'noise', 'vibration': 'vibration',
    'humidity': 'humidity', 'pressure': 'pressure', 'protection_rating': 'protection_rating',
    'cost': 'cost', 'thrust': 'thrust', 'drag': 'drag', 'lift': 'lift', 'stability': 'stability',
    'control_surface': 'control_surface', 'emissions': 'emissions', 'fuel_capacity': 'fuel_capacity',
    'battery_health': 'battery_health', 'redundancy': 'redundancy', 'structural_integrity': 'structural_integrity',
    'airflow': 'airflow', 'cooling_capacity': 'cooling_capacity', 'reliability': 'reliability',
    'operational_time': 'operational_time', 'turn_rate': 'turn_rate', 'fuel_efficiency': 'fuel_efficiency',
    'battery_cycles': 'battery_cycles'
}

limit_keywords = {
    'max': 'upper', 'min': 'lower', 'upper': 'upper', 'lower': 'lower', 'threshold': 'upper',
    'critical_max': 'upper', 'critical_min': 'lower', 'high': 'upper', 'low': 'lower',
    'limit': 'upper', 'floor': 'lower', 'ceiling': 'upper', 'safe_max': 'upper', 'safe_min': 'lower',
    'peak': 'upper', 'baseline': 'lower', 'target': 'upper', 'optimum_high': 'upper', 'optimum_low': 'lower',
    'upper_bound': 'upper', 'lower_bound': 'lower'
}

# Define a list of components to look for
components_list = ['motor', 'battery', 'converter', 'DC bus', 'aircraft', 'propeller', 'gearbox']

# Regular expression to detect numerical values with units
value_unit_pattern = re.compile(r"(-?\d+\.?\d*)\s*([a-zA-Z%°]*)")

# Function to parse each requirement description
def parse_requirement(description):
    components = []
    constraints = {}

    # Check for any component in the description from the components list
    for component in components_list:
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

# Example requirements list with only descriptions
requirements_list = [
    {'description': 'Battery weight shall not exceed 500 kg'},
    {'description': 'Motor shall operate at a maximum of 7000 RPM'},
    {'description': 'Battery capacity shall be at least 6000 mAh'},
    {'description': 'Converter shall operate within safe limits'},
    {'description': 'Aircraft noise level shall not exceed 85 dB'},
]

# Convert requirements list to dictionary with parsed components and constraints
requirements = generate_requirements_dict(requirements_list)
print(requirements)
