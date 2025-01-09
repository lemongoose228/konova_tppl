import pytest
from hashMap import ModifiedDict

class TestMyDict:

    def test_correct_iloc(self):
        mydict = ModifiedDict()
        mydict["value1"] = 1
        mydict["value2"] = 2
        mydict["value3"] = 3
        mydict["1"] = 10
        mydict["2"] = 20
        mydict["3"] = 30
        mydict["1, 5"] = 100
        mydict["5, 5"] = 200
        mydict["10, 5"] = 300

        assert mydict.iloc[0] == 10
        assert mydict.iloc[2] == 300
        assert mydict.iloc[5] == 200
        assert mydict.iloc[8] == 3

    def test_incorrect_index_iloc(self):
        mydict = ModifiedDict()
        mydict["value1"] = 1
        mydict["value2"] = 2
        mydict["value3"] = 3
        mydict["1"] = 10
        mydict["2"] = 20
        mydict["3"] = 30
        mydict["1, 5"] = 100
        mydict["5, 5"] = 200
        mydict["10, 5"] = 300

        with pytest.raises(IndexError):
            mydict.iloc[10]


    def test_correct_ploc(self):
        mydict = ModifiedDict()
        mydict["value1"] = 1
        mydict["value2"] = 2
        mydict["value3"] = 3
        mydict["1"] = 10
        mydict["2"] = 20
        mydict["3"] = 30
        mydict["(1, 5)"] = 100
        mydict["(5, 5)"] = 200
        mydict["(10, 5)"] = 300
        mydict["(1, 5, 3)"] = 400
        mydict["(5, 5, 4)"] = 500
        mydict["(10, 5, 5)"] = 600

        assert mydict.ploc[">=1"] == {"1": 10, "2": 20, "3": 30}
        assert mydict.ploc["<3"] == {"1": 10, "2": 20}
        assert mydict.ploc[">0, >0"] == {"(1, 5)": 100, "(5, 5)": 200, "(10, 5)": 300}
        assert mydict.ploc["<5, >=5, >=3"] == {"(1, 5, 3)": 400}
        assert mydict.ploc["=2"] == {"2": 20}
        assert mydict.ploc["<=2"] == {"1": 10, "2": 20}

    def test_incorrect_index_ploc(self):
        mydict = ModifiedDict()
        mydict["value1"] = 1

        with pytest.raises(KeyError):
            mydict.ploc[1]

    def test_incorrect_key_length_ploc(self):
        mydict = ModifiedDict()
        mydict["value1"] = 1

        with pytest.raises(KeyError):
            mydict.ploc["="]
