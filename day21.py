TEST = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""


def process_input(raw: str) -> (list, set, set):
    food = []
    ingredients = set()
    allergens = set()
    for line in raw.split("\n"):
        if not line:
            continue
        ingreds = []
        allergs = []
        ing = line.split(" (contains ")[0]
        for i in ing.split(" "):
            ingredients.add(i)
            ingreds.append(i)
        allerg = line.split("(contains ")[1]
        for a in allerg.split(" "):
            if "," in a or ")" in a:
                a = a[:-1]
            allergens.add(a)
            allergs.append(a)
        food.append([ingreds, allergs])
    return food, ingredients, allergens


def find_possible_allergens(food, ingredients, allergens) -> dict:
    poss = {}
    allergen_frees = []
    for ingreds, allergs in food:
        for allerg in allergs:
            if allerg not in poss:
                poss[allerg] = set(ingreds.copy())
            else:
                poss[allerg] &= set(ingreds)
    return poss


def find_allergen_frees(ingredients, possible_allergens) -> list:
    allergen_frees = []
    for ingredient in ingredients:
        allergen_free = True
        for allerg in possible_allergens:
            if ingredient in possible_allergens[allerg]:
                allergen_free = False
        if allergen_free:
            allergen_frees.append(ingredient)
    return allergen_frees


def ans1(food, ingredients, allergens) -> int:
    poss = find_possible_allergens(food, ingredients, allergens)
    allergen_frees = find_allergen_frees(ingredients, poss)
    ans = 0
    for ingreds, allergs in food:
        for all_free in allergen_frees:
            if all_free in ingreds:
                ans += 1
    return ans


def ans2(possible_allergens) -> str:
    n = len(possible_allergens)
    known = []
    known_prev = known.copy()
    while len(known) < n:
        for poss in possible_allergens.copy():
            if len(possible_allergens[poss]) == 1:
                ingredient = possible_allergens[poss].pop()
                known.append((ingredient, poss))
                for poss in possible_allergens.copy():
                    if ingredient in possible_allergens[poss]:
                        possible_allergens[poss].remove(ingredient)
    known.sort(key=lambda x: x[1])
    return ",".join([x[0] for x in known])


food, ingredients, allergens = process_input(TEST)
assert ans1(food, ingredients, allergens) == 5
assert (
    ans2(find_possible_allergens(food, ingredients, allergens)) == "mxmxvkd,sqjhc,fvjkl"
)

with open("day21input") as f:
    raw = f.read()
    food, ingredients, allergens = process_input(raw)
    print(ans1(food, ingredients, allergens))
    print(ans2(find_possible_allergens(food, ingredients, allergens)))

