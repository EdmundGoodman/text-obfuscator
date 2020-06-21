import pickle

#Taken from, and hence with thanks to "https://github.com/words/moby", under public domain

thesaurus = {}
with open("thesaurusRawA.txt") as foo:
    for line in foo.read().split("\n"):
        words = line.split(",")
        thesaurus[words[0]] = tuple(words[1:])

with open("thesaurusA.pickle", "wb") as handle:
    pickle.dump(thesaurus, handle, protocol=pickle.HIGHEST_PROTOCOL)


if 0:
    with open("thesaurusA.pickle", "rb") as handle:
        thesaurus = pickle.load(handle)
    print( list(thesaurus.items())[0] )
