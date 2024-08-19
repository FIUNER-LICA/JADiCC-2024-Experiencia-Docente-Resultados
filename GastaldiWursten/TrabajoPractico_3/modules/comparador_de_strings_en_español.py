import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import FreqDist
from nltk.stem import SnowballStemmer
nltk.download('stopwords')
nltk.download('punkt')

class ComparadorDeStrings():
    """ Clase que modela un comparador que determina el grado de similitud de dos strings en español
    ------------------------------------------------
    Atributos:
    * stop_words: set
    * stemmer: SnowballStemmer
    """

    def __init__(self):

        self.__stop_words = set(stopwords.words('spanish'))
        self.__stemmer = SnowballStemmer('spanish')


    def comparar_strings(self, p_string_1, p_string_2):
        """ Método que compara la similitud de dos strings en español, quitando stopwords y reduciendo las palabras a sus raices
        
        Argumentos:
        * p_string_1: String
        * p_string_2: String
        
        Returns:
        * float        
        """ 

        words1 = [self.__stemmer.stem(word.lower()) for word in word_tokenize(p_string_1) if word.isalnum() and word.lower() not in self.__stop_words]
        words2 = [self.__stemmer.stem(word.lower()) for word in word_tokenize(p_string_2) if word.isalnum() and word.lower() not in self.__stop_words]


        freq_dist1 = FreqDist(words1)
        freq_dist2 = FreqDist(words2)

        common_words = set(words1).intersection(set(words2))
        num_common_words = sum(min(freq_dist1[word], freq_dist2[word]) for word in common_words)

        total_words = max(sum(freq_dist1.values()), sum(freq_dist2.values()))

        similarity_ratio = num_common_words / total_words

        return similarity_ratio
