class Configuration:
    """Common configuration for all environments """
    pass


class TestConfiguration(Configuration):
    """Configuration for the test environment"""
    TESTING = True


class DevelopmentConfiguration(Configuration):
    """Configuration for Development Environment"""
    pass


class ProductionConfiguration(Configuration):
    """Configuration for Development Environment"""
    pass


config = {
    "development": DevelopmentConfiguration,
    "testing": TestConfiguration,
    "production": ProductionConfiguration
}
