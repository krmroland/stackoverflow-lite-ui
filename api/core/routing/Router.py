from .Route import Route
from .RouteGroup import RouteGroup
from .RouteResource import RouteResource


class Router:
    """A fluent routing wrapper"""

    #: A dictionary of all the routes and their respective actions
    routes = {}

    """The url rules that have to be mapped"""
    url_rules = []

    @classmethod
    def get(cls, url, controller, method):
        """Creates a route of type get"""
        return cls.add("GET", url, controller, method)

    @classmethod
    def put(cls, url, controller, method):
        """creates a route of  type put"""
        return cls.add("PUT", url, controller, method)

    @classmethod
    def post(cls, url, controller, method):
        """creates a route of type put"""

        return cls.add("POST", url, controller, method)

    @classmethod
    def delete(cls, url, controller, method):
        """ creates a route of type delete"""
        return cls.add("DELETE", url, controller, method)

    @classmethod
    def resource(cls, url, controller):
        """ creates a an api resourcefull route"""
        return RouteResource(url, controller).register_routes(cls.add)

    @classmethod
    def register_route(cls, route):
        return cls.routes[route].rule()
    # @classmethod
    # def load(cls, app):
    #     """ loads the routes into the application"""
    #     for route in cls.routes:
    #         app.url_map.add(cls.routes[route].rule())

    @classmethod
    def add(cls, verb, url, controller, method):
        # use the index as the name of the route
        name = str(len(cls.routes))
        route = Route(verb, url, name, controller, method)
        cls.routes[name] = route
        return route

    @classmethod
    def match(cls, name, params):
        """ matches a given route to its corresponding action"""
        return cls.routes[name].run(**params)

    @classmethod
    def group(cls, routes):
        """ creates a group of given routes"""
        return RouteGroup(routes)
