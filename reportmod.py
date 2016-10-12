################################################################################
# File:			reportmod.py
# Author:		Andrew M. Lamarra
# Modified:		4/6/2016
# Purpose:		This script will open a file called data.csv and modify
#			the contents to create the necessary metrics report and
#			save it to data-modified.csv.
#			This is for metrics reporting.
################################################################################

import os, csv

################################################################################
# FUNCTION TO MODIFY THE CATEGORY COLUMN & CREATE ANOTHER ARRAY
################################################################################
# The Categories Template array will allow you to copy from the categories.csv
# file & paste into the 1st Call Resolution and Priority Level tabs
catTemp = []
def modcat (category):
	if (   category == 'New User'
		or category == 'Deactivate User'
		or category == 'Outage'):
			catTemp.append(['Access', category])
			category = 'Access - ' + category
			
	elif ( category == 'Data Recovery'
		or category == 'Data Request'
		or category == 'Latency'
		or category == 'Management Reports'
		or category == 'RTC'
		or category == 'Tooltip'
		or category == 'Violation'):
			catTemp.append(['Admin Misc.', category])
			category = 'Admin Misc. - ' + category
			
	elif ( category == 'Add/Delete'
		or category == 'Modify'
		or category == 'Combine'):
			catTemp.append(['Agency/Officer', category])
			category = 'Agency/Officer - ' + category
			
	elif ( category == 'Admin - Case Record Override'
		or category == 'Admin - Delete Case'
		or category == 'Admin - Delete Case Record'
		or category == 'Admin - Delete Submission'
		or category == 'Case Record'
		or category == 'Case Notes'
		or category == 'Communication Log'
		or category == 'Sensitive'
		or category == 'Submission'
		or category == 'Object Repository'
		or category == 'Search'):
			catTemp.append(['Case', category])
			category = 'Case - ' + category
			
	elif ( category == 'Delegate'
		or category == 'Exam Authorization'
		or category == 'Lab/Section'
		or category == 'Roles'
		or category == 'Storage Area Authorization'
		or category == 'User ID'):
			catTemp.append(['Employee Card', category])
			category = 'Employee Card - ' + category
			
	elif ( category == 'Admin - COC Update' 
		or category == 'Admin - Modify Evidence Number'
		or category == 'Batches'
		or category == 'Chain of Custody'
		or category == 'Comments'
		or category == 'Delete'
		or category == 'Parent/Unparent'
		or category == 'Search'
		or category == 'Transfer'
		or category == 'Verify/Unverify'):
			catTemp.append(['Evidence', category])
			category = 'Evidence - ' + category
			
	elif ( category == '1A Packet'
		or category == 'Amend Report'
		or category == 'Cancel Report'
		or category == 'Check In/Check Out'
		or category == 'Generate Report'
		or category == 'Release Report'
		or category == 'Reviews'):
			catTemp.append(['Lab Reports', category])
			category = 'Lab Reports - ' + category
			
	elif ( category == 'Resource Action'
		or category == 'Manufacturer'
		or category == 'Add/Remove Role'
		or category == 'Bulk RARI Script'):
			catTemp.append(['Resource Manager', category])
			category = 'Resource Manager - ' + category
			
	elif ( category == 'FA Portal'
		or category == 'Instrument Integration'
		or category == 'IOSS PDF Tool'
		or category == 'Legacy Case Closure'
		or category == 'Sentinel'
		or category == 'STaCS'):
			catTemp.append(['Services', category])
			category = 'Services - ' + category
			
	elif ( category == 'Add/Remove User Access'
		or category == 'Add Storage Area/Location'
		or category == 'Deactivate Storage Area'):
			catTemp.append(['Storage Area/Location', category])
			category = 'Storage Area/Location - ' + category
			
	elif ( category == 'Admin-Case Record Override'):
			catTemp.append(['TEDAC', category])
			category = 'TEDAC - ' + category
			
	elif ( category == 'Case'
		or category == 'Evidence'
		or category == 'Lab Reports'
		or category == 'Navigation'
		or category == 'Other'):
			catTemp.append(['Training', category])
			category = 'Training - ' + category
			
	elif ( category == 'Password Reset'
		or category == 'Data Spill'
		or category == 'Other'
		or category == 'Usage'
		or category == 'Account Locked'
		or category == 'Disable Account'
		or category == 'Forensic Advantage'
		or category == 'Equipment Move'
		or category == 'Access'):
			catTemp.append([category, ''])
			
	return category

