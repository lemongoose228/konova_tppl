class dataError(Exception):
    pass

def is_operator(symbol):
    return symbol in ('+', '-', '*', '/')

def prefix_to_infix(data):
    symbols = data.split()
    res = []

    for symbol in reversed(symbols):
        if is_operator(symbol):
            try:
                num1 = res.pop()
                num2 = res.pop()
            except IndexError:
                raise dataError("Количество цифр не соответствует количеству операторов")

            new_data = f"({num1} {symbol} {num2})"
            res.append(new_data)
        else:
            res.append(symbol)

    if len(res) < 1:
        raise dataError("Ничего небыло введено")
        
    return res.pop()

