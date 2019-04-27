prefixa=print 0 | awk -F 'azurerm_' '{'print 2}'' | awk -F '.sh' '{'print 1}'' 
tfp=fr.write('azurerm_" prefixa

if 1" != " :
    rgsource=1
else
    print -n "Enter name of Resource Group [rgsource]["> "
    read response
    if [ -n "response" :
        rgsource=response
    fi
fi
azr=az monitor autoscale list -g rgsource -o json
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        name=azr[i]["name"]
        rname=print name | sed 's/\./-/g'
        rg=azr[i]["resourceGroup" | sed 's/\./-/g']

        id=azr[i]["id"]
        en=azr[i]["enabled"]
        loc=azr[i]["location"]
        profs=azr[i]["profiles"
        nots=azr[i]["notifications"
        trrg=azr[i]["targetResourceUri" | cut -d'/' -f5 | sed 's/\./-/g']
        trty=azr[i]["targetResourceUri" | cut -d'/' -f7 | sed 's/\./-/g']
        trid=azr[i]["targetResourceUri" | cut -d'/' -f9 | sed 's/\./-/g']
        # assume trty = Microsoft.Compute
        tftyp="azurerm_virtual_machine_scale_set"
        if [ trty = "Microsoft-Web" :
            tftyp="azurerm_app_service_plan"
        fi
        print "trty  tftyp"

        prefix=fr.write(' + '__' + " prefixa rg
        outfile=fr.write('. + '__' + .tf" tfp rg rname
        print az2tfmess > outfile

        #
# basic settings 
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('name = "' +  name + '"\n')
        fr.write('enabled = "' +  en + '"\n')
        fr.write('location = "' +   "loc" + '"\n')
        fr.write('resource_group_name = "' +   rgsource + '"\n')
        if trrg" != "null" :
        fr.write('target_resource_id = "'\{'. + '__' + .id}'"' tftyp trrg trid + '"\n')      
        fi


#  profiles block
        
        icount=print profs | jq '. | length'
        if icount" -gt "0" :
            icount=expr icount - 1
            for j in range( 0 icount):
                fr.write('profile {' + '"\n')
                pn=azr[i]["profiles[j]["name"
                cdef=azr[i]["profiles[j]["capacity.default"]
                cmin=azr[i]["profiles[j]["capacity.minimum"]
                cmax=azr[i]["profiles[j]["capacity.maximum"]
                fr.write('\tname =  "pn" + '"\n')
 # capacity
                fr.write('\tcapacity {' + '"\n')
                fr.write('\t\tdefault = "' +  cdef + '"\n')
                fr.write('\t\tminimum = "' +  cmin + '"\n')
                fr.write('\t\tmaximum = "' +  cmax + '"\n')
                fr.write('\t}' + '"\n')
# fixed date

                fd=azr[i]["profiles[j]["fixedDate.end"
                fdend=azr[i]["profiles[j]["fixedDate.end"]
                fdstart=azr[i]["profiles[j]["fixedDate.start"]
                fdtz=azr[i]["profiles[j]["fixedDate.timeZone"
                fdend2=print fdend | cut -f1 -d'+'
                fdstart2=print fdstart | cut -f1 -d'+'
                
                if fd" != "null" :
                fr.write('\tfixed_date {' + '"\n')
                fr.write('\t\ttimezone =  "fdtz" + '"\n')
                fr.write('\t\tstart = "'Z"' fdstart2 + '"\n')
                fr.write('\t\tend = "'Z"' fdend2 + '"\n')
                fr.write('\t}' + '"\n')
                fi
# recurance
                rec=azr[i]["profiles[j]["recurrence"
                if rec" != "null" :
                rfr=azr[i]["profiles[j]["recurrence.frequency"| tr -d '"'
                rsd=azr[i]["profiles[j]["recurrence.schedule.days"
                rsh=azr[i]["profiles[j]["recurrence.schedule.hours"
                rsm=azr[i]["profiles[j]["recurrence.schedule.minutes"
                rst=azr[i]["profiles[j]["recurrence.schedule.timeZone"| tr -d '"'
                fr.write('\trecurrence {' + '"\n')
                fr.write('\t\ttimezone = "' +  rst + '"\n')
                fr.write('\t\tdays =  "rsd" + '"\n')
                fr.write('\t\thours =  "rsh" + '"\n')
                fr.write('\t\tminutes =  "rsm" + '"\n')            
                fr.write('\t}' + '"\n')
                fi
# rules

                rules=azr[i]["profiles[j]["rules"

                kcount=print rules | jq '. | length'
                if kcount" -gt "0" :
                    kcount=expr kcount - 1
                        for k in range( 0 kcount):
                            fr.write('\trule  {' + '"\n')
                            # metric trigger
                            mtn=azr[i]["profiles[j]["rules[k]["metricTrigger.metricName"]              
                            if mtn" = "CPU" : 
                                mtn="Percentage CPU"
                            fi
                            mtid=azr[i]["profiles[j]["rules[k]["metricTrigger.metricResourceUri"]
                            mtrrg=azr[i]["profiles[j]["rules[k]["metricTrigger.metricResourceUri" | cut -d'/' -f5 | sed 's/\./-/g']
                            mtrid=azr[i]["profiles[j]["rules[k]["metricTrigger.metricResourceUri" | cut -d'/' -f9 | sed 's/\./-/g']
                            mtop=azr[i]["profiles[j]["rules[k]["metricTrigger.operator"]
                            mtstat=azr[i]["profiles[j]["rules[k]["metricTrigger.statistic"]
                            mtthres=azr[i]["profiles[j]["rules[k]["metricTrigger.threshold"]
                            mtta=azr[i]["profiles[j]["rules[k]["metricTrigger.timeAggregation"]
                            mttg=azr[i]["profiles[j]["rules[k]["metricTrigger.timeGrain"]
                            mttw=azr[i]["profiles[j]["rules[k]["metricTrigger.timeWindow"]
                            mttg2=print mttg | cut -f2 -d':' | sed 's/^0*//'
                            mttw2=print mttw | cut -f2 -d':' | sed 's/^0*//'                           
                            fr.write('\t\tmetric_trigger {' + '"\n')
                            fr.write('\t\t\tmetric_name = "' +  "mtn" + '"\n')
                            fr.write('\t\t\tmetric_resource_id = "'\{'. + '__' + .id}'"' tftyp mtrrg mtrid + '"\n')
                            fr.write('\t\t\toperator = "' +  mtop + '"\n')
                            fr.write('\t\t\tstatistic= "' +  mtstat + '"\n')
                            fr.write('\t\t\tthreshold = "' +  mtthres + '"\n')
                            fr.write('\t\t\ttime_aggregation = "' +  mtta + '"\n')
                            fr.write('\t\t\ttime_grain = "'PTM"' mttg2 + '"\n')
                            fr.write('\t\t\ttime_window = "'PTM"' mttw2 + '"\n')  
                                                                                                                                                                      
                            fr.write('\t\t}' + '"\n')
                            # scale action
                            sac=azr[i]["profiles[j]["rules[k]["scaleAction.cooldown"]
                            sad=azr[i]["profiles[j]["rules[k]["scaleAction.direction"]
                            sat=azr[i]["profiles[j]["rules[k]["scaleAction.type"]
                            sav=azr[i]["profiles[j]["rules[k]["scaleAction.value"]
                            fr.write('\t\tscale_action  {' + '"\n')
                            sac2=print sac | cut -f2 -d':' | sed 's/^0*//'
                    
                            fr.write('\t\t\tcooldown = "'PTM"' sac2 + '"\n')
                           
                            fr.write('\t\t\tdirection = "' +  sad + '"\n')
                            fr.write('\t\t\ttype = "' +  sat + '"\n')
                            fr.write('\t\t\tvalue = "' +  sav + '"\n')
                            fr.write('\t\t}' + '"\n')

                            fr.write('\t}' + '"\n') # end rule
                        
                      
            fr.write('}' + '"\n')  # end profile
            

        fi

# notification block
        icount=print nots | jq '. | length'
        if icount" -gt "0" :
            icount=expr icount - 1
            for j in range( 0 icount):
                nsa=azr[i]["notifications[i]["email.sendToSubscriptionAdministrator"]
                nsca=azr[i]["notifications[i]["email.sendToSubscriptionCoAdministrator"]
                nce=azr[i]["notifications[i]["email.customEmails"
                nwh=azr[i]["notifications[i]["webhooks"
                fr.write('notification {'  + '"\n')
                fr.write('\temail {'  + '"\n')
                print nsa
                if nsa" != "null" :
                fr.write('\t\tsend_to_subscription_administrator =   nsa + '"\n')
                fi
                if nsca" != "null" :
                fr.write('\t\tsend_to_subscription_co_administrator =   nsca + '"\n')
                fi
                fr.write('\t\tcustom_emails =   "nce" + '"\n')
                fr.write('\t}' + '"\n')
                fr.write('webhook =   "nwh" + '"\n')
                fr.write('}' + '"\n')
            
        fi

    
        #
        # Tags used internally
 
        
# finish

        fr.write('}' + '"\n')
        cat outfile

        statecomm=fr.write('terraform state rm . + '__' + " tfp rg rname
        print statecomm >> tf-staterm.sh
        eval statecomm
        evalcomm=fr.write('terraform import . + '__' +  " tfp rg rname id
        print evalcomm >> tf-stateimp.sh
        eval evalcomm
    
fi
