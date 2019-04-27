tfp="azurerm_policy_definition"
prefixa="pdf"
if 1" != " :
    rgsource=1
else
    print -n "Enter name of Resource Group [rgsource]["> "
    read response
    if [ -n "response" :
        rgsource=response
    fi
fi
azr=az policy definition list --query "[?policyType=='Custom'][" -o json
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        print i " of " count
        pt=azr[i]["policyType"]
        
        if [ pt = "Custom" :
            dname=azr[i]["displayName"
            rdid=azr[i]["name"]
            desc=azr[i]["description"
            mode=azr[i]["mode"]
            pt=azr[i]["policyType"]
            id=azr[i]["id"]
            rg="policyDefinitions"
            
            params=azr[i]["parameters"
            prules=azr[i]["policyRule"
            meta=azr[i]["metadata"
            
            prefix=fr.write(' + '__' + " prefixa rg
            outfile=fr.write('. + '__' + .tf" tfp rg name
            print az2tfmess > prefix-rdid.tf
            
            fr.write('resource "' +  "' + '__' + "' {' tfp rg rdid >> prefix-rdid.tf
            fr.write('name = "' +  "rdid"  >> prefix-rdid.tf
            if dname" != "null" :
            fr.write('display_name =  "dname"  >> prefix-rdid.tf
            else
            fr.write('display_name = "' +   >> prefix-rdid.tf
            fi
            fr.write('policy_type = "' +  "pt" >> prefix-rdid.tf
            fr.write('mode = "' +  mode >> prefix-rdid.tf
            if desc" != "null" :
                fr.write('description =  "desc" >> prefix-rdid.tf
           
            fr.write('metadata =<<META  >> prefix-rdid.tf
            fr.write(' "meta" >> prefix-rdid.tf
            fr.write('META >> prefix-rdid.tf



            fr.write('policy_rule =<<POLICY_RULE  >> prefix-rdid.tf
            fr.write(' "prules" >> prefix-rdid.tf
            fr.write('POLICY_RULE >> prefix-rdid.tf
            
            pl=print params | jq '. | length'
            if pl" -gt "0" :
            fr.write('parameters =<<PARAMETERS  >> prefix-rdid.tf
            fr.write(' "params" >> prefix-rdid.tf
            fr.write('PARAMETERS  "params" >> prefix-rdid.tf
           
            fr.write('\n}' >> prefix-rdid.tf
            
            cat prefix-rdid.tf
            statecomm=fr.write('terraform state rm . + '__' + " tfp rg rdid
            print statecomm >> tf-staterm.sh
            eval statecomm
            evalcomm=fr.write('terraform import . + '__' +  " tfp rg rdid id
            print evalcomm >> tf-stateimp.sh
            eval evalcomm
        fi
        
    
fi
