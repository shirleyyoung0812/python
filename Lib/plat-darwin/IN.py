# Generated by h2py from /usr/include/netinet/in.h

# Included from sys/appleapiopts.h
IPPROTO_IP = 0
IPPROTO_HOPOPTS = 0
IPPROTO_ICMP = 1
IPPROTO_IGMP = 2
IPPROTO_GGP = 3
IPPROTO_IPV4 = 4
IPPROTO_IPIP = IPPROTO_IPV4
IPPROTO_TCP = 6
IPPROTO_ST = 7
IPPROTO_EGP = 8
IPPROTO_PIGP = 9
IPPROTO_RCCMON = 10
IPPROTO_NVPII = 11
IPPROTO_PUP = 12
IPPROTO_ARGUS = 13
IPPROTO_EMCON = 14
IPPROTO_XNET = 15
IPPROTO_CHAOS = 16
IPPROTO_UDP = 17
IPPROTO_MUX = 18
IPPROTO_MEAS = 19
IPPROTO_HMP = 20
IPPROTO_PRM = 21
IPPROTO_IDP = 22
IPPROTO_TRUNK1 = 23
IPPROTO_TRUNK2 = 24
IPPROTO_LEAF1 = 25
IPPROTO_LEAF2 = 26
IPPROTO_RDP = 27
IPPROTO_IRTP = 28
IPPROTO_TP = 29
IPPROTO_BLT = 30
IPPROTO_NSP = 31
IPPROTO_INP = 32
IPPROTO_SEP = 33
IPPROTO_3PC = 34
IPPROTO_IDPR = 35
IPPROTO_XTP = 36
IPPROTO_DDP = 37
IPPROTO_CMTP = 38
IPPROTO_TPXX = 39
IPPROTO_IL = 40
IPPROTO_IPV6 = 41
IPPROTO_SDRP = 42
IPPROTO_ROUTING = 43
IPPROTO_FRAGMENT = 44
IPPROTO_IDRP = 45
IPPROTO_RSVP = 46
IPPROTO_GRE = 47
IPPROTO_MHRP = 48
IPPROTO_BHA = 49
IPPROTO_ESP = 50
IPPROTO_AH = 51
IPPROTO_INLSP = 52
IPPROTO_SWIPE = 53
IPPROTO_NHRP = 54
IPPROTO_ICMPV6 = 58
IPPROTO_NONE = 59
IPPROTO_DSTOPTS = 60
IPPROTO_AHIP = 61
IPPROTO_CFTP = 62
IPPROTO_HELLO = 63
IPPROTO_SATEXPAK = 64
IPPROTO_KRYPTOLAN = 65
IPPROTO_RVD = 66
IPPROTO_IPPC = 67
IPPROTO_ADFS = 68
IPPROTO_SATMON = 69
IPPROTO_VISA = 70
IPPROTO_IPCV = 71
IPPROTO_CPNX = 72
IPPROTO_CPHB = 73
IPPROTO_WSN = 74
IPPROTO_PVP = 75
IPPROTO_BRSATMON = 76
IPPROTO_ND = 77
IPPROTO_WBMON = 78
IPPROTO_WBEXPAK = 79
IPPROTO_EON = 80
IPPROTO_VMTP = 81
IPPROTO_SVMTP = 82
IPPROTO_VINES = 83
IPPROTO_TTP = 84
IPPROTO_IGP = 85
IPPROTO_DGP = 86
IPPROTO_TCF = 87
IPPROTO_IGRP = 88
IPPROTO_OSPFIGP = 89
IPPROTO_SRPC = 90
IPPROTO_LARP = 91
IPPROTO_MTP = 92
IPPROTO_AX25 = 93
IPPROTO_IPEIP = 94
IPPROTO_MICP = 95
IPPROTO_SCCSP = 96
IPPROTO_ETHERIP = 97
IPPROTO_ENCAP = 98
IPPROTO_APES = 99
IPPROTO_GMTP = 100
IPPROTO_IPCOMP = 108
IPPROTO_PIM = 103
IPPROTO_PGM = 113
IPPROTO_DIVERT = 254
IPPROTO_RAW = 255
IPPROTO_MAX = 256
IPPROTO_DONE = 257
IPPORT_RESERVED = 1024
IPPORT_USERRESERVED = 5000
IPPORT_HIFIRSTAUTO = 49152
IPPORT_HILASTAUTO = 65535
IPPORT_RESERVEDSTART = 600
def IN_CLASSA(i): return (((u_int32_t)(i) & 0x80000000) == 0)

