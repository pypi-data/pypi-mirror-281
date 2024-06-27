# common-logging
python logging handler to fix the problem of your program having multiple instances and logging to the same file

> package name reservation

planned is something along the lines of

```python
import logging
from commonlogging import CommonLoggingHandler

APPLICATION_PORT=12345

logging.basicConfig(
    handlers=[
        CommonLoggingHandler(port=12345, handler=logging.FileHandler("file.log"))
    ]
)
```
