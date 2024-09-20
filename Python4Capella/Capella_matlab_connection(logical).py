'''
Created on 31 dic 2022

@author: Utente
'''
# include needed for the Capella modeller API
include('workspace://Python4Capella/simplified_api/capella.py')
if False:
    from simplified_api.capella import *
    
# include needed for the PVMT API
include('workspace://Python4Capella/simplified_api/pvmt.py')
if False:
    from simplified_api.pvmt import *
    
# include needed for utilities
include('workspace://Python4Capella/utilities/CapellaPlatform.py')
if False:
    from utilities.CapellaPlatform import *

# include needed for the requirement API
include('workspace://Python4Capella/simplified_api/requirement.py')
if False:
    from simplified_api.requirement import *
    
import matlab.engine
eng = matlab.engine.start_matlab()

aird_path = '/TMS_test_6/TMS_test_5.aird'

model = CapellaModel()
model.open(aird_path)

se = model.get_system_engineering()

allLC = se.get_all_contents_by_type(LogicalComponent)

allPVs = []

print('start')

def set_p_v_value(elem, PVName, value):
    for group in elem.get_java_object().getOwnedPropertyValueGroups():
        for pv in group.getOwnedPropertyValues():
            if PVName == pv.getName():
                pv.setValue(value)
                return

for lc in allLC:
    for pvName in PVMT.get_p_v_names(lc):
        if pvName not in allPVs:
            allPVs.append(pvName)
 
 
thl=0                
m=0
rac=0
pc=0
config='None'


for lc in allLC:
    print(lc.get_name())
    for pvName in allPVs:
        if str(PVMT.get_p_v_value(lc, pvName)) != 'None':
            if pvName=='Configuration':
                config=int(PVMT.get_p_v_value(lc, pvName))
                print('  '+pvName,config)
        
            if pvName=='N°':
                n=int(PVMT.get_p_v_value(lc, pvName))
                print('  '+pvName,n)
                
            if pvName=='Heat load':
                hl=float(PVMT.get_p_v_value(lc, pvName))
                print('  '+pvName,str(hl)+' KW')
        
            if pvName=='T max':
                T_max=float(PVMT.get_p_v_value(lc, pvName))+float(273) # C° -> K°
                print('  '+pvName,str(T_max)+' K°')
        
            if pvName=='T min':
                T_min=float(PVMT.get_p_v_value(lc, pvName))+float(273) # C° -> K°
                print('  '+pvName,str(T_min)+' K°')
                
    if str(config)!= 'None':
        eng.workspace['T_InEquip']=T_min
        eng.workspace['Q_equip']=hl
                
        if config==1:
            #run simulation
            eng.run('C:/Users/Utente/PycharmProjects/pythonProject7/Case1.m',nargout=0)
            eng.run('C:/Users/Utente/PycharmProjects/pythonProject7/Case1Results.m',nargout=0)
            mass=eng.workspace['m_TMS']
            ram_air_cons=eng.workspace['mdra']
            power_cons=eng.workspace['w_tot']
            print('  Mass = '+str(round(mass,2))+' kg, Ram air consumption = '+str(round(ram_air_cons,2))+' kg/s, Power consumption = '+str(round(power_cons,2))+' W, Configuration: '+str(config))
                
                
        elif config==2:
            eng.run('C:/Users/Utente/PycharmProjects/pythonProject7/Case2.m',nargout=0)
            eng.run('C:/Users/Utente/PycharmProjects/pythonProject7/Case2Results.m',nargout=0)
            mass=eng.workspace['m_TMS']
            ram_air_cons=eng.workspace['mdra']
            power_cons=eng.workspace['w_tot']
            print('  Mass = '+str(round(mass,2))+' kg, Ram air consumption = '+str(round(ram_air_cons,2))+' kg/s, Power consumption = '+str(round(power_cons,2))+' W, Configuration: '+str(config))
                
                
        elif config==3:
            eng.run('C:/Users/Utente/PycharmProjects/pythonProject7/Case4.m',nargout=0)
            eng.run('C:/Users/Utente/PycharmProjects/pythonProject7/Case4Results.m',nargout=0)
            mass=eng.workspace['m_TMS']
            ram_air_cons=eng.workspace['mdra']
            power_cons=eng.workspace['w_tot']
            print('  Mass = '+str(round(mass,2))+' kg, Ram air consumption = '+str(round(ram_air_cons,2))+' kg/s, Power consumption = '+str(round(power_cons,2))+' W, Configuration: '+str(config))

                
                
        elif config==4:
            eng.run('C:/Users/Utente/PycharmProjects/pythonProject7/Case6.m',nargout=0)
            eng.run('C:/Users/Utente/PycharmProjects/pythonProject7/Case6Results.m',nargout=0)
            mass=eng.workspace['m_TMS']
            ram_air_cons=eng.workspace['mdra']
            power_cons=eng.workspace['w_tot']
            print('  Mass = '+str(round(mass,2))+' kg, Ram air consumption = '+str(round(ram_air_cons,2))+' kg/s, Power consumption = '+str(round(power_cons,2))+' W, Configuration: '+str(config))
        thl=thl+hl        
        m=m+mass
        rac=rac+ram_air_cons
        pc=pc+power_cons
        
    config='None'
eng.quit()


