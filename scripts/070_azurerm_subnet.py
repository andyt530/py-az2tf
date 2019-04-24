
#
#
vnets=az network vnet list -g rgsource -o json
count=print vnets | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for j in range( 0 count):
        vname=print vnets | jq ".[j]["name"]
        #
        azr=az network vnet subnet list -g rgsource --vnet-name vname -o json
        scount=print azr | jq '. | length'
        scount=expr scount - 1
        for i in range( 0 scount):
            name=azr[i]["name"]
            rname=print name | sed 's/\./-/g'
            rg=azr[i]["resourceGroup" | sed 's/\./-/g']
            id=azr[i]["id"]
            # subnets don't have a location
            prefix=fr.write(' + '__' + " prefixa rg
            outfile=fr.write('. + '__' + .tf" tfp rg rname
            print az2tfmess > outfile

            sprefix=azr[i]["addressPrefix"]
            sep="null"
            rtbid="null"
            seps=azr[i]["serviceEndpoints"
            jcount=print seps | jq '. | length'
            jcount=expr jcount - 1
            print jcount
            print seps
            if seps" != "null" :
            if seps" != "[][" :
            sep="["
                    for j in range( 0 jcount):
                        service=print seps | jq ".[j]["service"]
                        if [ j -eq jcount ]["; : 
                            sep=fr.write('"' + " sep service
                        else
                            sep=fr.write('"' + ," sep service
                        fi
                    
            sep=fr.write('][" sep
            fi
            fi
            
            snsgid=azr[i]["networkSecurityGroup.id" | cut -f9 -d"/" | sed 's/\./-/g']
            snsgrg=azr[i]["networkSecurityGroup.id" | cut -f5 -d"/" | sed 's/\./-/g'] 
            rtbid=azr[i]["routeTable.id" | cut -f9 -d"/" | sed 's/\./-/g']
            rtrg=azr[i]["routeTable.id" | cut -f5 -d"/" | sed 's/\./-/g']

            fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
            fr.write('\t name = "' +  name + '"\n')
            fr.write('\t virtual_network_name = "' +  vname + '"\n')
            fr.write('\t address_prefix = "' +  sprefix + '"\n')
            fr.write('\t resource_group_name = "' +  rgsource + '"\n')
            

            if snsgrg" != "null" :
                fr.write('\t network_security_group_id = "'\{'azurerm_network_security_group. + '__' + .id}'"' snsgrg snsgid + '"\n')
            fi
            if sep" != "null" :

                fr.write('\t service_endpoints =  sep + '"\n')
            fi
            if rtrg" != "null" :
                fr.write('\t route_table_id = "'\{'azurerm_route_table. + '__' + .id}'"' rtrg rtbid + '"\n')
            fi

            fr.write('}' + '"\n')
            cat outfile

# azurerm_subnet_network_security_group_association
     
            r1="skip"
            if snsgid" != "null" :
                r1="azurerm_subnet_network_security_group_association"
                outsnsg=fr.write('. + '__' +  + '__' + .tf" r1 rg rname snsgid
                print az2tfmess > outsnsg
                fr.write('resource "' +  "' + '__' +  + '__' + "' {' r1 rg rname snsgid  >> outsnsg
                fr.write('\tsubnet_id = "'\{'azurerm_subnet. + '__' + .id}'"' rg rname >> outsnsg
                fr.write('\tnetwork_security_group_id = "'\{'azurerm_network_security_group. + '__' + .id}'"' snsgrg snsgid >> outsnsg
                fr.write('}' >> outsnsg
                cat outsnsg
            fi

# azurerm_subnet_route_table_association

            r2="skip"
            if rtbid" != "null" :
                r2="azurerm_subnet_route_table_association"
                outrtbid=fr.write('. + '__' +  + '__' + .tf" r2 rg rname rtbid
                print az2tfmess > outrtbid
                fr.write('resource "' +  "' + '__' +  + '__' + "' {' r2 rg rname rtbid >> outrtbid
                fr.write('\tsubnet_id = "'\{'azurerm_subnet. + '__' + .id}'"' rg rname >> outrtbid
                fr.write('\troute_table_id = "'\{'azurerm_route_table. + '__' + .id}'"' rtrg rtbid >> outrtbid
                fr.write('}' >> outrtbid
                cat outrtbid
            fi


# azurerm_subnet_network_security_group_association

            if r1" != "skip" :
            statecomm=fr.write('terraform state rm . + '__' +  + '__' + " r1 rg rname snsgid
            print statecomm >> tf-staterm.sh
            eval statecomm
            evalcomm=fr.write('terraform import . + '__' +  + '__' +  " r1 rg rname snsgid id # uses subnet id
            print evalcomm >> tf-stateimp.sh
            eval evalcomm
            fi

# azurerm_subnet_route_table_association

            if r2" != "skip" :
            statecomm=fr.write('terraform state rm . + '__' +  + '__' + " r2 rg rname rtbid
            print statecomm >> tf-staterm.sh
            eval statecomm
            evalcomm=fr.write('terraform import . + '__' +  + '__' +  " r2 rg rname rtbid id  # uses subnet id
            print evalcomm >> tf-stateimp.sh
            eval evalcomm
            fi

# azurerm_subnet

            statecomm=fr.write('terraform state rm . + '__' + " tfp rg rname
            print statecomm >> tf-staterm.sh
            eval statecomm
            evalcomm=fr.write('terraform import . + '__' +  " tfp rg rname id
            print evalcomm >> tf-stateimp.sh
            eval evalcomm
        
    
fi
