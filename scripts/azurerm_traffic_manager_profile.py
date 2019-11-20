def azurerm_traffic_manager_profile(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    #  124 Traffic manager profile
    tfp="azurerm_traffic_manager_profile"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Traffic Manager Profile"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/trafficmanagerprofiles"
        params = {'api-version': '2017-05-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf="124-"+tfp+"-staterm.sh"
        tfimf="124-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            #loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            #fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

            trm=azr[i]["properties"]["trafficRoutingMethod"]
            fr.write('\t traffic_routing_method = "' +  trm + '"\n')
            ps=azr[i]["properties"]["profileStatus"]
            fr.write('\t profile_status = "' + ps + '"\n') 
        
            #dnsc=azr[i]["properties"]["dnsConfig"]
            #monc=azr[i]["properties"]["monitorConfig"]
                    

    # dns_config block

            rn=azr[i]["properties"]["dnsConfig"]["relativeName"]
            ttl=azr[i]["properties"]["dnsConfig"]["ttl"]
            
            if ttl == 0: 
                ttl=30
            
            fr.write('\t dns_config { \n')
            fr.write('\t\t relative_name = "' + rn + '"\n')
            #TF bug returning 0
            fr.write('\t\t ttl  = "' + str(ttl) + '"\n')
            fr.write('\t} \n')
            
    # monitor_config block

            prot=azr[i]["properties"]["monitorConfig"]["protocol"]
            port=azr[i]["properties"]["monitorConfig"]["port"]

            fr.write('\t monitor_config { \n')
            fr.write('\t\t protocol = "' + prot + '"\n')
            fr.write('\t\t port  = "' + str(port) + '"\n')
            try:
                path=azr[i]["properties"]["monitorConfig"]["path"]
                if path is not None:
                    fr.write('\t\t path  = "' + path + '"\n')
            except KeyError:
                pass
            fr.write('\t} \n')  
            


    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
        return azr
    #end traffic manager profile