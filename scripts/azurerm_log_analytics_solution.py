# azurerm_log_analytics_solution
def azurerm_log_analytics_solution(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_log_analytics_solution"
    tcode="330-"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST solutions"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.OperationsManagement/solutions"
        params = {'api-version': '2015-11-01-preview'}
        #2015-11-01-preview
        r = requests.get(url, headers=headers, params=params)
        
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]

            skip="false"
            #print id
            if "[" in id or "]" in id :
                print ("Skipping this soluion "+ name+ " can't process currently")
                skip="true"
                return


            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            rname=rname.replace("(","-")  #| sed s/\(/-/
            rname=rname.replace(")","-") # | sed s/\)/-/

            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            #fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

            pname= name
            name= name.replace("(","-")  #| sed s/\(/-/
            name= name.replace(")","-") # | sed s/\)/-/
   

           
            pub=azr[i]["plan"]["publisher"]
            prod=azr[i]["plan"]["product"]
            soln=azr[i]["plan"]["product"].split("/")[1]
            workname=azr[i]["properties"]["workspaceResourceId"].split("/")[8]
            workn1=azr[i]["name"].split("(")[1]
            workn= workn1.split(")")[0]
            workid=azr[i]["properties"]["workspaceResourceId"]
            
            if skip != "true" :
                
                fr.write('\t solution_name = "' +  soln + '"\n')
                fr.write('\t workspace_name = "' +  workn + '"\n')
                fr.write('\t workspace_resource_id = "' +  workid + '"\n')
                
                fr.write('\t plan {\n')
                fr.write('\t\t publisher =  "'+pub + '"\n')
                fr.write('\t\t product = "' + prod + '"\n')
                fr.write('\t }\n')

# tags cause errors                
                

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' "'+id+'"\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
