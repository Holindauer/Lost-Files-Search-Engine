"""
This class defition is used to build a corpus of local file content.

Given a specificed directory, it will gather all file names named and 
text content from within all further subdirectories. This text content
will be put into a python list and saved as a text file.

This list will be encoded with a Sentence Bert Model to compare semantic
similarity between all documents within the specified directory and a 
search query. This step, though, will happen in a separate file.


At this stage, the only files that will be gathered are text files. This 
will be expanded in the future to include other file types.

"""
import pandas as pd
import os

class BuildCorpus:
    def __init__(self):
        self.dash = "-" * 50 + "\n"

    def corpus(self):
        #print start message
        print(f"{self.dash*2}\n\nStarting corpus building process...")

        #get directory from user
        director = self.specify_directory()

        #gather all subdirectories into list
        print(f"{self.dash*2}\nGathering subdirectories...")
        subdirs = self.gather_subdirs(director)

        #gather all text files into list
        txt_paths = self.gather_txt_paths(subdirs)

        #gather all file names into list
        file_names = self.gather_file_names(txt_paths)

        #gather all file content into list
        file_content = self.gather_file_content(txt_paths)

        #save corpus as csv
        self.save_corpus(file_names, file_content)

        
    def specify_directory(self):
        '''This function prompts for the directory to encode and returns the path'''

        directory = input(f"{self.dash}\nEnter the directory you wish to search within: ")

        #check to make sure directory exists and was input correctly
        if os.path.isdir(directory):
            print(f"{self.dash}\nThe directory you specified exists.")
            return directory
        #otherwise call function again
        else:
            print(f"{self.dash}\nThe directory you specified does not exist. Please try again.")
            #recursively call function again
            return self.specify_directory()

    def gather_subdirs(self, directory, subdir_list=None):
        '''
        This function recursively gathers all subdirectories of a 
        given directory. It returns a list of all subdirectories.
        '''
        # If no list is given, create a new list
        if subdir_list is None:
            subdir_list = []
            
        # Loop over all files and directories in the given directory
        for name in os.listdir(directory):

            # Create the full path to the file or directory
            path = os.path.join(directory, name)

            # If the path is a directory, append it to the list
            if os.path.isdir(path):
                subdir_list.append(path)

                # Call the function recursively with the new path
                self.gather_subdirs(path, subdir_list)

        #update number of subdirectories gathered
        print(f"{self.dash}\{len(subdir_list)} subdirectories have been gathered.")
                
        return subdir_list

    def gather_txt_paths(self, subdirs):
        '''This function gathers all text file paths into a list'''

        #start message
        print(f"{2*self.dash}\nGathering text files...")

        txt_paths = []

        #gather all text file paths into list
        for i, subdir in enumerate(subdirs):
            for file in os.listdir(subdir):
                if file.endswith(".txt"):
                    txt_paths.append(os.path.join(subdir, file))
                    print(f"+{i+1}", sep="", end="")
        
        print(f"\n{self.dash}\n{len(txt_paths)} text files have been gathered in total.")

        return txt_paths

    def gather_file_names(self, text_paths):
        '''This function gathers all file names into a list'''

        file_names = []

        #gather all file names into list
        for path in text_paths:
            file_name = os.path.basename(path)
            file_names.append(file_name)

        print(f"{self.dash*2}\n{len(file_names)} file names have been gathered in total.")

        return file_names  

    def gather_file_content(self, txt_paths):
        '''This function gathers all file content into a list'''

        file_content = []

        #gather all file content into list
        for path in txt_paths:
            with open(path, "r") as file: # open file in read mode
                content = file.read()
                file_content.append(content)

        print(f"{self.dash*2}\n{len(file_content)} files' content has been gathered in total.")

        return file_content

    def save_corpus(self, file_names, file_content):
        """This functions saves the corpus as a csv after converting to df"""
        
        #create df
        df = pd.DataFrame(list(zip(file_names, file_content)), columns=["File Name", "File Content"])

        #save df as csv
        df.to_csv("corpus.csv", index=False)

        print(f"{self.dash*2}\nCorpus has been saved as a csv file.\n\n{self.dash*2}")