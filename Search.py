from Build_Corpus import BuildCorpus
from Sentence_Encoding import EncodeCorpus
from scipy.spatial.distance import cdist
import numpy as np
import subprocess
import time

'''
This class is responsible for directing the search process. 
It begins by using the class in Build_Corpus.py to build a corpus 
of files from a specified directory. It then uses the class in 
Sentence_Encoding.py to retireve the model that will be used to
encode the corpus and search query into vectors. The method
similarity() is then called to compute the cosise similarity between
the query and each document in the corpus. 

Cosine_Similarity = (A.dot(B)) / (||A|| * ||B||) 

'''

class Search_Files:
    def __init__(self):

        #make it loop pretty :)
        self.dash = "-" * 50 + "\n"


    def search(self):
        '''
        This is the main function that directs the search process.

        It begins by using the class in Build_Corpus.py to build a corpus
        of files from a specified directory. It then uses the class in
        Sentence_Encoding.py to retireve the model that will be used to
        encode the corpus and search query into vectors. The method
        similarity() is then called to compute the cosise similarity between
        the query and each document in the corpus. It should be noted that 
        the vectors are represented as numpy arrays. The method display_results()
        is then called to display the top 5 results to the user.This process is
        looped until the user is done searching.
        '''
        #print start message
        print(f"{self.dash*2}\n\nWelcome to the Lost Files Search Engine...{self.dash*2}\n\n")

        start_time = time.time()
        #instantiate corpus builder
        corpus_builder = BuildCorpus()

        #build corpus as df
        corpus_df = corpus_builder.corpus()

        #instantiate corpus encoder passing in the path to the corpus
        corpus_encoder = EncodeCorpus()

        #retrieve model and encode corpus with it
        model, encoded_corpus, file_names, file_content, file_paths = corpus_encoder.encode_corpus(corpus_df)

        keep_searching = True

        #loop search until user is done searching
        while keep_searching == True:
            #prompt user for query
            encoded_query = self.prompt_query(model)

            #compute similarity between query and corpus  --- result is indicies of files ranked
            similarity_rankings = self.similarity(encoded_corpus, encoded_query)

            #display results
            self.display_results(similarity_rankings, file_names, file_content)

            #prompt user to search again
            keep_searching = self.continue_search()



    def prompt_query(self, model):
        ''' this function prompts the user for a query and encodes it '''

        print(f"{self.dash*2}\nLost Files Search Engine Ready\n{self.dash*2}\n\n")

        #prompt user for query
        query = input(f"{self.dash*2}\nEnter your search query: ")

        #encode unsqueezed query
        return model.encode(query).reshape(1, -1)

    def similarity(self, encoded_corpus, encoded_query):
        ''' this function computes the cosine similarity between the query and each document in the corpus '''

        #compute similarity between query and corpus
        similarity = cdist(encoded_corpus, encoded_query, "cosine").reshape(-1)

        #sort similarity scores in ascending order
        return  np.argsort(similarity)
    
    def display_results(self, similarity_rankings, file_names, file_content):
        ''' this function displays the results of the search '''

        #print start message
        print(f"{self.dash*5}\nDisplaying Top 5 Most Similar Results to your Query...\n{self.dash}\n")

        #display top 5 results
        for i in range(5):
            print("Ranking: ", i+1)
            print(f"File Name: {file_names[similarity_rankings[i]]}\n\nFile Content: {file_content[similarity_rankings[i]]}\n\n{self.dash}\n")
        

    def continue_search(self):
            ''' This function prompts the user to search again or quit'''
        #prompt user to search again
            keep_searching = input(f"{self.dash}\n\nWould you like to search again? (y/n): ")
            if keep_searching == "n":
                keep_searching = False
            elif keep_searching == "y":
                keep_searching = True
            else:
                print(f"{self.dash}\n\nInvalid input. Please try again.\n\n")
                #recursively call function again
                return self.continue_search()
            
            return keep_searching
        
       



if __name__ == "__main__":
    Search = Search_Files()
    Search.search()