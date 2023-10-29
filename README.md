# Learn_Czech
A project to help people learn Czech 

# Have leaderboard say who's the champ
# Limit leaderboard so it won't show over 3 people
# TODO Add option to say word in a sentence and then repeat it back 
# TODO On correct choice, have words repeat once more in your session pool before disapearing
# TODO add line breaks so the formating is nicer in the terminal 
# TODO add the 'sounds like' in the first prompt when you first see a czech word
# TODO Have hints
# TODO have answer have the word in a sentence with the english translation of that sentence
# ~~TODO Have the app say the word back to you~~
# ~~TODO add some sort of scoreboard or points system to the game~~
# TODO you need grammer in there somehow. 
# ~~TODO Add user login~~
# TODO Add in game functions. If user enters 
    :q to quit
    :su to swtich user
    :score to check score
    :update to update word list
    :help to see commands
    :swtch to switch game
    :lang to switch langauge 
    


Title art from https://patorjk.com/software/taag/#p=display&f=Crawford2&t=Type%20Something%20


Word selection algorhythm logic

Leitner System: The core of the Leitner system is to review words at increasing intervals based on the user's performance. In your code, this is implemented through the progress dictionary, where each word has a level that increases when the user answers correctly and decreases when answered incorrectly. The selection of words for review is still based on these levels.

Adaptive Spacing Algorithm: This is an enhancement to the Leitner system. Instead of waiting for the entire deck to be reviewed before repeating words, this algorithm adjusts the intervals dynamically. Words that are answered incorrectly can be shown more frequently, while those answered correctly follow the traditional Leitner intervals. This is implemented in your code by giving higher chances for words with lower levels to be selected.

Interleaved Practice: This strategy involves mixing new words with review words. Instead of going through all new words before reviewing, the code mixes new words with words that need to be reviewed. This has been shown to improve learning and retention.

Confidence Boost Words: Including a few words that the user knows well helps maintain confidence and motivation. These words are selected from the set of words that have been answered correctly.

Session limits: Wordpools in sessions are limited to 5 words, until you get one correct, if you get one correct, it is removed from the 5, and a new one replaces it

____________

Leitner System: Words are organized into levels based on user performance. Correct answers move words up a level, incorrect answers move them down.

Interleaved Practice: Mix new words with words that need to be reviewed within the same session.

Confidence Boost Words: Include a few words that the user has consistently answered correctly to maintain confidence.

Adaptive Spacing: Adjust the intervals at which words are presented based on the user's performance.

Session Limits: Limit each session to 20 words.

Focused Repetition: Prioritize words that have been answered incorrectly or are new for repetition.