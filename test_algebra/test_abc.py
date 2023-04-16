import operator as op
from dataclasses import dataclass
import pytest

DOMAIN = (0, 1)

@pytest.fixture(params=DOMAIN)
def data_1(request):
    return Data(request.param, request.param)

data_2 = data_1

def generate_fixture(someparam):
    @pytest.fixture
    def my_fixture():
        return someparam
    return my_fixture

def inject_fixture(name, someparam):
    globals()[name] = generate_fixture(someparam)

inject_fixture('my_user', 100)

MAX_LEVEL = 4

@dataclass(frozen=True)
class Data:
    exp: int
    act: float
    level: int = 0

    def __post_init__(self):
        assert self.level <= MAX_LEVEL
        assert self.exp == self.act

    def __add__(self, other):
        return Data(self.exp + other.exp, self.act + other.act)

    def __sub__(self, other):
        return Data(self.exp - other.exp, self.act - other.act)

    def __mul__(self, other):
        return Data(self.exp * other.exp, self.act * other.act)
    
    def relin(self):
        result = Data(self.exp, self.act, self.level + 1)
        assert result.level == self.level + 1
        return result
    
    
    def assert_valid(self):
        assert self.exp == self.act

@pytest.fixture(params=[op.add, op.sub, op.mul])
def b_operator(request):
    return request.param

# TODO pair u_operator with count
@pytest.fixture(params=[Data.relin])
def u_operator(request):
    return request.param

def test(data_1, data_2, b_operator):
    b_operator(data_1, data_2)




def test_1(data_1, u_operator):
    assert data_1.level == 0

    for i in range(MAX_LEVEL):
        data_1 = u_operator(data_1)
    
    with pytest.raises(AssertionError):
        data_1 = u_operator(data_1)
    
    assert data_1.level == MAX_LEVEL

        

