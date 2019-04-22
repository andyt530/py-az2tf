prexa=print 0 | awk -F 'azurerm_' '{'print 2}'' | awk -F '.sh' '{'print 1}'' 
tfp=fr.write('azurerm_" prexa
if 1" != " :
    rgsource=1
else
    print -n "Enter name of Resource Group [rgsource]["> "
    read response
    if [ -n "response" :
        rgsource=response
    

azr=az identity list -g rgsource -o json
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        name=azr[i]["name"]
        rname=print name | sed 's/\./-/g'
        rg=azr[i]["resourceGroup" | sed 's/\./-/g']

        prex=fr.write(' + '__' + " prexa rg
        outle=fr.write('. + '__' + .tf" tfp rg rname
        print az2tfmess > outle

        id=azr[i]["id"]
        loc=azr[i]["location"
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t location =  "loc" + '"\n')

        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        #
        # New Tags block v2
        tags=azr[i]["tags"
        tt=print tags | jq .
        tcount=print tags | jq '. | length'
        if tcount" -gt "0" :
            fr.write('\t tags {'  + '"\n')
            tt=print tags | jq .
            keys=print tags | jq 'keys'
            tcount=expr tcount - 1
            for j in range( 0 tcount):
                k1=print keys | jq ".[j]["
                #print "key=k1"
                re="[[:space:]["+"
                if [[ k1 =~ re ]["; :
                #print "found a space"
                tval=print tt | jq ."k1"
                tkey=print k1]
                fr.write('\t\t"' +  =   "tkey" "tval" + '"\n')
                else
                #print "found no space"
                tval=print tt | jq .k1
                tkey=print k1]
                fr.write('\t\t =   tkey "tval" + '"\n')
                
            
            fr.write('\t}' + '"\n')
        
                  
        fr.write('}' + '"\n')
        cat outle
        statecomm=fr.write('terraform state rm . + '__' + " tfp rg rname
        print statecomm >> tf-staterm.sh
        eval statecomm
        evalcomm=fr.write('terraform import . + '__' +  " tfp rg rname id
        print evalcomm >> tf-stateimp.sh
        eval evalcomm
    