IN_CLASSA_NET = 0xff000000
IN_CLASSA_NSHIFT = 24
IN_CLASSA_HOST = 0x00ffffff
IN_CLASSA_MAX = 128
def IN_CLASSB(i): return (((u_int32_t)(i) & 0xc0000000) == 0x80000000)

IN_CLASSB_NET = 0xffff0000
IN_CLASSB_NSHIFT = 16
IN_CLASSB_HOST = 0x0000ffff
IN_CLASSB_MAX = 65536
def IN_CLASSC(i): return (((u_int32_t)(i) & 0xe0000000) == 0xc0000000)

IN_CLASSC_NET = 0xffffff00
IN_CLASSC_NSHIFT = 8
IN_CLASSC_HOST = 0x000000ff
def IN_CLASSD(i): return (((u_int32_t)(i) & 0xf0000000) == 0xe0000000)

IN_CLASSD_NET = 0xf0000000
IN_CLASSD_NSHIFT = 28
IN_CLASSD_HOST = 0x0fffffff
def IN_MULTICAST(i): return IN_CLASSD(i)

def IN_EXPERIMENTAL(i): return (((u_int32_t)(i) & 0xf0000000) == 0xf0000000)

def IN_BADCLASS(i): return (((u_int32_t)(i) & 0xf0000000) == 0xf0000000)

INADDR_NONE = 0xffffffff
def IN_LINKLOCAL(i): return (((u_int32_t)(i) & IN_CLASSB_NET) == IN_LINKLOCALNETNUM)

IN_LOOPBACKNET = 127
INET_ADDRSTRLEN = 16
IP_OPTIONS = 1
IP_HDRINCL = 2
IP_TOS = 3
IP_TTL = 4
IP_RECVOPTS = 5
IP_RECVRETOPTS = 6
IP_RECVDSTADDR = 7
IP_RETOPTS = 8
IP_MULTICAST_IF = 9
IP_MULTICAST_TTL = 10
IP_MULTICAST_LOOP = 11
IP_ADD_MEMBERSHIP = 12
IP_DROP_MEMBERSHIP = 13
IP_MULTICAST_VIF = 14
IP_RSVP_ON = 15
IP_RSVP_OFF = 16
IP_RSVP_VIF_ON = 17
IP_RSVP_VIF_OFF = 18
IP_PORTRANGE = 19
IP_RECVIF = 20
IP_IPSEC_POLICY = 21
IP_FAITH = 22
IP_STRIPHDR = 23
IP_FW_ADD = 40
IP_FW_DEL = 41
IP_FW_FLUSH = 42
IP_FW_ZERO = 43
IP_FW_GET = 44
IP_FW_RESETLOG = 45
IP_OLD_FW_ADD = 50
IP_OLD_FW_DEL = 51
IP_OLD_FW_FLUSH = 52
IP_OLD_FW_ZERO = 53
IP_OLD_FW_GET = 54
IP_NAT__XXX = 55
IP_OLD_FW_RESETLOG = 56
IP_DUMMYNET_CONFIGURE = 60
IP_DUMMYNET_DEL = 61
IP_DUMMYNET_FLUSH = 62
IP_DUMMYNET_GET = 64
IP_DEFAULT_MULTICAST_TTL = 1
IP_DEFAULT_MULTICAST_LOOP = 1
IP_MAX_MEMBERSHIPS = 20
IP_PORTRANGE_DEFAULT = 0
IP_PORTRANGE_HIGH = 1
IP_PORTRANGE_LOW = 2
IPPROTO_MAXID = (IPPROTO_AH + 1)
IPCTL_FORWARDING = 1
IPCTL_SENDREDIRECTS = 2
IPCTL_DEFTTL = 3
IPCTL_DEFMTU = 4
IPCTL_RTEXPIRE = 5
IPCTL_RTMINEXPIRE = 6
IPCTL_RTMAXCACHE = 7
IPCTL_SOURCEROUTE = 8
IPCTL_DIRECTEDBROADCAST = 9
IPCTL_INTRQMAXLEN = 10
IPCTL_INTRQDROPS = 11
IPCTL_STATS = 12
IPCTL_ACCEPTSOURCEROUTE = 13
IPCTL_FASTFORWARDING = 14
IPCTL_KEEPFAITH = 15
IPCTL_GIF_TTL = 16
IPCTL_MAXID = 17

