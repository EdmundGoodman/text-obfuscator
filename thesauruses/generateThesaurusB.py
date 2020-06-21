import pickle
import nltk

#Taken from, and hence with thanks to "https://www.smart-words.org/list-of-synonyms/"

thesaurus = {}
with open("thesaurusRawB.txt") as foo:
    for line in foo.read().lower().split("\n"):
        if line == "":
            continue

        starter, *synonyms = line.split(" — ")
        synonyms = synonyms[0].split(", ")
        words = [starter] + synonyms
        for word in words:
            tag = nltk.pos_tag([word])[0][1]
            thisWords = set([w for w in words if nltk.pos_tag([w])[0][1] == tag])
            thesaurus[word] = tuple(thisWords - set([word]))

with open('thesaurusB.pickle', 'wb') as handle:
    pickle.dump(thesaurus, handle, protocol=pickle.HIGHEST_PROTOCOL)

if 0:
    with open("thesaurusB.pickle", "rb") as handle:
        thesaurus = pickle.load(handle)
    print( list(thesaurus.items())[0] )
