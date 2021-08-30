import json

def save_to_file(data,file_name):
    with open(file_name, "w") as write_file:
        json.dump(data,write_file,indent=2)
        print("You sucessfully saved to {}.".format(file_name))




