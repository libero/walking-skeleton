# *Libero Flow: A POC Workflow Management System
 ###### A work in progress name *
 
##### What does it do?
It allows the creation and execution of user defined workflows and activities.

##### Workflows
A `Workflow` is defined with `JSON` and describes some basic attributes along with the activities it needs to run. 

Example:
```json
{
  "name": "DummyWorkflow",
  "config": {
    "some": "values"
  },
  "activities": [
      {
          "name": "DoSomethingActivity",
          "independent": false,
          "required": true,
          "config": {}
      },
      {
          "name": "DoAnotherThingActivity",
          "independent": false,
          "required": true,
          "config": {}
      }
  ]
}
```
`name` : can be whatever you would like to call the workflow. Current convention is capitalized camel case with `Workflow` at the end.

`config` : an object containing key value configuration pairs. Please see the available config values for details.

`activities` : these are the activities you are going to execute when you start an instance of your workflow.

`name` : the name of the target `Activity` class. This has to have a existing `Activity` class available in the `activities` package. See activities section below for how to create them.

`independent` : do you want this `Activity` to wait for previous list in this list to have completed before executing?

`required` : if this `Activity` fails permanently should it cause the workflow to fail?

`config` : an object containing key value configuration pairs. Please see the available config values for details.
 
##### Activities
An `Activity` is defined by subclassing the `BaseActivity` class in the `activities` package. The only thing you must implement is it's `do_activity` method. This is what will be executed by the worker processes. Below are examples of how you could implement the two activities defined in the above workflow definition: 

`do_something_activity.py`
```python
from libero_flow.activities.base_activity import BaseActivity


class DoSomethingActivity(BaseActivity):

    def do_activity(self):
        """Actually do some work"""
        
        num = 10
        
        if num > 20:
            return self.PERMANENT_FAILURE
        
        return self.SUCCEEDED

```

`do_another_thing_activity.py`
```python
import requests

from libero_flow.activities.base_activity import BaseActivity


class DoAnotherThingActivity(BaseActivity):

    def do_activity(self):
        """Actually do some work"""
        
        response = requests.get('http://foobar.com/foo')
        
        if response.status_code == 200:
            return self.SUCCEEDED
        
        return self.PERMANENT_FAILURE

```

You can place and retrieve values from the session store from within your activities using the `session_get` and `session_set` methods. 
This is a way of passing data between activities.


#### Default Workflows

The default installation contains a default workflow.

Ingest Article XML Workflow:
- Downloads some xml into a publicly hosted directory
- Parses the xml and finds any .tif files
- Downloads the .tif assets into the publicly hosted directory
- Changes the URIs in the xml to refer to the local files  

To trigger this workflow on your local instance POST the below payload to http://localhost:8000/workflows/api/v1/start-workflow/

```json
{
	"name": "IngestArticleXMLWorkflow",
	"input_data": {
		"data_dir": "/srv/app/article-data-public",
		"urls": [
			"https://s3.amazonaws.com/libero-workflow-test/00666/00666-body.xml", 
			"https://s3.amazonaws.com/libero-workflow-test/00666/00666-front.xml"
			]
	}
}
```


## Installation

`docker-compose up --build`

This will spin up the following containers:

- Workflow API (Django application)
- Web UI
- Scheduler process
- Decider process
- Worker process
- Postgres instance
- Redis instance
- RabbitMQ instance

## Usage

#### Starting a Workflow
...

Start a Workflow by message (via RabbitMQ using pika):
```python
import pika

CREDENTIALS = pika.PlainCredentials('user', 'password')  # NOT REAL VALUES, USE CORRECT CREDENTIALS
PARAMS = pika.ConnectionParameters(host='localhost', credentials=CREDENTIALS)

connection = pika.BlockingConnection(parameters=PARAMS)


with connection.channel() as channel:
    msg = '{"name": "DummyWorkflow", "input_data": {}}'

    channel.basic_publish(exchange='start_workflow',
                          routing_key='workflow_starter',
                          body=msg,
                          properties=pika.BasicProperties(delivery_mode=2))

```

Start a Workflow by http request:
```python

import requests

api_root = 'http://localhost:8000'  # this will depend on your workflow API server deployment 

payload = {"name": "DummyWorkflow", "input_data": {}}
url = api_root + '/workflows/api/v1/startworkflow/'

response = requests.post(url=url, data=payload)

```

## Configuration

...
 
## Components
 
#### API
- Stores Workflow state, Activity state and Event history

#### UI
- A very basic web app to display a workflow list and allow you to view workflow details.
- The UI is a vailable on http://localhost:4200
 
#### Scheduler
- Listens to x3 message queues on a target broker:
    - Workflow Starter
    - Activity Results
    - Decision Results
 
- Starts Workflows
- Handles the scheduling of Workflow decisions and Workflow Activities
- Updates Workflow and Activity State via the Workflow API
    
#### Decider
- Listens to x1 message queue on a target broker:
    - Scheduled Decisions
    
- Based on a Workflow's state it can make the following decisions:
    - do-nothing
    - reschedule-activity
    - schedule-activity
    - start-workflow
    - workflow-failure
    - workflow-finished

- Returns it's results to the Decision results queue
    
#### Worker
- Listens to x1 message queue on a target broker:
    - Scheduled Activities
    
- Runs the target Activity task and returns a result to the Activity results queue
- You can run multiple workers, if you do not then you Activities will obviously be executed synchronously

 
#### Events

Each Workflow contains a list of Events that have been captured throughout its lifetime. The types of events are currently:

- `WorkflowCreated` 
- `WorkflowInProgress` 
- `WorkflowDecisionScheduled` 
- `WorkflowActivityScheduled` 
- `WorkflowActivityStarted` 
- `WorkflowActivityFailed` 
- `WorkflowActivityFinished` 
- `WorkflowFailed` 
- `WorkflowFinished` 

Each Event has an `id`, `type`, `created` timestamp and a reference to the workflow it belongs to. 

Example Event:

```json
{
    "id": "f049ca9b-8926-4c8f-ae49-bcba48ef1621",
    "created": "2018-04-22T19:51:30.310756Z",
    "type": "WorkflowCreated",
    "workflow": "144b5d5e-0fa3-4f84-9943-b14d2ed8a2cd"
}
```

 
## Tests
`$ ./project_tests.sh`


## Workflow configuration options

...

## Activity configuration options

...

