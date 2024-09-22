from charm.schemes.grpsig.groupsig_bgls04 import ShortSig
from charm.toolbox.pairinggroup import PairingGroup, serialize, deserialize


def split_list(lst, n):
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

def serializeGPK(group: PairingGroup, gpk: dict)->bytes:
    res = b''
    for _,v in gpk.items():
        res = res + group.serialize(v)
    return res

def deserializeGPK(group: PairingGroup, bytes: bytes)->dict:
    gpk = {}
    gpk['g1'] = group.deserialize(bytes[:42])
    gpk['g2'] = group.deserialize(bytes[42:160])
    gpk['h'] = group.deserialize(bytes[160:202])
    gpk['u'] = group.deserialize(bytes[202:244])
    gpk['v'] = group.deserialize(bytes[244:286])
    gpk['w'] = group.deserialize(bytes[286:404])
    return gpk


def serializeSig(group: PairingGroup, sig: dict)->bytes:
    res = b''
    for _,v in sig.items():
        res = res + group.serialize(v)
    return res

def deserializeSig(group: PairingGroup, bytes: bytes)->dict:
    sig = {}
    list = split_list(bytes,9)
    sig['T1'] = group.deserialize(list[0])
    sig['T2'] = group.deserialize(list[1])
    sig['T3'] = group.deserialize(list[2])
    sig['c'] = group.deserialize(list[3])
    sig['s_alpha'] = group.deserialize(list[4])
    sig['s_beta'] = group.deserialize(list[5])
    sig['s_x'] = group.deserialize(list[6])
    sig['s_delta1'] = group.deserialize(list[7])
    sig['s_delta2'] = group.deserialize(list[8])
    return sig

def serializeGSK(group: PairingGroup, gsk: dict)->bytes:
    return group.serialize(gsk[0])+group.serialize(gsk[1])

def deserializeGSK(group: PairingGroup, bytes: bytes)->tuple:
    a1 = bytes[:42]
    a2 = bytes[42:]
    return (group.deserialize(a1),group.deserialize(a2))