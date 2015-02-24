"""Misc functions needed for text_dj"""

def stringify_results(results):
	text_response = "Text back the number of your preffered song or search again for another song: \n\n"

	for i in range(0,len(results)):
		text_response = text_response + str(i) + ": '" + results[i]['name'] + "' by " + results[i]['artists'] + "\n\n"
	return text_response 