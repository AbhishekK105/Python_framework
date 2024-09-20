'''
Created on 23 feb 2023

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

aird_path = '/Transition_test_2/Transition_test_2.aird'

model = CapellaModel()
model.open(aird_path)

se = model.get_system_engineering()

allPC = se.get_all_contents_by_type(NodePC)

allPVs = []

print('start\n')

def set_p_v_value(elem, PVName, value):
    for group in elem.get_java_object().getOwnedPropertyValueGroups():
        for pv in group.getOwnedPropertyValues():
            if PVName == pv.getName():
                pv.setValue(value)
                return

for pc in allPC:
    for pvName in PVMT.get_p_v_names(pc):
        if pvName not in allPVs:
            allPVs.append(pvName)
 
ns='REQUIREMENT NOT SATISFIED'
s='REQUIREMENT SATISFIED'
thl=0                
m=0
rac=0
pcs=0
config=0
hl=0
flag=0
n=0
output=0
req1=0
req2=0
req3=0
req4=0

while output < 1 or output > 3:
    def showInputDialog():
        pass
    
    loadModule('/System/UI')
    
    
    output = int(showInputDialog('Select console output type\n1 - All results\n2 - Verification results\n3 - No results\n\n(In any case all results will be placed in the model)', 'Results type number'))


while n < 1 or n > 9:
    def showInputDialog():
        pass
    
    loadModule('/System/UI')
    
    
    n = int(showInputDialog('Select flight phase number\nFlight phases:\n1 - Parked\n2 - Taxi out\n3 - Take-off\n4 - Start of climb\n5 - End of climb\n6 - Cruise\n7 - Descent\n8 - Landing\n9 - Taxi in', 'Flight phase number'))
        

if n==1:
    phase='Parked'
elif n==2:
    phase='Taxi out'              
elif n==3:
    phase='Take-off' 
elif n==4:
    phase='Start of climb' 
elif n==5:
    phase='End of climb' 
elif n==6:
    phase='Cruise' 
elif n==7:
    phase='Descent' 
elif n==8:
    phase='Landing' 
elif n==9:
    phase='Taxi in' 

print('TMS sizing on "'+str(phase)+'" conditions\n')


for pc in allPC:
    
    for pvName in allPVs:
        if str(PVMT.get_p_v_value(pc, pvName)) != 'None':
            if pvName=='Configuration':
                config=int(PVMT.get_p_v_value(pc, pvName))
                
                
            if pvName=='T':
                T=float(PVMT.get_p_v_value(pc, pvName))+float(273) # C° -> K°
                                
        
            
    if isinstance(config,int) and int(config) > 0:
        print(pc.get_name())
        eng.workspace['T_InEquip']=T       
        
        sms=pc.get_owned_state_machines()
        for sm in sms:
            regions=sm.get_owned_regions()
            for region in regions:
                states = region.get_owned_states()
                for state in states:
                    rs=state.get_owned_regions()
                    for r in rs:
                        if state.get_name()==phase:
                            hl=float(r.get_name())
                            
        print('  Configuration '+str(config))
        print('  T = '+str(T)+' °K')                    
        print('  Heat load = '+str(hl)+' KW')
        eng.workspace['Q_equip']= float(hl)
        
        if hl > 0:
            flag=1
       
            if config==1:
                #run simulation
                eng.run('C:/Users/Utente/PycharmProjects/pythonProject7/Case1.m',nargout=0)
                eng.run('C:/Users/Utente/PycharmProjects/pythonProject7/Case1Results.m',nargout=0)
                mass=eng.workspace['m_TMS']
                ram_air_cons=eng.workspace['mdra']
                power_cons=eng.workspace['w_tot']
                if power_cons > 0:
                    print('  Mass = '+str(round(mass,2))+' kg, Ram air consumption = '+str(round(ram_air_cons,2))+' kg/s, Power consumption = '+str(round(power_cons,2))+' W\n')
                else:
                    mass=0
                    ram_air_cons=0
                    power_cons=0
                    print('  The evaluated power consumption is < 0, cooling not required for '+str(pc.get_name())+' in '+str(phase)+' phase')    
                    
            elif config==2:
                eng.run('C:/Users/Utente/PycharmProjects/pythonProject7/Case2.m',nargout=0)
                eng.run('C:/Users/Utente/PycharmProjects/pythonProject7/Case2Results.m',nargout=0)
                mass=eng.workspace['m_TMS']
                ram_air_cons=eng.workspace['mdra']
                power_cons=eng.workspace['w_tot']
                if power_cons > 0:
                    print('  Mass = '+str(round(mass,2))+' kg, Ram air consumption = '+str(round(ram_air_cons,2))+' kg/s, Power consumption = '+str(round(power_cons,2))+' W\n')
                else:
                    mass=0
                    ram_air_cons=0
                    power_cons=0
                    print('  The evaluated power consumption is < 0, cooling not required for '+str(pc.get_name())+' in '+str(phase)+' phase')    
                       
                    
            elif config==3:
                eng.run('C:/Users/Utente/PycharmProjects/pythonProject7/Case4.m',nargout=0)
                eng.run('C:/Users/Utente/PycharmProjects/pythonProject7/Case4Results.m',nargout=0)
                mass=eng.workspace['m_TMS']
                ram_air_cons=eng.workspace['mdra']
                power_cons=eng.workspace['w_tot']
                if power_cons > 0:
                    print('  Mass = '+str(round(mass,2))+' kg, Ram air consumption = '+str(round(ram_air_cons,2))+' kg/s, Power consumption = '+str(round(power_cons,2))+' W\n')
                else:
                    mass=0
                    ram_air_cons=0
                    power_cons=0
                    print('  The evaluated power consumption is < 0, cooling not required for '+str(pc.get_name())+' in '+str(phase)+' phase')    
                
                    
                    
            elif config==4:
                eng.run('C:/Users/Utente/PycharmProjects/pythonProject7/Case6.m',nargout=0)
                eng.run('C:/Users/Utente/PycharmProjects/pythonProject7/Case6Results.m',nargout=0)
                mass=eng.workspace['m_TMS']
                ram_air_cons=eng.workspace['mdra']
                power_cons=eng.workspace['w_tot']
                if power_cons > 0:
                    print('  Mass = '+str(round(mass,2))+' kg, Ram air consumption = '+str(round(ram_air_cons,2))+' kg/s, Power consumption = '+str(round(power_cons,2))+' W\n')
                else:
                    mass=0
                    ram_air_cons=0
                    power_cons=0
                    print('  The evaluated power consumption is < 0, cooling not required for '+str(pc.get_name())+' in '+str(phase)+' phase')    
                
            thl=thl+hl        
            m=m+mass
            rac=rac+ram_air_cons
            pcs=pcs+power_cons
            

                
        else:
            print('  Cooling not required for '+str(pc.get_name())+' in '+str(phase)+' phase, heat load = '+str(hl))
            
    config=0
            
if pcs == 0:
    flag=0 
           
eng.quit()

if flag==1:
    for req in se.get_all_contents_by_type(Requirement):
        #print(str(req.get_id()))
        #print(req.get_long_name())
        incoming_req_names = []
        for res in req.get_incoming_linked_elems():
            incoming_req_names.append(res.get_name())
        outgoing_req_names = []
        for res in req.get_outgoing_linked_elems():
            outgoing_req_names.append(res.get_name())
            
        if ('TMS for electrical drive train' in outgoing_req_names)==1:
            
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
                            #print(target_spec_pow_diss)
        
            elif str(req.get_id())=='4':
                
                # Extracts Requirements Attributes and Values
                if req.get_java_object().getOwnedAttributes() != None:
                    for att in req.get_java_object().getOwnedAttributes():
                        #print("- Attribute: "+att.getDefinition().getReqIFLongName()+", value: "+str(att.getValue()))
                        if str(att.getDefinition().getReqIFLongName())=='Value':
                            target_cop=float(att.getValue())
                            #print(target_cop)
                            
    req_mass_perc= (m/max_mass)*100    
    req_power_perc= ((pcs/1000)/max_power)*100 #KW
    spd=thl/m 
    req_spec_pow_diss=(spd/target_spec_pow_diss)*100
    cop=thl/(pcs/1000)
    req_cop_perc=(cop/target_cop)*100
    
    
    model.start_transaction()
    try: 
        for pc in allPC:
            if pc.get_name() == 'TMS for electrical drive train':
                for pvName in allPVs:
                    if pvName=='Mass':
                        set_p_v_value(pc,str(pvName),round(m,2))
                    elif pvName=='Power_consumption':
                        set_p_v_value(pc,str(pvName),round(pcs,2))
                    elif pvName=='Ram_air_consumption':
                        set_p_v_value(pc,str(pvName),round(rac,2))
                    elif pvName=='Mass_req':
                        set_p_v_value(pc,str(pvName),round(req_mass_perc,2))
                    elif pvName=='Mass_req_bool':
                        if req_mass_perc<= 100:
                            set_p_v_value(pc,str(pvName),'True')
                            req1=1
                        else:
                            set_p_v_value(pc,str(pvName),'False')
                    elif pvName=='Power_req':
                        set_p_v_value(pc,str(pvName),round(req_power_perc,2))
                    elif pvName=='Power_req_bool':
                        if req_power_perc <= 100:
                            set_p_v_value(pc,str(pvName),'True')
                            req2=1
                        else:
                            set_p_v_value(pc,str(pvName),'False')
                    elif pvName=='SPD_req':
                        set_p_v_value(pc,str(pvName),round(req_spec_pow_diss,2))
                    elif pvName=='SPD_req_bool':
                        if req_spec_pow_diss >= 100:
                            set_p_v_value(pc,str(pvName),'True')
                            req3=1
                        else:
                            set_p_v_value(pc,str(pvName),'False')
                    elif pvName=='COP_req':
                        set_p_v_value(pc,str(pvName),round(req_cop_perc,2))
                    elif pvName=='COP_req_bool':
                        if req_cop_perc >= 100:
                            set_p_v_value(pc,str(pvName),'True')
                            req4=1
                        else:
                            set_p_v_value(pc,str(pvName),'False')
                    elif pvName=='Run_result':
                        set_p_v_value(pc, pvName,'TMS evaluated')
                    elif pvName=='Run_phase':
                        set_p_v_value(pc,pvName,phase)
        
        for req in se.get_all_contents_by_type(Requirement):
        #print(str(req.get_id()))
        #print(req.get_long_name())
            incoming_req_names = []
            for res in req.get_incoming_linked_elems():
                incoming_req_names.append(res.get_name())
            outgoing_req_names = []
            for res in req.get_outgoing_linked_elems():
                outgoing_req_names.append(res.get_name())
                
            if ('TMS for electrical drive train' in outgoing_req_names)==1:
                
                if str(req.get_id())=='1':
                    if req1==0:
                        req.set_prefix(ns)
                        
                    else:
                        req.set_prefix(s)
                        
                if str(req.get_id())=='2':
                    if req2==0:
                        req.set_prefix(ns)
                        
                    else:
                        req.set_prefix(s)
                        
                
                if str(req.get_id())=='3':
                    if req3==0:
                        req.set_prefix(ns)
                        
                    else:
                        req.set_prefix(s)
                        
                        
                if str(req.get_id())=='4':
                    if req4==0:
                        req.set_prefix(ns)
                        
                    else:
                        req.set_prefix(s)
                        

    except:
        # if something went wrong we rollback the transaction
        model.rollback_transaction()
        raise
    else:
        # if everything is ok we commit the transaction
        model.commit_transaction() 
    
    print('\n---------RESULTS--------\n')
    
    if output==1:
        print('Total mass = '+str(round(m,2))+' kg, Total ram air consumption = '+str(round(rac,2))+' kg/s, Total power consumption = '+str(round(pcs/1000,2))+' KW')
        print('Total heat load dissipated = '+str(round(thl,3))+' KW')
        print('Specific power dissipation = '+str(round(spd,3))+' KW/kg')
        print('COP = '+str(round(cop,3)))
        print('\n')
        if req1==0:
            print('Mass obtained is '+str(round(req_mass_perc,3))+'% to the Maximum Mass, '+ns)
        else:
            print('Mass obtained is '+str(round(req_mass_perc,3))+'% to the Maximum Mass, '+s)
        if req2==0:
            print('Power obtained is '+str(round(req_power_perc,3))+'% to the Maximum Power, '+ns)
        else:
            print('Power obtained is '+str(round(req_power_perc,3))+'% to the Maximum Power, '+s)
        if req3==0:
            print('Specific power dissipation obtained is '+str(round(req_spec_pow_diss,3))+'% to the target Specific power dissipation, '+ns)
        else:
            print('Specific power dissipation obtained is '+str(round(req_spec_pow_diss,3))+'% to the target Specific power dissipation, '+s)
        
        if req4==0:
            print('COP obtained is '+str(round(req_cop_perc,3))+'% to the COP target, '+ns)
        else:
            print('COP obtained is '+str(round(req_cop_perc,3))+'% to the COP target, '+s+'\n')
    
    elif output==2:
        if req1==0:
            print('Mass '+ns)
        else:
            print('Mass '+s)
        if req2==0:
            print('Power '+ns)
        else:
            print('Power '+s)
        if req3==0:
            print('Specific power dissipation '+ns)
        else:
            print('Specific power dissipation '+s)
        
        if req4==0:
            print('COP '+ns)
        else:
            print('COP '+s+'\n')
    elif output==3:
        print('All results in the model\n')
else:
    print(str(phase)+' does not require cooling, TMS not evaluated')
    model.start_transaction()
    try: 
        for pc in allPC:
            if pc.get_name() == 'TMS for electrical drive train':
                for pvName in allPVs:
                    if pvName=='Mass':
                        set_p_v_value(pc,str(pvName),float(0))
                    elif pvName=='Power_consumption':
                        set_p_v_value(pc,str(pvName),float(0))
                    elif pvName=='Ram_air_consumption':
                        set_p_v_value(pc,str(pvName),float(0))
                    elif pvName=='Mass_req':
                        set_p_v_value(pc,str(pvName),float(0))
                    elif pvName=='Mass_req_bool':
                        set_p_v_value(pc,str(pvName),'-')

                    elif pvName=='Power_req':
                        set_p_v_value(pc,str(pvName),float(0))
                    elif pvName=='Power_req_bool':
                        set_p_v_value(pc,str(pvName),'-')
                    elif pvName=='SPD_req':
                        set_p_v_value(pc,str(pvName),float(0))
                    elif pvName=='SPD_req_bool':
                        set_p_v_value(pc,str(pvName),'-')
                    elif pvName=='COP_req':
                        set_p_v_value(pc,str(pvName),float(0))
                    elif pvName=='COP_req_bool':
                        set_p_v_value(pc,str(pvName),'-')
                    elif pvName=='Run_result':
                        set_p_v_value(pc, pvName,'TMS not evaluated')
                    elif pvName=='Run_phase':
                        set_p_v_value(pc, pvName,phase)
    except:
        # if something went wrong we rollback the transaction
        model.rollback_transaction()
        raise
    else:
        # if everything is ok we commit the transaction
        model.commit_transaction()
        
print('end')

