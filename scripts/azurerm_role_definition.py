tfp="azurerm_role_definition"
prefixa="rdf"
if 1" != " :
    rgsource=1
else
    print -n "Enter name of Resource Group [rgsource]["> "
    read response
    if [ -n "response" :
        rgsource=response
    fi
fi
azr=az role definition list -o json
#azr=az role definition list --query "[?roleType!='BuiltInRole'][" -o json 
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        print i " of " count
        
        name=azr[i]["roleName"
 
        rdid=azr[i]["name"]
        desc=azr[i]["description"
        id=azr[i]["id"]
        rg="roleDefinitions"

        scopes=azr[i]["assignableScopes"
        dactions=azr[i]["permissions[0]["dataActions"
        ndactions=azr[i]["permissions[0]["notDataActions"
        actions=azr[i]["permissions[0]["actions"
        nactions=azr[i]["permissions[0]["notActions"

        prefix=fr.write(' + '__' + " prefixa rg
        outfile=fr.write('. + '__' + .tf" tfp rg name
        print az2tfmess > prefix-rdid.tf
        
 #      fr.write('data "'azurerm_subscription"' "'primary"' {'}'\n prefix-rdid.tf
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rdid >> prefix-rdid.tf
        fr.write('name =  "name"  >> prefix-rdid.tf
        fr.write('role_definition_id = "' +  >> prefix-rdid.tf
        fr.write('description =  "desc" >> prefix-rdid.tf
#        fr.write('scope = "${data.azurerm_subscription.primary.id}'"'  >> prefix-rdid.tf
#        fr.write('scope = "'/subscriptions/"' rgsource >> prefix-rdid.tf
        fr.write('scope = "' +   >> prefix-rdid.tf
        #
        fr.write('permissions {'  >> prefix-rdid.tf
    
        fr.write('data_actions =  >> prefix-rdid.tf
        fr.write(' dactions >> prefix-rdid.tf

        fr.write('not_data_actions =  >> prefix-rdid.tf
        fr.write(' ndactions >> prefix-rdid.tf

        fr.write('actions =  >> prefix-rdid.tf
        fr.write(' actions >> prefix-rdid.tf
    
        fr.write('not_actions =   >> prefix-rdid.tf
        fr.write(' nactions >> prefix-rdid.tf
    
        fr.write('}'  >> prefix-rdid.tf
        
        fr.write('assignable_scopes =   >> prefix-rdid.tf
        fr.write(' scopes >> prefix-rdid.tf
       
        fr.write('}' >> prefix-rdid.tf
        
        cat prefix-rdid.tf
        statecomm=fr.write('terraform state rm . + '__' + " tfp rg rdid
        print statecomm >> tf-staterm.sh
        eval statecomm
        evalcomm=fr.write('terraform import . + '__' +  " tfp rg rdid id
        print evalcomm >> tf-stateimp.sh
        eval evalcomm
        
        
    
fi
