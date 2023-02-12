from shared import settings
from pprint import pprint
from decouple import config,AutoConfig
import inspect

# attributes  = dir(settings)
# for attribute in attributes:
#     print(attribute + '')
# pprint(settings)

attributes = inspect.getmembers(settings)
n_max = len(attributes)
for (n, (attribute, value)) in enumerate(attributes, start=1):
    print(f'{n}/{n_max} {attribute} {type(value)} {value}')