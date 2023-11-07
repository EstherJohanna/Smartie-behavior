#run locally in Terminal:  streamlit run streamlit-example\streamlit_app.py
#run on website: commit and push: https://smartie-behavior-mmz5gtkp2523426eymrmph.streamlit.app/

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from sqlalchemy.sql import text


st.title("Test-Titel2")

conn = st.connection('pets_db', type='sql')


session_name = st.text_input("Name of the session")
if session_name:
    with conn.session as s:
        s.execute(text(f'CREATE TABLE IF NOT EXISTS {session_name} (index1 TEXT NOT NULL, index2 TEXT NOT NULL, index3 TEXT NOT NULL, index4 TEXT NOT NULL);'))


    listOfAnswers = ['Ich stimme gar nicht zu', 'Ich stimme nicht zu', 'Weder - noch', 'Ich stimme zu','Ich stimme voll und ganz zu']
    answer1 = st.radio('Ich bin ein Detektiv, der die Geheimnisse des menschlichen Verhaltens lüftet, wenn ich eine Vorlesung über Human Factors besuche.', listOfAnswers)
    index1 = listOfAnswers.index(answer1)

    answer2 = st.radio('Meine Freunde würden mir ein ‚High Five‘ dafür geben, dass ich regelmäßig an Human Factors-Vorlesungen teilnehme.', listOfAnswers)
    index2 = listOfAnswers.index(answer2)

    answer3 = st.radio('Ich kann einen engen Zeitplan überwinden, um Zeit für den Besuch von Human Factors-Vorlesungen zu finden.', listOfAnswers)
    index3 = listOfAnswers.index(answer3)

    answer4 = st.radio('Gäbe es für die Teilnahme an Human Factors-Vorlesungen „Smarty-Punkte", würde ich sie einsammeln.', listOfAnswers)
    index4 = listOfAnswers.index(answer4)


    if st.button('Speichern'):
        if session_name:
            with conn.session as s:
                s.execute(
                    text(f'INSERT INTO {session_name} (index1, index2, index3, index4) VALUES(:index1, :index2, :index3, :index4);'),
                    params=dict(
                        index1=index1, index2=index2, index3=index3, index4=index4
                    ),
                )
                s.commit()
        st.write('Vielen Dank!')
        

    if st.button('Update'):
        query = f'select * from {session_name}'
        session_result = conn.query(query, ttl=0)
        session_index1 = [int(i) for i in session_result["index1"]]
        session_index2 = [int(i) for i in session_result["index2"]]
        session_index3 = [int(i) for i in session_result["index3"]]
        session_index4 = [int(i) for i in session_result["index4"]]
        
        chart_data = pd.DataFrame(list(zip(session_index1, session_index2, session_index3, session_index4)), columns=["index1", "index2", "index3", "index4"])

        print(chart_data)
        c = (
            alt.Chart(chart_data)
            .mark_circle()
            .encode(x="index1", y="index2", tooltip=["index1", "index2", "index3", "index4"])
        )

        st.altair_chart(c, use_container_width=True)

#st.title("Ergebnis: Wie gut passt die Theorie des geplanten Verhaltens auf Sie?")
#password = st.text_input('Bitte geben Sie das Passwort ein.')

#typ ausrechnen

#collectingchance = index4

#if (collectingchance > 2):
#    answer = 'Sie werden die Smarties einsammeln!'
#else:
#    answer = 'Sie werden die Smarties nicht einsammeln!'



#if password == "HKA":
#    st.write(f"Ergebnis: {answer}")