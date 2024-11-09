import pytest
from notation.main import dataError, prefix_to_infix  

class TestPrefixToInfix:

    def test_notation(self):
        assert prefix_to_infix("+ - 13 4 55") == "((13 - 4) + 55)"
        assert prefix_to_infix(" / + 3 10 * + 2 3 - 3 5") == "((3 + 10) / ((2 + 3) * (3 - 5)))"
        assert prefix_to_infix("+ 2 * 2 - 2 1") == "(2 + (2 * (2 - 1)))"
        assert prefix_to_infix("+ + 10 20 30") == "((10 + 20) + 30)"
        

    def test_invalid_input(self):
        with pytest.raises(dataError, match="Количество цифр не соответствует количеству операторов"):
            prefix_to_infix("+ 2")

        with pytest.raises(dataError, match="Количество цифр не соответствует количеству операторов"):
            prefix_to_infix("2 -")

        with pytest.raises(dataError, match="Количество цифр не соответствует количеству операторов"):
            prefix_to_infix("- - 1 2")

        with pytest.raises(dataError, match="Ничего небыло введено"):
            prefix_to_infix("")


