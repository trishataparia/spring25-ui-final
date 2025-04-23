from flask import Flask, abort, jsonify, render_template, request, session
from datetime import datetime
import copy
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)
app.secret_key = 'keyToBeMadeLater'

lessons = {
    "1":{
        "lesson_id": "1",
        "title": "Glittering Generalities",
        "core_idea": "Uses vague, positive-sounding words without explaining anything specific.",
        "example": "https://youtu.be/g63K80akPts?si=oNYRcO_4nTLYxkr_",
        "why_effective": "It bypasses critical thinking and makes viewers emotionally agree with something vague.",
        "how_spot": "Look for broad emotional words (freedom, loyalty), uplifting music, and scenes of families, flags, etc.",
        "prev": "lessons_home",
        "next": "2",
        "icon_url": "https://emojigraph.org/media/joypixels/brain_1f9e0.png"
    },
    "2":{
        "lesson_id": "2",
        "title": "Bandwagon",
        "core_idea": "Convinces the audience to join in because “everyone else is doing it.”",
        "example": "https://www.youtube.com/watch?v=_u1WBBzJGh4",
        "why_effective": "People don’t want to feel excluded so this technique plays on social pressure and the desire to belong.",
        "how_spot": "Look for large crowds or happy groups and phrases like “join the movement” or “don’t be left out.”",
        "prev": "1",
        "next": "3",
        "icon_url": "https://emojigraph.org/media/facebook/people-holding-hands_1f9d1-200d-1f91d-200d-1f9d1.png"
    },
    "3":{
        "lesson_id": "3",
        "title": "Name-Calling",
        "core_idea": "Attaches negative labels to a person, group, or idea to discredit them without presenting evidence.",
        "example": "https://youtu.be/KbMI-coRIhs?t=10",
        "why_effective": "It triggers disgust, fear, or anger, making you judge someone emotionally instead of thinking critically.",
        "how_spot": "Look for loaded words like “traitor,” “corrupt,” “freeloader,” used instead of reasoned arguments.",
        "prev": "2",
        "next": "4",
        "icon_url": "https://emojigraph.org/media/twitter/speaking-head_1f5e3-fe0f.png" 
    },
    "4":{
        "lesson_id": "4",
        "title": "Card Stacking",
        "core_idea": "Presents only the best information in favor of an idea or product, while omitting opposing facts.",
        "example": "https://www.youtube.com/watch?v=jhdX7YtV04w",
        "why_effective": "It creates a biased view that seems convincing because the audience doesn’t see the full picture.",
        "how_spot": "Look for overly selective facts, missing context, or stats that seem too good to be true.",
        "prev": "3",
        "next": "5" ,
        "icon_url": "https://emojigraph.org/media/twitter/clipboard_1f4cb.png"
    },
    "5":{
        "lesson_id": "5",
        "title": "Appeal to Fear",
        "core_idea": "Tries to scare you into thinking or acting a certain way.",
        "example": "https://youtu.be/ffRl9L-vBrI?t=68",
        "why_effective": "It triggers strong emotions, making people more likely to act quickly to avoid danger.",
        "how_spot": "Look for extreme language, dark visuals, or talk of danger/loss.",
        "prev": "4",
        "next": "quiz_home" ,
        "icon_url": "https://emojigraph.org/media/facebook/warning_26a0-fe0f.png"
    },
}

quiz_part2 = {
    "1":{
        "id": 1,
        "Question": "What technique is being used in this video clip?",
        "Video": "https://www.youtube.com/embed/2IpVDkg3kL8?si=xqshgpsO1hx0E21h",
        "AnswerChoices": ["Glittering Generalities", "Appeal to Fear", "Card Stacking"],
        "Answer": "Card Stacking",
        "AnswerMessage": "The video uses card-stacking by focusing only on Nutella’s positives (such as “simple, quality ingredients”) and ignoring the negatives.",
        "next": "2"
    },
    "2":{
        "id": 2,
        "Question": "Which technique is being used in this video clip?",
        "Video": "https://www.youtube.com/embed/L-xm_9zjNwI?si=oLJfMjkTts4gLKFU",
        "AnswerChoices": ["Glittering Generalities", "Appeal to Fear", "Bandwagon"],
        "Answer": "Appeal to Fear",
        "AnswerMessage": "He uses Appeal to Fear, listing scary places like prisons to push anti-immigrant sentiment.",
        "next": "finish"
    }
    
}

