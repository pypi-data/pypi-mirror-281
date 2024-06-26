
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from .api.basic_api import BasicApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from fds.sdk.RealTimeQuotes.api.basic_api import BasicApi
from fds.sdk.RealTimeQuotes.api.category_api import CategoryApi
from fds.sdk.RealTimeQuotes.api.instrument_api import InstrumentApi
from fds.sdk.RealTimeQuotes.api.notation_api import NotationApi
from fds.sdk.RealTimeQuotes.api.prices_api import PricesApi
