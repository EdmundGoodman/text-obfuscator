import random
import copy
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
        textObfuscated = self.obfuscate(textTokenised)
        textDetokenised = self.detokenise(textObfuscated)
        self.textOut = self.getTextFromWordArray(textDetokenised)


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
        textObfuscated = textTokenised[:]
        funcs = [
            self.substituteSynonyms, #Maybe do this later - after tenses/voice?
            self.substitutePunctuation,
            self.changePassiveActiveVoice, #Maybe do this first?
            self.changeTense,
            self.changeUnitsAndCurrency,
            self.evaluateMathematics,
            self.formatText,
        ]

        for func in funcs:
            #Consider how to do opt in/out of changes manually
            textObfuscated = func(textObfuscated)
        return textObfuscated







    def substituteSynonyms(self, textToSubstitute):
        textSubstituted = []
        return textToSubstitute #textSubstituted


    def substitutePunctuation(self, textToSubstitute):
        textSubstituted = []

        #validSubstitutions = {
        #    "\"" : "'", #Must work in matching pairs!!!!
        #    ";" : ",",
        #    "," : ";",
        #    "!" : "!?", #And vice versa
        #    "?" : "??", #And any number of ?
        #    #", text," -> " - text - " and vice versa
        #    #"(text)" -> " - text - " and vice versa
        #}

        return textToSubstitute #textSubstituted


    def changePassiveActiveVoice(self, textToChange):
        textChanged = []
        return textToChange #textChanged


    def changeTense(self, textToChange):
        textChanged = []
        return textToChange #textChanged


    def changeUnitsAndCurrency(self, textToChange):
        textChanged = []
        return textToChange #textChanged


    def evaluateMathematics(self, textToEvaluate):
        textEvaluated = []
        return textToEvaluate #textEvaluated


    def formatText(self, textToFormat):
        textFormatted = []
        return textToFormat #textFormatted






    def detokenise(self, textObfuscated):
        #Schema: [(word, tag, capsFlag), (word, tag, capsFlag), ...] -> [word, word, ...]
        return [[token[0] for token in sentence] for sentence in textObfuscated]


    def getTextFromWordArray(self, textObfuscated):
        textOut = " ".join([
            " ".join([item for item in sentence])
            for sentence in textObfuscated
        ])

        for item in ". , ? ! ... : ; ) ] } > %".split(" "):
            textOut = textOut.replace(" "+item, item)
        for item in "( [ { < # @ £ $".split(" "):
            textOut = textOut.replace(item+" ", item)

        """sentenceEnd = ". ? ! ...".split(" ")
        textOut = "".join([
            "".join([" "+word if word[-1] not in sentenceEnd else word
                     for word in sentenceIn])
            for sentenceIn in textObfuscated
        ])[1:]"""

        return textOut


    def __str__(self):
        return self.textOut


#text = """One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections. The bedding was hardly able to cover it and seemed ready to slide off any moment. His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked. "What's happened to me? " he thought. It wasn't a dream.
#His room, a proper human room although a little too small, lay peacefully between its four familiar walls. A collection of textile samples lay spread out on the table - Samsa was a travelling salesman - and above it there hung a picture that he had recently cut out of an illustrated magazine and housed in a nice, gilded frame. It showed a lady fitted out with a fur hat and fur boa who sat upright, raising a heavy fur muff that covered the whole of her lower arm towards the viewer. Gregor then turned to look out the window at the dull weather."""

#text = "The quick brown fox jumped over the lazy dog, and this is a test (no really, it is - and it stole £20)!"

"""
text = "\"This\" is \"a test\""
print(text)
text = re.sub("\"([^\"]*)\"", "\'\\1\'", text)
print(text)
exit()
"""

print(text)
t = Obfuscator(text)
print(t)
