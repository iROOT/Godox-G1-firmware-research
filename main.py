#%%
def decode_data(data):
    '''
    v122 = 0i64;
    v125 = &unk_132F080;
    v124 = &unk_132F080 + qword_132F040;
    do
    {
      v62 = byte_E490C1[(v122 & 3) + 2] & (*v125 << ((v122 & 3) + 2)) | byte_E490CA[6 - (v122 & 3)] & (*v125 >> (8 - ((v122 & 3) + 2)));
      ++v122;
      *v125++ = v62;
    }
    while ( v125 != v124 )
    '''
    byte_E490CA = (0, 0, 0, 0x1F, 0x0F, 0x07, 0x03)
    byte_E490C1 = (0, 0, 0xFC, 0xF8, 0xF0, 0xE0)
    
    v122 = 0
    v125 = 0
    v124 = len(data)
    
    dec_data = []
    while v125 != v124:
        v62 = byte_E490C1[(v122 & 3) + 2] & (data[v125] << ((v122 & 3) + 2)) | byte_E490CA[6 - (v122 & 3)] & (data[v125] >> (8 - ((v122 & 3) + 2)))
        v122 += 1
        v125 += 1
        dec_data.append(v62)
    
    return bytes(dec_data)    
      
  
#%%
def reformat_data(file):
    f = open(file + '.dat', 'rb')
    f.seek(32)
    f_out = open(file + '.txt', 'w')
    b_out = open(file + '.bin', 'wb')
    try:
        start = 8
        end = -2
        
        for line in f:
            l = line[1:].strip().decode('utf8')
            
            out = l[:6] + '  ' + l[6:start] + '  '
                    
            if len(l) == 42:
                out += split(l, 2, start, end) + '  ' + l[end:]
                
                b_out.write(bytes.fromhex(l[start:end]))
            else:
                out += split(l, 2, start, 0)
                
            f_out.write(out+'\n')
    finally:
        f.close()
        f_out.close()
        b_out.close()


#%%     
def split(l, n, start, end):
    return ' '.join([l[i:i+n] for i in range(start, len(l)+end, n)])


#%%
import os

path = '.'

for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith('.fri'):
            file_path = os.path.splitext(os.path.join(root, file).replace('\\', '/'))[0]
            # for name in ['X1T-C_V20.1', 'X1T-N_V20', 'X1T-S V1.4']:
            with open(file_path+'.fri', 'rb') as f:
                with open(file_path+'.dat', 'wb') as out:
                    out.write(decode_data(f.read()))
            
            reformat_data(file_path)
