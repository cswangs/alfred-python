## Overview

A simple Python Alfred workflow template

### Installation

```
pip install -e .

alfred-python multiline_to_comma "line1
line2
line3"


```

### Debug

```
python -m alfred.main multiline_to_comma "line1
line2
line3"

```

### script filter config

```
export PATH="/Users/wangchunsheng/miniforge3/bin:$PATH"
query=$1
alfred-python "multiline_to_comma" "$query" "empty"
```



![1736857035042](image/README/1736857035042.png)
