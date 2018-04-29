from microsoftbotframework import ReplyToActivity

#json_state = JsonState();

food = ["food", "hunger", "hungry", "starve", "starving"]
shelter = ["shelter", "house", "housing", "home", "roof"]


def echo_response(message):
	if message["type"] == "message":
		for string in food:
			if (message["text"].find(string) != -1):
				message["text"] = "Sounds like you're hungry, do you want to find out about food?"
				ReplyToActivity(fill=message, text=message["text"]).send()
				break;
		for string in shelter:
			if (message["text"].find(string) != -1):
				message["text"] = "Lets get you inside, do you want to find out about shelters!"
				ReplyToActivity(fill=message, text=message["text"]).send()
				break;
		else:
			ReplyToActivity(fill=message, text=message["text"]).send()

#def respond_to_food(message):
#	if (message["type"] == "message" and (message["text"].find("food", message["text"].length()) != -1)):
#		ReplyToActivity(fill=message,
#						text="You want to know about food!").send()
