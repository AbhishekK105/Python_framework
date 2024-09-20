'''
Created on 01 Aug 2024

@author: Abhishek
'''
# Setup and imports
include('workspace://Python4Capella/simplified_api/capella.py')
if False:
    from simplified_api.capella import *
    
include('workspace://Python4Capella/utilities/CapellaPlatform.py')
if False:
    from utilities.CapellaPlatform import *

include('workspace://Python4Capella/simplified_api/requirement.py')
if False:
    from simplified_api.requirement import *

import pandas as pd

# Model loading
aird_path = '/Electric_propulsion_system/Electric_propulsion_system.aird'

model = CapellaModel()
model.open(aird_path)

se = model.get_system_engineering()

# Data extraction
allLC = se.get_all_contents_by_type(LogicalComponent)
data = []

def extract_element_data(elem, parent_name=""):
    elem_name = elem.get_name()
    elem_type = elem.eClass().getName()
    metadata = {attr: elem.get_java_object().eGet(attr) for attr in elem.get_java_object().eClass().getEAllAttributes()}
    metadata['Parent'] = parent_name
    metadata['Element Name'] = elem_name
    metadata['Element Type'] = elem_type
    data.append(metadata)
    
    for child in elem.get_contained_elems():
        extract_element_data(child, elem_name)

for lc in allLC:
    extract_element_data(lc)

# Export to Excel
df = pd.DataFrame(data)
excel_path = 'Electric_Propulsion_System_Data.xlsx'
df.to_excel(excel_path, index=False)

# Requirement verification
affected_requirements = []

for req in se.get_all_contents_by_type(Requirement):
    outgoing_req_names = [res.get_name() for res in req.get_outgoing_linked_elems()]
    
    for lc in allLC:
        if lc.get_name() in outgoing_req_names:
            affected_requirements.append({
                'Requirement ID': req.get_id(),
                'Requirement Name': req.get_long_name(),
                'Linked Element': lc.get_name()
            })

# Export affected requirements to Excel
df_reqs = pd.DataFrame(affected_requirements)
reqs_excel_path = 'Affected_Requirements.xlsx'
df_reqs.to_excel(reqs_excel_path, index=False)

print(f'Data exported to {excel_path}')
print(f'Affected requirements exported to {reqs_excel_path}')

model.close()
