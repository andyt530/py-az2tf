rm -f run1.py not.py run.py
outfile="not.py"
while read p; do
  #echo "$p"
  if [ "$p" == "# RUNBOOK ON" ] ; then
    outfile="run.py"
  fi
  if [ "$p" == "# RUNBOOK OFF" ] ; then
    outfile="not.py"
  fi
  if [[ $p =~ "import azurerm" ]] ; then
    f=`echo "$p" | cut -f2 -d" "`
    echo " " >> $outfile
    echo "#" >> $outfile
    echo "# $f" >> $outfile
    echo "#" >> $outfile
    cat ../scripts/$f.py >> $outfile

  elif [[ $p =~ "# RUNBOOK INLINE1" ]] ; then
    echo " " >> $outfile
    echo "#" >> $outfile
    echo "# runbook auth" >> $outfile
    echo "#" >> $outfile
    cat inline/runbook_auth.py >> $outfile
    echo " " >> $outfile
  elif [[ $p =~ "# RUNBOOK INLINE2" ]] ; then
    echo "#" >> $outfile
    echo "# runbook get token" >> $outfile
    echo "#" >> $outfile
    cat inline/rbauth.py >> $outfile
    echo " " >> $outfile
  else 
    f1=`echo $p | cut -f1 -d'.'`
    f2=`echo $p | cut -f2 -d'.'`
    if [[ $f1 == azurerm_* ]] ; then
        echo $f2 >> $outfile
    else 
        echo $p >> $outfile
    fi
  fi
done <../scripts/az2tf.py

sed -i .bak -e 's/cde=True/cde=False/g' run.py

#sed -i .bak -e 's/fr.write/print/g' run.py
cat inline/end.py >> run.py
rm -f not.py *.bak
mv run.py az2tf-runbook.py
