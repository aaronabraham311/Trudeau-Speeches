# Trudeau's Speeches: An Exercise in Sentiment Analysis and Topic Modelling
Canada will be entering the election season soon, with the projected election date to be on October 21, 2019. This election, in many ways, will be an interesting event. From the rise of populism across the world to refugee crises, Prime Minister Justin Trudeau had an extremely difficult term. These elections will be the chance for Canadian citizens to voice their concerns over Prime Minister Trudeau's policies. 

Usually, citizens like to listen to debates and speeches by candidates on the campaign trail and occasionally dive into party platforms. But I propose a new way of judging candidates, especially incumbents: their official speeches. More often than not, they are a general representation of the government's agenda. I was inspired to analyze Prime Minister Trudeau's speeches when I heard of individuals examining President Trump's Twitter analysis; I thought speeches would be a great way of looking at a politician's sentiment over time, especially in lieu of elections.

The general structure of the project was as follows:
1. Find a way to scrape speeches from Prime Minister's Trudeau's website (https://pm.gc.ca/en/news/speeches)
2. Store the speeches in some database
3. Analyze the speeches sentiment
4. Analyze and predict speech topics from speech transcripts

I am proud that I was able to accomplish each of these steps and learn so many new techniques and technologies. If you would like to experiment with this on your own, please follow these instructions.

## Running the code:
1. Navigate to your local directory and `git clone` this repo
2. Navigate to the project repo using your CLI and type the following commands:
    1. `source env/bin/activate`: activates the virtual environment that hosts all modules
    2. `mongod`: initiates MongoDB server to store speeches
3. Run the scraping script by typing `python src/crawler_ajax.py`. Note: AJAX requests were used. Selenium was the initial choice but it was hard to implement. The code for my initial work can be found in `src/crawler_selenium.py`
4. Clean the speech by running `python src/speech_clean.py`
5. Process the speech for natural language processing by running `python src/speech_process.py`
6. Analyze speech sentiments by running `python src/sentiment_analysis.py`
7. Find and predict speech topics by running `python src/topic_modelling.py`. Please follow the CLI instructions!

Note: visualizations were also created! You can examine them at `src/Visualizations.ipynb`

## Technologies used
* Languages: Python
* Techniques learned: natural language processing, topic modelling via latent Dirichlet allocation models, sentiment analysis, web scraping via Selenium, database storage
* Frameworks: Selenium, MongoDB, NLTK

## Things to work on
- [ ] Refactoring to run all scripts with one command
- [ ] Scrape more speeches and potentially predict sentiment scores over time
