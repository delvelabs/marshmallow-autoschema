# MIT License
#
# Copyright (c) 2017- Delve Labs Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from pytest import raises
from typing import List

from marshmallow_autoschema import schema_metafactory
from marshmallow_autoschema import autoschema, One, Many, validate_field

from marshmallow.fields import Url
from marshmallow.validate import Range, URL as ValURL, Length
from marshmallow.exceptions import ValidationError


class URL:
    pass


custom = schema_metafactory(extended_field_map={
    URL: Url,
})


@custom
class A:
    def __init__(self, *,
                 target: URL) -> None: pass


def test_custom_field():
    a = A(target="http://example.com/")

    data, errors = a.dump()
    assert data == {"target": "http://example.com/"}


def test_custom_field_fails_validation():
    a = A(target="example.com/")

    data, errors = a.dump(strict=False)
    assert errors == {"target": ["Not a valid URL."]}


@validate_field('popularity', Range(1, 10))
@validate_field('links', ValURL())
@autoschema
class MyPageRank:
    '''
    Eat your heart out, Eric Schmidt.
    '''

    def __init__(self, *, popularity: int, links: List[str]):
        pass


def test_load_validation():
    record = MyPageRank(popularity=5, links=['http://www.foo.com']).dump()
    tampered_record = {'popularity': 1, 'links': ['1337']}
    with raises(ValidationError):
        MyPageRank.load(tampered_record)
