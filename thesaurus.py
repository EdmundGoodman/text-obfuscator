import pickle


class Thesaurus:
    def __init__(self, filename="./thesauruses/thesaurusB.pickle", disallowPhrases=True):
        self.disallowPhrases = disallowPhrases
        self.filename = filename


    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        self._filename = filename
        self.content = self.getThesaurus()


    def getThesaurus(self):
        with open(self.filename, "rb") as handle:
            thesaurus = {}
            for key,value in pickle.load(handle).items():
                if self.disallowPhrases and " " not in key:
                    synonyms = [item for item in value
                        if self.disallowPhrases and " " not in item]
                    if synonyms != []:
                        thesaurus[key] = synonyms

        return thesaurus


    def getSynonyms(self, word):
        if word in self.content.keys():
            return self.content[word]
        else:
            return ()


    def __repr__(self, numShow=-1):
        return "\n\n".join([
            "{} : {}".format(key, "["+", ".join(value)+"]")
            for key,value in self.content.items()
        ][:numShow])


if __name__=="__main__":
    thesaurus = Thesaurus()
    print(thesaurus.__repr__(numShow=5))
