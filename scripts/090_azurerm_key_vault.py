
azr=az keyvault list -g rgsource -o json
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        name=azr[i]["name"]
        rname=print name | sed 's/\./-/g'
        rg=azr[i]["resourceGroup" | sed 's/\./-/g']

        kvshow=az keyvault show -n name -o json
        id=azr[i]["id"]
        loc=azr[i]["location"
        
        sku=print kvshow | jq ".properties.sku.name"]
        #if sku" = "premium" : sku="Premium" ; fi
        #if sku" = "standard" : sku="Standard" ; fi

        ten=print kvshow | jq ".properties.tenantId"]
        
        endep=print kvshow | jq ".properties.enabledForDeployment"]
        endisk=print kvshow | jq ".properties.enabledForDiskEncryption"]
        entemp=print kvshow | jq ".properties.enabledForTemplateDeployment"]
        
        #print tags | jq .
        ap=print kvshow | jq ".properties.accessPolicies"
        
        prefix=fr.write(' + '__' + " prefixa rg
        outfile=fr.write('. + '__' + .tf" tfp rg rname
        print az2tfmess > outfile

        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('location =  "loc" + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        #
        fr.write('\t sku {'  + '"\n')
        
        fr.write('\t\t name="' +  sku + '"\n')
        fr.write('\t }'  + '"\n')
        
        fr.write('\t tenant_id="' +  ten + '"\n')
        if endep" != "null" :
            fr.write('\t enabled_for_deployment="' +  endep + '"\n')
        fi
        if endisk" != "null" ]["; :
            fr.write('\t enabled_for_disk_encryption="' +  endisk + '"\n')
        fi
        if entemp" != "null" :
        fr.write('\t enabled_for_template_deployment="' +  entemp + '"\n')
        fi
        #
        # Access Policies
        #
        pcount=print ap | jq '. | length'
        if pcount" -gt "0" :
            
            pcount=expr pcount - 1
            for j in range( 0 pcount):
                
                fr.write('\taccess_policy {' + '"\n')
                
                apten=print kvshow | jq ".properties.accessPolicies[j]["tenantId"]
                apoid=print kvshow | jq ".properties.accessPolicies[j]["objectId"]
                
                fr.write('\t\t tenant_id="' +  apten + '"\n')
                fr.write('\t\t object_id="' +  apoid + '"\n')
                
                kl=print kvshow | jq ".properties.accessPolicies[j]["permissions.keys" | jq '. | length'
                sl=print kvshow | jq ".properties.accessPolicies[j]["permissions.secrets" | jq '. | length'
                cl=print kvshow | jq ".properties.accessPolicies[j]["permissions.certificates" | jq '. | length'
                
                kl=expr kl - 1
                sl=expr sl - 1
                cl=expr cl - 1
                
                fr.write('\t\t key_permissions = [ + '"\n')
                if kl" -ge "0" :
                    
                    for k in range( 0 kl):
                        tk=print kvshow | jq ".properties.accessPolicies[j]["permissions.keys[k]["
                        if [ k -lt kl :
                            tk=fr.write('," tk
                        fi
                        fr.write('\t\t\t tk + '"\n')
                    
                    #fr.write('\t\t ]["n" + '"\n')
                fi
                fr.write('\t\t ]["n" + '"\n')
                
                if sl" -ge "0" :
                    fr.write('\t\t secret_permissions = [ + '"\n')
                    for k in range( 0 sl):
                        tk=print kvshow | jq ".properties.accessPolicies[j]["permissions.secrets[k]["
                        if [ k -lt sl :
                            tk=fr.write('," tk
                        fi
                        fr.write('\t\t\t tk + '"\n')
                    
                    fr.write('\t\t ]["n" + '"\n')
                else
                    fr.write('\t\t secret_permissions = []["n" + '"\n')
            
                fi
                
                if cl" -ge "0" :
                    fr.write('\t\t certificate_permissions = [ + '"\n')
                    for k in range( 0 cl):
                        tk=print kvshow | jq ".properties.accessPolicies[j]["permissions.certificates[k]["
                        ttk=print tk]
                        if [ k -lt cl :
                            tk=fr.write('," tk   # add comma to all but last
                        fi
                        fr.write('\t\t\t tk + '"\n')                       
                    
                    fr.write('\t\t ]["n" + '"\n')
                            
                fr.write('\t}' + '"\n')
            
        fi
        
        fr.write('}' + '"\n')
                
        
    
fi
