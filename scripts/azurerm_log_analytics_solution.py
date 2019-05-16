# azurerm_log_analytics_solution
def azurerm_log_analytics_solution(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    tfp="azurerm_log_analytics_solution"
    tcode="330-"
    azr=""
    if crf in tfp:
    # REST or cli
        print "REST Managed Disk"
        url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Compute/disks"
        params = {'api-version': '2017-03-30'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]
        if cde:
            print(json.dumps(azr, indent=4, separators=(',', ': ')))

        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
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
            rgs=id.split("/")[4]
            if crg is not None:
                if rg.lower() != crg.lower():
                    continue  # back to for
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

    ###############
    # specific code start
    ###############

            

            pname= name
            name= name | sed s/\(/-/
            name= name | sed s/\)/-/
            
            
            id=az"]["id"]
            skip="false"
            if [[ id = *"]["* ]["; :
                echo "Skipping this soluion pname - can't process currently"
                skip="true"
           


            pub=azrplan.publisher"
            prod=azrplan.product"]
            soln=azrplan.product" | cut -f2 -d'/']
            workname=azrproperties.workspaceResourceId"].split("/")[8]
            workn1=azrname" | cut -d'(' -f2
            workn= workn1 | cut -d')' -f1
            workid=azrproperties.workspaceResourceId"]
            echo "workname=workn"
            
            
            if skip != "true" :
                

                fr.write('\t solution_name = "' +  soln + '"\n')
                fr.write('\t workspace_name = "' +  workn + '"\n')
                fr.write('\t workspace_resource_id = "' +  workid + '"\n')
                
                fr.write('\t plan {'  + '"\n')
                fr.write('\t\t publisher =  "pub" + '"\n')
                fr.write('\t\t product = "' +  "prod" + '"\n')
                fr.write('\t }'  + '"\n')

# tags cause errors                
                

            fr.write('}\n') 
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
    #end stub
