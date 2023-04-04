import streamlit as st
import openai
import re
import os

openai.api_key = "YOUR_API_KEY"

def grade_essay(essay, weights):
    prompt = """
    Califica el siguiente ensayo sobre el tema "{}" en una escala del 1 al 10 según los siguientes criterios:

    Contenido: {}
    Comprensión: {}
    Precisión: {}
    Creatividad: {}
    Organización: {}
    Presentación: {}
    Coherencia: {}
    Habilidad técnica: {}
    Investigación: {}
    Participación: {}

    Ensayo:

    {}
    """

    criteria = [
        "Contenido",
        "Comprensión",
        "Precisión",
        "Creatividad",
        "Organización",
        "Presentación",
        "Coherencia",
        "Habilidad técnica",
        "Investigación",
        "Participación"
    ]

    prompt = prompt.format(
        st.session_state.topic,
        *criteria,
        essay
    )

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    output = response.choices[0].text
    rating = re.findall(r'\d+', output)
    rating = [int(r) for r in rating]

    # Multiply the ratings by the user-defined weights
    weighted_ratings = [rating[i] * weights[i] for i in range(len(rating))]

    # Calculate the final grade
    grade = sum(weighted_ratings) / sum(weights)
    grade = round(grade, 2)

    return grade
