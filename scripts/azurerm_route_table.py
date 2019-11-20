def azurerm_route_table(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    #  030 Route Table
    tfp="azurerm_route_table"
    azr=""
    # debug - uncomment this line
    # cde=True
    if crf in tfp:
        # REST
        # print "REST ASG"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/routeTables"
        params = {'api-version': '2018-07-01'}
        r=requests.get(url, headers=headers, params=params)
        azr=r.json()["value"]



    #############
        tfrmf="030-"+tfp+"-staterm.sh"
        tfimf="030-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):
            try:
                name=azr[i]["name"]
                loc=azr[i]["location"]
                id=azr[i]["id"]
                rg=id.split("/")[4].replace(".","-").lower()
                if rg[0].isdigit(): rg="rg_"+rg
                rgs=id.split("/")[4]   
            except KeyError:
                continue

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
            fr.write("")
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')   

        #
            # Interate routes
            #
            routes=azr[i]["properties"]["routes"]
            rcount=len(routes)
            for j in range(0, rcount):
                rtname=routes[j]["name"]
                adpr=routes[j]["properties"]["addressPrefix"]
                nhtype=routes[j]["properties"]["nextHopType"]

                fr.write('\t route {' + '\n')
                fr.write('\t\t name = "' + rtname + '"\n')
                fr.write('\t\t address_prefix = "' + adpr + '"\n')
                fr.write('\t\t next_hop_type = "' + nhtype + '"\n')
                try:
                    nhaddr=routes[j]["properties"]["nextHopIpAddress"]
                    fr.write('\t\t next_hop_in_ip_address = "' +  nhaddr + '"\n')
                except KeyError:
                    pass             
                fr.write('\t }' + '\n')

        # tags block
            
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                    #print tval
                #print(json.dumps(mtags, indent=4, separators=(',', ': ')))
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
    #end route table