import random
import nltk
import copy
import re

from thesaurus import Thesaurus

random.seed(0)


class Obfuscated:
    def __init__(self, textIn, thesaurus=Thesaurus(filename="./thesauruses/thesaurusA.pickle")):
        self.textOut = None
        self.thesaurus = thesaurus
        self.punctuation = ", . ? ! : ;".split(" ") #Add more ???

        self.textIn = textIn


    @property
    def textIn(self):
        return self._textIn

    @textIn.setter
    def textIn(self, text):
        self._textIn = text

        preProcessedText = self.preProcess(text)
        tokenisedText = self.tokenise(preProcessedText)
        obfuscatedText = self.obfuscate(tokenisedText)
        detokenisedText = self.detokenise(obfuscatedText)

        self.textOut = detokenisedText


    def preProcess(self, text):
        #Schema: string -> string

        #Add newlines to the beginning and end of the text for convenience
        out = "\n" + text + "\n"
        #Differentiate between single quotes as apostrophes and quotation marks
        out = re.sub(
            "\ \'(.*)(?!s)\'[\W]",
            " \"\\1\"",
            out
        )

        """out, lenOut = len(out), list(out)
        apostrophesToReplace, insideFlag, insideMetaFlag = [], 0, 0
        for i in range(lenOut):
            if out[i]=="\"":
                insideMetaFlag ^= 1
            if i+1<lenOut and out[i]==" " and out[i+1]=="\'":
                insideFlag ^= 1
                apostrophesToReplace.append(i)
            elif i+2<lenOut and out[i]=="\'" and out[i+1]!="s" and out[i+2]!=" ":
                insideFlag ^= 1
                apostrophesToReplace.append(i)

        for i in apostrophesToReplace:
            out[i] = "\""

        print( "".join(out) )
        exit()"""

        return out


    def tokenise(self, text):
        #Schema: string -> [<token>, (word, tag, capsFlag), ...]
        out = []

        #Split the text up into atomic words
        words = nltk.word_tokenize(text)
        """ This is where formatting is dropped - either add diff. formatting as
        a feature, or explicitly preserve/drop it???"""
        #Tag the words
        tags = [list(tag) for tag in nltk.pos_tag(words)]
        #Add other flags for convenience later
        capsFlags = [[ word==word.capitalize() ] for word in words]
        puncFlags = [[ word in self.punctuation ] for word in words]

        for i in range(len(words)):
            out.append(tags[i] + capsFlags[i] + puncFlags[i])
        return out


    def obfuscate(self, tokens):
        #Schema: [<token>, (word, tag, capsFlag), ...] -> [<token>, (word, tag, capsFlag), ...]
        out = tokens
        funcs = [
            self.substituteSynonyms, #Maybe do this later - after tenses/voice?
            #self.substitutePunctuation,
            #self.changePassiveActiveVoice, #Maybe do this first?
            #self.changeTense,
            #self.multiplyAdjectives
            #self.breakUpSentences
            #self.breakDownSentences
            #self.changeUnitsAndCurrency,
            #self.evaluateMathematics,
            #self.formatText,
        ]

        #Consider how to do opt in/out of changes manually
        for func in funcs:
            out = func(out)
        return out


    def detokenise(self, tokens):
        #Schema: [<token>, (word, tag, capsFlag), ...] -> string

        #https://stackoverflow.com/questions/21948019/python-untokenize-a-sentence
        #Consider messing with things based on their tags if need be???
        """print(tokens)
        return nltk.tokenize.treebank.TreebankWordDetokenizer().detokenize([
            token[0] for token in tokens
        ])"""

        text = ' '.join([token[0] for token in tokens])
        step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .',  '...')
        step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
        step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
        step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
        step5 = step4.replace(" '", "'").replace(" n't", "n't").replace(
             "can not", "cannot")
        step6 = step5.replace(" ` ", " '").strip()
        return step6


    def substituteSynonyms(self, tokens):
        #Schema: [<token>, (word, tag, capsFlag), ...] -> [<token>, (word, tag, capsFlag), ...]
        out = []

        for i, token in enumerate(tokens):
            synonyms, possSubstitutions = self.thesaurus.getSynonyms(token[0]), []
            for synonym in synonyms:
                #Check if the current synonym has the correct tag to fit in place
                newSynonymTokens = copy.deepcopy(tokens)
                newSynonymTokens[i][0] = synonym
                newSynonymTokens = self.tokenise(self.detokenise(newSynonymTokens))
                if newSynonymTokens[i][1] == token[1]:
                    #Add any correct synonyms, and handle their capitalisation
                    finalToken = newSynonymTokens[i]
                    if finalToken[2]:
                        finalToken[0] = finalToken[0].capitalize()
                    possSubstitutions.append(finalToken)

            #If there are any possible substitutions, randomly make one
            if len(possSubstitutions) == 0:
                out.append(token)
            else:
                out.append( random.choice(possSubstitutions) )

        return out



    def __str__(self):
        return self.textOut



if __name__=="__main__":
    text = "The quick brown fox \'jumped\' over the lazy dog."

#    text = """
#One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections. The bedding was hardly able to cover it and seemed ready to slide off any moment. His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked. "What's happened to me? " he thought. It wasn't a dream.
#
#His room, a proper human room although a little too small, lay peacefully between its four familiar walls. A collection of textile samples lay spread out on the table - Samsa was a travelling salesman - and above it there hung a picture that he had recently cut out of an illustrated magazine and housed in a nice, gilded frame. It showed a lady fitted out with a fur hat and fur boa who sat upright, raising a heavy fur muff that covered the whole of her lower arm towards the viewer. Gregor then turned to look out the window at the dull weather.
#"""

    o = Obfuscated(text)
    print(o.textIn)
    print()
    print(o)
