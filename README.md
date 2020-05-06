
# Karfka Tracker  
Dead simple web application which allows to track way points of routes using 
latitude and longitude coordinates.  
  
## Run  
Just execute:  
```bash  
docker-compose up  
```  
Project was developed using:
 * Docker `19.03.5`
 * docker-compose `1.25.2`

## API  
Web service is available under http://localhost:5000.  
  
### `/route/`
| Method | `POST` |  
| --- | --- |  
| Description | Create a new route. |  
| Request |  |  
| Response | `{"route_id": "some id"}` |  
  
### `/route/:route_id/way_point/` 
| Method | `POST` |  
| --- | --- |  
| Description | Add way point to existing route. |  
| Request | `{"lat": 15.55, "lon": 22.12}` |  
| Response | `{"route_id": "some id"}` |  

### `/route/:route_id/length/`
| Method | `GET` |  
| --- | --- |  
| Description | Get a length of existing route. |  
| Request | |  
| Response | `{"km": 25.73}` |

### `/longest_route_of_day/:date/`
| Method | `GET` |  
| --- | --- |  
| Description | Get a longest route for a given date (ISO format, ex. `2020-03-22`). |  
| Request | |  
| Response | `{"route_id": "some id"}` |

## Assumptions
1. Due to asynchronous nature, this service provides _eventual consistency_ 
guarantee. 
For example, `/route/:route_id/length/` endpoint might not give the correct 
answer immediately after way points have ben submitted. 
1. Connected to above. No error response is given to the client in 
case of trying to submit way point to route of the past.
This is easy to fix by introducing `tracking ID` - a JWT with a following payload:
   ```javascript
   {"route_id": "...", "track_expiration": "..."}
   ```
   Client could use this to create way points. Server would be able to validate
   request without any lookups.
1. In _real life_, picking longest route for given day would be a periodic task
or at least separate worker. Here, it is done live to be more interactive and fun.


## Test
Unit tests:
```bash
docker-compose run --rm app py.test tests/unit/
```

All the tests (tracker must be running):
```bash
docker-compose run --rm app py.test
```
