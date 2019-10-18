# Third party
from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution("edapy").version
except DistributionNotFound:
    __version__ = "Not installed"
