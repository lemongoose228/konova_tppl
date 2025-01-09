import re

class ModifiedDict(dict):
    def __init__(self):
        super().__init__()
        self.iloc = Iloc(self)
        self.ploc = Ploc(self)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.sort_keys()

    def sort_keys(self):
        sorted_items = sorted(self.items())
        self.clear()
        for k, v in sorted_items:
            super().__setitem__(k, v)

class Iloc:
    def __init__(self, modified_dict):
        self.modified_dict = modified_dict

    def __getitem__(self, index):
        if isinstance(index, int):
            keys = list(self.modified_dict.keys())
            if 0 <= index < len(keys):
                return self.modified_dict[keys[index]]
            else:
                raise IndexError("Index out of range")
        else:
            raise TypeError("Only int type can be specified")

class Ploc:
    def __init__(self, modified_dict):
        self.modified_dict = modified_dict

    def read(self, key: str):
        # Регулярное выражение для извлечения знаков и чисел
        sign_pattern = r'([<>]=?|=)'  # Matches >, >=, <, <=, <>, =
        number_pattern = r'(\d+\.?\d*)'  # Matches integers and floats

        # Find all signs and numbers using regex findall
        signs = re.findall(sign_pattern, key)
        numbers = re.findall(number_pattern, key)

        # Validate the extracted numbers and convert to float
        float_numbers = []
        for number in numbers:
            if number.count(".") > 1:
                raise KeyError("Incorrect key specified")
            float_numbers.append(float(number))

        # Return the results
        return signs, float_numbers


    def comparison(self, signs, numbers, keys):
        result = {}

        for j, key in enumerate(keys):
            key_numbers = [int(n) for n in key.replace("(", '').replace(")", '').split(', ') if n.isdigit()]

            if len(key_numbers) != len(signs):
                continue

            # Проверяем соответствие условий
            conditions_met = True

            for i, sign in enumerate(signs):
                if sign == '>':
                    conditions_met &= (key_numbers[i] > numbers[i])
                elif sign == '<':
                    conditions_met &= (key_numbers[i] < numbers[i])
                # Можно добавить другие знаки сравнения здесь, если потребуется
                elif sign == '>=':
                    conditions_met &= (key_numbers[i] >= numbers[i])
                elif sign == '<=':
                    conditions_met &= (key_numbers[i] <= numbers[i])
                elif sign == '=':
                    conditions_met &= (key_numbers[i] == numbers[i])
                elif sign == '<>':
                    conditions_met &= (key_numbers[i] != numbers[i])

            if conditions_met:
                result[key] = self.modified_dict[key]

        return result

    def __getitem__(self, key):
        if isinstance(key, str):
            if len(key) < 2:
                raise KeyError("The key length must be more than two")

            signs, numbers = self.read(key)
            keys = list(self.modified_dict.keys())

            return self.comparison(signs, numbers, keys)
        else:
            raise KeyError("Only string type can be specified")




# map = ModifiedDict()
# map["value1"] = 1
# map["value2"] = 2
# map["value3"] = 3
# map["1"] = 10
# map["2"] = 20
# map["3"] = 30
# map["1, 5"] = 100
# map["5, 5"] = 200
# map["10, 5"] = 300
#
# print(map.iloc[0])  # >>> 10
# print(map.iloc[2])  # >>> 300
# print(map.iloc[5])  # >>> 200
# print(map.iloc[8])  # >>> 3

map = ModifiedDict()
map["value1"] = 1
map["value2"] = 2
map["value3"] = 3
map["1"] = 10
map["2"] = 20
map["3"] = 30
map["(1, 5)"] = 100
map["(5, 5)"] = 200
map["(10, 5)"] = 300
map["(1, 5, 3)"] = 400
map["(5, 5, 4)"] = 500
map["(10, 5, 5)"] = 600

print(map.ploc[">=1"]) # >>> {1=10, 2=20, 3=30}
print(map.ploc["<3"]) # >>> {1=10, 2=20}

print(map.ploc[">0, >0"]) # >>> {(1, 5)=100, (5, 5)=200, (10, 5)=300}
print(map.ploc[">=10, >0"]) # >>> {(10, 5)=300}

print(map.ploc["<5, >=5, >=3"]) # >>> {(1, 5, 3)=400}