for i in `ls scripts/*.sh`; do
# test 1
grep '$rg >>' $i
if [ $? -eq 0 ]; then
echo "$i"
echo " "
fi
grep '$rg $name' $i
if [ $? -eq 0 ]; then
echo "$i"
echo " "
fi
grep 'cut' $i | grep f5 | grep -v sed
if [ $? -eq 0 ]; then
echo "$i"
echo " "
fi

done