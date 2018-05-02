import matplotlib.pyplot as plt
import IPython
import numpy

def readFile(chatFileName):
    '''
    Returns list of timestamps, speaker, and text.
    @param filename The path to the chat's .txt file.
    '''
    chat = []
    with open(chatFileName) as file:
        for line in file:
            # If line does not have a date, skip it
            if 'AM]' in line:
                data = line.split('AM]')
            elif 'PM]' in line:
                data = line.split('PM]')
            else:
                # Ignore links and attachements
                # Ignore empty lines
                # TODO (avk): Attribute this non-empty line to previously obtained speaker
                continue
            timestamp = data[0]
            content = data[1].split(': ')
            # Ignore lines like XYZ created this group
            if len(content) < 2:
                continue
            speaker = content[0]
            text = content[1]
            chat.append([timestamp, speaker, text])

    return chat

def getNumberOfTexts(chatList):
    '''
    Returns the number of texts sent by each speaker
    @param chatList The list of timestamps, speaker, and content
    @param startDate The start date to compute frequency from
    @param endDate The end date to compute frequency upto
    '''
    numberOfTexts = {}
    for chat in chatList:
        speaker = chat[1]
        if speaker not in numberOfTexts.keys():
            numberOfTexts[speaker] = 1
        else:
            numberOfTexts[speaker] += 1
    return numberOfTexts

def getNumberOfWords(chatList):
    '''
    Returns the number of words sent by each speaker
    @param chatList The list of timestamps, speaker, and content
    @param startDate The start date to compute frequency from
    @param endDate The end date to compute frequency upto
    '''
    numberOfWords = {}
    for chat in chatList:
        speaker = chat[1]
        text = chat[2]
        currentNumberOfWords = len(text.split())
        if speaker not in numberOfWords.keys():
            numberOfWords[speaker] = currentNumberOfWords
        else:
            numberOfWords[speaker] += currentNumberOfWords
    return numberOfWords

def getFrequencyOfWords(chatList, stopwordsFileName):
    '''
    Returns the frequency of words sent by each speaker
    @param chatList The list of timestamps, speaker, and content
    @param stopwordsFileName Path to the file with words to be ignored
    '''

    # Generate the stopwords to be ignored
    with open(stopwordsFileName) as file:
        for line in file:
            stopwords = line.strip()

    # Datastructure: Dictionary of Dictionaries
    wordFrequency = {}
    for chat in chatList:
        speaker = chat[1]
        text = chat[2]
        words = text.split()
        for word in words:
            word = word.lower()
            # Ignore useless words
            if word in stopwords:
                continue
            if speaker not in wordFrequency.keys():
                wordFrequency[speaker] = {}
            if word not in wordFrequency[speaker].keys():
                wordFrequency[speaker][word] = 1
            else:
                wordFrequency[speaker][word] += 1

    orderedWordFrequency = {}
    for speaker in wordFrequency.keys():
        sortedList = []
        for word in wordFrequency[speaker].keys():
            sortedList += [(word, wordFrequency[speaker][word])]

        sortedList.sort(key=lambda x: x[1], reverse=True)
        orderedWordFrequency[speaker] = sortedList

if __name__ == '__main__':
    
    chatFileName = 'FundaySunday.txt'
    stopwordsFileName = 'stopwords.txt'

    # Create the list of [timestamp, speaker, text]
    chatList = readFile(chatFileName)

    # Get the number of texts 
    numberOfTexts = getNumberOfTexts(chatList)

    # Get the number of words
    numberOfWords = getNumberOfWords(chatList)

    # Get the frequency of words
    frequencyOfWords = getFrequencyOfWords(chatList, stopwordsFileName)

    IPython.embed()
    # Plot
