# azurerm_image
def azurerm_image(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_image"
    tcode="340-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Compute/images"
        params = {'api-version': '2019-03-01'}
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
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')
             
# hardwire this - as source vm may of been deleted after image created
            try:
                svm=azr[i]["properties"]["sourceVirtualMachine"]["id"]
                fr.write('\t source_virtual_machine_id = "' +  svm + '"\n')
            except KeyError:        
                try :
                    osdisk=azr[i]["properties"]["storageProfile"]["osDisk"]
                    ostype=azr[i]["properties"]["storageProfile"]["osDisk"]["osType"]
                    osstate=azr[i]["properties"]["storageProfile"]["osDisk"]["osState"]
                    oscache=azr[i]["properties"]["storageProfile"]["osDisk"]["caching"]

                    fr.write('\t os_disk {\n')
                    fr.write('\t os_type = "' +  ostype + '"\n')
                    fr.write('\t os_state = "' +  osstate + '"\n')
                    fr.write('\t caching = "' +  oscache + '"\n')
                    
                    try :
                        blob_uri=azr[i]["properties"]["storageProfile"]["osDisk"]["blobUri"]
                        fr.write('\t blob_uri = "' +  blob_uri + '"\n')
                    except KeyError:
                        pass
                    fr.write('\t}\n')
            
                except KeyError:
                    pass
                    
                pass

            try:
                zros=azr[i]["properties"]["storageProfile"]["zoneResilient"]
                fr.write('\t zone_resilient = '+ str(zros).lower() + '\n')
            except KeyError:
                pass

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
    #end stub
