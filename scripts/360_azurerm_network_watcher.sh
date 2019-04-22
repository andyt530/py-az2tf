
azr=`az network watcher list -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        #name=`echo $name | awk '{print tolower($0)}'`
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`

        prefix=`printf "%s__%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
        echo $az2tfmess > $outfile

        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location"`
        
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
        printf "\t name = \"%s\"\n" $name >> $outfile
        #printf "\t id = \"%s\"\n" $id >> $outfile
        printf "\t location = %s\n" "$loc" >> $outfile
        #printf "\t resource_group_name = \"\${var.rgtarget}\"\n" >> $outfile
        printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
            
        #

            
        
        printf "}\n" >> $outfile
        cat $outfile

    done
fi
