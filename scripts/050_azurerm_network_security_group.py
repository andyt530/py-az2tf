prefixa=echo 0 | awk -F 'azurerm_' '{'print 2}'' | awk -F '.sh' '{'print 1}'' 
tfp=fr.write('azurerm_" prefixa
echo ftp
if 1" != " :
    rgsource=1
else
    echo -n "Enter name of Resource Group [rgsource]["> "
    read response
    if [ -n "response" :
        rgsource=response
    fi
fi
azr=az network nsg list -g rgsource -o json
#comm=fr.write('cat .json | jq '. | select (.[]["id | contains("' + ))'" tfp rgsource
#echo comm
#azr=eval comm
count=echo azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        name=azr[i]["name"]
        rname=echo name | sed 's/\./-/g'
        rg=azr[i]["resourceGroup" | sed 's/\./-/g']

        id=azr[i]["id"]
        loc=azr[i]["location"]
        srules=azr[i]["securityRules"

        prefix=fr.write(' + '__' + " prefixa rg
        outfile=fr.write('. + '__' + .tf" tfp rg rname
        echo az2tfmess > outfile
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +    "name" + '"\n')
        fr.write('\t location = "' +  loc + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        #
        # Security Rules
        #
        scount=echo srules | jq '. | length'
        #echo scount
        if scount" -gt "0" :
        scount=expr scount - 1
            for j in range( 0 scount):    
                      
            fr.write('\t security_rule {'  + '"\n')
            srname=azr[i]["securityRules[j]["name"]  
            echo "Security Rule srname   j of scount"                     
            fr.write('\t\t name = "' +    "srname" + '"\n')
            srdesc=azr[i]["securityRules[j]["description"                       
            if srdesc" != "null" :
                fr.write('\t\t description =  "srdesc" + '"\n')
            fi

            sraccess=azr[i]["securityRules[j]["access"]                       
            fr.write('\t\t access = "' +    sraccess + '"\n')
            srpri=azr[i]["securityRules[j]["priority"] 
            fr.write('\t\t priority = "' +    srpri + '"\n')
            srproto=azr[i]["securityRules[j]["protocol" 
            fr.write('\t\t protocol =    srproto + '"\n')
            srdir=azr[i]["securityRules[j]["direction"] 
            fr.write('\t\t direction = "' +    srdir + '"\n')

#source address block
            srsp=azr[i]["securityRules[j]["sourcePortRange" 
            if srsp" != "null" ]["then
            fr.write('\t\t source_port_range =    "srsp" + '"\n')
            fi
            srsps=azr[i]["securityRules[j]["sourcePortRanges" 
            if srsps" != "[][" ]["then
            fr.write('\t\t source_port_ranges =    "srsps" + '"\n')
            fi
            srsap=azr[i]["securityRules[j]["sourceAddressPrefix" 
            if srsap" != "null" ]["then
                fr.write('\t\t source_address_prefix =    "srsap" + '"\n')
            fi
            srsaps=azr[i]["securityRules[j]["sourceAddressPrefixes" 
            if srsaps" != "[][" ]["then
                fr.write('\t\t source_address_prefixes =    "srsaps" + '"\n')
            fi

# source asg's
            srsasgs=azr[i]["securityRules[j]["sourceApplicationSecurityGroups" 
            kcount=echo srsasgs | jq '. | length'
            if kcount" -gt "0" :
                kcount=expr kcount - 1
                for k in range( 0 kcount):
                    asgnam=azr[i]["securityRules[j]["sourceApplicationSecurityGroups[k]["id" | cut -d'/' -f9 | sed 's/\./-/g']
                    asgrg=azr[i]["securityRules[j]["sourceApplicationSecurityGroups[k]["id" | cut -d'/' -f5 | sed 's/\./-/g']    
                    fr.write('\t\t source_application_security_group_ids = ["'\{'azurerm_application_security_group. + '__' + .id}'"']["n" asgrg asgnam + '"\n')
                done
            fi

#destination address block
            
            srdp=azr[i]["securityRules[j]["destinationPortRange" 
            if srdp" != "null" ]["then
                fr.write('\t\t destination_port_range =    "srdp" + '"\n')
            fi
            srdps=azr[i]["securityRules[j]["destinationPortRanges" 
            if srdps" != "[][" ]["then
                fr.write('\t\t destination_port_ranges =   "srdps" + '"\n')
            fi
            srdap=azr[i]["securityRules[j]["destinationAddressPrefix" 
            if srdap" != "null" ]["then
            fr.write('\t\t destination_address_prefix =    "srdap" + '"\n')
            fi
            srdaps=azr[i]["securityRules[j]["destinationAddressPrefixes" 
            if srdaps" != "[][" ]["then
            fr.write('\t\t destination_address_prefixes =    "srdaps" + '"\n')
            fi

# destination asg's
            srdasgs=azr[i]["securityRules[j]["destinationApplicationSecurityGroups" 
            kcount=echo srdasgs | jq '. | length'
            if kcount" -gt "0" :
                kcount=expr kcount - 1
                for k in range( 0 kcount):
                    asgnam=azr[i]["securityRules[j]["destinationApplicationSecurityGroups[k]["id" | cut -d'/' -f9 | sed 's/\./-/g']
                    asgrg=azr[i]["securityRules[j]["destinationApplicationSecurityGroups[k]["id" | cut -d'/' -f5 | sed 's/\./-/g']    
                    fr.write('\t\t destination_application_security_group_ids = ["'\{'azurerm_application_security_group. + '__' + .id}'"']["n" asgrg asgnam + '"\n')
                done
            fi
            fr.write('\t}' + '"\n')
            done
        fi

            #
            # New Tags block v2
            tags=azr[i]["tags"
            tt=echo tags | jq .
            tcount=echo tags | jq '. | length'
            if tcount" -gt "0" :
                fr.write('\t tags {'  + '"\n')
                tt=echo tags | jq .
                keys=echo tags | jq 'keys'
                tcount=expr tcount - 1
                for j in range( 0 tcount):
                    k1=echo keys | jq ".[j]["
                    re="[[:space:]["+"
                    if [[ k1 =~ re ]["; then
                        tval=echo tt | jq ."k1"
                        tkey=echo k1]
                        fr.write('\t\t"' +  =   "tkey" "tval" + '"\n')
                    else
                        tval=echo tt | jq .k1
                        tkey=echo k1]
                        fr.write('\t\t =   tkey "tval" + '"\n')
                    fi
                done
                fr.write('\t}' + '"\n')
            fi

        fr.write('}' + '"\n')
        cat outfile
        statecomm=fr.write('terraform state rm . + '__' + " tfp rg rname
        echo statecomm >> tf-staterm.sh
        eval statecomm
        evalcomm=fr.write('terraform import . + '__' +  " tfp rg rname id
        echo evalcomm >> tf-stateimp.sh
        eval evalcomm
      
    done
fi
