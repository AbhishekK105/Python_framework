# Function to map data to a requirement node
def map_data_to_requirement(data, requirement):
    """
    Maps the given model output data to a requirement node.

    """
    # Create a mapping dictionary for later use
    mapping = {
        "requirement": requirement,
        "data": data
    }
    print(f"Mapped data to requirement: {requirement}")
    return mapping


# Function to validate data against a requirement node
def validate_data(mapping):
    """
    Validates the model output (data) against the requirement node's constraints.
    """
    data = mapping["data"]
    requirement = mapping["requirement"]
    
    # Assuming the requirement has attributes like `lower_bound` and `upper_bound`
    if "value" in data:
        value = data["value"]

        # Check lower bound if it exists
        if hasattr(requirement, 'lower_bound') and value < requirement.lower_bound:
            print(f"Data {value} is below the lower bound of {requirement.lower_bound}")
            return False
        
        # Check upper bound if it exists
        if hasattr(requirement, 'upper_bound') and value > requirement.upper_bound:
            print(f"Data {value} is above the upper bound of {requirement.upper_bound}")
            return False

        # If within bounds
        print(f"Data {value} meets the requirement bounds.")
        return True
    else:
        print("No 'value' found in data for validation.")
        return False
