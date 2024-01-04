import struct
import sys
import pandas as pd
import numpy as np

#Reads file and returns a dataframe with the contents

def ReadInput(file_path, IsQueryFile=False):
    try:
        with open(file_path, 'rb') as file:
            magic_number = struct.unpack('>I', file.read(4))[0]
            num_images = struct.unpack('>I', file.read(4))[0]
            num_rows = struct.unpack('>I', file.read(4))[0]
            num_cols = struct.unpack('>I', file.read(4))[0]

            images = []

            if IsQueryFile:
                num_images = min(num_images, 10)

            for _ in range(num_images):
                image = np.frombuffer(file.read(num_rows * num_cols), dtype=np.uint8)
                images.append(image)

    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
        exit(-1)
    except IOError:
        print(f"An error occurred while reading the file '{file_path}'.")
        exit(-1)

    images_array = np.array(images)
    images_array = images_array.reshape(-1, num_rows, num_cols, 1).astype(np.float32) / 255.0

    return images_array

def WriteOutput(output_dir,data):
    np.savetxt(output_dir,data)


def HandleArguments():

    if len(sys.argv) != 9: #Error check so correct argument number is given
        print('Incorrect number of arguments was given!')
        exit(-1)

    dataset, queryset, output_dataset, output_query = None, None, None, None

    for i in range(1, len(sys.argv), 2): #Check for each argument and i is incremented by 2 each iteration
        if sys.argv[i] == '-d': #At each iteration if the given argument if found ,the next is the value
            dataset = sys.argv[i + 1]
        elif sys.argv[i] == '-q':
            queryset = sys.argv[i + 1]
        elif sys.argv[i] == '-od':
            output_dataset = sys.argv[i + 1]
        elif sys.argv[i] == '-oq':
            output_query = sys.argv[i + 1]
    
    if None in(dataset,queryset,output_dataset,output_query): #If one of these values is still its initialized value(None)
        print('Missing required argument!') #Incorrect input was given
        exit(-1) #terminate the program

    return dataset,queryset,output_dataset,output_query
