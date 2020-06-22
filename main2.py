import random
import nltk
import re

from thesaurus import Thesaurus

random.seed(0)


class Obfuscated:
    def __init__(self, textIn, thesaurus=Thesaurus()):
        self.textOut = None
        self.thesaurus = thesaurus

        self.textIn = textIn


    @property
    def textIn(self):
        return self._textIn

    @textIn.setter
    def textIn(self, text):
        self._textIn = text

        preProcessedText = self.preProcess(text)
        sentences = self.splitToSentences(preProcessedText)
        exit(print(sentences))
        tokens = self.tokenise(sentences)
        obfuscatedTokens = self.obfuscate(tokens)
        rejoinedTokens = self.rejoinTokens(obfuscatedTokens)
        postProcessed = self.postProcess(rejoinedTokens)

        self.textOut = postProcessed


    def preProcess(self, text):
        #Schema: string
        out = text #""

        #Add null byte to start and end to help delimit??

        return out

    def splitToSentences(self, text):
        #Schema: [sentence, sentence, ...]
        out = nltk.sent_tokenize(text)
        return out

    def tokenise(self, sentences):
        #Schema: [(word, tag, capsFlag), (word, tag, capsFlag), ...]
        out = []
        for sentence in sentences:
            words = nltk.word_tokenize(sentence)
            tags = nltk.pos_tag(words) #Change this to tag
            capsFlags = [tuple([ word==word.capitalize() ]) for word in words]
            out.append([
                tags[i]+capsFlags[i]
                for i in range(len(words))
            ])
        return out

    def obfuscate(self, tokens):
        #Schema: [(word, tag, capsFlag), (word, tag, capsFlag), ...]
        out = tokens #[]
        return out

    def rejoinTokens(self, tokens):
        #Schema: string

        out = " ".join([
            " ".join([item[0] for item in sentence])
            for sentence in tokens
        ])

        """ #Handle punctuation which shouldn't have a space before it
        for item in [".",",","?","!","...",":",";",")","]","}",">","%"]:
            out = out.replace(" "+item, item)
        #Handle punctuation which shouldn't have a space after it
        for item in ["(","[","{","<","#","@","£","$"]:
            out = out.replace(item+" ", item)
        #Handle the nltk tagged format of double quotation marks
        for item in ["`` "," ''"]:
            out = out.replace(item, "\"") """

        """sentenceEnd = ". ? ! ...".split(" ")
        out = "".join([
            "".join([" "+word if word[-1] not in sentenceEnd else word
                     for word in sentenceIn])
            for sentenceIn in textObfuscated
        ])[1:]"""


        return out


    def postProcess(self, text):
        #Schema: string
        out = text
        return out


    def __str__(self):
        return self.textOut



if __name__=="__main__":
    text = "The quick brown fox jumped over the \"lazy\" dog, and this is a test (no really, it is - and it stole £20)!"

    text = "\"This is a test. This is another test.\" This is a further test."

    o = Obfuscated(text)
    print(o.textIn)
    print()
    print(o)
