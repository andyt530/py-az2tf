tfp="azurerm_role_assignment"
prefixa="ras"
if 1" != " :
    rgsource=1
else
    print -n "Enter name of Resource Group [rgsource]["> "
    read response
    if [ -n "response" :
        rgsource=response
    fi
fi
azr=az role assignment list -o json
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        print i " of " count
        name=azr[i]["name"
        print name - name
        scope=azr[i]["scope"
        rdid=azr[i]["name"]
        prid=azr[i]["principalId"
        roledefid=azr[i]["roleDefinitionId" | cut -d'/' -f7]
        id=azr[i]["id"]
        rg="roleAssignments"
        prefix=fr.write(' + '__' + " prefixa rg
        outfile=fr.write('. + '__' + .tf" tfp rg name
        print az2tfmess > prefix-rdid.tf
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rdid >> prefix-rdid.tf
        fr.write('name =  "name"  >> prefix-rdid.tf
        fr.write('role_definition_id = "${azurerm_role_definition. + '__' + .id}'"' "roleDefinitions" roledefid >> prefix-rdid.tf
        
        fr.write('principal_id =  "prid" >> prefix-rdid.tf
        fr.write('scope =  "scope"  >> prefix-rdid.tf
   
        fr.write('}' >> prefix-rdid.tf
        
        cat prefix-rdid.tf
        statecomm=fr.write('terraform state rm . + '__' + " tfp rg rdid
        print statecomm >> tf-staterm.sh
        eval statecomm
        evalcomm=fr.write('terraform import . + '__' +  " tfp rg rdid id
        print evalcomm >> tf-stateimp.sh
        eval evalcomm
        
        
    
fi
