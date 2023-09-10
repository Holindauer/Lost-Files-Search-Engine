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

var mu sync.Mutex // This program uses go routines to operate on slices concurrently. Mutex,
// which stands for mutual exclusion, ensures that variables that could be
// be access by multiple go routines are only accessible to one go routine.
// This is to prevent a race condition I was running into.

func gatherTextFiles(dir string, textFiles *[]string, fileNames *[]string, wg *sync.WaitGroup) {
	// This function gathers the text files from a directory and its subdirectories

	defer wg.Done() // Decrement the WaitGroup counter when the function completes

	// These local slices are intialized to reduce the amount of time the slices are locked
	// by the mutex. The local slices are then appended to the global slices after operations complete.
	var localTextFiles []string
	var localFileNames []string

	// Walk the directory to gather its text files
	err := filepath.Walk(dir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if !info.IsDir() && strings.HasSuffix(info.Name(), ".txt") {
			localTextFiles = append(localTextFiles, path)
			localFileNames = append(localFileNames, info.Name())
		}
		return nil
	})

	if err != nil {
		fmt.Println("Error walking the path:", err)
	}

	mu.Lock() // lock up the slices so that only one go routine can access them at a time

	*textFiles = append(*textFiles, localTextFiles...) // Append the text files to the slice
	*fileNames = append(*fileNames, localFileNames...) // Append the file names to the slice

	mu.Unlock() // unlock the slices so that other go routines can access them
}

func readTextFiles(filePath string, fileContents *[]string, wg *sync.WaitGroup) {
	// This function reads the contents of the text files gathered
	// in the function above and appends them to a slice

	defer wg.Done() // Decrement the WaitGroup counter when the function completes

	// Read the file contents
	content, err := os.ReadFile(filePath)
	if err != nil {
		fmt.Println("Error reading the file:", err)
		return
	}

	mu.Lock() // lock up the slice so that only one go routine can access it at a time

	*fileContents = append(*fileContents, string(content)) // Append the file contents to the slice

	mu.Unlock() // unlock the slice so that other go routines can access it
}

func main() {

	// Inform Python Controller Script that the Go Script has started
	fmt.Println("\ngo_gather_subdirectories.go has successfully started...")

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
	var fileNames []string

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
	// print len of subdirs
	fmt.Println("\nNumber of subdirectories:", len(subdirs))

	//----------------------------------------------------------------------------------------------------------go routine 1 for getting text file paths
	// For each subdirectory, start a goroutine to gather the text files
	for _, subdir := range subdirs {
		wg.Add(1)                                               // Add 1 to the WaitGroup counter
		go gatherTextFiles(subdir, &textFiles, &fileNames, &wg) // Start a goroutine to gather text files
	}

	wg.Wait() // Wait for all goroutines to finish

	//----------------------------------------------------------------------------------------------------------go routine 2 for reading text file contents
	// For each text file, start a goroutine to read the file contents
	for _, textFile := range textFiles {
		wg.Add(1)                                      // Add 1 to the WaitGroup counter
		go readTextFiles(textFile, &fileContents, &wg) // Start a goroutine to read file contents
	}

	wg.Wait() // Wait for all goroutines to finish

	fmt.Println("\nNumber of text files:", len(fileContents))

	//----------------------------------------------------------------------------------------------------------save file contents as JSON

	// Print a message to the console

	fmt.Println("\nStarting corpus save process...")

	// Save the fileContents slice to JSON
	jsonData, err := json.Marshal(fileContents)
	if err != nil {
		fmt.Println("Error marshaling fileContents to JSON:", err)
		return
	}

	// Write the JSON data to a file
	err = os.WriteFile("file_contents.json", jsonData, 0644)
	if err != nil {
		fmt.Println("\nError writing fileContents JSON to file:", err)
		return
	}

	// Print a message to the console
	fmt.Println("\nText file contents saved to file_contents.json")

	// Save the text file paths slice to JSON
	jsonDataPaths, err := json.Marshal(textFiles)
	if err != nil {
		fmt.Println("\nError marshaling textFiles to JSON:", err)
		return
	}

	// Write the JSON data to a file
	err = os.WriteFile("file_paths.json", jsonDataPaths, 0644)
	if err != nil {
		fmt.Println("\nError writing textFiles JSON to file:", err)
		return
	}

	// Print a message to the console
	fmt.Println("\nText file paths saved to file_paths.json")

	// Save the text file names slice to JSON
	jsonDataNames, err := json.Marshal(fileNames)
	if err != nil {
		fmt.Println("\nError marshaling fileNames to JSON:", err)
		return
	}

	// Write the JSON data to a file
	err = os.WriteFile("file_names.json", jsonDataNames, 0644)
	if err != nil {
		fmt.Println("\nError writing fileNames JSON to file:", err)
		return
	}

	// Print a message to the console
	fmt.Println("\nText file names saved to file_names.json")
}
