"""
This class is caleld within Search.py to retrieve a directory from the user for 
which directory to search within. It then runs a go script that searches though
the directory and all subdirectories for .txt files. It then saves the names,
paths, and contents of the files to json files. It then returns the corpus as a
dataframe.

"""
import pandas as pd
import os
import subprocess
import json

class BuildCorpus:
    def __init__(self):
        self.dash = "-" * 50 + "\n"

    def corpus(self):
        #print start message
        print(f"{self.dash*2}\n\nStarting corpus building process...")

        #get directory from user
        directory = self.specify_directory()

        #run go_gather_subdirectories.go script and retrieve data it saved to JSON
        file_names, file_paths, file_content = self.run_go_script(directory)

        #return corpus as df
        return self.corpus_to_df(file_names, file_paths, file_content)


        
    def specify_directory(self):
        '''This function prompts for the directory to encode and returns the path'''

        directory = input(f"{self.dash}\nEnter the directory you wish to search within: ")

        #check to make sure directory exists and was input correctly
        if os.path.isdir(directory):
            print(f"{self.dash}\nThe directory you specified exists.")

            #move to go_fast directory
            current_dir, write_to_dir = os.getcwd(), os.path.join(os.getcwd(), "go_fast")
            os.chdir(write_to_dir)

            #save direcrtory as txt to be accessed by the go script
            with open("directory_to_search.txt", "w") as f:
                f.write(directory)

            #change directory back to previous
            os.chdir(current_dir)

        #otherwise call function again
        else:
            print(f"{self.dash}\nThe directory you specified does not exist. Please try again.")
            #recursively call function again
            return self.specify_directory()


    def run_go_script(self, directory):

        # get cwd to return to later
        previopus_dir = os.getcwd()

        # get current path + go_fast 
        script_dir = os.path.join(os.getcwd(), "go_fast")

        # change directory to go_fast
        os.chdir(script_dir)

        # run go script -- this will save .txt names, paths, and contents to json
        subprocess.run(["go", "run", "go_gather_subdirectories.go"])

        data_retrieved = []

        # retrieve json files
        for file in ["file_names.json", "file_paths.json", "file_contents.json"]:
            with open(os.path.join(script_dir, file), 'r', encoding="utf-8", errors="replace") as f:
                data_retrieved.append(json.load(f))

        # remove unnecessary files after data is retrieved
        for file in ["file_names.json", "file_paths.json", "file_contents.json", "directory_to_search.txt"]:
            os.remove(file)

        # change directory back to previous
        os.chdir(previopus_dir)

        # print lengths and types of data retrieved
        print(f"{self.dash*2}\n\nPrinting Types of Retrieved Data\n\nFile Names: {type(data_retrieved[0])}\n\nFile Paths: {type(data_retrieved[1])}\n\nFile Content: {type(data_retrieved[2])}\n\n") # print types
        print(f"{self.dash*2}\n\nPrinting Lengths of Retrieved Data\n\nFile Names: {len(data_retrieved[0])}\n\nFile Paths: {len(data_retrieved[1])}\n\nFile Content: {len(data_retrieved[2])}\n\n")  #print lengths
 

        return data_retrieved[0], data_retrieved[1], data_retrieved[2]
    

    def corpus_to_df(self, file_names, file_paths, file_content):
        """This functions saves the corpus as a csv after converting to df"""
        return pd.DataFrame(list(zip(file_names, file_paths, file_content)), columns=["File Name", "File Path", "File Content"])

