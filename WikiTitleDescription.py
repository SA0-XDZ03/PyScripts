import wikipedia

searchInput = input("Enter Search: ")

def searchWikipedia(searchTerm):
    searchResults = wikipedia.search(searchTerm)
    for result in searchResults:
        print(result)

searchWikipedia(searchInput)

def getWikipediaArticle(articleTitle):
    article = wikipedia.page(articleTitle)
    print(article.title)
    print(article.summary)

getWikipediaArticle(searchInput)