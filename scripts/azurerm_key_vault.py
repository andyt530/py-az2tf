def azurerm_key_vault(crf,cde,crg,headers,requests,sub,json,az2tfmess,subprocess):
    #############
    #  090 key vault
    tfp="azurerm_key_vault"
    azr=""
    if crf in tfp:
        # REST or cli
        p = subprocess.Popen('az keyvault list -o json', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, errors = p.communicate()
        azr=json.loads(output)
        if cde:
            print(json.dumps(azr, indent=4, separators=(',', ': ')))
        tfrmf="090-"+tfp+"-staterm.sh"
        tfimf="090-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print tfp,
        count=len(azr)
        print count
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-")

            if crg is not None:
                if rg.lower() != crg.lower():
                    continue  # back to for
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write("")
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rg + '"\n')
            comm="az keyvault show -n "+name+" -o json"
            print comm
            p = subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output, errors = p.communicate()
            kvshow=json.loads(output)
            #jcount=len(kvshow)
            print(json.dumps(kvshow, indent=4, separators=(',', ': ')))

            sku=kvshow["properties"]["sku"]["name"]
            #if sku" = "premium" : sku="Premium" ; fi
            #if sku" = "standard" : sku="Standard" ; fi
    
            fr.write('\t sku {' + '\n')     
            fr.write('\t\t name="' + sku + '"\n')
            fr.write('\t }' + '\n')

            ten=kvshow["properties"]["tenantId"]     
            fr.write('\t tenant_id="' + ten + '"\n')

            try: 
                endep=str(kvshow["properties"]["enabledForDeployment"])
                fr.write('\t enabled_for_deployment="' +  endep + '"\n')
            except KeyError:
                pass
            
            try:
                endisk=str(kvshow["properties"]["enabledForDiskEncryption"])
                fr.write('\t enabled_for_disk_encryption="' +  endisk + '"\n')
            except KeyError:
                pass       
            
            try:
                entemp=str(kvshow["properties"]["enabledForTemplateDeployment"])
                fr.write('\t enabled_for_template_deployment="' +  entemp + '"\n')
            except KeyError:
                pass

            ap=kvshow["properties"]["accessPolicies"]
                    
            #
            # Access Policies
            #
            pcount=len(ap)
            for j in range(0, pcount):    
                fr.write('\t access_policy {' + '\n')
                apten=kvshow["properties"]["accessPolicies"][j]["tenantId"]           
                fr.write('\t\t tenant_id="' + apten + '"\n')
                apoid=kvshow["properties"]["accessPolicies"][j]["objectId"]
                fr.write('\t\t object_id="' + apoid + '"\n')
                    
                jkl=kvshow["properties"]["accessPolicies"][j]["permissions"]["keys"]
                jsl=kvshow["properties"]["accessPolicies"][j]["permissions"]["secrets"]
                jcl=kvshow["properties"]["accessPolicies"][j]["permissions"]["certificates"]
                    
                kl=len(jkl)
                sl=len(jsl)
                cl=len(jcl)
                print kl  
                fr.write('\t\t key_permissions = [ \n')
                for k in range(0,kl):
                    tk=kvshow["properties"]["accessPolicies"][j]["permissions"]["keys"][k]
                    fr.write('\t\t\t "' + tk + '",\n')
                fr.write('\t\t ]\n')

                print sl  
                fr.write('\t\t secret_permissions = [ \n')
                for k in range(0,sl):
                    tk=kvshow["properties"]["accessPolicies"][j]["permissions"]["secrets"][k]
                    fr.write('\t\t\t "' + tk + '",\n')
                fr.write('\t\t ]\n')
                
                print cl  
                fr.write('\t\t certificate_permissions = [ \n')
                for k in range(0,cl):
                    tk=kvshow["properties"]["accessPolicies"][j]["permissions"]["certificates"][k]
                    fr.write('\t\t\t "' + tk + '",\n')
                fr.write('\t\t ]\n')                          
                fr.write('\t} \n') # end access policy

            
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

            

            fr.write('} \n')
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
    #end key vault