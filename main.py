import random
import nltk
import re

from thesaurus import Thesaurus

random.seed(0)


class Obfuscator:
    def __init__(self, textIn, thesaurus=Thesaurus()):
        self.textIn = textIn
        self.thesaurus = thesaurus


    @property
    def textIn(self):
        return self._textIn

    @textIn.setter
    def textIn(self, textIn):
        self._textIn = textIn
        textSentences = self.splitToSentences(self._textIn)
        textTokenised = self.tokenise(textSentences)
        print(textTokenised)
        textObfuscated = self.obfuscate(textTokenised)
        textDetokenised = self.detokenise(textObfuscated)
        self.textOut = self.getTextFromWordArray(textDetokenised)


    def preProcess(self, textIn):
        pass


    def splitToSentences(self, textIn):
        #Schema: [sentence, sentence, ...]
        return nltk.sent_tokenize(textIn)


    def tokenise(self, textSentences):
        #Schema: [(word, tag, capsFlag), (word, tag, capsFlag), ...]
        textTokenised = []
        for sentence in textSentences:
            words = nltk.word_tokenize(sentence)
            tags = nltk.pos_tag(words) #Change this to tag
            capsFlags = [tuple([ word==word.capitalize() ]) for word in words]
            textTokenised.append([
                tags[i]+capsFlags[i]
                for i in range(len(words))
            ])
        return textTokenised


    def obfuscate(self, textTokenised):
        textObfuscated = self.substituteSynonyms(textTokenised)
        return textObfuscated


    def substituteSynonyms(self, textToSubstitute):
        textSubstituted = []
        return textToSubstitute #textSubstituted


    def detokenise(self, textObfuscated):
        #Schema: [(word, tag, capsFlag), (word, tag, capsFlag), ...] -> [word, word, ...]
        return [[token[0] for token in sentence] for sentence in textObfuscated]


    def getTextFromWordArray(self, textObfuscated):
        textOut = " ".join([
            " ".join([item for item in sentence])
            for sentence in textObfuscated
        ])

        #Handle punctuation which shouldn't have a space before it
        for item in [".",",","?","!","...",":",";",")","]","}",">","%"]:
            textOut = textOut.replace(" "+item, item)
        #Handle punctuation which shouldn't have a space after it
        for item in ["(","[","{","<","#","@","£","$"]:
            textOut = textOut.replace(item+" ", item)
        #Handle the nltk tagged format of double quotation marks
        for item in ["`` "," ''"]:
            textOut = textOut.replace(item, "\"")

        return textOut


    def __str__(self):
        return self.textOut



#text = "The quick brown fox jumped over the lazy dog, and this is a test (no really, it is - and it stole £20)!"

text = "This is a test - Edmund's test. He says \"Hello\"."

#Find something to match all single quote quotations

print(text)
t = Obfuscator(text)
print(t)
