import wikipedia

def wikipediaAPIData(enterSearchMode):
    dataSearch = wikipedia.summary(enterSearchMode, sentences = int(10))
    dataSearch2 = wikipedia.search(str(enterSearchMode), results = int(10))
    print(dataSearch)
    print("\n\n\n")
    print(dataSearch2)

wikiInput = input("Enter Keyword: ")
wikipediaAPIData(wikiInput)
