from zope.interface import Interface, Attribute

class IPengine(Interface):
    """Interface to a pengine thread on a server"""

    id=Attribute("Identifier (session) of pengine interaction.")
    options=Attribute("Dictionary of stanadard options used in communications")
    connection=Attribute("Connection data in form of (server_name, port)")
    alias=Attribute("Alias of the pengine or None.")

    def create(src):
        """Create a pengine with sending there a
        prolog-program as src"""

    def ask(src):
        """Perform query (ask) for
        the first solution if any."""

    def query(src):
        """Alias for ask."""

    def next(count):
        """Query next count solution."""

    def stop(count):
        """Stop searching for solution."""

    def abort():
        """Abort execution."""

    def detroy():
        """Abort execution."""

    def prompt(term):
        """Runned if a pengine wants some data"""

    def output(term):
        """Runned if a pengine wanst
        to send some output"""

    def falure():
        """Runned if no solution found."""

    def error(term):
        """Runned if an error occurs."""

    def success(term, more):
        """Runned when pengine got some success
        on obtaining a query result."""

    def define_app(app):
        """Define an application"""

    def get_app(app):
        """Check if the application exists"""

    def get_property(name):
        """Get property of the pengine by name."""

    def set_property(name, value):
        """Set property name of the pengine to
        value val."""

    def properties():
        """Enumerate properties as (name,value)
        of the pengine."""

    #Other useful methods will folow.
