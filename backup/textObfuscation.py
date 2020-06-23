import random
import pickle
import copy
import nltk

random.seed(0)


class Thesaurus:
    def __init__(self, filename="smallThesaurus.pickle"):
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
            thesaurus = pickle.load(handle)

        return {
            key : [item for item in value if " " not in item]
            for key,value in thesaurus.items()
        }


    def getSynonyms(self, word):
        if word in self.content.keys():
            return self.content[word]
        else:
            return ()


    def __repr__(self):
        return "\n\n".join(["{}:{}".format(key,value) for key,value in self.content.items()])


class Text:
    def __init__(self, text):
        self.text = text


    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self.tokenisedSections = self.tokenise()


    def tokenise(self):
        sentences, tokenisedSections = nltk.sent_tokenize(self.text), []
        for sentence in sentences:
            words = nltk.word_tokenize(sentence)
            tokens = nltk.pos_tag(words)
            capsFlags = [tuple([ word==word.capitalize() ]) for word in words]
            tokenisedSections.append([
                tokens[i]+capsFlags[i]
                for i in range(len(words))
            ])
        return tokenisedSections

        """punctuationNoSpaceAfter = "( [ { < # @ £ $".split(" ")
        punctuationNoSpaceBefore = ". , ? ! ... : ; ) ] } > %".split(" ")"""




    def obfuscate(self, thesaurus):
        self.text = self.substituteSynonyms(thesaurus)

    def substituteSynonyms(self, thesaurus):

        print(self.tokenisedSections)

        for i in range(len(self.tokenisedSections)):
            print(self.tokenisedSections[i])
        exit()

    def substituteSynonyms(self, thesaurus):
        newText = ""
        for i in range(len(self.tokenisedSections)):
            allValidSubstitutions = []
            for j, tokenisedWord in enumerate(self.tokenisedSections[i]):

                #print(i, j, tokenisedWord)

                synonyms = thesaurus.getSynonyms(tokenisedWord[0])
                allValidSubstitutions.append([])
                for synonym in synonyms:
                    textSub = Text( " ".join([
                        value[0] if j != k else synonym
                        for k,value in enumerate(self.tokenisedSections[i])
                    ]) ) #Work needed to allow turns of phrases to be substituted
                    #           https://www.nltk.org/api/nltk.tokenize.html - maybe a MWE tokeniser??

                    #print(textSub)

                    #print(i,j)
                    #print(self.tokenisedSections[i])
                    #print(textSub.tokenisedSections)
                    #print()

                    if self.tokenisedSections[i][j][1] == textSub.tokenisedSections[i][j][1]:
                        sub = textSub.tokenisedSections[i][j][0]
                        if textSub.tokenisedSections[i][j][2]:
                            sub.capitalize()
                        allValidSubstitutions[-1].append(sub)

            for j, validSubstitutions in enumerate(allValidSubstitutions):
                if len(validSubstitutions) == 0:
                    newText += self.tokenisedSections[i][j][0]
                else:
                    newText += random.choice(validSubstitutions)

                #Maintain formatting - or maybe not, since it looks diff, but is still comprehensible
                #Ensure punctuation doesn't have spaces before it

                #if j+1 != len(allValidSubstitutions) and self.tokenisedSections[i][j+1][0] not in list(",.?\'\"!"):
                #    newText += " "
                try:
                    if self.tokenisedSections[i][j+1][0] not in list(",.?\'\"!"):
                        newText += " "
                except IndexError:
                    pass

            newText += " "
            #print()

        return newText


    def __repr__(self):
        return self.text


#text = """One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections. The bedding was hardly able to cover it and seemed ready to slide off any moment. His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked. "What's happened to me? " he thought. It wasn't a dream.

#His room, a proper human room although a little too small, lay peacefully between its four familiar walls. A collection of textile samples lay spread out on the table - Samsa was a travelling salesman - and above it there hung a picture that he had recently cut out of an illustrated magazine and housed in a nice, gilded frame. It showed a lady fitted out with a fur hat and fur boa who sat upright, raising a heavy fur muff that covered the whole of her lower arm towards the viewer. Gregor then turned to look out the window at the dull weather."""

text = "The quick brown fox jumped over the lazy dog."


t = Text(text)
print(t)
t.obfuscate( Thesaurus() )
print(t)
