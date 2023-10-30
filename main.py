import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import string
import pandas as pd
import os


# nltk.download("syllables")
nltk.download("stopwords")
nltk.download("punkt")


nltk_stopwords_list = set(stopwords.words("english"))


nltk_stopwords_str = ""
for word in nltk_stopwords_list:
    nltk_stopwords_str = nltk_stopwords_str + " " + word


punctuation = string.punctuation
# print(punctuation)
try:
    os.mkdir('url_id_text')

except:
    pass

def get_web_content(url, path):
    r = requests.get(url)
    with open(path, "wb") as f:

        f.write(r.content)



input_data_structure = 'Input.xlsx'
df = pd.read_excel(input_data_structure, index_col=0)

url_id_list = df.index.tolist()

# print(url_id_list)



column_name = "URL"
url_list = df[column_name].tolist()
# print(url_list)


# ---------------------------------------------------------------for loop for whole code

data_list = []

df1 = pd.DataFrame()

for i in range(len(url_id_list)):

    url_id = url_id_list[i]
    url = url_list[i]

    # print("URL_ID List:", url_id_list)
    # print("URL List:", url_list)
    
    path = f'url_id_text/{str(url_id)}.txt'

    get_web_content(url, path)

    
    with open(f'url_id_text/{url_id}.txt', "r", encoding='utf-8') as f:
        text_doc = f.read()



#  defining BEAUTIFULSOUP

    soup = BeautifulSoup(text_doc, "html.parser")


    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-     title of an article      -*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*

    title = soup.title.string
    print(f"Title of the Article is: {title}")



