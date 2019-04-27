tfp="azurerm_policy_assignment"
prefixa="pas"
if 1" != " :
    rgsource=1
else
    print -n "Enter name of Resource Group [rgsource]["> "
    read response
    if [ -n "response" :
        rgsource=response
    fi
fi
azr=az policy assignment list -o json
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        
        dname=azr[i]["displayName"
        rdid=azr[i]["name"]
        desc=azr[i]["description"
        scope=azr[i]["scope"]
        pdid=azr[i]["policyDefinitionId"]
        id=azr[i]["id"]
        rg="policyAssignments"
        
        params=azr[i]["parameters"
              
        prefix=fr.write(' + '__' + " prefixa rg
        outfile=fr.write('. + '__' + .tf" tfp rg name
        print az2tfmess > prefix-rdid.tf
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rdid >> prefix-rdid.tf
        fr.write('name = "' +  "rdid"  >> prefix-rdid.tf
        fr.write('display_name =  "dname"  >> prefix-rdid.tf
        fr.write('policy_definition_id = "' +  "pdid" >> prefix-rdid.tf
        fr.write('scope = "' +  scope >> prefix-rdid.tf
        if desc" != "null" :
            fr.write('description =  "desc" >> prefix-rdid.tf
        fi
        pl=print params | jq '. | length'
        if pl" -gt "0" :
            fr.write('parameters =<<PARAMETERS  >> prefix-rdid.tf
            fr.write(' "params" >> prefix-rdid.tf
            fr.write('PARAMETERS  "params" >> prefix-rdid.tf
        fi
        fr.write('\n}' >> prefix-rdid.tf
        
        cat prefix-rdid.tf
        statecomm=fr.write('terraform state rm . + '__' + " tfp rg rdid
        print statecomm >> tf-staterm.sh
        eval statecomm
        evalcomm=fr.write('terraform import . + '__' +  " tfp rg rdid id
        print evalcomm >> tf-stateimp.sh
        eval evalcomm
        
        
    
fi
