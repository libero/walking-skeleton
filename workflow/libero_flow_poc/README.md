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

## Installation

`docker-compose up --build`

This will spin up the following containers:

- Workflow API (Django application)
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

```

## Configuration

...
 
## Components
 
#### API
- Stores Workflow state, Activity state and Event history
 
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

- ...

 
## Tests
`$ ./project_tests.sh`


## Workflow configuration options

...

## Activity configuration options

...
