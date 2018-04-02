# Import Python functions from flask framework, install to env as needed

    from flask import Flask, render_template, request, jsonify
    from pusher import Pusher
    import json

    # Define flask app variable
    app = Flask(__name__)

    # configure object #These are custom credentials when you sign up with Pusher. I have not completed the process and have yet to update them here.
    pusher = Pusher(
      app_id='YOUR_APP_ID',
      key='YOUR_APP_KEY',
      secret='YOUR_APP_SECRET',
      cluster='YOUR_APP_CLUSTER',
      ssl=True
    )
    # index route for main page
    @app.route('/')
    def index():
      return render_template('index.html')

    # endpoint for storing todo item
    @app.route('/add-todo', methods = ['POST'])
    def addTodo():
      data = json.loads(request.data) # load JSON data from request
      pusher.trigger('todo', 'item-added', data) # trigger added item
      return jsonify(data)

    # endpoint for deleting todo item
    @app.route('/remove-todo/<item_id>')
    def removeTodo(item_id):
      data = {'id': item_id }
      pusher.trigger('todo', 'item-removed', data)
      return jsonify(data)

    # endpoint for updating
    @app.route('/update-todo/<item_id>', methods = ['POST'])
    def updateTodo(item_id):
      data = {
        'id': item_id,
        'completed': json.loads(request.data).get('completed', 0)
      }
      pusher.trigger('todo', 'item-updated', data)
      return jsonify(data)

    # run Flask app in debug mode
    app.run(debug=True)
