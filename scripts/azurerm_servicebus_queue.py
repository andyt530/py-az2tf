# azurerm_servicebus_queue
def azurerm_servicebus_queue(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_servicebus_queue"
    tcode="510-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST namespace for queue"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.ServiceBus/namespaces"
        params = {'api-version': '2017-04-01'}
        r = requests.get(url, headers=headers, params=params)
        #print(json.dumps(r.json(), indent=4, separators=(',', ': ')))
        try:
            azr= r.json()["value"]
        except KeyError:
            if cde: print ("Found no Namespaces for Queues")
            return

        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            nname=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            rgs=id.split("/")[4]
            #print id
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
 
            url="https://management.azure.com/" + id + "/queues"
            params = {'api-version': '2017-04-01'}
            r = requests.get(url, headers=headers, params=params)
            #print(json.dumps(r.json(), indent=4, separators=(',', ': ')))
            try:
                azr2= r.json()["value"]
            except KeyError:
                print ("Found no SB Queues")
                return
            
            if cde:
                print(json.dumps(azr2, indent=4, separators=(',', ': ')))
        

    ###############
    # specific code start
    ###############
        
        
      
        #azr2=az servicebus queue list -g rgsource --namespace-name nname -o json
            icount=len(azr2)
            if icount > 0 :
                for j in range(0,icount):
                    name= azr2[j]["name"]
                    rname= name.replace(".","-")
                    id= azr2[j]["id"]
                    rg=id.split("/")[4].replace(".","-").lower()
                    if rg[0].isdigit(): rg="rg_"+rg
                    rgs=id.split("/")[4]

                    rname=name.replace(".","-")
                    prefix=tfp+"."+rg+'__'+rname
                    #print prefix
                    rfilename=prefix+".tf"
                    fr=open(rfilename, 'w')
                    fr.write(az2tfmess)
                    fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                    fr.write('\t name = "' + name + '"\n')
                   
                    fr.write('\t resource_group_name = "'+ rgs + '"\n')


                    ep= azr2[j]["properties"]["enablePartitioning"]
                    adoni= azr2[j]["properties"]["autoDeleteOnIdle"]
                    
                    ee= azr2[j]["properties"]["enableExpress"]
                    dd= azr2[j]["properties"]["requiresDuplicateDetection"]
                    rs= azr2[j]["properties"]["requiresSession"]
                    mx= azr2[j]["properties"]["maxSizeInMegabytes"]
                    dl= azr2[j]["properties"]["deadLetteringOnMessageExpiration"]
                    
                    fr.write('\t namespace_name = "' +  nname + '"\n')
                    fr.write('\t enable_partitioning =  '+str(ep).lower() + '\n')
                    fr.write('\t enable_express =  '+str(ee).lower() + '\n')
                    fr.write('\t requires_duplicate_detection ='+  str(dd).lower() + '\n')
                    fr.write('\t requires_session =  '+ str(rs).lower() + '\n')
                    # tf problem with this one. tf=1k cli=16k
                    #fr.write('\t max_size_in_megabytes =  mx + '"\n')
                    fr.write('\t dead_lettering_on_message_expiration = ' +str(dl).lower() + '\n')
                

        # no tags block       


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
    #end stub
