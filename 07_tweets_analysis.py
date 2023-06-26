##
# Utilerías del proyecto
##
from utils import *

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

header("9 casos de negocio con Streamlit")
st.subheader("7. Análisis de sentimiento de tweets sobre aerolíneas estadounidenses")

st.sidebar.title("Análisis de sentimiento de tweets sobre aerolíneas estadounidenses")

st.markdown("Esta aplicación es una aplicación de Streamlit utilizada para analizar el sentimiento de los tweets 🐦 sobre aerolíneas estadounidenses ✈️")
#st.sidebar.markdown("Esta aplicación es una aplicación de Streamlit utilizada para analizar el sentimiento de los tweets 🐦 sobre aerolíneas estadounidenses ✈️")

DATA_URL = ("Tweets.csv")

st.cache_data(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()

st.sidebar.subheader("Mostrar un tweet al azar")
random_tweet = st.sidebar.radio('Elija un tipo de sentimiento', ('positive', 'negative', 'neutral'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0, 0])

st.sidebar.markdown("### Número de tweets por tipo de sentimiento")
select = st.sidebar.selectbox('Tipo de visualización', ['Histograma', 'Gráfico de sectores'], key='1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})

st.markdown("### Cantidad de tweets por sentimiento")
if select == "Histograma":
    fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=500)
    st.plotly_chart(fig)
else:
    fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
    st.plotly_chart(fig)

st.sidebar.subheader("¿Cuándo y desde dónde están twitteando los usuarios?")
hour = st.sidebar.slider("Hora del día", 0, 23)
modified_data = data[data['tweet_created'].dt.hour == hour]

st.markdown("### Ubicación de los tweets según la hora del día")
st.markdown("%i tweets entre las %i:00 y las %i:00" % (len(modified_data), hour, (hour+1) % 24))
st.map(modified_data)

st.write(modified_data)

st.sidebar.subheader("Desglose de tweets de aerolíneas por sentimiento")
choice = st.sidebar.multiselect("Seleccionar aerolíneas", ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'), key='0')

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_0 = px.histogram(choice_data, x='airline', y='airline_sentiment', histfunc='count', color='airline_sentiment', facet_col='airline_sentiment', labels={'airline_sentiment': 'tweets'}, height=600, width=800)
    st.plotly_chart(fig_0)

st.sidebar.header("Nube de palabras")
word_sentiment = st.sidebar.radio('Mostrar nube de palabras para qué sentimiento?', ('positive', 'negative', 'neutral'))

st.header('Nube de palabras para el sentimiento %s' % (word_sentiment))
df = data[data['airline_sentiment'] == word_sentiment]
words = ' '.join(df['text'])
processed_words = ' '.join([word for word in words.split() if 'http' not in word and word.startswith('@') and word != 'RT'])
wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height=600, width=800).generate(processed_words)
plt.imshow(wordcloud)
plt.xticks([])
plt.yticks([])
st.pyplot(plt)

"""
Fuente: *https://github.com/singhishita/Interactive-Dashboards-With-Streamlit*
"""