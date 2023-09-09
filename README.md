# Lost-Files-Search-Engine
A Search Engine for Lost Local Files using Semantic Search
----------------------------------------------------------------------------------

## Currently, to run the search engine on a local directory, run Search.py

This project intends to build a search engine for local files that have been lost
somewhere within a directory. 

The Seach engine works well for small directories with minimal subdirectories. 
However, because it is all written in python, it is extremely slow for larger 
directories. I am in the process of rewriting much of the python scripts into
Go to take advantage of the speed of go routines.

----------------------------------------------------------------------------------<>

The way this project works is as follows:

1.) Use a sentence embedding model to encode contents of all files within
    a directory (and its subdirectories) into vector embeddings

2.) Gather a semantic description of the lost file wanting to be found

3.) Encode this semantic description into a vector embedding 

4.) Use a simmilarity function to find the file within the directory that most 
    resembles the search

----------------------------------------------------------------------------------<>
    
