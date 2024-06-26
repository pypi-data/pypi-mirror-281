# unsure

`unsure` is a library for creating operations on uncertain or ambiguous values, utilizing an inference endpoint to determine transformations and comparisons. It's meant to leverage ai while yielding predictable and invariant results.

## Installation

To install the package, run:

```bash
pip install py-unsure
```

## Configuration

All that needs to be configured is the inference endpoint.

### Through API Key

It supports Groq apis and OpenAi apis for now, so a groqApiKey can be provided like this

```python

from unsurepy import config_global_unsure

config_global_unsure(groq_api_key='your key here')

```

and for openAi

```python

import { unsure, configGlobalunsure } from 'unsure-js';

configGlobalunsure({ openAiApiKey: 'your key here' });

```

### Through and inference function

```python

from unsurepy import config_global_unsure

def inference_endpoint(q: str) -> str:
    # any function that returns a string here, you can call OpenAI, Gemini, Claude, or your own model, just return a string
    pass

config_global_unsure(inference_endpoint=inference_endpoint)

```

## Usage

Once it's configured you can start using the operators just like this

### Is operator:
Checks equality. Example:

```python
from unsurepy import config_global_unsure

config_global_unsure(groq_api_key='your key here')

print(unsure("Lion").is_("Mammal"))  # True

```

### Pick operator:
Picks an information from a string. Example:

```python
from unsurepy import config_global_unsure

config_global_unsure(groq_api_key='your key here')

print(unsure("Contact Number: +1-800-555-5555").pick("phone number"))  # "+1-800-555-5555"
print(unsure("Phone: +1-800-555-5555").pick("phone number"))  # "+1-800-555-5555"
print(unsure("Call us at +1-800-555-5555").pick("phone number"))  # "+1-800-555-5555"

```

### Categorize operator:
Categorizes the string into the given categories. Example:

```python
from unsurepy import config_global_unsure

config_global_unsure(groq_api_key='your key here')

print(unsure("Sky").categorize(["blue", "green"]))  # "blue"
print(unsure("Grass").categorize(["blue", "green"]))  # "green"

```

### flatMapTo operator:
Transforms the string into what's demanded. Example:

```python
from unsurepy import config_global_unsure

config_global_unsure(groq_api_key='your key here')

print(unsure("Response: {\"key\": \"should get this\"}").flat_map_to("key's value"))  # "should get this"
print(
    unsure("HTML Content: <html><body><div class=\"scrapable\">Target Content<div></body></html>")
    .flat_map_to("content of the div with the class scrapable")
)  # "target content"
print(unsure("Favorite Color: #FF5733").flat_map_to("color in hex"))  # "#ff5733"
print(unsure("Order Total: 12345 USD").flat_map_to("price"))  # "12345"

```

### mapTo operator:
Transforms the string into what's demanded but returns an unsure, so it's chainable. Example:

```python
from unsurepy import config_global_unsure

config_global_unsure(groq_api_key='your key here')

print(unsure("Amount: 200.23 $").map_to("number").map_to("integer").flat())  # "200"
```

### flat operator:
Returns either the changed transformation's result or the initial value if no mapTo was used. Example:

```python
from unsurepy import config_global_unsure

config_global_unsure(groq_api_key='your key here')

print(unsure("Amount: 200.23 $").map_to("number").map_to("integer").flat())  # "200"
print(unsure("Some value").flat())  # "Some value"
```

## Options
`inferenceEndpoint`: The function that will be called in the operators.
`groqApiKey`: The Api key that will be used to call groq APIs using llama3-70b-8192 model.
`openAiApiKey`: The Api key that will be used to call Open Ai APIs using gpt-3.5-turbo.
`model`: You can specify the model you want to use, for open source models llama3-70b-8192 works best which is the default. 
`preventLowerCase`: Prevents lowercasing the inference response.

Note: If both `inferenceEndpoint` and `groqApiKey` are provided `inferenceEndpoint` will be used.

## Create and insure instance
You might have noticed so far that a global unsure instance is used. You can also create your own
instance with it's own configuration.

```python
from unsurepy import create_unsure, config_global_unsure

config_global_unsure(groq_api_key='your key here')

my_unsure = create_unsure(openai_api_key='your key here')

print(unsure("Amount: 200.23 $").map_to("number").map_to("integer").flat())  # Uses Groq
print(my_unsure("Some value").flat())  # Uses OpenAI APIs
```

## License
This project is under the ISC license. Requests and contributions are most welcomed.