import os
import mimetypes

from flask import Flask, request, make_response, abort
from elevator import Elevator

app = Flask(__name__)
elevator = None


@app.route('/reset')
def reset():
  global elevator
  elevator = Elevator(int(request.args['landings']))
  return 'OK'


@app.route('/arrive')
def arrive():
  global elevator

  if not elevator:
    return "Elevator not initialized", 422

  should_open = elevator.arrive(int(request.args['landing']))
  return 'true' if should_open else 'false'


@app.route('/hallcall')
def hall_call():
  global elevator

  if not elevator:
    return "Elevator not initialized", 422

  elevator.hall_call(int(request.args['landing']), request.args['direction'])
  return 'OK'


@app.route('/carcall')
def car_call():
  global elevator

  if not elevator:
    return "Elevator not initialized", 422

  elevator.car_call(int(request.args['landing']))
  return 'OK'


@app.route('/direction')
def direction():
  global elevator

  if not elevator:
    return "Elevator not initialized", 422

  return elevator.direction()

@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def asset(path):
  filepath = os.path.join(os.getcwd(), 'frontend', path)

  try:
    f = open(filepath, 'rb')
  except IOError, e:
    abort(404)
    return

  body = f.read()
  response = make_response(body, 200)
  response.headers['Content-Type'] = mimetypes.guess_type(filepath)[0]

  return response


if __name__ == '__main__':
  app.run('127.0.0.1', 3130, True)