################################################################################
# USER INPUT
################################################################################
names = []
name = ' '
print('Enter the names of individuals to keep (not case sensitive).')
print('Tickets not assigned to these individuals will be removed from the list.')
print('Only part of the name is necessary. First or last.')
print('If "Andre" is entered, then "Andrew" will be included as well.')
print('Enter nothing to stop...\n')
while name:
	name = input('Enter a name: ')
	names.append(name)
names.pop()

if 'FA Support' not in names:
	ans = input('Include tickets assigned to FA Support? [Y/n] ')
	if (ans == '') or (ans.lower() == 'y'):
		names.append('FA Support')

# Gathering information on the holidays of the month
holidays = []
holiday = ' '
print('\nEnter the date of each holiday in M/D/YYYY format')
print('Enter nothing to stop...')
while holiday:
	holiday = input('Enter holiday: ')
	holidays.append(holiday)
holidays.pop()

################################################################################
# READING THE DATA CAPTURED FROM SERVICE MANAGER
################################################################################
# Declaring a few variables
data = []
add = False
workingdir = os.getenv('USERPROFILE') + '\\Desktop\\'
csvpath = workingdir + 'data.csv'
# Read from the CSV file and write to an array
with open(csvpath, newline='') as f:
	reader = csv.reader(f)
	for row in reader:		# Step through each row
		for name in names:	# Step through each name inputted by the user
			# Compare each inputted name with the "Assigned To" column
			if name.lower() in row[2].lower():
				add = True	# If it's in there, then add the row to the array
				# Add the full Classification Category
				row[7] = modcat(row[7])
				break	# No need to keep searching with every other name
		if add == True:
			data.append(row)	# Save the data to a 2D array
			add = False
data = sorted(data, key=lambda category: category[7]) # Sort by Category

################################################################################
# MODIFYING THE SEPARATE CATEGORIES ARRAY & WRITING TO A FILE
################################################################################
catTemp.sort() # Sort the Categories Template array
# This while loop will remove duplicate values in the catTemp array
i = 1
while i < len(catTemp):
	if catTemp[i] == catTemp[i-1]:
		catTemp.pop(i)
	else:
		i += 1
# This while loop will ensure only the 1st instance of each top level 
# category (the first column) is displayed
x = 1
y = 0
while x < len(catTemp):
	if catTemp[x][0] == catTemp[y][0]:
		catTemp[x][0] = ''
	else:
		y = x
	x += 1
catTemp.insert(0, ['Incident Category','Incident Sub Categories'])
# Write the results to a new CSV file
catout = workingdir + 'categories.csv'
with open(catout, 'w', newline='') as f:
	writer = csv.writer(f)
	writer.writerows(catTemp)

################################################################################
# MODIFYING THE MAIN DATA ARRAY TO ADD ADDITIONAL INFORMATION
################################################################################
email = 0
phone = 0
lync = 0
portal = 0
walkin = 0
i = 0		# i = the almighty Iterator
catnum = 0	# catnum = Numer of incidents in the Category
# The separators array keeps a list of the element numbers of each separator of
# the categories (used for Total Avg Resolution Time)
separators = []
# This while loop steps through the data array & adds all of the additional
# information, including a divider row between each category
while i < len(data):
	rn = i+2	# rn = Row Number (use i+2 to account for headers)
	timeworked = '=TEXT(((E{0}-INT(E{0}))-(D{0}-INT(D{0})))+((NETWORKDAYS(D{0},E{0}'.format(rn)
	# Use the holidays option in the NETWORKDAYS Excel function
	if len(holidays) > 0:
		timeworked += ',P2:%s2' % (chr(ord('P')+len(holidays)-1))
	timeworked += ')-1)*0.5),"[h]:mm")'
	# Mark if this incident was resolved in Less Than 3 hours
	lt3 = '=IF(AND(I{0}-INT(I{0})<0.125,DAY(I{0})<1)," ","")'.format(rn)
	# Mark if this incident was resolved in Less Than 8 hours
	lt8 = '=IF(AND(I{0}-INT(I{0})<0.333,DAY(I{0})<1)," ","")'.format(rn)
	if data[i][4]:
		data[i].extend([timeworked,'',lt3,'',lt8])
	else:
		data[i].append('')
	catnum += 1
	
	# Add an extra row at the end of each different Classification Category
	if (i == len(data)-1) or (data[i][7] != data[i+1][7]):
		cattotal = '=COUNTA(I%s:I%s)' % (i+3-catnum, rn)
		lt3total = '=COUNTIF(K%s:K%s,"= ")' % (i+3-catnum, rn)
		percent3 = '=IF(K{0}=0,"0%",TEXT(K{0}/J{0},"#%"))'.format(i+3)
		lt8total = '=COUNTIF(M%s:M%s,"= ")' % (i+3-catnum, rn)
		percent8 = '=IF(M{0}=0,"0%",TEXT(M{0}/J{0},"#%"))'.format(i+3)
		avgTime = '=TEXT(('
		for x in range(int(rn)-catnum, int(rn)):
			avgTime += 'I%s+' % (x+1)
			if not data[x-1][8]:
				catnum -= 1
		avgTime = avgTime[:-1]
		avgTime += ')/%s,"[h]:mm")' % (catnum)
		# If all of the tickets in a particular category are still open when
		#	the script runs, then the number of tickets will be 0
		if catnum == 0:
			avgTime = ''
		data.insert(i+1, ['','','','','','','',data[i][7],'',cattotal,lt3total
			,percent3,lt8total,percent8,avgTime])
		separators.append(i+1) # Keep track of the row number of each separator
		i += 1
		catnum = 0
	i += 1

