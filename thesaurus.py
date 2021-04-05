import pickle


class Thesaurus:
    def __init__(self, filename="./thesauruses/thesaurusB.pickle", disallowPhrases=True):
        self._disallowPhrases = disallowPhrases
        self.filename = filename


    @property
    def filename(self):
        """Getter for the filename property"""
        return self._filename

    @filename.setter
    def filename(self, filename):
        """Setter for the filename property, which automatically loads the
        new file on change"""
        self._filename = filename
        self.content = self.getThesaurus()


    def getThesaurus(self):
        """Load the thesaurus from a pickled file"""
        with open(self.filename, "rb") as handle:
            thesaurus = {}
            for key,value in pickle.load(handle).items():
                if self._disallowPhrases and " " not in key:
                    synonyms = [item for item in value
                        if self._disallowPhrases and " " not in item]
                    if synonyms != []:
                        thesaurus[key] = synonyms

        return thesaurus


    def getSynonyms(self, word):
        """Get the synonym for a given word in the loaded thesaurus"""
        if word in self.content.keys():
            return self.content[word]
        else:
            return ()


    def __repr__(self, numShow=-1):
        """Show the contents of the thesaurus, by default all of it, with the
        option to select only the first `numShow`, an optional parameter"""
        return "\n\n".join([
            "{} : {}".format(key, "["+", ".join(value)+"]")
            for key,value in self.content.items()
        ][:numShow])


if __name__=="__main__":
    thesaurus = Thesaurus()
    print(thesaurus.__repr__(numShow=5))
