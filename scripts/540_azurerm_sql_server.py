prefixa= 0 | awk -F 'azurerm_' '{'print 2}'' | cut -f1 -d'.'
tfp=fr.write('azurerm_" prefixa

if 1" != " :
    rgsource=1
else
    echo -n "Enter name of Resource Group [rgsource]["> "
    read response
    if [ -n "response" :
        rgsource=response
   
fi
azr=az sql server list -g rgsource -o json
count= azr | | len(
if count" != "0" :
    for i in range(0,count):
        name=azr[i]["name"]
        rname= name.replace(".","-")
        rg=azr[i]["resourceGroup"].replace(".","-")

        id=azr[i]["]["id"]
        loc=azr[i]["location"]
        ver=azr[i]["version"]
        al=azr[i]["administratorLogin"]
        ap=azr[i]["administratorLoginPassword"]


        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t location = "' +  loc + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t version = "' +  ver + '"\n')
        fr.write('\t administrator_login= "' +  al + '"\n')
        
        if ap" try :
            fr.write('\t administrator_login_password= "' +  ap + '"\n')
        else
            fr.write('\t administrator_login_password= "' +   + '"\n')
       

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
       
     
        #
        fr.write('}\n')
        #
        cat outfile
        statecomm=fr.write('terraform state rm . + '__' + " tfp rg rname
        echo statecomm >> tf-staterm.sh
        eval statecomm
        evalcomm=fr.write('terraform import . + '__' +  " tfp rg rname id
        echo evalcomm >> tf-stateimp.sh
        eval evalcomm
        
    
fi