# Included from netinet6/in6.h
__KAME_VERSION = "20010528/apple-darwin"
IPV6PORT_RESERVED = 1024
IPV6PORT_ANONMIN = 49152
IPV6PORT_ANONMAX = 65535
IPV6PORT_RESERVEDMIN = 600
IPV6PORT_RESERVEDMAX = (IPV6PORT_RESERVED-1)
INET6_ADDRSTRLEN = 46
IPV6_ADDR_INT32_ONE = 1
IPV6_ADDR_INT32_TWO = 2
IPV6_ADDR_INT32_MNL = 0xff010000
IPV6_ADDR_INT32_MLL = 0xff020000
IPV6_ADDR_INT32_SMP = 0x0000ffff
IPV6_ADDR_INT16_ULL = 0xfe80
IPV6_ADDR_INT16_USL = 0xfec0
IPV6_ADDR_INT16_MLL = 0xff02
IPV6_ADDR_INT32_ONE = 0x01000000
IPV6_ADDR_INT32_TWO = 0x02000000
IPV6_ADDR_INT32_MNL = 0x000001ff
IPV6_ADDR_INT32_MLL = 0x000002ff
IPV6_ADDR_INT32_SMP = 0xffff0000
IPV6_ADDR_INT16_ULL = 0x80fe
IPV6_ADDR_INT16_USL = 0xc0fe
IPV6_ADDR_INT16_MLL = 0x02ff
def IN6_IS_ADDR_UNSPECIFIED(a): return \

def IN6_IS_ADDR_LOOPBACK(a): return \

def IN6_IS_ADDR_V4COMPAT(a): return \

def IN6_IS_ADDR_V4MAPPED(a): return \

IPV6_ADDR_SCOPE_NODELOCAL = 0x01
IPV6_ADDR_SCOPE_LINKLOCAL = 0x02
IPV6_ADDR_SCOPE_SITELOCAL = 0x05
IPV6_ADDR_SCOPE_ORGLOCAL = 0x08
IPV6_ADDR_SCOPE_GLOBAL = 0x0e
__IPV6_ADDR_SCOPE_NODELOCAL = 0x01
__IPV6_ADDR_SCOPE_LINKLOCAL = 0x02
__IPV6_ADDR_SCOPE_SITELOCAL = 0x05
__IPV6_ADDR_SCOPE_ORGLOCAL = 0x08
__IPV6_ADDR_SCOPE_GLOBAL = 0x0e
def IN6_IS_ADDR_LINKLOCAL(a): return \

def IN6_IS_ADDR_SITELOCAL(a): return \

def IN6_IS_ADDR_MC_NODELOCAL(a): return \

def IN6_IS_ADDR_MC_LINKLOCAL(a): return \

def IN6_IS_ADDR_MC_SITELOCAL(a): return \

def IN6_IS_ADDR_MC_ORGLOCAL(a): return \

def IN6_IS_ADDR_MC_GLOBAL(a): return \

def IN6_IS_ADDR_MC_NODELOCAL(a): return \

def IN6_IS_ADDR_MC_LINKLOCAL(a): return \

