from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key' # Change this!

# A simple user data store
users = {
    'yordi': {'password': '123'},
    'alex': {'password': '123'}
}

# In-memory data for the game
game_data = {
    'tasks': [
        {'id': 1, 'name': 'Solve a puzzle', 'points': 100},
        {'id': 2, 'name': 'Write a short story', 'points': 150},
        {'id': 3, 'name': 'Draw a picture', 'points': 80}
    ],
    'members': {
        'yordi': {'points': 0, 'completed_tasks': []},
        'alex': {'points': 0, 'completed_tasks': []}
    }
}

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if username in users:
            flash('Login successful!')
            return redirect(url_for('game', username=username))
        else:
            flash('Username not found. Please try again.')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/game/<username>', methods=['GET', 'POST'])
def game(username):
    if username not in game_data['members']:
        return redirect(url_for('login'))

    if request.method == 'POST':
        task_id = int(request.form['task_id'])
        task_name = next((t['name'] for t in game_data['tasks'] if t['id'] == task_id), None)

        if task_id not in game_data['members'][username]['completed_tasks']:
            task_points = next((t['points'] for t in game_data['tasks'] if t['id'] == task_id), 0)
            game_data['members'][username]['points'] += task_points
            game_data['members'][username]['completed_tasks'].append(task_id)
            flash(f'Task "{task_name}" completed! You earned {task_points} points.')
        else:
            flash(f'You have already completed "{task_name}".')

        return redirect(url_for('game', username=username))

    user_points = game_data['members'][username]['points']
    return render_template('game.html', username=username, user_points=user_points)

@app.route('/earn/<username>')
def earn(username):
    if username not in game_data['members']:
        return redirect(url_for('login'))

    tasks = game_data['tasks']
    return render_template('earn.html', username=username, tasks=tasks)

@app.route('/members/<username>')
def members(username):
    if username not in game_data['members']:
        return redirect(url_for('login'))

    members = game_data['members']
    return render_template('members.html', username=username, members=members)

@app.route('/task/<username>')
def task(username):
    if username not in game_data['members']:
        return redirect(url_for('login'))

    completed_tasks = game_data['members'][username]['completed_tasks']
    tasks_details = [t for t in game_data['tasks'] if t['id'] in completed_tasks]

    return render_template('task.html', username=username, tasks=tasks_details)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
