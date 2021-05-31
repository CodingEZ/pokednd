from move_enum import MoveEnum

POKEDATA = dict()
with open('pokemon.csv', 'r') as file:
    lines = file.readlines()
    flag = True
    for line in lines:
        if flag:
            flag = False
            continue
        attack, base_egg_steps, base_happiness, base_total, capture_rate, \
            classfication, defense, experience_growth, height_m, hp, \
            name, percentage_male, pokedex_number, sp_attack, sp_defense, \
            speed, type1, type2, weight_kg, generation, is_legendary = line.strip().split(',')

        POKEDATA[name] = {
            'hp': int(hp),
            'attack': int(attack),
            'defense': int(defense),
            'sp_attack': int(sp_attack),
            'sp_defense': int(sp_defense),
            'speed': int(speed),
            'friendship': int(base_happiness),
            'weight': float(weight_kg),
            'types': []
        }

        for v in [type1, type2]:
            if v == "normal":
                POKEDATA[name]['types'].append(MoveEnum.NORMAL)
            elif v == "fire":
                POKEDATA[name]['types'].append(MoveEnum.FIRE)
            elif v == "water":
                POKEDATA[name]['types'].append(MoveEnum.WATER)
            elif v == "grass":
                POKEDATA[name]['types'].append(MoveEnum.GRASS)
            elif v == "psychic":
                POKEDATA[name]['types'].append(MoveEnum.PSYCHIC)
            elif v == "dark":
                POKEDATA[name]['types'].append(MoveEnum.DARK)
            elif v == "fighting":
                POKEDATA[name]['types'].append(MoveEnum.FIGHTING)
            elif v == "dragon":
                POKEDATA[name]['types'].append(MoveEnum.DRAGON)
            elif v == "fairy":
                POKEDATA[name]['types'].append(MoveEnum.FAIRY)
            elif v == "steel":
                POKEDATA[name]['types'].append(MoveEnum.STEEL)
            elif v == "flying":
                POKEDATA[name]['types'].append(MoveEnum.FLYING)
            elif v == "ground":
                POKEDATA[name]['types'].append(MoveEnum.GROUND)
            elif v == "electric":
                POKEDATA[name]['types'].append(MoveEnum.ELECTRIC)

        if len(POKEDATA[name]['types']) == 0:
            POKEDATA[name]['types'].append(MoveEnum.NORMAL)