def IN6_IS_ADDR_MC_SITELOCAL(a): return \

def IN6_IS_ADDR_MC_ORGLOCAL(a): return \

def IN6_IS_ADDR_MC_GLOBAL(a): return \

def IN6_IS_SCOPE_LINKLOCAL(a): return \

def IFA6_IS_DEPRECATED(a): return \

def IFA6_IS_INVALID(a): return \

IPV6_OPTIONS = 1
IPV6_RECVOPTS = 5
IPV6_RECVRETOPTS = 6
IPV6_RECVDSTADDR = 7
IPV6_RETOPTS = 8
IPV6_SOCKOPT_RESERVED1 = 3
IPV6_UNICAST_HOPS = 4
IPV6_MULTICAST_IF = 9
IPV6_MULTICAST_HOPS = 10
IPV6_MULTICAST_LOOP = 11
IPV6_JOIN_GROUP = 12
IPV6_LEAVE_GROUP = 13
IPV6_PORTRANGE = 14
ICMP6_FILTER = 18
IPV6_PKTINFO = 19
IPV6_HOPLIMIT = 20
IPV6_NEXTHOP = 21
IPV6_HOPOPTS = 22
IPV6_DSTOPTS = 23
IPV6_RTHDR = 24
IPV6_PKTOPTIONS = 25
IPV6_CHECKSUM = 26
IPV6_V6ONLY = 27
IPV6_BINDV6ONLY = IPV6_V6ONLY
IPV6_IPSEC_POLICY = 28
IPV6_FAITH = 29
IPV6_FW_ADD = 30
IPV6_FW_DEL = 31
IPV6_FW_FLUSH = 32
IPV6_FW_ZERO = 33
IPV6_FW_GET = 34
IPV6_RTHDR_LOOSE = 0
IPV6_RTHDR_STRICT = 1
IPV6_RTHDR_TYPE_0 = 0
IPV6_DEFAULT_MULTICAST_HOPS = 1
IPV6_DEFAULT_MULTICAST_LOOP = 1
IPV6_PORTRANGE_DEFAULT = 0
IPV6_PORTRANGE_HIGH = 1
IPV6_PORTRANGE_LOW = 2
IPV6PROTO_MAXID = (IPPROTO_PIM + 1)
IPV6CTL_FORWARDING = 1
IPV6CTL_SENDREDIRECTS = 2
IPV6CTL_DEFHLIM = 3
IPV6CTL_DEFMTU = 4
IPV6CTL_FORWSRCRT = 5
IPV6CTL_STATS = 6
IPV6CTL_MRTSTATS = 7
IPV6CTL_MRTPROTO = 8
IPV6CTL_MAXFRAGPACKETS = 9
IPV6CTL_SOURCECHECK = 10
IPV6CTL_SOURCECHECK_LOGINT = 11
IPV6CTL_ACCEPT_RTADV = 12
IPV6CTL_KEEPFAITH = 13
IPV6CTL_LOG_INTERVAL = 14
IPV6CTL_HDRNESTLIMIT = 15
IPV6CTL_DAD_COUNT = 16
IPV6CTL_AUTO_FLOWLABEL = 17
IPV6CTL_DEFMCASTHLIM = 18
IPV6CTL_GIF_HLIM = 19
IPV6CTL_KAME_VERSION = 20
IPV6CTL_USE_DEPRECATED = 21
IPV6CTL_RR_PRUNE = 22
IPV6CTL_MAPPED_ADDR = 23
IPV6CTL_V6ONLY = 24
IPV6CTL_RTEXPIRE = 25
IPV6CTL_RTMINEXPIRE = 26
IPV6CTL_RTMAXCACHE = 27
IPV6CTL_USETEMPADDR = 32
IPV6CTL_TEMPPLTIME = 33
IPV6CTL_TEMPVLTIME = 34
IPV6CTL_AUTO_LINKLOCAL = 35
IPV6CTL_RIP6STATS = 36
IPV6CTL_MAXID = 37
