# Functions that generate the simple flask pages




def home():
    return """
    <h1>Song Recommender</h1>
    <a href="go">Start!</a>
    """



def start():
    songOptions = ""
    dm.getTrackIterator()
    return """
    <h1>Start Page</h1>
    <h2>Select a song that you like to get started!</h2>
    {}
    """.format(songOptions)


def radio():
    return "RADIO PAGE"




# MOVE EVERYTHING BELOW TO recommender.py

app = Flask(__name__)
def FlaskMain():
    print('RUNNING AS FLASK WEBAPP')

    app.add_url_rule('/', None, ff.home)

    #Initialize DataManager
    dm = initializeDataManager()

    #Load/Create preference data
    if os.path.isfile('preference-data-cache'):
        dm.loadPreferencesFromFile('preference-data-cache')
        app.add_url_rule('/go', None, ff.radio)
    else:
        app.add_url_rule('/go', None, ff.start)



#If app is running as Flask webapp
if __name__ == 'recommender':
    FlaskMain()
