# Planlos Event Schedule Software

Calendar application based on Flask

Frontend includes an admin interface based on Angular.js



## API

Short documentation of API-calls

### '/api/events/'

#### GET

Get a list of events that are scheduled for today

#### POST

Create a new event


### '/api/events/<int:year>/<int:month>/<int:day>'

#### GET

Get all events for a certain day. Useful for 'tomorrow' or 'next friday'
example GET /api/events/2015/02/21

### '/api/events/<int:year>/<int:month>'

#### GET
Get all events for a certain month
example GET /api/events/2015/02

### '/api/event/<int:id>'

#### GET
Get a event by it's ID

#### POST

Update/Modify an event by it's ID.


### '/locations/'

#### GET
Get a list of locations

#### POST
Create a new location entry

### '/locations/<int:id>'

#### GET
get location by it's ID

#### POST

Update/modify location by it's ID






