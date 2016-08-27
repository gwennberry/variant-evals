import sys
import os

# Parse arguments
path = sys.argv[1]
variant = sys.argv[2]

# Grab and parse variant of interest
varSplit = variant.split("_")
varPos = varSplit[0]
varAlleles = varSplit[1]

varChr = varPos.split(":")[0]
varCoord = int(varPos.split(":")[1])
varRef = varAlleles.split("#")[0]
varAlt = varAlleles.split("#")[1]

varPos = varChr + ":" + str(varCoord)
varAlleles = varRef + "#" + varAlt

# Initialize counters
variantsFound = 0
passVariantsFound = 0
myVariantsFound = 0
myVariantsFoundPassing = 0
variantsInRange = 0

# Define functions
def isMatch(tpos, tallele, fpos, fref, falt, fromRight, fromLeft, rightFirst):
	tchr,tcoord = tpos.split(":")
	fchr,fcoord = fpos.split(":")
	tref,talt = tallele.split("#")
	
	cleanRef = tref.strip()
	cleanAlt = talt.strip()
	bump_pos = 0

	found_match = False

	if fromRight and rightFirst:
		while(True):
			if tchr == fchr and int(tcoord) + bump_pos == int(fcoord) and cleanRef == fref and cleanAlt == falt:
				found_match = True
				break
			if len(cleanRef)==1 or len(cleanAlt)==1:
				break
			if cleanRef[-1] == cleanAlt[-1]:
				cleanRef = cleanRef[:-1]
				cleanAlt = cleanAlt[:-1]
			else:
				break
	if fromLeft:
		while(True):
			if tchr == fchr and int(tcoord) + bump_pos == int(fcoord) and cleanRef == fref and cleanAlt == falt:
				found_match = True
				break
			if len(cleanRef)==1 or len(cleanAlt)==1:
				break
			if cleanRef[0] == cleanAlt[0]:
				cleanRef = cleanRef[1:]
				cleanAlt = cleanAlt[1:]
				bump_pos +=1
			else:
				break

	
	if fromRight and not rightFirst:
		while(True):
			if tchr == fchr and int(tcoord) + bump_pos == int(fcoord) and cleanRef == fref and cleanAlt == falt:
				found_match = True
				break
			if len(cleanRef)==1 or len(cleanAlt)==1:
				break
			if cleanRef[-1] == cleanAlt[-1]:
				cleanRef = cleanRef[:-1]
				cleanAlt = cleanAlt[:-1]
			else:
				break

	if tchr == fchr and int(tcoord) + bump_pos == int(fcoord) and cleanRef == fref and cleanAlt == falt:
		return True
	if found_match:
		return True
	return False


# Initialize info fields
foundVar = ""
myfilters = []

# Read the VCF file
lines = open(path, 'r').readlines()
for line in lines:
	if line.startswith("#"):
		continue
	splitline = line.strip().split("\t")
	if len(splitline)==1:
		splitline = line.strip().split(",")
	chr = splitline[0]
	coord = splitline[1]
	ref = splitline[3]
	alt = splitline[4]
	filters = splitline[6]

	if alt != ".":
		variantsFound +=1
		if filters == "PASS":
			passVariantsFound +=1

	if alt == ".":
		continue

	pos = chr + ":" + coord
	alleles = ref + "#" + alt

	desiredChr,desiredCoord=varPos.split(":")
	
	if desiredChr==chr and abs(int(desiredCoord)-int(coord))<5:
		variantsInRange+=1
	# TODO - this is silly. Should do all the options from within isMatch.
	if isMatch(varPos,varAlleles,pos,ref,alt,True,False,False) or isMatch(varPos,varAlleles,pos,ref,alt,False,True, False) or isMatch(varPos,varAlleles,pos,ref,alt,True,True, False) or isMatch(varPos,varAlleles,pos,ref,alt,True,True, True):
			foundVar = pos+"_"+alleles
			myVariantsFound += 1
			if filters == "PASS":
				myVariantsFoundPassing += 1
			else:
				myfilters.append(filters)
	
	
# Assign diagnosis based on the collected counts
diagnosis = "Unknown"
if variantsFound == 0:
	diagnosis = "No variants found"
elif variantsInRange == 0:
	if passVariantsFound > 0:
		diagnosis = "No variants in range and some pass"
	else:
		diagnosis = "No variants in range and all fail"
elif passVariantsFound == 1 and myVariantsFoundPassing == 0:
	diagnosis = "Different pass variant found"
elif variantsFound == 1 and passVariantsFound == 0 and myVariantsFound == 0:
	diagnosis = "Different filtered variant found"
elif variantsFound == myVariantsFoundPassing:
	diagnosis = "Correct variant"
elif variantsFound == 1 and myVariantsFound ==1:
	diagnosis = "Correct but filtered" + " (" + "|".join(myfilters) + ")"
elif variantsFound > 1:
	if myVariantsFound > 0:
		if myVariantsFoundPassing == 1 and passVariantsFound == 1:
			diagnosis = "Passing with failing extra variant(s)"
		elif myVariantsFoundPassing == 1 and passVariantsFound > 1:
			diagnosis = "Found passing but with extra passing variants"
		elif myVariantsFoundPassing == 0 and passVariantsFound > 0:
			diagnosis = "Found failing and with extra passing variants"
		elif myVariantsFoundPassing == 0 and passVariantsFound == 0:
			diagnosis = "Found failing and with extra failing variants"
		else:
			diagnosis = "Unknown"
	else:
		if passVariantsFound > 0:
			diagnosis = "Not found and extra passing variants"
		else:
			diagnosis = "Not found and extra failing variants"
elif passVariantsFound == 0:
	diagnosis = "No passing variants found"

values = [variantsFound, passVariantsFound, myVariantsFound, myVariantsFoundPassing, diagnosis, foundVar]
print ','.join([str(x) for x in values])

