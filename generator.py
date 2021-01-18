import random
from math import floor


class ContainerNumberValidator:

    LETTER_NUMBERS = {
        'A': 10,
        'B': 12,
        'C': 13,
        'D': 14,
        'E': 15,
        'F': 16,
        'G': 17,
        'H': 18,
        'I': 19,
        'J': 20,
        'K': 21,
        'L': 13,
        'M': 24,
        'N': 25,
        'O': 26,
        'P': 27,
        'Q': 28,
        'R': 29,
        'S': 30,
        'T': 31,
        'U': 32,
        'V': 34,
        'W': 35,
        'X': 36,
        'Y': 37,
        'Z': 38,
    }

    EQUIPMENT_CATEGORIES = ['U', 'J', 'Z']

    POSITIONAL_MULTIPLIERS = {
        0: pow(2, 0),
        1: pow(2, 1),
        2: pow(2, 2),
        3: pow(2, 3),
        4: pow(2, 4),
        5: pow(2, 5),
        6: pow(2, 6),
        7: pow(2, 7),
        8: pow(2, 8),
        9: pow(2, 9)
    }

    def get_checksum(self, input: str):
        sum = 0
        
        for i in range(0, 10):
            char = input[i]
            number = 0
            
            if i < 4:
                number = self.LETTER_NUMBERS[char]
            else:
                number = int(char)

            number = number * self.POSITIONAL_MULTIPLIERS[i]
            
            sum += number

        checksum = sum % 11

        if checksum == 10:
            checksum = 0

        return checksum

    @classmethod
    def get_default_validation_result(cls):
        return {
            'invalidLength': False,
            'invalidOwner': False,
            'invalidEquipmentCategory': False,
            'invalidSerialNumber': False,
            'invalidChecksum': False,
            'isValid': False,
            'checksum': 0,
        }

    def validate(self, input: str):
        result = self.get_default_validation_result()
        
        exit = False
        
        if not input or len(input) != 11:
            result['invalidLength'] = True
            exit = True
        
        
        if len(input) >= 1 and any([c < 65 or c > 90 for c in map(ord, input[0:3])]):
            result['invalidOwner'] = True
            exit = True
        
        if (
            len(input) >= 4 and 
            input[3] not in self.EQUIPMENT_CATEGORIES
        ):
            result['invalidEquipmentCategory'] = True
            exit = True
        

        if (
            len(input) >= 6 and 
            not input[4:].isnumeric()
        ):
            result['invalidSerialNumber'] = True
            exit = True
        

        if exit:
            return result

        result['checksum'] = self.get_checksum(input)
        result['invalidChecksum'] = result['checksum'] != int(input[10])
        result['isValid'] = not result['invalidChecksum']
        return result



if __name__ == '__main__':
    validator = ContainerNumberValidator()

    GENERATE_COUNT = 1000000
    LETTERS = list(ContainerNumberValidator.LETTER_NUMBERS.keys())

    generated = []

    for i in range(1, GENERATE_COUNT + 1):
        owner = str(random.choice(LETTERS)) + str(random.choice(LETTERS)) + str(random.choice(LETTERS))
        category = 'U'
        serial_number = str(random.randint(0, 999999)).zfill(6)

        container_number_raw = owner + category + serial_number
        checksum = validator.get_checksum(container_number_raw)
        container_number = container_number_raw + str(checksum)

        generated.append(container_number)

        if i == 1 or i == GENERATE_COUNT or i % (GENERATE_COUNT / 100) == 0:
            print(f'{i}/{GENERATE_COUNT} generated')


    with open('container-numbers.txt', 'w') as file:
        # Let's just write 10MB of data at once
        file.write('\n'.join(generated))
