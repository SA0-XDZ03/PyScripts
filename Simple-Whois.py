import subprocess
import sys
import os

def getWhois(domain):
    """Fetch WHOIS information for a given domain safely."""
    try:
        result = subprocess.run(['whois', domain], capture_output=True, text=True, check=True)
        return result.stdout
    except FileNotFoundError:
        return "Error: The 'whois' command is not installed. Please install it and try again."
    except subprocess.CalledProcessError:
        return f"Error: Unable to retrieve WHOIS information for {domain}. Check if the domain is valid."

def processInput(user_input):
    """Determine if the input is a file or a single domain, then process accordingly."""
    if os.path.isfile(user_input):
        with open(user_input, 'r') as file:
            domains = [line.strip() for line in file if line.strip()]
    else:
        domains = [user_input]
    
    return domains

def main():
    """Main function to execute the WHOIS lookup script."""
    user_input = input("Enter a domain or path to a file containing domains: ").strip()
    domains = processInput(user_input)
    
    outputFile = "Whois_Results.txt"
    with open(outputFile, 'w') as file:
        for domain in domains:
            print(f"Fetching WHOIS for: {domain}...")
            whois_info = getWhois(domain)
            print(whois_info + "\n" + "-"*50 + "\n")
            file.write(f"WHOIS for {domain}:\n{whois_info}\n{'-'*50}\n")
    
    print(f"WHOIS lookup completed. Results saved in '{outputFile}'")

if __name__ == "__main__":
    main()