# Adding the holiday dates if applicable
if len(holidays) > 0:
	data[0].extend(['',''])
	if not data[0][4]:
		data[0].extend(['','','','',''])
	for holiday in holidays:
		data[0].append(holiday)

################################################################################
# ADDING TOTALS TO THE BOTTOM OF THE SPREADSHEET
################################################################################
LR = len(data)+1			# LR = Last Row
Total = '=SUM(J2:J%s)'%LR	# Total number of incidents
Total3 = '=SUM(K2:K%s)'%LR	# Total number of incidents closed on first call
Total8 = '=SUM(M2:M%s)'%LR	# Total number of incidents closed in 8 hours
TotalAvg = '=TEXT(('		# Average resolution time of all calls
for i in separators:
	TotalAvg += 'O%s+' % (i+2)
TotalAvg = TotalAvg[:-1]
TotalAvg += ')/%s,"[h]:mm")' % len(separators)
# Total percentage of tickets closed in 3 hours (first call resolution)
TotPerc3 = '=IF(K{0}=0,"0%",TEXT(K{0}/J{1},"#%"))'.format(len(data)+4,len(data)+3)
# Total percentage of tickets closed in 8 hours
TotPerc8 = '=IF(M{0}=0,"0%",TEXT(M{0}/J{1},"#%"))'.format(len(data)+5,len(data)+3)

# Counting how many we have from each source
email = '=COUNTIF(F2:F%s,"E-Mail")' % len(data)
phone = '=COUNTIF(F2:F%s,"Phone")' % len(data)
lync = '=COUNTIF(F2:F%s,"Lync")' % len(data)
portal = '=COUNTIF(F2:F%s,"Portal")' % len(data)
walkin = '=COUNTIF(F2:F%s,"Walk-Ins")' % len(data)

data.append(['','','','','','','','',''])
data.append(['','','','','','','','','Total Incidents',Total])
data.append(['','','','','','','','','Total First Call','',Total3])
data.append(['','','','','','','','','Total Close in 8 Hours','','','',Total8])
data.append(['','','','','','','','','Average Response Time','','','','','',TotalAvg])
data.append(['','','','','','','','','% of First Call Response','','','E-Mail',email])
data.append(['','','','','','','','',TotPerc3,'','','Phone',phone])
data.append(['','','','','','','','','% of Closed in 8 hours','','','Lync',lync])
data.append(['','','','','','','','',TotPerc8,'','','Portal',portal])
data.append(['','','','','','','','','','','','Walk-Ins',walkin])
data.append(['','','','','','','','','','','','Total Incidents',Total])

################################################################################
# CREATING THE HEADERS ROW
################################################################################
header = (['Incident ID','Title','Assigned To','Created On','Resolved On'
			,'Source','Priority','Classification Category','HH:MM','Total Incidents'
			,'First Call','Percent First Call','Incidents Closed 8 hrs'
			,'Percent 8 Hours','Avg Resolution Time'])
for i in range(len(holidays)):
	header.append('Holiday') # Create a Holiday column for each holiday inputted
data.insert(0, header)	# Inserting the header

################################################################################
# WRITE THE RESULTS TO DATA-MODIFIED.CSV
################################################################################
csvout = workingdir + 'data-modified.csv'
with open(csvout, 'w', newline='') as f:
	writer = csv.writer(f)
	writer.writerows(data)

input('\nPress any key to exit...')
