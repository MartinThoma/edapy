from pkg_resources import get_distribution
try:
    __version__ = get_distribution('edapy').version
except:
    __version__ = 'Not installed'
