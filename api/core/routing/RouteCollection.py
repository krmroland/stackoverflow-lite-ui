from abc import ABC, abstractmethod


class RouteCollection(ABC):
    def __init__(self, routes=None):
        """ creates an instance of a RouteCollection"""
        self.routes = routes
        self._middleware = None
        self._url_prefix = None
        self.ignored_routes_middleare = []

    def set_routes(self, routes):
        """sets the rest full routes"""
        self.routes = routes

    def prefix(self, url_prefix):
        """prefixes all the url routes in this collection"""
        self._url_prefix = url_prefix
        self.iterate_recusively(self.routes, self.add_url_prefix)
        return self

    def add_url_prefix(self, route):
        """add a url prefix to a given route"""
        route.prefix(self._url_prefix)

    @abstractmethod
    def iterate_recusively(self, routes):
        """iterates recursively through all routes in the collection"""
        pass
