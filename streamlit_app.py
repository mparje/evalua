
import streamlit as st
import openai
import re


# Pide la clave de API de OpenAI al usuario
openai.api_key = st.text_input("Introduce tu clave de API de OpenAI:")

# Define function to grade essay
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

# Define Streamlit app
def app():
    st.title("Calificador de ensayos")

    st.write("Ingrese el tema del ensayo:")
    st.session_state.topic = st.text_input("Tema", "")

    st.write("Ingrese el ensayo:")
    essay = st.text_area("Ensayo", "", height=300)

    st.write("Elija los criterios de calificación y sus ponderaciones:")
    weights = []
    for criterion in [
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
    ]:
        weight = st.slider(criterion, 0, 100, 10, 10)
        weights.append(weight)

    if sum(weights) != 100:
        st.error("La suma de las ponderaciones debe ser 100.")
        return

    if len(essay.split()) < 500:
        st.error("El ensayo debe tener al menos 500 palabras.")
        return

    grade = grade_essay(essay, weights)

    st.write("La calificación del ensayo es: {}".format(grade))