#           MAKING TXT FILES



    
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-     fetching content of an article      -*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*


    content_element = soup.find(class_="td_block_wrap tdb_single_content tdi_130 td-pb-border-top td_block_template_1 td-post-content tagdiv-type")

    if content_element is None:
        content_element = soup.find(class_="td-post-content tagdiv-type")
    if content_element:
            content = content_element.get_text()


    # print(content)
    # print(content_element)


    content_words = content.split()
    # print(content_words)

    content_words = [words.lower() for words in content_words]
    # print(content_words)
    
        
    with open(path, "w", encoding='utf-8') as f:
        text_doc = f.write(f"Title of The Article is: {title}\n\n\n")
        f.write(content)


    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-     fetching stopwords from file      -*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*

    stopwords_files = [
        "StopWords/StopWords_Auditor.txt",
        "StopWords/StopWords_Currencies.txt",
        "StopWords/StopWords_DatesandNumbers.txt",
        "StopWords/StopWords_Generic.txt",
        "StopWords/StopWords_GenericLong.txt",
        "StopWords/StopWords_Geographic.txt",
        "StopWords/StopWords_Names.txt",
    ]
    stopwords_text = []

    for stopwords_file in stopwords_files:
        with open(stopwords_file, "r") as stopword_file:
            stopwords = stopword_file.read()
            stopwords_text.extend(stopwords.split())


    stopwords_text = [word.lower() for word in stopwords_text]


    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-     removing stopwords from main content      -*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*

    main_content = list(set(content_words + stopwords_text))
    # print(main_content)

    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-     POSITIVE SCORE      -*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*

    positive_score = 0
    positive_words = []


    with open("MasterDictionary/positive-words.txt", "r") as f:
        positive = f.read()
        positive_words.extend(positive.split())


    for word in main_content:
        if word in positive_words:
            positive_score += 1

    print(f"The Positive Score of an Article is: {positive_score}")


    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-     NEGATIVE SCORE      -*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*

    negative_score = 0
    negative_words = []


    with open("MasterDictionary/negative-words.txt", "r") as f:
        negative = f.read()
        negative_words.extend(negative.split())


    for word in main_content:
        if word in negative_words:
            negative_score += 1

    print(f"The Negative Score of an Article is: {negative_score}")


    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-     POLAROTY SCORE      -*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*


    polarity_score = (positive_score - negative_score) / (
        (positive_score + negative_score) + 0.000001
    )
    # Polarity Score = (Positive Score – Negative Score)/ ((Positive Score + Negative Score) + 0.000001)

    print(f"The Polarity Score of an Article is: {polarity_score}")


    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-     SUBJECTIVE SCORE      -*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*


    subjective_score = (positive_score + negative_score) / ((len(main_content)) + 0.000001)
    # Subjectivity Score = (Positive Score + Negative Score)/ ((Total Words after cleaning) + 0.000001)

    print(f"The Subjective Score of an Article is: {subjective_score}")


    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-     AVERAGE SENTENCE LENGTH      -*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*

    words_length = len(content_words)
    print(words_length)

    content_string = ""

    for word in content_words:
        content_string = content_string + word + " "


    sentences = nltk.sent_tokenize(content_string)

    number_of_sentences = len(sentences)


    average_sentence_length = words_length / number_of_sentences

    print(f"Average Sentence Length: {average_sentence_length}")

    # Average Sentence Length = the number of words / the number of sentences


    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-     PERCENTAGE OF COMPLEX WORDS      -*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*


    def calculate_vowels(words):
        vowels = "aeiouAEIOU"
        vowel_count = 0
        for word in words:
            if word in vowels:
                vowel_count += 1
        return vowel_count


    def count_complex_words(text_list):
        words = text_list.split()
        complex_count = 0

        for word in words:
            if calculate_vowels(word) > 2:
                complex_count += 1

        return complex_count


    complex_numbers = 0

    for word in content_words:
        total_complex = count_complex_words(word)
        complex_numbers += total_complex


    percentage_complex_number = (complex_numbers / words_length) * 100


    print(f"The Percentage of Complex Words are: {percentage_complex_number}")


    # Percentage of Complex words = the number of complex words / the number of words


    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-     FOG INDEX      -*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*

    # Fog Index = 0.4 * (Average Sentence Length + Percentage of Complex words)

    fog_index = 0.4 * (average_sentence_length / percentage_complex_number)
    print(f"Fog Index is: {fog_index}")


    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-     AVG NUMBER OF WORDS PER SENTENCE      -*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*

    average_number_per_sentence = words_length / number_of_sentences

    print(f"Average Number of Words Per Sentence: {average_number_per_sentence}")
    # Average Number of Words Per Sentence = the total number of words / the total number of sentences


    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-     COMPLEX WORD COUNT      -*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*


    print(f"Total Complex Character are: {complex_numbers} ")


    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-     WORD COUNT      -*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*


    cleaned_content = ""

    cleaned_words = [
        word
        for word in content_words
        if word not in punctuation and word.lower() not in nltk_stopwords_str
    ]


    for cleaned_word in cleaned_words:
        cleaned_content = cleaned_content + cleaned_word + " "

    cleaned_content_length = len(cleaned_content)

    print(f"Word Count: {cleaned_content_length}")


    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-     SYLLABLE PER WORD      -*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*


    def count_syllables(word):
        vowels = "aeiou"
        syllable_count = 0

        word = word.lower()

        for char in word:
            if char in vowels:
                syllable_count += 1

        if word.endswith("es") or word.endswith("ed"):
            syllable_count -= 1

        syllable_count = max(1, syllable_count)  # ensure atleast one syllable

        return syllable_count


    total_syllables = 0


    for word in content_words:
        syllable_count = count_syllables(word)
        total_syllables += syllable_count
        # print(f"{word}: {syllable_count} syllable(s)")

    print(f"Total syllables in the list: {total_syllables}")


    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-     PERSONAL PRONOUNS      -*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*


    personal_pronouns = ["i", "we", "my", "ours", "us"]

    number_of_personal_pronouns = 0

    for word in content_words:
        if word in personal_pronouns:
            number_of_personal_pronouns += 1
    # print(main_content)
    print(f"Number of Personal Pronouns: {number_of_personal_pronouns}")


    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-     AVG WORD LENGTH      -*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*


    total_letters = 0

    for character in content_words:
        for char in character:
            total_letters += 1
    # print(total_letters)

    average_word_length = total_letters / words_length

    print(f"Average Word Length: {average_word_length}")


    i+=1
    print(f'--------------------------------__X________Article {i} is Executed Successfully________X__----------------------------------------------------------------')

    # Sum of the total number of characters in each word/Total number of words
    # print(number_of_words)
    # print(words_length)


    # Saving Data To xlxs sheet
    


    data = {
        # "URL_ID": url_id_list,
        "URL": url,
        "POSITIVE SCORE": positive_score,
        "NEGATIVE SCORE": negative_score,
        "POLARITY SCORE": polarity_score,
        "SUBJECTIVE SCORE": subjective_score,
        "AVG SENTENCE LENGTH": average_sentence_length,
        "PERCENTAGE OF COMPLEX WORDS": percentage_complex_number,
        "FOG INDEX": fog_index,
        "AVG NUMBER OF WORDS PER SENTENCE": average_number_per_sentence,
        "COMPLEX WORD COUNT": complex_numbers,
        "WORD COUNT": cleaned_content_length,
        "SYLLABLE PER WORD": total_syllables,
        "PERSONAL PRONOUNS": number_of_personal_pronouns,
        "AVG WORD LENGTH": average_word_length,
    }


    # df = pd.DataFrame (data)
    # to_xlsx = df.to_excel ('delete.xlsx')
    
    # print(url_id_list)
    # print(url_list)

    data_list.append(data)
    # print(data_list)

output_data_structure='Output Data Structure.xlsx'


df1 = pd.concat([df1, pd.DataFrame(data_list)], axis=0)

df1.index = url_id_list
# data_transfer = df1.to_excel()


    


df1.to_excel(output_data_structure, index_label='URL_ID')




