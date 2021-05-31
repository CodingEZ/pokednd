from move_enum import MoveEnum, match_move_type

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
            if len(v) == 0:
                continue
            t = match_move_type(v)
            if t is None:
                raise Exception()
            POKEDATA[name]['types'].append(t)

        if len(POKEDATA[name]['types']) == 0:
            POKEDATA[name]['types'].append(MoveEnum.NORMAL)
