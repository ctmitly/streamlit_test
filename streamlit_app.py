import streamlit as st 
import requests
import random
import html

# Function to fetch quiz questions
def get_questions(amount=5, category=None, difficulty=None):
    url = f"https://opentdb.com/api.php?amount={amount}&type=multiple"
    if category:
        url += f"&category={category}"
    if difficulty:
        url += f"&difficulty={difficulty}"

    response = requests.get(url)
    data = response.json()

    #if data.get("response_code") != 0:
      #  st.error(f"Error fetching questions. API response code: {data.get('response_code')}")
       # st.stop()
    if data.get("response_code") == 5:
        st.error("No questions available for the selected category and difficulty. Please try different options.")
        st.stop()


    return data['results']

# Initialize session state
if 'questions' not in st.session_state:
    categories = {
        "General Knowledge": 9,
        "Science: Computers": 18,
        "Science: Gadgets": 30,
        "Entertainment: Video Games": 15,
    }
    difficulties = ["easy", "medium", "hard"]

    selected_category = st.selectbox("Select Category", list(categories.keys()))
    selected_difficulty = st.selectbox("Select Difficulty", difficulties)

    category_id = categories[selected_category]
    st.session_state.questions = get_questions(category=category_id, difficulty=selected_difficulty)
    st.session_state.current = 0
    st.session_state.score = 0
    st.session_state.answers = []

st.title("🧠 Quiz App")

# Show current question
if st.session_state.current < len(st.session_state.questions):
    question = st.session_state.questions[st.session_state.current]
    st.subheader(f"Question {st.session_state.current + 1}")

    question_text = html.unescape(question['question'])
    st.write(question_text)

    options = question['incorrect_answers'] + [question['correct_answer']]
    options = [html.unescape(opt) for opt in options]
    random.shuffle(options)

    selected = st.radio("Choose your answer:", options)

    if st.button("Submit"):
        correct = html.unescape(question['correct_answer'])
        if selected == correct:
            st.success("✅ Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Incorrect! Correct answer: **{correct}**")
        st.session_state.answers.append((question_text, selected, correct))
        st.session_state.current += 1
        st.rerun()

else:
    st.title("🎉 Quiz Complete!")
    st.write(f"Your final score is **{st.session_state.score}/{len(st.session_state.questions)}**")

    with st.expander("Review Answers"):
        for q, selected, correct in st.session_state.answers:
            st.write(f"**Q:** {q}")
            st.write(f"Your Answer: {selected}")
            st.write(f"Correct Answer: {correct}")
            st.markdown("---")

    if st.button("Restart Quiz"):
        st.session_state.clear()
        st.rerun()
