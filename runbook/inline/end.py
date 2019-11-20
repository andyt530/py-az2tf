tffile="*.tf"
fileList = glob.glob(tffile) 
# Iterate over the list of filepaths & remove each file.
for filePath in fileList:
    with open(filePath) as f: 
        print (f.read())

tffile="*stateimp.sh"
fileList = glob.glob(tffile) 
# Iterate over the list of filepaths & remove each file.
for filePath in fileList:
    with open(filePath) as f: 
        print (f.read())
print "# END \n"