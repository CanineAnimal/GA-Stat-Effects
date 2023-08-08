import time

# Get R-generated data of stat effects
path = input("Enter path to stat effect CSV file: ")
f = open(path, "r")
data = f.read()
f.close()

# Clean up data to remove trailing comma and create readable list
data = data.replace("\n", ",")
if data[len(data) - 1] == ",":
	data = data[:-1]
data = data.split(",")

# Add category title
text = "[size=150]" + input("Enter category/AoE/strength: ") + "[/size]\n\n[spoiler=Data]"

# Loop through each stat
item = 9

while item < len(data):
	print("Processing " + data[item] + "...")
	if data[item + 4] == "0" and data[item + 5] == "0":
		# Assume no data exists if both max and min are zero
		pass
	else:
		if eval(data[item + 1]) > 30 and eval(data[item + 5]) >= eval(data[item + 1]) * -0.05 or eval(data[item + 1]) < -30 and eval(data[item + 4]) <= eval(data[item + 1]) * -0.05:
			# Highlight stat name if correlation is exceptionally strong
			text += "[color=green][b]" + data[item] + "[/b][/color]\n"
		else:
			text += "[b]" + data[item] + "[/b]\n"
		text += "[list][*]Mean: " + data[item + 1] + "[*]Standard Deviation: " + data[item + 2] + "[*]Skewness: " + data[item + 3] + "[*]Maximum: " + data[item + 4] + "[*]Minimum: " + data[item + 5] + "[/list]\n"
		
		# Include linear relationship data if p-value is below 0.05
		if eval(data[item + 6]) < 0.05:
			text += "Linear relationship data (NB: Linear model may be inaccurate),[list][*]P-Value: " + data[item + 6] + "[*]Slope: " + data[item + 7] + "[*]Intercept: " + data[item + 8] + "[/list]\n"
	item += 9
text += "[/spoiler]"
# Print text content
print(text)
time.sleep(30) # Wait before ending script to give reasonable time to copy content, if not script is for some reason not run from command line