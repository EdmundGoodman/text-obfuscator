import random
import copy
import nltk

from thesaurus import Thesaurus

random.seed(0)


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
        print(tokenisedSections)
        return tokenisedSections

        """punctuationNoSpaceAfter = "( [ { < # @ £ $".split(" ")
        punctuationNoSpaceBefore = ". , ? ! ... : ; ) ] } > %".split(" ")"""


    def obfuscate(self, thesaurus):
        self.text = self.substituteSynonyms(thesaurus)


    def substituteSynonyms(self, thesaurus):
        newText = ""
        for i in range(len(self.tokenisedSections)):
            allValidSubstitutions = []
            for j, tokenisedWord in enumerate(self.tokenisedSections[i]):

                synonyms = thesaurus.getSynonyms(tokenisedWord[0])
                allValidSubstitutions.append([])
                for synonym in synonyms:
                    textSub = Text( " ".join([
                        value[0] if j != k else synonym
                        for k,value in enumerate(self.tokenisedSections[i])
                    ]) ) #Work needed to allow turns of phrases to be substituted
                    #           https://www.nltk.org/api/nltk.tokenize.html - maybe a MWE tokeniser??

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
                try:
                    if self.tokenisedSections[i][j+1][0] not in list(",.?\'\"!"):
                        newText += " "
                except IndexError:
                    pass

            newText += " "
        return newText


    def __repr__(self):
        return self.text


text = "The quick brown fox jumped over the lazy dog."

t = Text(text)
print(t)
t.obfuscate( Thesaurus() )
print(t)
