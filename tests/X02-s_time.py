#!
"""Unit test of simptime module"""

import s_time as st

local_time_string = st.get_local()
print(f'Local time = {local_time_string}')
print()

epoch_sec = st.get_epoch()
print(f'Epoch sec = {epoch_sec}')
print()

tstring = st.to_local(epoch_sec)
print(f'Local time from epoch = {tstring}')
print()

tstring = st.to_local(epoch_sec, '%B %d, %Y  %I:%M %p %Z')
print(f'Local time from epoch = {tstring}')
print()
