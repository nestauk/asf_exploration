#!/usr/bin/env python
# coding: utf-8

# ## Taking a look at RECC complaints data

# In[ ]:


import getters


# In[ ]:


# Downloading raw RECC complaints data from S3
getters.download_recc_data_from_s3()

# Saving raw RECC complaints data as one sheet csv
getters.raw_recc_data_to_one_sheet()


# In[ ]:



# Getting raw RECC complaints data
raw_recc_data = getters.get_raw_recc_data()


# In[ ]:


raw_recc_data


# In[ ]:


from processing_recc_data import process_recc_data


# In[ ]:


# Processing raw RECC data
process_recc_data(raw_recc_data)


# In[ ]:


#Taking a look at processed RECC data
processed_recc_data = getters.get_processed_recc_data() 


# In[ ]:


processed_recc_data


# In[ ]:




