"""Misc functions needed for text_dj"""

def stringify_results(results):
	if len(results) == 0:
		return "Sorry, no results matched. Please try another search"
	else:
		text_response = "Text back the number of your preffered song or search again for another song: \n\n"
		
		for i in range(0,len(results)):
			text_response = text_response + str(i) + ": '" + results[i]['name'] + "' by " + results[i]['artists'] + "\n\n"
		return text_response 