# azurerm_monitor_autoscale_setting
def azurerm_monitor_autoscale_setting(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    tfp="azurerm_monitor_autoscale_setting"
    tcode="650-"
    azr=""
    if crf in tfp:
    # REST or cli
        print "REST Managed Disk"
        url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Compute/disks"
        params = {'api-version': '2017-03-30'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]
        if cde:
            print(json.dumps(azr, indent=4, separators=(',', ': ')))

        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print tfp,
        count=len(azr)
        print count
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-")

            if crg is not None:
                if rg.lower() != crg.lower():
                    continue  # back to for
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rg + '"\n')

    ###############
    # specific code start
    ###############

            en=azr[i]["enabled"]
            loc=azr[i]["location"]
            profs=azr[i]["profiles"]
            nots=azr[i]["notifications"]
            trrg=azr[i]["targetResourceUri"].split("/")[4].replace(".","-")
            trty=azr[i]["targetResourceUri"].split("/")[6].replace(".","-")
            trid=azr[i]["targetResourceUri"].split("/")[8].replace(".","-")
            # assume trty = Microsoft.Compute
            tftyp="azurerm_virtual_machine_scale_set"
            if  trty == "Microsoft-Web" :
                tftyp="azurerm_app_service_plan"
        
            print "trty  tftyp"


            #
    # basic settings 
  
            fr.write('enabled = "' + en + '"\n')
   
            if trrg" try :
            fr.write('target_resource_id = "${. + '__' + .id}'"' tftyp trrg trid + '"\n')      
        


    #  profiles block
            
            icount= profs | | len(
            if icount > 0" :
                for j in range(0,icount):
                    fr.write('profile {\n')
                    pn=azr[i]["profiles[j]["name"
                    cdef=azr[i]["profiles[j]["capacity.default"]
                    cmin=azr[i]["profiles[j]["capacity.minimum"]
                    cmax=azr[i]["profiles[j]["capacity.maximum"]
                    fr.write('\tname =  "pn" + '"\n')
    # capacity
                    fr.write('\tcapacity {\n')
                    fr.write('\t\tdefault = "' + cdef + '"\n')
                    fr.write('\t\tminimum = "' + cmin + '"\n')
                    fr.write('\t\tmaximum = "' + cmax + '"\n')
                    fr.write('\t}\n')
    #xed date

                    fd=azr[i]["profiles[j]["fixedDate.end"]
                    fdend=azr[i]["profiles[j]["fixedDate.end"]
                    fdstart=azr[i]["profiles[j]["fixedDate.start"]
                    fdtz=azr[i]["profiles[j]["fixedDate.timeZone"]
                    fdend2= fdend | cut -f1 -d'+'
                    fdstart2= fdstart | cut -f1 -d'+'
                    
                    if fd" try :
                    fr.write('\tfixed_date {\n')
                    fr.write('\t\ttimezone =  "fdtz" + '"\n')
                    fr.write('\t\tstart = "'Z"' fdstart2 + '"\n')
                    fr.write('\t\tend = "'Z"' fdend2 + '"\n')
                    fr.write('\t}\n')
                
    # recurance
                    rec=azr[i]["profiles[j]["recurrence"]
                    if rec" try :
                    rfr=azr[i]["profiles[j]["recurrence.frequency"]| tr -d '"'
                    rsd=azr[i]["profiles[j]["recurrence.schedule.days"]
                    rsh=azr[i]["profiles[j]["recurrence.schedule.hours"]
                    rsm=azr[i]["profiles[j]["recurrence.schedule.minutes"]
                    rst=azr[i]["profiles[j]["recurrence.schedule.timeZone"]| tr -d '"'
                    fr.write('\trecurrence {\n')
                    fr.write('\t\ttimezone = "' +  rst + '"\n')
                    fr.write('\t\tdays =  "rsd" + '"\n')
                    fr.write('\t\thours =  "rsh" + '"\n')
                    fr.write('\t\tminutes =  "rsm" + '"\n')            
                    fr.write('\t}\n')
                
    # rules

                    rules=azr[i]["profiles"][j]["rules"]

                    kcount= rules | | len(
                    if kcount > 0" :
                            for k in range(0,kcount):
                                fr.write('\trule  {\n')
                                # metric trigger
                                mtn=azr[i]["profiles[j]["rules[k]["metricTrigger.metricName"]              
                                if mtn" = "CPU" : 
                                    mtn="Percentage CPU"
                            
                                mtid=azr[i]["profiles[j]["rules[k]["metricTrigger.metricResourceUri"]
                                mtrrg=azr[i]["profiles[j]["rules[k]["metricTrigger.metricResourceUri"].split("/")[4].replace(".","-")
                                mtrid=azr[i]["profiles[j]["rules[k]["metricTrigger.metricResourceUri"].split("/")[8].replace(".","-")
                                mtop=azr[i]["profiles[j]["rules[k]["metricTrigger.operator"]
                                mtstat=azr[i]["profiles[j]["rules[k]["metricTrigger.statistic"]
                                mtthres=azr[i]["profiles[j]["rules[k]["metricTrigger.threshold"]
                                mtta=azr[i]["profiles[j]["rules[k]["metricTrigger.timeAggregation"]
                                mttg=azr[i]["profiles[j]["rules[k]["metricTrigger.timeGrain"]
                                mttw=azr[i]["profiles[j]["rules[k]["metricTrigger.timeWindow"]
                                mttg2= mttg | cut -f2 -d':' | sed 's/^0*//'
                                mttw2= mttw | cut -f2 -d':' | sed 's/^0*//'                           
                                fr.write('\t\tmetric_trigger {\n')
                                fr.write('\t\t\tmetric_name = "' +  "mtn" + '"\n')
                                fr.write('\t\t\tmetric_resource_id = "${. + '__' + .id}'"' tftyp mtrrg mtrid + '"\n')
                                fr.write('\t\t\toperator = "' +  mtop + '"\n')
                                fr.write('\t\t\tstatistic= "' +  mtstat + '"\n')
                                fr.write('\t\t\tthreshold = "' +  mtthres + '"\n')
                                fr.write('\t\t\ttime_aggregation = "' +  mtta + '"\n')
                                fr.write('\t\t\ttime_grain = "'PTM"' mttg2 + '"\n')
                                fr.write('\t\t\ttime_window = "'PTM"' mttw2 + '"\n')  
                                                                                                                                                                        
                                fr.write('\t\t}\n')
                                # scale action
                                sac=azr[i]["profiles[j]["rules[k]["scaleAction.cooldown"]
                                sad=azr[i]["profiles[j]["rules[k]["scaleAction.direction"]
                                sat=azr[i]["profiles[j]["rules[k]["scaleAction.type"]
                                sav=azr[i]["profiles[j]["rules[k]["scaleAction.value"]
                                fr.write('\t\tscale_action  {\n')
                                sac2= sac | cut -f2 -d':' | sed 's/^0*//'
                        
                                fr.write('\t\t\tcooldown = "'PTM"' sac2 + '"\n')
                            
                                fr.write('\t\t\tdirection = "' +  sad + '"\n')
                                fr.write('\t\t\ttype = "' +  sat + '"\n')
                                fr.write('\t\t\tvalue = "' +  sav + '"\n')
                                fr.write('\t\t}\n')

                                fr.write('\t}\n') # end rule
                            
                        
                fr.write('}\n')  # end profile
                

        

    # notification block
            icount= nots | | len(
            if icount > 0" :
                for j in range(0,icount):
                    nsa=azr[i]["notifications[i]["email.sendToSubscriptionAdministrator"]
                    nsca=azr[i]["notifications[i]["email.sendToSubscriptionCoAdministrator"]
                    nce=azr[i]["notifications[i]["email.customEmails"
                    nwh=azr[i]["notifications[i]["webhooks"
                    fr.write('notification {\n')
                    fr.write('\temail {\n')
                    echo nsa
                    if nsa" try :
                    fr.write('\t\tsend_to_subscription_administrator =   nsa + '"\n')
                
                    if nsca" try :
                    fr.write('\t\tsend_to_subscription_co_administrator =   nsca + '"\n')
                
                    fr.write('\t\tcustom_emails =   "nce" + '"\n')
                    fr.write('\t}\n')
                    fr.write('webhook =   "nwh" + '"\n')
                    fr.write('}\n')
                
            


    ###############
    # specific code end
    ###############

    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write('\t "' + key + '"="' + tval + '"\n')
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print f.read()

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
