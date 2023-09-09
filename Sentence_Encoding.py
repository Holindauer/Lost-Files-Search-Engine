
'''
This class is used to encode the corpus of text files gathered from the Build-Corpus.py file.

Running the encode_corpus() function will encode the corpus using a pretrained distilbert model
and save the encoded corpus to the encoded_corpus.csv file. It should be noted that each document
was encoded into a 768 dimensional vector. The way this is represented in this CSV file is that 
each row is indexed by the file name and each column is a dimension of the vector.

'''

from sentence_transformers import SentenceTransformer
import pandas as pd
import os

class EncodeCorpus:
    def __init__(self):
        '''
        corpus_path refers to the path to the csv file containing 
        the corpus that was created by the Build_Corpus.py file.
        '''
        self.dash = "-"*50 + "\n"

    def encode_corpus(self, corpus_path):
        
        #retireve model
        model = self.instantiate_model()

        #get corpus
        file_names, file_content = self.retrieve_corpus(corpus_path)

        #encode corpus
        encoded_corpus = self.encode_sentence(model, file_content, file_names)

        #save encoded corpus
        self.save_encoded_corpus(encoded_corpus)

        #convert to numpy array
        encoded_corpus = encoded_corpus.to_numpy()

        return model, encoded_corpus, file_names, file_content

    
    def instantiate_model(self):
        """This function instantiates the model to be used for encoding the corpus.
        The model is a pretrained distilbert from the SentenceTransformer library.
        It was fine tuned for quora duplicate questions detection retrieval .

        If this is the first time this function is called, the model will be retrieved
        from sentence-transformers and saved. Otherwise, the model will be loaded from
        where it was saved the first time.
        """
        #get script directory
        script_dir = os.path.dirname(__file__)

        #check if models dir is present
        if "models" in os.listdir(script_dir):
            #if present, load model
            model = SentenceTransformer('models/')
            
        #otherwise instantiate new model
        else:
            #print start message
            print(f"{self.dash*2}\n\nRetrieving Model...")

            #instantiate model
            model =  SentenceTransformer('quora-distilbert-base')

            #save model to models dir
            model.save("models/")

            #print success message
            print(f"\n\nModel Retrieved Successfully!")

        return model


    def retrieve_corpus(self, corpus_path):
        """This function retrieves the corpus from the corpus.csv file."""
        
        #print start message
        print(f"{self.dash*2}\n\nRetrieving Corpus...")

        #read in corpus as dataframe
        df = pd.read_csv(corpus_path)

        #return column values as lists
        return df["File Name"].tolist(), df["File Content"].tolist()


    def encode_sentence(self, model, file_content, file_names):
        """This function encodes the corpus of text files using the model."""
        
        #print start message
        print(f"{self.dash*2}\n\nEncoding Corpus...")

        #encode corpus
        encoded_corpus = model.encode(file_content)

        #create dataframe of encoded corpus with file names as index
        encoded_corpus_df= pd.DataFrame(encoded_corpus, index=file_names)

        print("\n\nPrinting First Few Encodings of Corpus\n", encoded_corpus_df.head(), "\n\n")

        #print success message
        print(f"\n\nCorpus Encoded Successfully!")

        #return encoded corpus
        return encoded_corpus_df


    def save_encoded_corpus(self, encoded_corpus):
        """This function saves the encoded corpus to the encoded_corpus.csv file."""
        
        #print start message
        print(f"{self.dash*2}\n\nSaving Encoded Corpus...")

        #save encoded corpus to corpus.csv
        encoded_corpus.to_csv("encoded_corpus.csv")

        #print success message
        print(f"\n\nCorpus Saved Successfully!")


