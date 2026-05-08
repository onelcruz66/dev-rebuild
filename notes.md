# Flask Overview

## Flask is a web framework that lets you build HTTP servers in Python

1. The imported Flask class is used to create the application itself. 
2. jsonify is a helper that converts dicts and lists into proper JSON HTTP responses (e.g. setting the correct Content-Type: application/json header automatically).
3. request is a global object Flask provides that gives access to the incoming HTTP requests data (body, headers, query params, etc)
