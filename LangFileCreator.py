#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.lang file helper for Tanks: The Crusades

Author: Ton
    Don't message me if you have any questions regarding this script,
    because I don't know what I'm doing either.
Python version: 3.11.3 (lower than 3.10.x is also fine, but idk for sure)
"""

"""
    Only keeps everything after the separator, removing everything else
    and creates a new file as output.
    
    Args:
        inputFile (str): the name of the input text file + file type
        outputFile (str): the name of the output text file + file type
        separator (str): the character(s) after which everything needs to be removed
    
    Output:
        A file called {outputFile} containing the output.
"""


def stripLanguage(inputFile, outputFile, separator):
    language = []

    try:
        # Read and store the input
        with open(inputFile, "r", errors="replace") as sourceDocument:
            # Source language name, append this separately to prevent writing an unnecessary newline
            language.append(sourceDocument.readline().strip("\n"))
            for line in sourceDocument:
                # Only keep the lines with actual letters in it
                if line != "\n" and line != " ":
                    language.append(line.split(separator, 1)[0])

        # Write the stored input
        with open(outputFile, "w") as outputDocument:
            for line in language:
                outputDocument.write(line + "\n")
                
        print(f"{outputFile} has been successfully created!")

    except Exception as e:
        print(e)


"""
    Merges the stripped English language file with the file containing your translation
    
    Args:
        englishWordsFile (str): the name of the input text file + file type
        translatedWordsFile (str): the name of the output text file + file type
		separator (str): the character(s) which separate the English 
                         and translated words/phrases
        
    Output:
        The .lang file, suitable for Tanks: The Crusades
"""


def createLanguage(englishWordsFile, translatedWordsFile, separator):
    englishLines = []
    try:
        # Read and store the input. This is the left side of the .lang file
        with open(englishWordsFile, "r", errors="replace") as englishDocument:
            # Skip the language name
            next(englishDocument)
            for line in englishDocument:
                # Only keep the lines with actual letters in it
                if line != "\n" and line != " ":
                    englishLines.append(line.rstrip("\n"))

    except Exception as e:
        print(e)

    translatedLines = []
    try:
        # Read and store the input again. This is the right side of the .lang file
        with open(translatedWordsFile, "r", errors="replace") as translatedDocument:
            # Use the first line of the file as the name of the language
            langName = translatedDocument.readline().strip("\n")
            for line in translatedDocument:
                # Only keep the lines with actual letters in it
                if line != "\n" and line != " ":
                    translatedLines.append(line.rstrip("\n"))
    except Exception as e:
        print(e)

    # Prevents index errors
    if len(englishLines) == len(translatedLines):
        try:
            # Merge the 2 stored inputs with an "=" and write it to an output file
            with open(f"{langName}.lang", "w") as outputLanguage:
                outputLanguage.write(f"{langName}\n")
                for i in range(len(englishLines)):
                    outputLanguage.write(
                        f"{englishLines[i]}{separator}{translatedLines[i]}\n"
                    )
            print(f"{langName}.lang has been successfully created!")

        except Exception as e:
            print(e)
    else:
        print(
            f"Error: {englishWordsFile} does not have an equal amount of lines compared to {translatedWordsFile}"
        )


"""
    For a list of English words separated with a newline, adds a character 
	(DEFAULT: '=') after all of them, and creates a file as its output.

    Args:
        nonSeparatedFile (str): the name of the input text file + file type
        separatedFile (str): the name of the output text file + file type
		separator (str): the character(s) which are added
        
    Output:
        A file called {separatedFile} containing the output.
"""


def addSeparatorToEnglish(nonSeparatedFile, separatedFile, separator):
    englishLines = []

    try:
        # Read and store the input
        with open(nonSeparatedFile, "r", errors="replace") as sourceDocument:
            langName = sourceDocument.readline().strip("\n")
            for line in sourceDocument:
                if line != "\n" and line != " ":
                    englishLines.append(line.rstrip("\n"))

        # Write the stored input
        with open(separatedFile, "w") as outputDocument:
            outputDocument.write(f"{langName}\n")
            for line in englishLines:
                outputDocument.write(f"{line}{separator}\n")
                
        print(f"{separatedFile} has been successfully created!")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    # A whole bunch of input / output, this isn't really important
    print("Quick(?) .lang file creator for Tanks: The Crusades")

    choice = ""
    while choice != "q":
        print("---------------")
        print("(1) Strip language/txt file: remove everything after and including the \"=\"-sign")
        print("(2) Create a language: output of 1 + a translation required")
        print("(3) Add an \"=\"-sign after every word")
        print("(q) Quit program")
        print("---------------")
        choice = input(">")
        if choice == "1":
            print("---------------")
            print("File to strip (INCLUDE file type):")
            inputFile = input(">")
            outputFile = f"{inputFile}_stripped.txt"
            print("Separator (press ENTER if you want to keep it as \"=\"): ")
            sepChoice = input(">")
            if sepChoice == "":
                separator = "="
            else:
                separator = sepChoice
            
            stripLanguage(inputFile, outputFile, separator)

        if choice == "2":
            print("---------------")
            print("Add the stripped file (INCLUDE file type):")
            inputStrippedFile = input(">")
            print("Add the translation file (INCLUDE file type):")
            inputTranslatedFile = input(">")
            print("Separator (press ENTER if you want to keep it as \"=\"): ")
            sepChoice = input(">")
            if sepChoice == "":
                separator = "="
            else:
                separator = sepChoice
            
            createLanguage(inputStrippedFile, inputTranslatedFile, separator)

        if choice == "3":
            print("---------------")
            print("Add the stripped file (INCLUDE file type):")
            inputFile = input(">")
            outputFile = f"{inputFile}_separated.txt"
            print("Separator (press ENTER if you want to keep it as \"=\"): ")
            sepChoice = input(">")
            if sepChoice == "":
                separator = "="
            else:
                separator = sepChoice
            addSeparatorToEnglish(inputFile, outputFile, separator)

    print("Program has been terminated!")
