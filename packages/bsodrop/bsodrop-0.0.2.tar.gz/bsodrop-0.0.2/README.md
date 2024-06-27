A simple python repository for calling bsod inside your code.

## Usage:

Installing:

`pip install -U bsodrop`

```python
import bsodrop as bsod

bsod.start()  # Start BSOD
```

Build `bst.dll`:

```shell
g++ -shared -o "bst.dll" "-Wl,--out-implib,libbst.a" "pbsod.cpp" "-lntdll"
```