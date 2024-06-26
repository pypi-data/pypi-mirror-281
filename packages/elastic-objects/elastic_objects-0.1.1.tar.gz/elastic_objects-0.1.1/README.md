# LiquidPy

![alt text](./liquid-objects-cover.svg "Liquid Objects")

LiquidPy introduces the concept of "liquid objects" in Python - a flexible approach to object-oriented programming that allows for dynamic attribute assignment and management at runtime.

## Features

- Dynamic attribute addition and removal
- Flexible object initialization
- Transparent attribute access
- Ideal for handling evolving data structures, configuration management, and API integrations

## Installation

You can install LiquidPy using pip:

```bash
pip install liquidpy
```

## Usage

### Basic Usage

```python
from liquidpy.liquid_object import LiquidObject

# Create a new liquid object
person = LiquidObject()

# Add attributes dynamically
person.name = "Alice"
person.age = 30

# Access attributes
print(person.name)  # Output: Alice
print(person.age)   # Output: 30

# Add a method
person.greet = lambda: f"Hello, I'm {person.name}!"
print(person.greet())  # Output: Hello, I'm Alice!

# Remove an attribute
del person.age

# Trying to access a removed attribute raises an AttributeError
# print(person.age)  # This would raise an AttributeError
```

### Initialization with Attributes

```python
# Initialize with attributes
config = LiquidObject(
    database="mysql",
    host="localhost",
    port=3306
)

print(config.database)  # Output: mysql
print(config.port)      # Output: 3306

# Add new attributes later
config.username = "admin"
```

### Use Case: Handling API Responses

```python
import requests
from liquidpy import LiquidObject

def get_user_data(user_id):
    # Simulating an API call
    response = requests.get(f"https://api.example.com/users/{user_id}")
    data = response.json()
    
    # Create a liquid object from the response
    user = LiquidObject(**data)
    
    return user

# Usage
user = get_user_data(123)
print(user.name)
print(user.email)

# If the API starts returning a new field, it's automatically accessible
print(user.new_field)  # No need to update the class definition
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.