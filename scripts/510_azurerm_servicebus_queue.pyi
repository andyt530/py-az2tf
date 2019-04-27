prefixa= 0 | awk -F 'azurerm_' '{'print 2}'' | awk -F '.sh' '{'print 1}'' 
tfp=fr.write('azurerm_" prefixa
if 1" != " :
    rgsource=1
else
    echo -n "Enter name of Resource Group [rgsource]["> "
    read response
    if [ -n "response" :
        rgsource=response
   
fi
azr=az servicebus namespace list -g rgsource -o json
count= azr | | len(
if count > 0" :
    for i in range(0,count):
        
        nname=azr[i]["name"]
        azr2=az servicebus queue list -g rgsource --namespace-name nname -o json
        icount= azr2 | | len(
        if icount > 0" :
            for j in range(0,icount):
                name= azr2 | jq ".[j]["name"]
                rname= name.replace(".","-")
                rg= azr2 | jq ".[j]["resourceGroup"].replace(".","-")
                id= azr2 | jq ".[j]["]["id"]
                ep= azr2 | jq ".[j]["enablePartitioning"]
                adoni= azr2 | jq ".[j]["autoDeleteOnIdle"]
                
                ee= azr2 | jq ".[j]["enableExpress"]
                dd= azr2 | jq ".[j]["requiresDuplicateDetection"]
                rs= azr2 | jq ".[j]["requiresSession"]
                mx= azr2 | jq ".[j]["maxSizeInMegabytes"]
                dl= azr2 | jq ".[j]["deadLetteringOnMessageExpiration"]
                
                
                fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
                fr.write('\t name = "' +  name + '"\n')
                fr.write('\t resource_group_name = "' +  rgsource + '"\n')
                fr.write('\t namespace_name = "' +  nname + '"\n')
                fr.write('\t enable_partitioning =  ep + '"\n')
                fr.write('\t enable_express =  ee + '"\n')
                fr.write('\t requires_duplicate_detection =  dd + '"\n')
                fr.write('\t requires_session =  rs + '"\n')
                # tf problem with this one. tf=1k cli=16k
                #fr.write('\t max_size_in_megabytes =  mx + '"\n')
                fr.write('\t dead_lettering_on_message_expiration =  dl + '"\n')
                
                #
                # New Tags block v2
                tags=azr[i]["tags"
                tt= tags | jq .
                tcount= tags | | len(
                if tcount > 0" :
                    fr.write('\t tags {'  + '"\n')
                    tt= tags | jq .
                    keys= tags |eys'
                    for j in range(0,tcount):
                        k1= keys | jq ".[j]["
                        #echo "key=k1"
                        re="[[:space:]["+"
                        if [[ k1 =~ re ]["; :
                            #echo "found a space"
                            tval= tt | jq ."k1"
                            tkey= k1]
                            fr.write('\t\t"' +  =   "tkey" "tval" + '"\n')
                        else
                            #echo "found no space"
                            tval= tt | jq .k1
                            tkey= k1]
                            fr.write('\t\t =   tkey "tval" + '"\n')
                       
                    
                    fr.write('\t}\n')
               
                
                
                fr.write('}\n')
                #
                echo prefix
                echo prefix + '__' + name
                cat outfile
                statecomm=fr.write('terraform state rm . + '__' + " tfp rg rname
                echo statecomm >> tf-staterm.sh
                eval statecomm
                evalcomm=fr.write('terraform import . + '__' +  " tfp rg rname id
                echo evalcomm >> tf-stateimp.sh
                eval evalcomm
                
            
       
    
fi
