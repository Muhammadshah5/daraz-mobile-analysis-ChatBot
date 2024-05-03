from flask import Flask, render_template, request
import engine
app = Flask(__name__)

question_counter = 0
count = 0

@app.route('/')
def index():
    return render_template('index.html', question_counter=question_counter, count=count)

@app.route('/search', methods=['POST'])
def search():
    global question_counter
    global count

    query = request.form.get('query')
    main_df,count = engine.search_phones(query)
    
    results = main_df.to_dict(orient = "records")
    # print(results)
    question_counter += 1

    return render_template('index.html', query=query, results=results, question_counter=question_counter, count=count)




if __name__ == '__main__':
    app.run(debug=True)


# 1: name main se uskay features wala kaam left 
# 3: price and rating condition

