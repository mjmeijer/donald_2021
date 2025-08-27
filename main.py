# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_app]
from flask import Flask, Response, render_template, request, stream_with_context

from google.cloud import datastore
from datetime import datetime

#
# a test code needs to be shown and transferred to the questionaire.
# we use alphanumeric encodong to make the code compact
#
chars = '0123456789ABCDEFGHIJKLMNPQRSTVWXYZ'


def alnum4(number):
    m = len(chars)
    r = ''
    r = chars[int(number % m)] + r
    r = chars[int((number / m) % m)] + r
    r = chars[int((number / (m * m)) % m)] + r
    r = chars[int((number / (m * m * m)) % m)] + r
    return 'T-' + r


#
# we need to maintain the index for which of the unique test ID's we're at
#
client = datastore.Client()
key = client.key('counter', 'test-ID')


def next_ID():
    with client.transaction():
        counter = client.get(key)
        if not counter:
            counter = datastore.Entity(key)
            counter.update({'value': 100})
        counter['value'] = counter['value'] + 1
        client.put(counter)
    return counter['value']
#
# received data needs to be stored for reference
#


def save_result(data):
    text = data.decode("utf-8")
    parts = text.split('\t')
    testID = parts[0]
    testIndex = parts[1]
    testSet = parts[2]
    timeStamp = datetime.now()
    text += timeStamp.strftime('\t%Y-%m-%d %H:%M:%S.%f')

    testKey = client.key('testRecord')
    testResult = datastore.Entity(key=testKey)
    testResult.update({'testID': testID, 'testIndex': testIndex, 'testSet': testSet,
                       'timeStamp': timeStamp, 'value': text})
    client.put(testResult)
#
#
#


def count_results():
    query = client.query(kind='testRecord')
    tests = list(query.fetch())
    return tests

#
# delete 200 old records on every request rceived. Change later to autodelete older than 100 days.
#


def delete_old_testRecords():
    return # all are deleted already
    kind = 'testRecord'
    fetch_limit = 200
    current_year = datetime(2024, 8, 1)

#    entities = True
#    while entities:
    query = client.query(kind=kind)
    query.add_filter('timeStamp', '<=', current_year)
#    query.add_filter('testID', '<=', 'S-0000')
    entities = list(query.fetch(limit=fetch_limit))
    for entity in entities:
        #        print('Deleting: {}'.format(entity))
        client.delete(entity.key)


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    delete_old_testRecords()
    if request.method == 'POST':
        data = request.get_data()
        save_result(data)
        return ''
    else:
        id = next_ID()
        testID = alnum4(id)
        set = request.args.get('set', default=str(id % 5), type=str)
        return render_template('index.html', testID=testID, set=set)


@app.route('/query', methods=['GET', 'POST'])
def query():
    delete_old_testRecords()
    #        count = len(count_results())
    count = "heul veel"
    return render_template('query.html', count=count)


filename = 'testID-'


@app.route('/q', methods=['GET', 'POST'])
def retrieve():
    delete_old_testRecords()

    if request.method == 'POST':
        testID = request.form.get('ID')
        testSet = request.form.get('set')
    else:
        testID = request.args.get('ID')
        testSet = request.args.get('set')

    if testID:
        filename = 'testID-' + testID + '.txt'
    else:
        filename = "allResults"

    def generate():
        global filename
        query = client.query(kind="testRecord")
        if testID:
            query.add_filter('testID', '=', testID)
            query.order = ["testIndex"]
        else:
            query.add_filter('testID', '>=', 'S-0000')
            query.order = ["testID", "testIndex"]
#        if testSet:
#            query.add_filter('testSet', '=', testSet)
#            filename = 'testset-' + testSet
        tests = list(query.fetch())
        for testResult in tests:
            yield(testResult['value'])
            yield('\n')
    return Response(stream_with_context(generate()), mimetype="text/plain", headers={"Content-Disposition": "attachment; filename=" + filename})
#    return Response("The application has been stopped on 2021 04 08", mimetype="text/plain", headers={"Content-Disposition":"attachment;filename=" + filename + ".txt"})
#    return ''


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # app.run(host='127.0.0.1', port=8080, debug=True)
    app.run(debug=False)
# [END gae_python38_app]
