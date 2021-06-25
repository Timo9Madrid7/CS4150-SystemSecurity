#!/usr/bin/env python
# coding: utf-8

# In[1]:


ascii_start = 0x20
ascii_end = 0x7E


# In[2]:


f = open("./commands.txt", "a+")

for param2_0 in range(ascii_start, ascii_end + 1):
    for param2_1 in range(ascii_start, ascii_end + 1):
        for param2_2 in range(ascii_start, ascii_end + 1):
            if (((param2_2 ^ param2_0) ^ (param2_1 << 1)) == 0x3D):
                command = chr(param2_0) + chr(param2_1) + chr(param2_2)
                f.write(command + '\n')

f.close()


# In[ ]:




