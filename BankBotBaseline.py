# %% [code]
pip install pyTelegramBotAPI

#Файлы
#cluster_indexes 
#cluster_info
#all_data
#tfidf_matrix
#tfidf_vectorizer
#secret_key

# %% [code]
def ask_question_clusters(question):  # Такая конструкция единственный известный способ избежать Broken Pie ошибки.
    try:
        query_vect = tfidf_vectorizer.transform([question])
    except:
        stopwords_list = stopwords.words('russian')
        stopwords_list.extend(['//','http','«\n','»\n','https',"''\n" ])
        lemmatizer = Mystem()
        def my_tokenizer(doc):
            words = word_tokenize(doc)
            pos_tags = pos_tag(words)
            non_stopwords = [w for w in pos_tags if not w[0].lower() in stopwords_list]
            non_punctuation = [w for w in non_stopwords if not w[0] in string.punctuation]
            lemmas = []
            for w in non_punctuation:
                lemmas.append(lemmatizer.lemmatize(w[0])[0])
        return lemmas
        
        query_vect = tfidf_vectorizer.transform([question])
        
    similarity = cosine_similarity(query_vect, tfidf_matrix)
    max_similarity = np.argmax(similarity, axis=None)
    cluster_one = all_data.iloc[max_similarity]['cluster']
    max_similarity2 = np.argmax(np.delete(similarity,cluster_indexes.get(cluster_one)), axis=None)
    cluster_two = all_data.iloc[max_similarity2]['cluster']
    max_similarity3 = np.argmax(np.delete(similarity,np.delete(similarity,cluster_indexes.get(cluster_one))), axis=None)
    cluster_three = all_data.iloc[max_similarity3]['cluster']
    
    one = question
    two = all_data.iloc[max_similarity]['question']
    three = similarity[0, max_similarity]
    four = all_data.iloc[max_similarity]['answer']
    five = cluster_info.get(cluster_one)
    six = all_data.iloc[max_similarity2]['question']
    seven = similarity[0, max_similarity2]
    eight = all_data.iloc[max_similarity2]['answer']
    nine = cluster_info.get(cluster_two)
    ten =  all_data.iloc[max_similarity3]['question']
    eleven = similarity[0, max_similarity3]
    tvelve = all_data.iloc[max_similarity3]['answer']
    last= cluster_info.get(cluster_three)
    
    return one, two,three,four,five,six,seven,eight,nine,ten,eleven,tvelve,last
    

# %% [code]
import telebot

# %% [code]
bot = telebot.TeleBot(secret_key) #token name

@bot.message_handler(commands=["start"])
def handle_start(message):
    print("нажали старт")
    bot.send_message(message.from_user.id,'Просто напишите ваш вопрос банку.')

@bot.message_handler(content_types=["text"])
def handle_command(message):
    print('пришло сообщение ',message.text)
    try:
        bot.send_message(message.from_user.id,"*{name} {last}*, сообщение получено идет обработка, ждите! Вас много, а я один!".format(name=message.chat.first_name, last=message.chat.last_name), parse_mode="Markdown") 
        
        one, two,three,four,five,six,seven,eight,nine,ten,eleven,tvelve,last = ask_question_clusters(str(message.text))
        
        bot.send_message(message.from_user.id,"Ваш вопрос: {one} , *Ответ 1: * Похожий вопрос  : {two} , Сходство: {three} ,Ответ  : {four} ,Название кластера  : {five} ".format(one = one, two=two,three=three,four=four,five= five),parse_mode="Markdown") 
        bot.send_message(message.from_user.id,"*Ответ 2: * Похожий вопрос  : {six}, Сходство  : {seven} ,Ответ  : {eight},Кластер  : {nine} ".format(six=six,seven=seven,eight=eight,nine=nine),parse_mode="Markdown") 
        bot.send_message(message.from_user.id,"*Ответ 3: * Похожий вопрос  : {ten} ,Сходство  : {eleven} ,Ответ  : {tvelve} ,Кластер  : {last} ".format(ten=ten,eleven=eleven,tvelve=tvelve,last=last),parse_mode="Markdown") 
    
    except:
        bot.send_message(message.from_user.id,"Ошибка, что-то пошло не так. попробуйте позже.")
        
        
bot.polling(none_stop=True, interval=0)