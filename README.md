# spark_twitter_AnalyseDeSentiments

Ce projet se porte sur l'analyse de sentiments d'un sujet Twitter réalisé avec Apache Spark Structured Streaming, Apache Kafka, Python et le module AFINN. L'objectif est de connaître l'état des sentiments d'un sujet.<br/> 
<br/>
Par exemple, vous pourriez être intéressé par l'opinion de quelqu'un qur le nouvel épisode de votre série préférée. <br/>
La réponse peut être NEGATIVE, POSITIVE ou NEUTRE. <br/>

## Explication du code

1. Les opérations d'authentification ont été effectuées avec le module Tweepy de Python.<br/>
Vous devez prendre les clés de l'API Twitter.<br/>

3. StreamListener nommé TweetListener a été créé pour le streaming Twitter. <br/>
StreamListener produit des données pour Kafka Topic nommé «twitter». <br/>

5. StreamListener calcule également la valeur de sentiment des Tweets avec le module AFINN et envoie cette valeur au sujet «twitter». <br/>

7. La production de données a été filtrée pour inclure le sujet souhaité.<br/>

9. Le consommateur Kafka qui consomme des données du sujet «Twitter» a été créé. <br/>

11. En outre, il convertit les données en continu en données structurées. Ces données structurées sont placées dans une table SQL nommée «data».<br/>

13. La table de données comporte 2 colonnes nommées «texte» et «senti_val». <br/>

15. La moyenne des valeurs de sentiment de la colonne senti_val est calculée par pyspark.sql.functions. <br/>

17. En outre, une fonction définie par l'utilisateur nommée fun est créée pour la colonne d'état. <br/>

19. La colonne d'état a POSITIVE, NEUTRAL ou NEGATIVE qui changent en fonction de la colonne avg (senti_val) en temps réel. <br/>
<br/>

## Fonctionnement

1. Créez un compte API Twitter et obtenez des clés pour twitter_config.py <br/>
2. Démarrez Apache Kafka <br/>
<br/>
**kafka-server-start.sh /config/server.properties**
<br/>
3. Exécutez tweet_listener.py avec Python version 3 et le nom de sujet souhaité.
<br/>
**spark-submit tweet_listener.py "Votre série préférée"**
<br/>
4. Exécutez twitter_topic_sentiment.py avec Python version 3.
<br/>
**spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.1.1 twitter_topic_sentiment.py**
