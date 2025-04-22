from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

lessons = {
    "1":{
        "lesson_id": "1",
        "title": "Glittering Generalities",
        "core_idea": "Uses vague, positive-sounding words without explaining anything specific.",
        "example": "https://youtu.be/g63K80akPts?si=oNYRcO_4nTLYxkr_",
        "why_effective": "It bypasses critical thinking and makes viewers emotionally agree with something vague.",
        "how_spot": "Look for broad emotional words (freedom, loyalty), uplifting music, and scenes of families, flags, etc.",
        "prev": "lessons_home",
        "next": "2" 
    },
    "2":{
        "lesson_id": "2",
        "title": "Bandwagon",
        "core_idea": "Convinces the audience to join in because “everyone else is doing it.”",
        "example": "https://www.youtubeeducation.com/watch?t=7&v=20u6ny8RvAE",
        "why_effective": "People don’t want to feel excluded so this technique plays on social pressure and the desire to belong.",
        "how_spot": "Look for large crowds or happy groups and phrases like “join the movement” or “don’t be left out.”",
        "prev": "1",
        "next": "3" 
    },
    "3":{
        "lesson_id": "3",
        "title": "Name-Calling",
        "core_idea": "Attaches negative labels to a person, group, or idea to discredit them without presenting evidence.",
        "example": "https://youtu.be/KbMI-coRIhs?t=10",
        "why_effective": "It triggers disgust, fear, or anger, making you judge someone emotionally instead of thinking critically.",
        "how_spot": "Look for loaded words like “traitor,” “corrupt,” “freeloader,” used instead of reasoned arguments.",
        "prev": "2",
        "next": "4" 
    },
    "4":{
        "lesson_id": "4",
        "title": "Card Stacking",
        "core_idea": "Presents only the best information in favor of an idea or product, while omitting opposing facts.",
        "example": "https://www.incrementors.com/blog/wp-content/uploads/2020/10/burger-king.jpg",
        "why_effective": "It creates a biased view that seems convincing because the audience doesn’t see the full picture.",
        "how_spot": "Look for overly selective facts, missing context, or stats that seem too good to be true.",
        "prev": "3",
        "next": "5" 
    },
    "5":{
        "lesson_id": "5",
        "title": "Appeal to Fear",
        "core_idea": "Tries to scare you into thinking or acting a certain way.",
        "example": "https://youtu.be/ffRl9L-vBrI?t=68",
        "why_effective": "It triggers strong emotions, making people more likely to act quickly to avoid danger.",
        "how_spot": "Look for extreme language, dark visuals, or talk of danger/loss.",
        "prev": "4",
        "next": "quiz_home" 
    },
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/view/<int:item_id>')
def view_item(item_id):
    lesson = lessons.get(str(item_id))  # Convert item_id to string to match keys

    if lesson is None:
        abort(404)  # Return a proper 404 error page

    return render_template('view_technique.html', lesson=lesson)

# @app.route('/review') NEEDS IMPLEMENTATION

# @app.route('/quiz') NEEDS IMPLEMENTATION




if __name__ == "__main__":
   app.run(debug=True, port=5001)
