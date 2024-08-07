import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probDistribution = {}
    totalPages = len(corpus)
    
    if corpus[page]:
        linkedPages = corpus[page]
    
    else:
        linkedPages = corpus.keys()




    for pg in corpus:
        if pg in linkedPages:
            probDistribution[pg] = (1 - damping_factor) / totalPages + (damping_factor / len(linkedPages))
        
        else:
            probDistribution[pg] = (1 - damping_factor) / totalPages
    
    return probDistribution



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    
    pageCounter = {page: 0 for page in corpus}
    totlaPages = list(corpus.keys())
    randomPage = random.choice(totlaPages)
    pageCounter[randomPage] += 1

    for i in range(1, n):
        probs = transition_model(corpus, randomPage, damping_factor)
        
        pages = list(probs.keys())
        weights = list(probs.values())
        nextPage = random.choices(pages, weights=weights)[0]
        
        pageCounter[nextPage] += 1
        randomPage = nextPage
    
    pageRank = {}
    for pg, count in pageCounter.items():
        pageRank[pg] = count / n
    
    return pageRank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    N = len(corpus)
    pageRank = {page: 1 / N for page in corpus}
    convergenceThreshold  = 0.001
    CONVERGENCE = False

    while not CONVERGENCE:
        newPageRank = {}
        
        for pg in corpus:
            newRank = (1 - damping_factor) / N
            
            for linkingPg, linkedPg in corpus.items():
                if pg in linkedPg:
                    numPages = len(linkedPg)
                    newRank += damping_factor * pageRank[linkingPg] / numPages
                
                elif len(linkedPg) == 0:
                    newRank += damping_factor * pageRank[linkingPg] / N
            
            newPageRank[pg] = newRank
        CONVERGENCE = True
        
        for pg in corpus:
            if abs(pageRank[pg] - newPageRank[pg]) > convergenceThreshold:
                CONVERGENCE = False
        
        pageRank = newPageRank.copy()
    
    return pageRank



if __name__ == "__main__":
    main()
