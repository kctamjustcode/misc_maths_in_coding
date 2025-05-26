### for AES sim
import os, random


# 16-bit key in bytes
key_length = 16     # bit, every bit represents a hexadecimal
random_bytes = os.urandom(key_length)
dm = os.urandom(key_length)

rbl = [random_bytes[i] for i in range(key_length)]
dml = [dm[i] for i in range(key_length)]


# inv_ps_table[ps_table[index]] == index
ps_table = [11, 4, 6, 0, 1, 14, 2, 12, 10, 7, 8, 3, 15, 9, 13, 5]
inv_ps_table = [3, 4, 6, 11, 1, 15, 2, 9, 10, 13, 8, 0, 7, 14, 5, 12]

### for AES sim
def shift_array_left(ary, pos):
    return ary[pos:] + ary[:pos]

def vector_xor_add(v1, v2):
    assert len(v1) == len(v2)
    return [v1[i]^v2[i] for i in range(len(v1))]

def get_col(matr, pos):
    return [matr[i][pos] for i in range(len(matr))]


# main procedure
def addroundkey_smp(bkey, codes): # xor addition
    return [bkey[i]^codes[i] for i in range(key_length)]

# 'multiplicative' in the sense of mod f, or 'Rijndael S-box', switch to 4by4 table by permutation
def subbyte_smp(mesg):
    return [mesg[ps_table[i]] for i in range(key_length)]

def desubbyte_smp(enmesg):
    return [enmesg[inv_ps_table[i]] for i in range(key_length)]

def shiftrow_smp(chnk):
    blck =  [[chnk[i+j] for i in range(4)] for j in range(0, 13, 4)]
    return [shift_array_left(blck[i], i) for i in range(4)]

def deshiftrow_smp(blck):
    #blck =  [[chnk[i+j] for i in range(4)] for j in range(0, 13, 4)]
    return [shift_array_left(blck[i], 4-i) for i in range(4)]

'''
# avoid inverse problem, attributing to Rijndael's (AES) finite field;
# another diffusion sheme here
'''
def mixcom_smp(matr):
    r0 = vector_xor_add(matr[0], matr[1])
    r2 = vector_xor_add(matr[2], matr[3])
    xa_matr = [r0, matr[1], r2, matr[3]]
    c0 = vector_xor_add(get_col(xa_matr, 0), get_col(xa_matr, 1))
    c2 = vector_xor_add(get_col(xa_matr, 2), get_col(xa_matr, 3))
    for i in range(len(xa_matr)):
        xa_matr[i][0] = c0[i]
        xa_matr[i][2] = c2[i]
    return [xa_matr[i][::-1] for i in range(len(xa_matr))]

def demixcom_smp(matr):
    cmatr = [matr[i][::-1] for i in range(len(matr))]
    c0 = vector_xor_add(get_col(cmatr, 0), get_col(cmatr, 1))
    c2 = vector_xor_add(get_col(cmatr, 2), get_col(cmatr, 3))
    for i in range(len(cmatr)):
        cmatr[i][0] = c0[i]
        cmatr[i][2] = c2[i]
    r0 = vector_xor_add(cmatr[0], cmatr[1])
    r2 = vector_xor_add(cmatr[2], cmatr[3])
    xa_matr = [r0, cmatr[1], r2, cmatr[3]]
    return xa_matr

def aes_en_simp(rbk,dmsg):
    ark = addroundkey_smp(rbk, dml)
    sb = subbyte_smp(ark)
    sr = shiftrow_smp(sb)
    mc = mixcom_smp(sr)
    return mc[0]+mc[1]+mc[2]+mc[3]

def aes_de_simp(emsg):
    dmc = demixcom_smp([[emsg[i+j] for i in range(4)] for j in range(0, 13, 4)])
    dsr = deshiftrow_smp(dmc)
    dsb = desubbyte_smp(dsr[0]+dsr[1]+dsr[2]+dsr[3])
    dmsg = addroundkey_smp(rbl, dsb)
    return dmsg

enmsg = aes_en_simp(rbl, dml)
demsg = aes_de_simp(enmsg)
#print("aes simp suceeded: ", demsg == dml)



### for SHA sim
'''
Initialize hash values
first 32 bits of the fractional parts of the square roots of the first 2 primes 2..19
'''
h0 = 0x6a09e667
h1 = 0xbb67ae85

# a chunk consists of 8 bytes
chunk = dml[:8]

def En(chnk):
    return (chnk[4]&chnk[5]) ^ (~chnk[6]&chnk[7])

def Da(chnk):
    return (chnk[0]&chnk[1])^(chnk[0]&chnk[2])^(chnk[0]&chnk[3])^(chnk[1]&chnk[2])^(chnk[1]&chnk[3])^(chnk[2]&chnk[3])

def SumA(chnk):
    return (chnk[0]>>2)^(chnk[0]>>13)^(chnk[0]>>22)

def SumE(chnk):
    return (chnk[4]>>6)^(chnk[4]>>11)^(chnk[4]>>25)

temp1 = h0 + En(chunk) + Da(chunk)
temp2 = h1 + SumA(chunk) + SumE(chunk)

hsh = hex(temp1^temp2)
print('hashed: ', hsh)



### ACSII table
import binascii

def display_acsii_table():
    alph = ['abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
    lc = []
    for la in alph[0]:
        lc.append(bin(int(binascii.hexlify(la.encode()),16)))
    uc = []
    for ua in alph[1]:
        uc.append(bin(int(binascii.hexlify(ua.encode()),16)))
    return [lc, uc]

alpha_table = display_acsii_table()
