prefixa=`echo $0 | awk -F 'azurerm_' '{print $2}' | awk -F '.sh' '{print $1}' `
tfp=`printf "azurerm_%s" $prefixa`

if [ "$1" != "" ]; then
    rgsource=$1
else
    echo -n "Enter name of Resource Group [$rgsource] > "
    read response
    if [ -n "$response" ]; then
        rgsource=$response
    fi
fi
azr=`az monitor autoscale list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`

        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        en=`echo $azr | jq ".[(${i})].enabled" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location" | tr -d '"'`
        profs=`echo $azr | jq ".[(${i})].profiles"`
        nots=`echo $azr | jq ".[(${i})].notifications"`
        trrg=`echo $azr | jq ".[(${i})].targetResourceUri" | cut -d'/' -f5 | sed 's/\./-/g' | tr -d '"'`
        trty=`echo $azr | jq ".[(${i})].targetResourceUri" | cut -d'/' -f7 | sed 's/\./-/g' | tr -d '"'`
        trid=`echo $azr | jq ".[(${i})].targetResourceUri" | cut -d'/' -f9 | sed 's/\./-/g' | tr -d '"'`
        # assume trty = Microsoft.Compute
        tftyp="azurerm_virtual_machine_scale_set"
        if [ $trty = "Microsoft-Web" ]; then
            tftyp="azurerm_app_service_plan"
        fi
        echo "$trty  $tftyp"

        prefix=`printf "%s__%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
        echo $az2tfmess > $outfile

        #
# basic settings 
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
        printf "name = \"%s\"\n" $name >> $outfile
        printf "enabled = \"%s\"\n" $en >> $outfile
        printf "location = \"%s\"\n"  "$loc" >> $outfile
        printf "resource_group_name = \"%s\"\n"  $rgsource >> $outfile
        if [ "$trrg" != "null" ]; then
        printf "target_resource_id = \"\${%s.%s__%s.id}\"\n" $tftyp $trrg $trid >> $outfile      
        fi


#  profiles block
        
        icount=`echo $profs | jq '. | length'`
        if [ "$icount" -gt "0" ]; then
            icount=`expr $icount - 1`
            for j in `seq 0 $icount`; do
                printf "profile {\n" >> $outfile
                pn=`echo $azr | jq ".[(${i})].profiles[(${j})].name"`
                cdef=`echo $azr | jq ".[(${i})].profiles[(${j})].capacity.default" | tr -d '"'`
                cmin=`echo $azr | jq ".[(${i})].profiles[(${j})].capacity.minimum" | tr -d '"'`
                cmax=`echo $azr | jq ".[(${i})].profiles[(${j})].capacity.maximum" | tr -d '"'`
                printf "\tname = %s\n" "$pn" >> $outfile
 # capacity
                printf "\tcapacity {\n" >> $outfile
                printf "\t\tdefault = \"%s\"\n" $cdef >> $outfile
                printf "\t\tminimum = \"%s\"\n" $cmin >> $outfile
                printf "\t\tmaximum = \"%s\"\n" $cmax >> $outfile
                printf "\t}\n" >> $outfile
# fixed date

                fd=`echo $azr | jq ".[(${i})].profiles[(${j})].fixedDate.end"`
                fdend=`echo $azr | jq ".[(${i})].profiles[(${j})].fixedDate.end" | tr -d '"'`
                fdstart=`echo $azr | jq ".[(${i})].profiles[(${j})].fixedDate.start" | tr -d '"'`
                fdtz=`echo $azr | jq ".[(${i})].profiles[(${j})].fixedDate.timeZone"`
                fdend2=`echo $fdend | cut -f1 -d'+'`
                fdstart2=`echo $fdstart | cut -f1 -d'+'`
                
                if [ "$fd" != "null" ]; then
                printf "\tfixed_date {\n" >> $outfile
                printf "\t\ttimezone = %s\n" "$fdtz" >> $outfile
                printf "\t\tstart = \"%sZ\"\n" $fdstart2 >> $outfile
                printf "\t\tend = \"%sZ\"\n" $fdend2 >> $outfile
                printf "\t}\n" >> $outfile
                fi
# recurance
                rec=`echo $azr | jq ".[(${i})].profiles[(${j})].recurrence"`
                if [ "$rec" != "null" ]; then
                rfr=`echo $azr | jq ".[(${i})].profiles[(${j})].recurrence.frequency"| tr -d '"'`
                rsd=`echo $azr | jq ".[(${i})].profiles[(${j})].recurrence.schedule.days"`
                rsh=`echo $azr | jq ".[(${i})].profiles[(${j})].recurrence.schedule.hours"`
                rsm=`echo $azr | jq ".[(${i})].profiles[(${j})].recurrence.schedule.minutes"`
                rst=`echo $azr | jq ".[(${i})].profiles[(${j})].recurrence.schedule.timeZone"| tr -d '"'`
                printf "\trecurrence {\n" >> $outfile
                printf "\t\ttimezone = \"%s\"\n" $rst >> $outfile
                printf "\t\tdays = %s\n" "$rsd" >> $outfile
                printf "\t\thours = %s\n" "$rsh" >> $outfile
                printf "\t\tminutes = %s\n" "$rsm" >> $outfile            
                printf "\t}\n" >> $outfile
                fi
# rules

                rules=`echo $azr | jq ".[(${i})].profiles[(${j})].rules"`

                kcount=`echo $rules | jq '. | length'`
                if [ "$kcount" -gt "0" ]; then
                    kcount=`expr $kcount - 1`
                        for k in `seq 0 $kcount`; do
                            printf "\trule  {\n" >> $outfile
                            # metric trigger
                            mtn=`echo $azr | jq ".[(${i})].profiles[(${j})].rules[(${k})].metricTrigger.metricName" | tr -d '"'`              
                            if [ "$mtn" = "CPU" ]; then 
                                mtn="Percentage CPU"
                            fi
                            mtid=`echo $azr | jq ".[(${i})].profiles[(${j})].rules[(${k})].metricTrigger.metricResourceUri" | tr -d '"'`
                            mtrrg=`echo $azr | jq ".[(${i})].profiles[(${j})].rules[(${k})].metricTrigger.metricResourceUri" | cut -d'/' -f5 | sed 's/\./-/g' | tr -d '"'`
                            mtrid=`echo $azr | jq ".[(${i})].profiles[(${j})].rules[(${k})].metricTrigger.metricResourceUri" | cut -d'/' -f9 | sed 's/\./-/g' | tr -d '"'`
                            mtop=`echo $azr | jq ".[(${i})].profiles[(${j})].rules[(${k})].metricTrigger.operator" | tr -d '"'`
                            mtstat=`echo $azr | jq ".[(${i})].profiles[(${j})].rules[(${k})].metricTrigger.statistic" | tr -d '"'`
                            mtthres=`echo $azr | jq ".[(${i})].profiles[(${j})].rules[(${k})].metricTrigger.threshold" | tr -d '"'`
                            mtta=`echo $azr | jq ".[(${i})].profiles[(${j})].rules[(${k})].metricTrigger.timeAggregation" | tr -d '"'`
                            mttg=`echo $azr | jq ".[(${i})].profiles[(${j})].rules[(${k})].metricTrigger.timeGrain" | tr -d '"'`
                            mttw=`echo $azr | jq ".[(${i})].profiles[(${j})].rules[(${k})].metricTrigger.timeWindow" | tr -d '"'`
                            mttg2=`echo $mttg | cut -f2 -d':' | sed 's/^0*//'`
                            mttw2=`echo $mttw | cut -f2 -d':' | sed 's/^0*//'`                           
                            printf "\t\tmetric_trigger {\n" >> $outfile
                            printf "\t\t\tmetric_name = \"%s\"\n" "$mtn" >> $outfile
                            printf "\t\t\tmetric_resource_id = \"\${%s.%s__%s.id}\"\n" $tftyp $mtrrg $mtrid >> $outfile
                            printf "\t\t\toperator = \"%s\"\n" $mtop >> $outfile
                            printf "\t\t\tstatistic= \"%s\"\n" $mtstat >> $outfile
                            printf "\t\t\tthreshold = \"%s\"\n" $mtthres >> $outfile
                            printf "\t\t\ttime_aggregation = \"%s\"\n" $mtta >> $outfile
                            printf "\t\t\ttime_grain = \"PT%sM\"\n" $mttg2 >> $outfile
                            printf "\t\t\ttime_window = \"PT%sM\"\n" $mttw2 >> $outfile  
                                                                                                                                                                      
                            printf "\t\t}\n" >> $outfile
                            # scale action
                            sac=`echo $azr | jq ".[(${i})].profiles[(${j})].rules[(${k})].scaleAction.cooldown" | tr -d '"'`
                            sad=`echo $azr | jq ".[(${i})].profiles[(${j})].rules[(${k})].scaleAction.direction" | tr -d '"'`
                            sat=`echo $azr | jq ".[(${i})].profiles[(${j})].rules[(${k})].scaleAction.type" | tr -d '"'`
                            sav=`echo $azr | jq ".[(${i})].profiles[(${j})].rules[(${k})].scaleAction.value" | tr -d '"'`
                            printf "\t\tscale_action  {\n" >> $outfile
                            sac2=`echo $sac | cut -f2 -d':' | sed 's/^0*//'`
                    
                            printf "\t\t\tcooldown = \"PT%sM\"\n" $sac2 >> $outfile
                           
                            printf "\t\t\tdirection = \"%s\"\n" $sad >> $outfile
                            printf "\t\t\ttype = \"%s\"\n" $sat >> $outfile
                            printf "\t\t\tvalue = \"%s\"\n" $sav >> $outfile
                            printf "\t\t}\n" >> $outfile

                            printf "\t}\n" >> $outfile # end rule
                        done
                fi        
            printf "}\n" >> $outfile  # end profile
            done

        fi

# notification block
        icount=`echo $nots | jq '. | length'`
        if [ "$icount" -gt "0" ]; then
            icount=`expr $icount - 1`
            for j in `seq 0 $icount`; do
                nsa=`echo $azr | jq ".[(${i})].notifications[(${i})].email.sendToSubscriptionAdministrator" | tr -d '"'`
                nsca=`echo $azr | jq ".[(${i})].notifications[(${i})].email.sendToSubscriptionCoAdministrator" | tr -d '"'`
                nce=`echo $azr | jq ".[(${i})].notifications[(${i})].email.customEmails"`
                nwh=`echo $azr | jq ".[(${i})].notifications[(${i})].webhooks"`
                printf "notification {\n"  >> $outfile
                printf "\temail {\n"  >> $outfile
                echo $nsa
                if [ "$nsa" != "null" ]; then
                printf "\t\tsend_to_subscription_administrator = %s \n" $nsa >> $outfile
                fi
                if [ "$nsca" != "null" ]; then
                printf "\t\tsend_to_subscription_co_administrator = %s \n" $nsca >> $outfile
                fi
                printf "\t\tcustom_emails = %s \n" "$nce" >> $outfile
                printf "\t}\n" >> $outfile
                printf "webhook = %s \n" "$nwh" >> $outfile
                printf "}\n" >> $outfile
            done
        fi

    
        #
        # Tags used internally
 
        
# finish

        printf "}\n" >> $outfile
        cat $outfile

        statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $rname`
        echo $statecomm >> tf-staterm.sh
        eval $statecomm
        evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $rname $id`
        echo $evalcomm >> tf-stateimp.sh
        eval $evalcomm
    done
fi
