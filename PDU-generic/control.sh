for f in `ls control*.json`; do
    dis=`cat $f`   
    erpeer=0
   
    dir=`echo $dis | jq ".control.director" | tr -d '"'`
    dd=`echo $dis | jq ".control.depd" | tr -d '"'`
    env=`echo $dis | jq ".control.env" | tr -d '"'`
    peerer=`echo $dis | jq ".control.peerer" | tr -d '"'`
    if [ "$peerer" = "yes" ]; then erpeer=1 ; fi

    export TF_VAR_director=$dir
    export TF_VAR_depd=$dd
    export TF_VAR_env=$env
    export TF_VAR_peerer=$erpeer
        
    echo $TF_VAR_director
    echo $TF_VAR_depd
    echo $TF_VAR_env
    echo $TF_VAR_erpeer     
    
done