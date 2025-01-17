#run locally in Terminal:  streamlit run streamlit-example\streamlit_app.py
#run on website: commit and push: https://smartie-behavior-mmz5gtkp2523426eymrmph.streamlit.app/

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from sqlalchemy.sql import text


st.title("Datenerhebung")

conn = st.connection('pets_db', type='sql')


session_name = st.text_input("Session-Name")
if session_name:
    with conn.session as s:
        s.execute(text(f'CREATE TABLE IF NOT EXISTS {session_name} (index1 TEXT NOT NULL, index2 TEXT NOT NULL, index3 TEXT NOT NULL, index4 TEXT NOT NULL);'))


    listOfAnswers = ['Ich stimme gar nicht zu', 'Ich stimme nicht zu', 'Weder - noch', 'Ich stimme zu','Ich stimme voll und ganz zu']
    answer1 = st.radio('Ich mag Schokolade.', listOfAnswers)
    index1 = listOfAnswers.index(answer1)

    answer2 = st.radio('In meinem Freundeskreis essen wir gern Süßigkeiten.', listOfAnswers)
    index2 = listOfAnswers.index(answer2)

    answer3 = st.radio('Ich denke, dass ich momentan Zugriff auf Schokolade hätte.', listOfAnswers)
    index3 = listOfAnswers.index(answer3)

    answer4 = st.radio('Gäbe es Schokolade, würde ich sie mir nehmen.', listOfAnswers)
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
        

#    if st.button('Update'):
#        query = f'select * from {session_name}'
#        session_result = conn.query(query, ttl=0)
#        session_index1 = [int(i) for i in session_result["index1"]]
#        session_index2 = [int(i) for i in session_result["index2"]]
#        session_index3 = [int(i) for i in session_result["index3"]]
#        session_index4 = [int(i) for i in session_result["index4"]]
#
#        chart_data = pd.DataFrame(list(zip(session_index1, session_index2, session_index3, session_index4)), columns=["index1", "index2", "index3", "index4"])###

#        print(chart_data)
#        c = (
#            alt.Chart(chart_data)
#            .mark_circle()
#            .encode(x="index1", y="index2", tooltip=["index1", "index2", "index3", "index4"])
#        )

#        st.altair_chart(c, use_container_width=True)

    password = st.text_input('Nach einer Erklärung teile ich Ihnen ein Passwort mit, das Sie bitte hier eingeben:')
    if password == "Bosch":
        with conn.session as s:
            # Query to fetch data from the session's table
            query = f'SELECT index1, index2, index3, index4 FROM {session_name}'
            df = pd.read_sql(query, s.connection())

            # Convert data to numeric type, as they were stored as TEXT in the database
            df = df.apply(pd.to_numeric)

            # Prepare the feature columns and the target column
            X = df[['index1', 'index2', 'index3']].values
            y = df['index4'].values

            # Add a constant to the model (the intercept)
            X = np.c_[np.ones(len(X)), X]

            # Fit the model using numpy.linalg.lstsq
            coefficients, _, _, _ = np.linalg.lstsq(X, y, rcond=None)

            # Display the coefficients
            st.write("Zahl 1: ", coefficients[1])
            st.write("Zahl 2: ", coefficients[2])
            st.write("Zahl 3: ", coefficients[3])

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