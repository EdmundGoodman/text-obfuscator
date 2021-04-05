from random import random, choice, seed
from nltk import sent_tokenize, word_tokenize, pos_tag
from thesaurus import Thesaurus


class Obfuscator:
    OPENING_PUNCTUATION = ".,!?"
    CLOSING_PUNCTUATION = "({[@#£$"

    def __init__(self, thesaurus, replaceFactor=0.3):
        self._thesaurus = thesaurus
        self._replaceFactor = replaceFactor

    def _tokenise(self, text):
        """Split the text into a list of sentences, which are composed of
        lists of words tagged by type"""
        #Split the text into sentences, then words
        sentences = sent_tokenize(text)
        words = [word_tokenize(sentence) for sentence in sentences]
        #Tag the words by type
        tokens = [pos_tag(word) for word in words]
        return tokens

    def _untokenise(self, tokens):
        """Re-join the list of tokens into a string of text, accounting for
        punctuation which shouldn't be wrapped in spaces"""
        text = ""
        for sentence in tokens:
            for i in range(len(sentence)-1):
                text += sentence[i]
                #Handle words which shouldn't be preceeded/proceeded by spaces
                if sentence[i+1] not in Obfuscator.OPENING_PUNCTUATION:
                    if sentence[i] not in Obfuscator.CLOSING_PUNCTUATION:
                        text += " "
            text += sentence[-1] + " "
        return text

    def _substituteSynonyms(self, tokens):
        """Make substitutions of words with synonyms of the same tag, a
        proportion of the time dependent on the object's replace factor"""
        textSubstitutions = []
        for sentence in tokens:
            sentenceSubstitutions = []
            for pos,(word,tag) in enumerate(sentence):
                #Only replace words a set fraction of the time
                if (random() < self._replaceFactor):
                    #Get the synonyms from the thesaurus
                    synonyms = thesaurus.getSynonyms(word)
                    #Filter synonyms to be of the same tag as the word
                    taggedSynonyms = []
                    for synonym in synonyms:
                        newSentence = [item[0] for item in sentence]
                        newSentence[pos] = synonym
                        taggedWord = pos_tag(newSentence)[pos]
                        if taggedWord[1] == tag:
                            taggedSynonyms.append(taggedWord[0])
                    #Randomly select a synonym of the correct tag to replace with
                    if len(taggedSynonyms) == 0:
                        sentenceSubstitutions.append(word)
                    else:
                        sentenceSubstitutions.append(
                            choice(synonyms)
                        )
                else:
                    sentenceSubstitutions.append(word)

            textSubstitutions.append(sentenceSubstitutions)
        return textSubstitutions

    def obfuscate(self, text):
        """Apply the functions in sequence to obfuscate the text"""
        functions = [
            self._tokenise,
            self._substituteSynonyms,
            self._untokenise
        ]
        temp = text
        for function in functions:
            temp = function(temp)
        return temp

    def __repr__(self):
        return "Text obfuscator on thesaurus: '{}', with replace factor: {}".format(
            self._thesaurus.filename, self._replaceFactor
        )


if __name__=="__main__":
    seed(0)

    thesaurus = Thesaurus(filename="./thesauruses/thesaurusA.pickle")
    obfuscator = Obfuscator(thesaurus, replaceFactor=1)
    print(obfuscator)
    text = "The quick brown fox jumped over the lazy dog!"

    obfuscatedText = obfuscator.obfuscate(text)
    print(text)
    print(obfuscatedText)
