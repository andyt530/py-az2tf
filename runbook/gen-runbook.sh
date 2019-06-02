rm -f run.py not.py
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
    echo "$p"
    f=`echo "$p" | cut -f2 -d" "`
    echo $f
    cat ../scripts/$f.py >> $outfile
  else
    echo $p >> $outfile
  fi
done <../scripts/resources.py



#for line in $(echo ../scripts/resources.py); do
#done
##printf "%s\n" "$line"
