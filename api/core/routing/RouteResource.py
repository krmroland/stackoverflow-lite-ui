from .RouteCollection import RouteCollection


class RouteResource(RouteCollection):
    def __init__(self, url, controller):
        """ creates an instance of a resourceful route"""
        self.controller = controller
        self.prepare_urls(url).set_urls()
        RouteCollection.__init__(self, [])

    def set_urls(self):
        """ sets the urls for the resource"""

        self.urls = (
            ("get", self.all_url, self.controller, "index"),
            ("get", self.single_url, self.controller, "show"),
            ("post", self.all_url, self.controller, "store"),
            ("put", self.single_url, self.controller, "update"),
            ("patch", self.single_url, self.controller, "update"),
            ("delete", self.single_url, self.controller, "destroy")
        )

    def register_routes(self, callback):
        """ registers all urls here as routes"""
        for url in self.urls:
            self.routes.append(callback(*url))
        return self

    def iterate_recusively(self, routes, callback):
        """ iterates recursively over all routes """
        for route in routes:
            callback(route)
        return self

    def prepare_urls(self, url):
        """prepares the url for both nested resources and single resources"""

        parts = str(url).split(".")
        if len(parts) == 1:
            self.all_url = parts[0]
            self.single_url = f"{parts[0]}/<param>"
        else:
            self.all_url = f"{parts[0]}/<param1>/{parts[1]}"
            self.single_url = f"{self.all_url}/<param2>"
        return self
