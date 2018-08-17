from .RouteResource import RouteResource
from .RouteCollection import RouteCollection


class RouteGroup(RouteCollection):
    def iterate_recusively(self, routes, callback):
        """ iterate through all routes"""
        for route in routes:
            # handle resource routes
            if isinstance(route, RouteResource):
                self.iterate_recusively(route.routes, callback)
            else:
                callback(route)
        return self
