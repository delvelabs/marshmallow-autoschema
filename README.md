[![Build Status](https://travis-ci.org/delvelabs/marshmallow-autoschema.svg?branch=master)](https://travis-ci.org/delvelabs/marshmallow-autoschema)

# marshmallow-autoschema

Generate marshmallow schemas from code annotations and type hinting, converting
object structures to serializable native types and back effortlessly.


```python
from marshmallow_autoschema import autoschema, Many, One


@autoschema
class Page:

    def __init__(self, *,
                 word_count: int) -> None: pass


@autoschema
class Book:

    def __init__(self, *,
                 cover: One[Page],
                 pages: Many[Page]) -> None: pass

data = {
    "cover": {"word_count": 12},
    "pages": [
        {"word_count": 0},
        {"word_count": 12},
        {"word_count": 100},
    ],
}

book, errors = Book.load(data)

assert isinstance(book, Book)
assert isinstance(book.cover, Page)

out, errors = book.dump()

assert data == out
```

## License

Copyright (c) 2017- Delve Labs Inc.

This library is distributed under the MIT License. See joined LICENSE file for details.