# checking reqirements
for req in se.get_all_contents_by_type(Requirement):
    #print(str(req.get_id()))
    #print(req.get_long_name())
    incoming_req_names = []
    for res in req.get_incoming_linked_elems():
        incoming_req_names.append(res.get_name())
    outgoing_req_names = []
    for res in req.get_outgoing_linked_elems():
        outgoing_req_names.append(res.get_name())
        
    if ('TMS for Electrical drive train' in outgoing_req_names)==1:
        
        if str(req.get_id())=='1':
            # Extracts Requirements Attributes and Values
            if req.get_java_object().getOwnedAttributes() != None:
                for att in req.get_java_object().getOwnedAttributes():
                    #print("- Attribute: "+att.getDefinition().getReqIFLongName()+", value: "+str(att.getValue()))
                    if str(att.getDefinition().getReqIFLongName())=='Value':
                        max_mass=float(att.getValue())
                        #print(max_mass)
                        
        elif str(req.get_id())=='2':
            
            # Extracts Requirements Attributes and Values
            if req.get_java_object().getOwnedAttributes() != None:
                for att in req.get_java_object().getOwnedAttributes():
                    #print("- Attribute: "+att.getDefinition().getReqIFLongName()+", value: "+str(att.getValue()))
                    if str(att.getDefinition().getReqIFLongName())=='Value':
                        max_power=float(att.getValue())
                        #print(max_power)
                        
        elif str(req.get_id())=='3':
            
            # Extracts Requirements Attributes and Values
            if req.get_java_object().getOwnedAttributes() != None:
                for att in req.get_java_object().getOwnedAttributes():
                    #print("- Attribute: "+att.getDefinition().getReqIFLongName()+", value: "+str(att.getValue()))
                    if str(att.getDefinition().getReqIFLongName())=='Value':
                        target_spec_pow_diss=float(att.getValue())
                        #print()
    
        elif str(req.get_id())=='4':
            
            # Extracts Requirements Attributes and Values
            if req.get_java_object().getOwnedAttributes() != None:
                for att in req.get_java_object().getOwnedAttributes():
                    #print("- Attribute: "+att.getDefinition().getReqIFLongName()+", value: "+str(att.getValue()))
                    if str(att.getDefinition().getReqIFLongName())=='Value':
                        target_cop=float(att.getValue())
                        #print()
                        
req_mass_perc= (m/max_mass)*100    
req_power_perc= ((pc/1000)/max_power)*100 #KW
spd=thl/m 
req_spec_pow_diss=(spd/target_spec_pow_diss)*100
cop=thl/(pc/1000)
req_cop_perc=(cop/target_cop)*100


model.start_transaction()
try: 
    for lc in allLC:
        if lc.get_name() == 'TMS for Electrical drive train':
            for pvName in allPVs:
                if pvName=='Mass':
                    set_p_v_value(lc,str(pvName),round(m,2))
                elif pvName=='Power consumption':
                    set_p_v_value(lc,str(pvName),round(pc,2))
                elif pvName=='Ram air consumption':
                    set_p_v_value(lc,str(pvName),round(rac,2))
                elif pvName=='Mass_req':
                    set_p_v_value(lc,str(pvName),round(req_mass_perc,2))
                elif pvName=='Mass_req_bool':
                    if req_mass_perc <= 100:
                        set_p_v_value(lc,str(pvName),'True')
                    else:
                        set_p_v_value(lc,str(pvName),'False')
                elif pvName=='Power_req':
                    set_p_v_value(lc,str(pvName),round(req_power_perc,2))
                elif pvName=='Power_req_bool':
                    if req_power_perc <= 100:
                        set_p_v_value(lc,str(pvName),'True')
                    else:
                        set_p_v_value(lc,str(pvName),'False')
                elif pvName=='SPD_req':
                    set_p_v_value(lc,str(pvName),round(req_spec_pow_diss,2))
                elif pvName=='SPD_req_bool':
                    if req_spec_pow_diss >= 100:
                        set_p_v_value(lc,str(pvName),'True')
                    else:
                        set_p_v_value(lc,str(pvName),'False')
                elif pvName=='COP_req':
                    set_p_v_value(lc,str(pvName),round(req_cop_perc,2))
                elif pvName=='COP_req_bool':
                    if req_cop_perc >= 100:
                        set_p_v_value(lc,str(pvName),'True')
                    else:
                        set_p_v_value(lc,str(pvName),'False')
except:
    # if something went wrong we rollback the transaction
    model.rollback_transaction()
    raise
else:
    # if everything is ok we commit the transaction
    model.commit_transaction() 






print('Total mass = '+str(round(m,2))+' kg, Total ram air consumption = '+str(round(rac,2))+' kg/s, Total power consumption = '+str(round(pc/1000,2))+' KW')
print('Total heat load dissipated = '+str(round(thl,3))+' KW')
print('Specific power dissipation = '+str(round(spd,3))+' KW/kg')
print('COP = '+str(round(cop,3)))
print('Mass obtained is '+str(round(req_mass_perc,3))+'% to the Maximum Mass')
print('Power obtained is '+str(round(req_power_perc,3))+'% to the Maximum Power')
print('Specific power dissipation obtained is '+str(round(req_spec_pow_diss,3))+'% to the target Specific power dissipation')
print('COP obtained is '+str(round(req_cop_perc,3))+'% to the COP target')
print('end')

