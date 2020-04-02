from flask import request, render_template, redirect, Blueprint
from app import db
# Import module models
from app.auth.models import Todo

# Define blueprint
auth = Blueprint('auth', __name__, url_prefix='/')

# Set route
@auth.route('/', methods = ('GET', 'POST'))
def index():
    if request.method == 'POST':
        error = None
        task_content = request.form['content']

        if not task_content:
            error = 'Please fill in the task to continue'

        if error is None:
            new_task = Todo(content = task_content)

            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue adding your task'
        
        return error
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = tasks)

@auth.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@auth.route('/update/<int:id>', methods=('GET', 'POST'))
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task = task)