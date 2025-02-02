import requests
import concurrent.futures
import logging
import os
import time
from itertools import product
from colorama import Fore, Style

# Configure Logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def loadTLDs(filePath):
    """Load TLDs from a single file securely."""
    if os.path.exists(filePath):
        with open(filePath, 'r', encoding='utf8') as file:
            return [line.strip() for line in file if line.strip()]
    else:
        logger.warning(f"TLD file not found: {filePath}")
        return []

def generateDomains(keyword, tlds):
    """Generate all possible domain combinations for the keyword."""
    domains = set()
    
    for tld in tlds:
        domains.add(f"{keyword}.{tld}")
    
    for combo in product(tlds, repeat=2):
        domains.add(f"{keyword}.{combo[0]}.{combo[1]}")
    
    return [f"https://{domain}" for domain in domains] + [f"http://{domain}" for domain in domains]

def checkDomainAvailability(domain):
    """Check if a domain is active by sending an HTTP request."""
    try:
        logger.debug(f"Testing TLD: {domain}")
        response = requests.head(domain, timeout=2, allow_redirects=True)
        if 200 <= response.status_code < 400:
            logger.info(Fore.GREEN + f"[ACTIVE] {domain} ({response.status_code})" + Style.RESET_ALL)
            return domain
        else:
            logger.debug(Fore.YELLOW + f"[INACTIVE] {domain} ({response.status_code})" + Style.RESET_ALL)
            return None
    except requests.exceptions.RequestException as e:
        logger.debug(Fore.RED + f"[ERROR] {domain} ({str(e)})" + Style.RESET_ALL)
        return None

def main():
    """Main function to handle user input and execution."""
    keywordInput = input("Enter Keyword or File Path for Keywords: ").strip()
    
    if not keywordInput:
        logger.warning("Please provide a valid keyword or file path.")
        return
    
    keywords = [keywordInput] if not os.path.isfile(keywordInput) else open(keywordInput, 'r').read().splitlines()
    
    tlds = loadTLDs("Supplies/UniqueTLDs.txt")
    
    if not tlds:
        logger.error("TLD file is missing. Please check your file path.")
        return
    
    availableDomains = []
    startTime = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        for keyword in keywords:
            logger.info(f"Checking domains for: {keyword}")
            domainsToCheck = generateDomains(keyword, tlds)
            results = executor.map(checkDomainAvailability, domainsToCheck)
            availableDomains.extend(filter(None, results))
    
    endTime = time.time()
    elapsedTime = endTime - startTime
    
    print("\n" + "="*50)
    print("Domain Availability Report")
    print("="*50 + "\n")
    
    if availableDomains:
        print(Fore.GREEN + "Active Domains Found:" + Style.RESET_ALL)
        for domain in availableDomains:
            print(Fore.GREEN + domain + Style.RESET_ALL)
    else:
        print(Fore.RED + "No active domains found." + Style.RESET_ALL)
    
    print(Fore.CYAN + f"Scan Completed in {elapsedTime:.2f} seconds" + Style.RESET_ALL)
    
if __name__ == "__main__":
    main()
