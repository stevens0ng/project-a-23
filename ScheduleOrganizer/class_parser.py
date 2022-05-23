'''  Requests module does not ship natively with Python! '''
import requests
import json
class_list = []
#returns only undergrad cs classes for spring 2022
def get():
    url = 'https://api.devhub.virginia.edu/v1/courses'
    data = requests.get(url).json()

    for item in data["class_schedules"]["records"]:
        if item[0] == "CS" and item[12] == "2022 Spring" and item[1] < str(5000) and item[2] < str(100):
            class_list.append(item)
    return class_list
	
