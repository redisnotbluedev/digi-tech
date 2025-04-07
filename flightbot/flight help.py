#!pip install nltk contractions deep_translator langdetect pyttsx3
# Uncomment the above line if using Google Colab
import random
import re
import time
from datetime import datetime

import contractions
import nltk
import pyttsx3
import requests
from deep_translator import GoogleTranslator, single_detection
from nltk.corpus import wordnet
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk import pos_tag


# Setup NLTK
nltk.download("punkt_tab", quiet=True)
nltk.download("averaged_perceptron_tagger_eng", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("vader_lexicon", quiet=True)

# API Configuration
FLIGHT_API_KEY = "4476d770e10a6aa6859c4f205bab7835"
DETECT_API_KEY = "28775e4bcad9e48b23d5a48387c4a7c5"
BASE_URL = "https://api.aviationstack.com/v1/flights"  

vader_thresholds = (-0.4, 0.5)
lemmatizer = nltk.WordNetLemmatizer()
sia = SentimentIntensityAnalyzer()
translator = GoogleTranslator()
engine = pyttsx3.init()

responses = {
    "TIME-DEPARTURE": [
        "Your flight {flight_number} departs at {departure_time} from {destination}.",
        "The departure time for flight {flight_number} is {departure_time}. It will be leaving from {destination}.",
        "Flight {flight_number} departs at {departure_time}. Make sure you're at {destination} on time!",
        "Don't miss your flight {flight_number}, departing at {departure_time} from {destination}.",
        "Flight {flight_number} is scheduled to depart at {departure_time} from {destination}."
    ],
    "TIME-BOARDING": [
        "We can't find the exact boarding time for flight {flight_number}, but it's approximately {boarding_time} at gate {gate}. Please be aware that it could vary.",
        "The exact boarding time for flight {flight_number} isn't available, but it's estimated to be around {boarding_time} at gate {gate}. Keep in mind this is an approximation.",
        "I can't find the exact boarding time for flight {flight_number}, but you can expect it to start around {boarding_time} at gate {gate}, though times may change.",
        "We don’t have the precise boarding time for flight {flight_number}, but it's roughly {boarding_time} at gate {gate}. Actual times may vary.",
        "Unfortunately, we can't find the exact boarding time for flight {flight_number}, but it’s approximately {boarding_time} at gate {gate}, subject to change."
    ],
    "TIME-UNKNOWN": [
        "What time do you need to know about? Can you specify a different way?",
        "Can you clarify which time you're asking about? Please give more details.",
        "What exactly are you looking for? Can you provide more details?",
        "I'm not sure what time you're asking about. Could you be more specific?",
        "Can you help me by rephrasing the time you're asking for?"
    ],
    "LOCATION-FLIGHT": [
        "Your flight {flight_number} is departing from gate {gate} in terminal {terminal}.",
        "Flight {flight_number} will board at gate {gate} in terminal {terminal}.",
        "You can find flight {flight_number} at terminal {terminal}, gate {gate}.",
        "Boarding for flight {flight_number} is at gate {gate} in terminal {terminal}.",
        "Flight {flight_number} departs from terminal {terminal}, gate {gate}."
    ],
    "LOCATION-UNKNOWN": [
        "What exactly are you looking for? Can you provide more details?",
        "Could you clarify where you’re asking about? I need more information to help you.",
        "I’m not sure what location you're asking about. Can you be more specific?",
        "Can you tell me more about the location you're referring to?",
        "Could you provide more context for me to help determine the location of your flight?"
    ],
    "OTHER-NUMBER": [
        "Your flight number is {flight_number}.",
        "The flight number you asked for is {flight_number}.",
        "Here is the flight number: {flight_number}.",
        "I found the flight number: {flight_number}.",
        "Your requested flight number is {flight_number}."
    ],
    "OTHER-STATUS": [
        "The status of your flight is {flight_status}.",
        "Your flight is currently {flight_status}.",
        "Flight status: {flight_status}.",
        "The status of flight {flight_number} is {flight_status}.",
        "Currently, the flight {flight_number} is {flight_status}."
    ],
    "OTHER-GREETING": [
        "Hello! How can I assist you today?",
        "Hi there! What can I help you with?",
        "Greetings! How may I assist you?",
        "Hey! How can I help you today?",
        "Salutations! What do you need help with?"
    ],
    "SENTIMENT-NEGATIVE": [
        "I'm sorry you're feeling down. How can I assist you?",
        "It seems you're feeling a bit frustrated. Let me know how I can help.",
        "I sense some frustration. Can I offer assistance?",
        "I understand you're feeling upset. How can I make it better?",
        "Sorry to hear you're not feeling great. How can I help?"
    ],
    "SENTIMENT-POSITIVE": [
        "I'm glad you're feeling good! How can I assist you further?",
        "Awesome to see you're in a positive mood! What do you need help with?",
        "It’s great that you’re feeling positive! How can I assist you?",
        "I love that you’re feeling upbeat! Let me know how I can help.",
        "It’s fantastic to see you in a good mood! What can I do for you?"
    ],
    "UNKNOWN": [
        "Sorry, I didn't understand that. Can you rephrase your question?",
        "Could you please clarify your query?",
        "I'm not sure what you're asking. Can you provide more details?",
        "I'm not sure I understand. Could you rephrase?",
        "Sorry, I couldn’t recognize that. Could you explain in a different way?"
    ]
}


def get_sentiment(text):
    sentiment = sia.polarity_scores(text)
    if sentiment['compound'] < min(vader_thresholds):
        return "SENTIMENT-NEGATIVE"
    elif sentiment['compound'] > max(vader_thresholds):
        return "SENTIMENT-POSITIVE"
    return "SENTIMENT-NEUTRAL"

def get_wordnet_pos(treebank_pos):
    if treebank_pos.startswith('J'):
        return wordnet.ADJ
    elif treebank_pos.startswith('V'):
        return wordnet.VERB
    elif treebank_pos.startswith('N'):
        return wordnet.NOUN
    elif treebank_pos.startswith('R'):
        return wordnet.ADV
    return wordnet.NOUN

def lemmatize(text):
    text = contractions.fix(text)
    words = word_tokenize(text)
    pos_tags = pos_tag(words)
    lemmatized_words = [
        lemmatizer.lemmatize(word, get_wordnet_pos(tag)) for word, tag in pos_tags
    ]
    return " ".join(lemmatized_words)

def get_flight_info(flight_number):
    params = {
        "access_key": FLIGHT_API_KEY,
        "flight_iata": flight_number
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    if "data" in data and data["data"]:
        flight = data["data"][0]
        return {
            "flight_number": flight_number,
            "status": flight.get("flight_status", "Unknown"),
            "departure_airport": flight.get("departure", {}).get("airport", "Unknown"),
            "arrival_airport": flight.get("arrival", {}).get("airport", "Unknown"),
            "gate": flight.get("departure", {}).get("gate", "Unknown"),
            "terminal": flight.get("departure", {}).get("terminal", "Unknown"),
            "scheduled_departure": flight.get("departure", {}).get("scheduled", "TBD"),
            "actual_departure": flight.get("departure", {}).get("actual", "TBD"),
            "departure_delay": flight.get("departure", {}).get("delay", "TBD"),
            "scheduled_arrival": flight.get("arrival", {}).get("scheduled", "TBD"),
            "actual_arrival": flight.get("arrival", {}).get("actual", "TBD")
        }
    return None

def is_greeting(text):
    greetings = ["hello", "hi", "hey", "greetings", "salutations", "good morning", "good evening", "good afternoon"]
    if any(word in text.lower() for word in greetings):
        return True
    words = word_tokenize(text)
    if any(any(syn.lemmas()[0].name() in greetings for syn in wordnet.synsets(word)) for word in words):
        return True
    return False

def get_intents(text):
    sentiment = get_sentiment(text)
    if sentiment != "SENTIMENT-NEUTRAL":
        return sentiment
    
    if "when" in text or ("time" in text and any(word in text for word in ["what", "which"])):
        if any(word in text for word in ["depart", "leave", "flight"]):
            return "TIME-DEPARTURE"
        elif "board" in text:
            return "TIME-BOARDING"
        else:
            return "TIME-UNKNOWN"
    elif "where" in text:
        if any(word in text for word in ["gate", "board", "terminal"]):
            return "LOCATION-FLIGHT"
        else:
            return "LOCATION-UNKNOWN"
    elif "number" in text:
        return "OTHER-NUMBER"
    elif any(word in text for word in ["on time", "status", "delayed", "doing"]):
        return "OTHER-STATUS"
    elif is_greeting(text):
        return "OTHER-GREETING"
    return "UNKNOWN"

def main():
    flight_number = ""
    
    print("Hello! I'm FlightBot, your personal airport assistant.")
    flight_number = input("What is your flight number? ").upper()
    
    while not re.match(r"^[A-Z]{2}\d{1,4}$", flight_number):
        flight_number = input("Sorry, that's not a valid flight number. What's your flight number? ").upper()

    flight_info = get_flight_info(flight_number)
    if flight_info == None:
        print("Sorry, something went wrong connecting to the API.")
        return
    valid = input("Is your flight " + flight_number + ", leaving " + flight_info["departure_airport"] + " to " + flight_info["arrival_airport"] + "? ")

    while not any(any(syn.lemmas()[0].name() in ("yes") for syn in wordnet.synsets(word)) for word in word_tokenize(valid)):
        flight_number = input("What is your flight number? ").upper()
        
        while not re.match(r"^[A-Z]{2}\d{1,4}$", flight_number):
            flight_number = input("Sorry, that's not a valid flight number. What's your flight number? ").upper()

        flight_info = get_flight_info(flight_number)
        if flight_info == None:
            print("Sorry, something went wrong connecting to the API.")
            return
        valid = input("Is your flight " + flight_number + ", leaving " + flight_info["departure_airport"] + " to " + flight_info["arrival_airport"] + "? ")

    last_call = time.time()
    _input = input("Please enter your question: ")
    
    while True:
        if len(_input.split()) > 3:
            try:
                language = single_detection(_input, api_key=DETECT_API_KEY).replace("zh", "zh-CN")
            except requests.exceptions.RequestException:
                print("Sorry, something went wrong connecting to the API.")
                return
            if language != "en":
                _input = translator.translate(_input)
        _input = _input.replace(",", "").replace(".", "").replace("?", "").replace("!", "").replace(";", "")
        lemma = lemmatize(_input)
        intent = get_intents(lemma.lower())

        if time.time() - last_call > 300: # 5 minutes
            flight_info = get_flight_info(flight_number)
            if flight_info == None:
                print("Sorry, something went wrong connecting to the API.")
                return
        last_call = time.time()
        
        response = random.choice(responses[intent]).format(
            flight_number = flight_number,
            flight_status = flight_info["status"],
            destination = flight_info["departure_airport"],
            arrival_airport = flight_info["arrival_airport"],
            gate = flight_info["gate"],
            terminal = flight_info["terminal"],
            departure_time = datetime.strptime(flight_info["scheduled_departure"], "%Y-%m-%dT%H:%M:%S%z").strftime("%H:%M:%S %d/%m/%Y"),
            scheduled_arrival = datetime.strptime(flight_info["scheduled_arrival"], "%Y-%m-%dT%H:%M:%S%z").strftime("%H:%M:%S %d/%m%Y")
        )
        
        response = GoogleTranslator(source="en", target=language).translate(response) if language != "en" else response
        print(response, end=" ")
        engine.say(response)
        engine.runAndWait()
        _input = input()

if __name__ == "__main__":
    main()
