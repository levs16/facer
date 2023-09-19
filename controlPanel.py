#############FACERPANEL###############
##   Last change Sep19 2023(1:26PM) ## 
##   Version: 1.2                   ##
##   Changelog is at the bottom     ##
######################################
# Written on the Sep18 2023(10:43PM) #
######################################


# Imports
import json, cv2, face_recognition, argparse, os

# argument parser
parser = argparse.ArgumentParser(description="Control panel for face recognition")
parser.add_argument("-a", "--add", help="Add a new face to the JSON file", action="store_true")
parser.add_argument("-d", "--delete", help="Delete an existing face from the JSON file", action="store_true")
parser.add_argument("-n", "--name", help="The name of the person to add or delete", type=str)
parser.add_argument("-i", "--image", help="The path of the image of the person to add", type=str)
args = parser.parse_args()

# path to the json faces data. Modify if you have your own
json_file = "dataset/faces.json"

# get the size of the json
file_size = os.path.getsize(json_file)

# if empty(0-sized) write the preset, so we're not gettin kickd out with the jsonparse errors
if file_size == 0:
    with open(json_file, "w") as f:
        data = {"emp_details": []}
        json.dump(data, f)

# open the json and assign it to the face_data variable
with open(json_file, "r") as f:
    face_data = json.load(f)

# check for an argument
if args.add:
    # check for the name and image arguments
    if args.name and args.image:
        # open/read the image and convert it to the RGB scale
        img = cv2.imread(args.image)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # get the face encoding(data/points) and assign/store them in the variables
        face_encoding = face_recognition.face_encodings(rgb_img)[0]
        # append the new face data to the json
        with open(json_file, "r+") as f:
            data = json.load(f)
            data["emp_details"].append({"name": args.name, "face_encoding": list(face_encoding)})
            f.seek(0)
            json.dump(data, f) # dump the changes
        print(f"Successfully added {args.name} to the JSON file.")
    else:
        print("Please provide a name and an image for adding a new face.")

# look for the delete arg
if args.delete:
    # if given
    if args.name:
        # find the name in the json
        for i, person in enumerate(face_data["emp_details"]):
            if person["name"] == args.name:
                # remove em
                with open(json_file, "r+") as f:
                    data = json.load(f)
                    del data["emp_details"][i]
                    f.seek(0)
                    json.dump(data, f)
                print(f"Successfully deleted {args.name} from the JSON file.")
                break
        else:
            print(f"No such name {args.name} found in the JSON file.")
    else:
        print("Please provide a name for deleting an existing face.")


#####CHANGELOG#######

# ver0.13 - started this changelog. Added json file fixing(if it's empty). Fixed and changed the default path to the faces.json
# ver0.14 - added some outputs for the program.
# ver0.5 - changed the version format from G.Ix (where G is the generation(initial) of the program, I is the generation(secondary) and the x is the version of the generation) to G.x(where G is the same, but only the x is now present)
# ver1.0 - GLOBAL CHANGES. Now program is console-run (using the argparse lib)
# ver1.1 - fixed the not-working argparsing, where it will output errors to the console insted of working with the args
# ver1.2 - added the bigger (--example) version of the arguments