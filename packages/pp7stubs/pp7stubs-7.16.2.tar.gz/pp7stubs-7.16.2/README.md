# pp7stubs

## Purpose
This project aims to simplify the usage of Python-generated stubs from ProPresenter 7 proto files. 

## Dependencies
- Python >= 3.8
- [protobuf](https://pypi.org/project/protobuf/)

## Installation
```
pip install pp7stubs
```

## How to use
```python
from pp7stubs import presentation_pb2

with open('example.pro', 'rb') as f:
    serialized_data = f.read()

presentation = presentation_pb2.Presentation()
presentation.ParseFromString(serialized_data)

print("uuid:", presentation.uuid.string)
print("name:", presentation.name)
```