user = {
    "1":{
        "Question1": "null",
        "Question2": "null",
        "Question3": "null",
        "Question4": "null",
        "Question5": "null",
        "Question6": "null",
        "Question7": "null",
        "Question8": "null"
    },
    "2":{
        "Home": "null",
        "Lesson1": "null",
        "Lesson2": "null",
        "Lesson3": "null",
        "Lesson4": "null",
        "Lesson5": "null"
    },
}

# firebase admin SDK information
cred = credentials.Certificate("UIserviceAccountKey.json")
firebase_admin.initialize_app(cred, {
   'databaseURL': "https://spring25-ui-quiz-questions-default-rtdb.firebaseio.com"
})

ref = db.reference('/questions')
data = ref.get()
print(data)

@app.route('/')
def home():
    if 'user' not in session:
        session['user'] = user.copy()

    session['user']["2"]["Home"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session.modified = True

    return render_template('home.html')

@app.route('/learn/<int:item_id>')
def view_item(item_id):
    if 'user' not in session:
        return redirect('/')

    lesson = lessons.get(str(item_id))  # Convert item_id to string to match keys
    if lesson is None:
        abort(404)  # Return a proper 404 error page

    session['user']["2"][f"Lesson{item_id}"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session.modified = True

    return render_template('view_technique.html', lesson=lesson)

@app.route('/debug')
def debug():
    return str(session.get('user', 'No user data'))

@app.route('/get_lessons')
def get_lessons():
    return jsonify(lessons)

@app.route('/review')
def review():
    return render_template('review.html')

@app.route('/quiz_home')
def quiz_home():
    return render_template('quiz_home.html')

@app.route('/log_flashcard_entry', methods=['POST'])
def log_flashcard_entry():
    if 'user' not in session:
        return "Session not initialized", 403

    title = request.form.get("title")
    if title:
        key = "Review_" + title.replace(" ", "_")

        session['user']["2"][key] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session.modified = True
        return "Logged", 200
    else:
        return "No title received", 400

@app.route('/quiz/<int:page_num>')
def quiz_page(page_num):
    # Determine which ID range corresponds to the current page
    if page_num == 1 or page_num == 2:
        questions_num = 3
        start_id = (page_num - 1) * questions_num + 1
        end_id = start_id + questions_num - 1

        # Use list comprehension to get only questions in this range
        selected_questions = [q for q in data.values() if start_id <= q['id'] <= end_id]
        
        return render_template('drag_drop_question.html', page_num=page_num, selected_questions=selected_questions)

@app.route('/drag_drop_submit', methods=['POST'])
def drag_drop_submit():
    user_update = request.get_json().get('user_update')
    print("Received user update:", user_update)

    for id, answer in user_update.items():
        user["1"][id] = answer
    
    return jsonify({"status": "success", "updated_user": user}), 200

@app.route('/quiz_part_2/<int:question_id>')
def quiz_part_2(question_id):
    item = quiz_part2.get(str(question_id))
    if item:
        return render_template('quiz_part_2.html', item=item)
    else:
        return "Question not found", 404

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    # Get the user_update data from the request
    user_update = request.get_json().get('user_update')
    
    # For example, user_update might look like {'Question7': 'true'}
    print("Received user update:", user_update)

    
    # Extract the question field (e.g., 'Question7') and the answer (e.g., 'true')
    question_field = list(user_update.keys())[0]  # Get the question field name like 'Question7'
    answer = user_update[question_field]  # Get the answer value ('true' or 'false')

    # Update the user object
    user["1"][question_field] = answer
    
    
    # Return a response back to the client
    return jsonify({"status": "success", "updated_user": user}), 200    

@app.route('/finish')
def finish():
    # Count the number of correct answers
    #correct_answers_count = sum(1 for q in user["1"].values() if q is "true")
    correct_answers_count = sum(1 for answer in user["1"].values() if isinstance(answer, bool) and answer)

    #check if user's answers were recorded correctly
    print(user)
    print(correct_answers_count)
    return render_template("finish.html", correct_answers_count=correct_answers_count)




if __name__ == "__main__":
   app.run(debug=True, port=5001)
