import pytest

class attribute_data:
    pass

@pytest.fixture(autouse=True)
def attr(request):
    allinfo = attribute_data()
    for data in dir(request.node.function):
        if len(data) > 4 and data[0:2] == "__" and data [-2:] == "__":
            continue
        dattr = getattr(request.node.function, data, "Unknown")
        setattr(allinfo, data, dattr)
    return allinfo

def attributes(**kwargs):
    def decorate(func):
        for key, value in kwargs.items():
            setattr(func, key, value)
        return func
    return decorate

