import subprocess
import os
from tld import get_tld

def getTopLevelDomain(url):
    """Fetch the top-level domain (TLD) for a given URL safely."""
    try:
        domain = get_tld(url, as_object=True)
        return domain.tld
    except Exception as e:
        return f"Error processing '{url}': {str(e)}"

def processInput(userInput):
    """Determine if the input is a file or a single URL, then process accordingly."""
    if os.path.isfile(userInput):
        with open(userInput, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
    else:
        urls = [userInput]
    
    return urls

def main():
    """Main function to execute the TLD extraction script."""
    userInput = input("Enter a URL or path to a file containing URLs: ").strip()
    urls = processInput(userInput)
    
    outputFile = "tld_results.txt"
    with open(outputFile, 'w') as file:
        for url in urls:
            print(f"Processing URL: {url}...")
            tldInfo = getTopLevelDomain(url)
            print(f"TLD: {tldInfo}\n{'-'*50}")
            file.write(f"URL: {url}\nTLD: {tldInfo}\n{'-'*50}\n")
    
    print(f"TLD extraction completed. Results saved in '{outputFile}'")

if __name__ == "__main__":
    main()
