from flask import Flask, render_template, request
import webbrowser
import csv
import re
import pandas as pd
import numpy as np
import math


def remove_stop_words(sentence):
    new_word_list = []
    splitted_words = re.split(r'[,\s]+', sentence.lower())
    for word in splitted_words:
        new_word_list.append(word)
    return [i for i in new_word_list if i]


def create_vector_from_input(formatted_word_list, columns):
    input_vector = []
    for column in columns:
        splitted_column = re.split("_", column)
        input_vector.append(1 if set(splitted_column).issubset(
            set(formatted_word_list)) else 0)
    return input_vector


def dot_product(vector1, vector2):
    return sum([vector1[i]*vector2[i] for i in range(len(vector1))])


def magnitude(vector):
    return math.sqrt(sum([x**2 for x in vector]))


def cosine_similarity(vector1, vector2):
    return dot_product(vector1, vector2) / (magnitude(vector1) * magnitude(vector2))


def sort_similarities(similarities, top_n):
    sorted_scores = sorted(similarities, key=lambda x: x[1], reverse=True)
    return sorted_scores[:top_n]


def get_cosine_similarities(vec2):
    similarities = []
    with open('updated_training_data.csv') as file_obj:
        reader_obj = csv.reader(file_obj)
        next(reader_obj)
        for row in reader_obj:
            int_row = [int(num) for num in row[1:]]
            result = cosine_similarity(int_row, vec2)
            similarities.append([int(row[0]), result])

    return similarities


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("input.html")


@app.route("/", methods=['GET', 'POST'])
def input():
    if request.method == "POST":
        # Getting the login details from
        symptoms = request.form['symptoms']
    return render_template("input.html")


@app.route("/output", methods=['GET', 'POST'])
def output():
    symptoms = request.form['symptoms']
    df = pd.read_csv("Training.csv")
    columns = df.columns[:-2]
    df.head()
    symptoms = symptoms
    word_list = remove_stop_words(symptoms)
    vec2 = create_vector_from_input(word_list, columns)
    if "Unnamed: 133" in df.columns:
        df.drop(["Unnamed: 133"], axis=1, inplace=True)
    new_df = df.iloc[:, :-2]
    new_df.head()
    remove_stop_words(symptoms)
    df["prognosis"].unique()
    columns = df.columns[:-2]

    word_list = remove_stop_words(symptoms)
    vec2 = create_vector_from_input(word_list, columns)
    len(vec2)
    new_df.head(3)
    new_df.head(3)
    df_result = new_df.multiply(vec2, axis=1)
    df_result
    new_df
    nump_array = new_df.to_numpy()
    num_vec = np.array(vec2)
    nump_array.shape
    num_vec.shape
    new_df.to_csv("updated_training_data.csv")
    sims = get_cosine_similarities(vec2)

    results = sort_similarities(sims, 5)
    for res in results:
        final_result = df.iloc[res[0]]["prognosis"]
        break
    with open("combined_data.csv", "r") as fp:
        records = csv.reader(fp)
        name = []
        specialization = []
        rating = []
        schedule = []
        for rec in records:
            if len(rec) > 0:
                if rec[0] == final_result:
                    name.append(rec[2])
                    specialization.append(rec[1])
                    rating.append(rec[3])
                    schedule.append(rec[4])

    return render_template("output.html", name0=name[0], name1=name[1], name2=name[2], name3=name[3], name4=name[4], specialization0=specialization[0], specialization1=specialization[1], specialization2=specialization[2], specialization3=specialization[3], specialization4=specialization[4], rating0=rating[0], rating1=rating[1], rating2=rating[2], rating3=rating[3], rating4=rating[4], schedule0=schedule[0], schedule1=schedule[1], schedule2=schedule[2], schedule3=schedule[3], schedule4=schedule[4])


if __name__ == "__main__":
    app.run(debug=True)
