from flask import Flask

app = None

def route_flask(location, returnValue):
    global app
    try:
        if app is None:
            app = Flask(__name__)

        def make_route(return_value):
            def route():
                return return_value
            return route

        endpoint = location.strip('/')
        if endpoint == '':
            endpoint = 'index'

        app.add_url_rule(location, endpoint, make_route(returnValue))
        return 'done'
    except Exception as error:
        raise error
    
def run(check=False, debug=True, host="0.0.0.0", port="8000"):
    global app
    try:
        if app is None:
            raise Exception("App not initialized")
        
        if check:
            if __name__ == "__main__":
                app.run(debug=debug, host=host, port=port)
        else:
            app.run(debug=debug, host=host, port=port)
        return 'done'
    except Exception as error:
        raise error
