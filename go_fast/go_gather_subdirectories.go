package main

// This program was written to replace the python script Build_Corpus.py which was used to gather the text file
// paths and contents from a directory and all of its subdirectories. The python script managed well for small
// directories but proved extremely slow for large directories. This go script perfroms the same task but takes
// advantage of goroutines to speed up the process.

// The program first reads a text file containing the directory to search. It then walks the directory to gather
// the subdirectories. For each subdirectory, a goroutine is started to gather the text files. For each text file,
// a goroutine is started to read the file contents. The file contents are then saved to a JSON file.

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"sync"
)

func gatherTextFiles(dir string, textFiles *[]string, wg *sync.WaitGroup) {
	// This function gathers the paths to text files
	// in a directory and adds them to a slice

	defer wg.Done() // Defer the Done() method to be called at the end of the function

	err := filepath.Walk(dir, func(path string, info os.FileInfo, err error) error { // Walk the directory to gather the text files
		if err != nil {
			return err
		}
		if !info.IsDir() && strings.HasSuffix(info.Name(), ".txt") { // If the path is a text file with a .txt extension
			*textFiles = append(*textFiles, path) // Add the text file to the slice
		}
		return nil
	})

	if err != nil {
		fmt.Println("Error walking the path:", err)
	}
}

func readTextFiles(filePath string, fileContents *[]string, wg *sync.WaitGroup) {
	// This function reads the contents of a text file and adds them to a slice

	defer wg.Done() // Defer the Done() method to be called at the end of the function

	content, err := os.ReadFile(filePath) // Read the file
	if err != nil {
		fmt.Println("Error reading the file:", err)
		return
	}

	*fileContents = append(*fileContents, string(content)) // Add the file contents to the slice
}

func main() {
	var wg sync.WaitGroup // Intiialize WaitGroup to wait for goroutines to finish

	//----------------------------------------------------------------------------------------------------------get directory to search
	// Read the directory to search from a text file
	content, err := os.ReadFile("directory_to_search.txt")
	if err != nil {
		fmt.Println("Error reading the file:", err)
		return
	}

	// Trim the whitespace from the directory path
	root := strings.TrimSpace(string(content))

	// Initalize slices to store the subdirectories, text files, and file contents
	var subdirs []string
	var textFiles []string
	var fileContents []string

	//----------------------------------------------------------------------------------------------------------gather subdirectories
	// Walk the root directory to gather the subdirectories
	err = filepath.Walk(root, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if info.IsDir() { // If the path is a directory
			subdirs = append(subdirs, path) // Add the subdirectory to the slice
		}
		return nil
	})

	if err != nil {
		fmt.Println("Error walking the path:", err) // If there is an error, print it
		return
	}

	//----------------------------------------------------------------------------------------------------------go routine 1 for getting text file paths
	// For each subdirectory, start a goroutine to gather the text files
	for _, subdir := range subdirs {
		wg.Add(1)                                   // Add 1 to the WaitGroup counter
		go gatherTextFiles(subdir, &textFiles, &wg) // Start a goroutine to gather text files
	}

	wg.Wait() // Wait for all goroutines to finish

	//----------------------------------------------------------------------------------------------------------go routine 2 for reading text file contents
	// For each text file, start a goroutine to read the file contents
	for _, textFile := range textFiles {
		wg.Add(1)                                      // Add 1 to the WaitGroup counter
		go readTextFiles(textFile, &fileContents, &wg) // Start a goroutine to read file contents
	}

	wg.Wait() // Wait for all goroutines to finish

	//----------------------------------------------------------------------------------------------------------save file contents

	// Save the fileContents slice to JSON
	jsonData, err := json.Marshal(fileContents)
	if err != nil {
		fmt.Println("Error marshaling fileContents to JSON:", err)
		return
	}

	// Write the JSON data to a file
	err = os.WriteFile("file_contents.json", jsonData, 0644)
	if err != nil {
		fmt.Println("Error writing fileContents JSON to file:", err)
		return
	}

	// Print a message to the console
	fmt.Println("Text file contents saved to file_contents.json")

	// Save the text file paths slice to JSON
	jsonDataPaths, err := json.Marshal(textFiles)
	if err != nil {
		fmt.Println("Error marshaling textFiles to JSON:", err)
		return
	}

	// Write the JSON data to a file
	err = os.WriteFile("file_paths.json", jsonDataPaths, 0644)
	if err != nil {
		fmt.Println("Error writing textFiles JSON to file:", err)
		return
	}

	// Print a message to the console
	fmt.Println("Text file paths saved to file_paths.json")
}
