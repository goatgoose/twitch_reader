import numpy as np
from collections import Counter

t = [
    (1602569007.2033665, "ariasaki"),
    (1602569026.5278213, "ariasaki"),
    (1602569029.4771373, "ariasaki"),
    (1602569035.1472967, "ariasaki"),
    (1602569210.2993395, "pokimane")
]

a = ["pokimane", "pokimane", "pokimane", "pokimane", "ariasaki", "ariasaki", "tinakitten"]

counter = Counter(a)
print(counter.most_common(1))
