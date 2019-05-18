# azurerm_monitor_autoscale_setting
import ast
def azurerm_monitor_autoscale_setting(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    tfp="azurerm_monitor_autoscale_setting"
    tcode="650-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST monitor autoscale"
        url="https://management.azure.com/subscriptions/" + sub + "/providers/microsoft.insights/autoscalesettings"
        params = {'api-version': '2015-04-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]
        if cde:
            print(json.dumps(azr, indent=4, separators=(',', ': ')))

        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print "# " + tfp,
        count=len(azr)
        print count
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            rgs=id.split("/")[4]
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
            fr.write('name = "' + name + '"\n')
            fr.write('location = "'+ loc + '"\n')
            fr.write('resource_group_name = "'+ rgs + '"\n')

            en=azr[i]["properties"]["enabled"]
            profs=azr[i]["properties"]["profiles"]
        
    # basic settings 
  
            fr.write('enabled = "' + str(en) + '"\n')
   
            try:
                trrg=azr[i]["properties"]["targetResourceUri"].split("/")[4].replace(".","-").lower()
                trty=azr[i]["properties"]["targetResourceUri"].split("/")[6].replace(".","-")
                trid=azr[i]["properties"]["targetResourceUri"].split("/")[8].replace(".","-")
                # assume trty = Microsoft.Compute
                tftyp="azurerm_virtual_machine_scale_set"
                if  trty == "Microsoft-Web" :
                    tftyp="azurerm_app_service_plan"

                fr.write('target_resource_id = "${'+ tftyp + '.' + trrg + '__' + trid+'.id}"\n')   
            except KeyError:
                pass 
        


    #  profiles block
            
            icount=len(profs)
            if icount > 0 :
                for j in range(0,icount):
                    fr.write('profile {\n')
                    pn=azr[i]["properties"]["profiles"][j]["name"]
                    pn=pn.replace('"',"'")
                    pn="dummy"
                    #pn=pn.replace('{','\{')
                    cdef=azr[i]["properties"]["profiles"][j]["capacity"]["default"]
                    cmin=azr[i]["properties"]["profiles"][j]["capacity"]["minimum"]
                    cmax=azr[i]["properties"]["profiles"][j]["capacity"]["maximum"]
                    fr.write('\tname =  "'+pn+ '"\n')
    # capacity
                    fr.write('\tcapacity {\n')
                    fr.write('\t\tdefault = "' + cdef + '"\n')
                    fr.write('\t\tminimum = "' + cmin + '"\n')
                    fr.write('\t\tmaximum = "' + cmax + '"\n')
                    fr.write('\t}\n')
    # fixed date


                    try :
                        fd=azr[i]["properties"]["profiles"][j]["fixedDate"]["end"]
                        fdend=azr[i]["properties"]["profiles"][j]["fixedDate"]["end"]
                        fdstart=azr[i]["properties"]["profiles"][j]["fixedDate"]["start"]
                        fdtz=azr[i]["properties"]["profiles"][j]["fixedDate"]["timeZone"]
                        fdend2= fdend.split("+")[0]
                        fdstart2= fdstart.split("+")[0]
                        fr.write('\tfixed_date {\n')
                        fr.write('\t\ttimezone =  "'+ fdtz + '"\n')
                        fr.write('\t\tstart = "Z' + fdstart2 + '"\n')
                        fr.write('\t\tend = "Z' + fdend2 + '"\n')
                        fr.write('\t}\n')
                    except KeyError:
                        pass
                
    # recurance
                    
                    try :
                        rec=azr[i]["properties"]["profiles"][j]["recurrence"]
                        rfr=azr[i]["properties"]["profiles"][j]["recurrence"]["frequency"]
                        #dns=str(ast.literal_eval(json.dumps(azr[i]["properties"]["dhcpOptions"]["dnsServers"])))
                        #dns=dns.replace("'",'"')

                        rsd=str(ast.literal_eval(json.dumps(azr[i]["properties"]["profiles"][j]["recurrence"]["schedule"]["days"])))
                        rsd=rsd.replace("'",'"')
                        rsh=str(ast.literal_eval(json.dumps(azr[i]["properties"]["profiles"][j]["recurrence"]["schedule"]["hours"])))
                        rsh=rsh.replace("'",'"')
                        rsm=str(ast.literal_eval(json.dumps(azr[i]["properties"]["profiles"][j]["recurrence"]["schedule"]["minutes"])))
                        rsm=rsm.replace("'",'"')
                        rst=azr[i]["properties"]["profiles"][j]["recurrence"]["schedule"]["timeZone"]
                        fr.write('\trecurrence {\n')
                        fr.write('\t\ttimezone = "' + rst + '"\n')
                        fr.write('\t\tdays =  '+ rsd + '\n')
                        fr.write('\t\thours =  '+ rsh + '\n')
                        fr.write('\t\tminutes =  '+ rsm + '\n')            
                        fr.write('\t}\n')
                    except KeyError:
                        pass
                
    # rules
                    try:
                        rules=azr[i]["profiles"][j]["rules"]
                        kcount=len(rules)
                        for k in range(0,kcount):
                                fr.write('\trule  {\n')
                                # metric trigger
                                mtn=azr[i]["profiles"][j]["rules"][k]["metricTrigger"]["metricName"]              
                                if mtn == "CPU" : 
                                    mtn="Percentage CPU"
                            
                                mtid=azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["metricResourceUri"]
                                mtrrg=azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["metricResourceUri"].split("/")[4].replace(".","-").lower()
                                mtrid=azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["metricResourceUri"].split("/")[8].replace(".","-")
                                mtop=azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["operator"]
                                mtstat=azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["statistic"]
                                mtthres=azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["threshold"]
                                mtta=azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["timeAggregation"]
                                mttg=azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["timeGrain"]
                                mttw=azr[i]["properties"]["profiles"][j]["rules"][k]["metricTrigger"]["timeWindow"]
                                mttg2= mttg.split(":")[1].replace("0","") # sed 's/^0*//'
                                mttw2= mttw.split(":")[1].replace("0","") #| cut -f2 -d':' | sed 's/^0*//'                           
                                fr.write('\t\tmetric_trigger {\n')
                                fr.write('\t\t\tmetric_name = "' +  "mtn" + '"\n')
                                fr.write('\t\t\tmetric_resource_id = "${'+tftyp + '.' + mtrrg + '__' + mtrid+ '.id}"\n')
                                fr.write('\t\t\toperator = "' +  mtop + '"\n')
                                fr.write('\t\t\tstatistic= "' +  mtstat + '"\n')
                                fr.write('\t\t\tthreshold = "' +  mtthres + '"\n')
                                fr.write('\t\t\ttime_aggregation = "' +  mtta + '"\n')
                                fr.write('\t\t\ttime_grain = "PTM' + mttg2 + '"\n')
                                fr.write('\t\t\ttime_window = "PTM' + mttw2 + '"\n')  
                                                                                                                                                                        
                                fr.write('\t\t}\n')
                                # scale action
                                sac=azr[i]["properties"]["profiles"][j]["rules"][k]["scaleAction"]["cooldown"]
                                sad=azr[i]["properties"]["profiles"][j]["rules"][k]["scaleAction"]["direction"]
                                sat=azr[i]["properties"]["profiles"][j]["rules"][k]["scaleAction"]["type"]
                                sav=azr[i]["properties"]["profiles"][j]["rules"][k]["scaleAction"]["value"]
                                fr.write('\t\tscale_action  {\n')
                                sac2= sac.split(":")[1].replace("0","") #| cut -f2 -d':' | sed 's/^0*//'
                        
                                fr.write('\t\t\tcooldown = "PTM' + sac2 + '"\n')
                            
                                fr.write('\t\t\tdirection = "' +  sad + '"\n')
                                fr.write('\t\t\ttype = "' +  sat + '"\n')
                                fr.write('\t\t\tvalue = "' +  sav + '"\n')
                                fr.write('\t\t}\n')

                                fr.write('\t}\n') # end rule
                    except KeyError:
                        pass        
                        
                    fr.write('}\n')  # end profile
                

        

    # notification block
            try:
                nots=azr[i]["properties"]["notifications"]
                icount= len(nots)

                for j in range(0,icount):
                    nsa=azr[i]["properties"]["notifications"][j]["email"]["sendToSubscriptionAdministrator"]
                    nsca=azr[i]["properties"]["notifications"][j]["email"]["sendToSubscriptionCoAdministrator"]
                    nce=azr[i]["properties"]["notifications"][j]["email"]["customEmails"]
                    nwh=azr[i]["properties"]["notifications"][j]["webhooks"]
                    fr.write('notification {\n')
                    fr.write('\temail {\n')
                    
                    if nsa:
                        fr.write('\t\tsend_to_subscription_administrator =   "'+ nsa + '"\n')
                
                    if nsca:
                        fr.write('\t\tsend_to_subscription_co_administrator =  "'+ nsca + '"\n')
                
                    fr.write('\t\tcustom_emails =   "'+nce+'"\n')
                    fr.write('\t}\n')
                    fr.write('webhook =   "'+nwh + '"\n')
                    fr.write('}\n')
            except KeyError:
                pass  
            


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
