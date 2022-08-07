import os

def make_folders():
    directory = "images"

    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, directory)  # ./images
    if not os.path.exists(path): os.makedirs(path)

    values_path = os.path.join(path, 'values')  # ./images/values
    if not os.path.exists(values_path):
        os.makedirs(values_path)
        print("Directory '% s' created" % values_path)

    mechanisms_path = os.path.join(path, 'mechanisms')  # ./images/mechanisms
    if not os.path.exists(mechanisms_path):
        os.makedirs(mechanisms_path)
        print("Directory '% s' created" % mechanisms_path)
