from Fuzzy import FuzzyUniverse, FuzzyRule, FuzzySystem
import Fuzzy.Function as Function
from Fuzzy.Term import Term

if __name__ == "__main__":
    # univerza předpokladů
    filmy = FuzzyUniverse(0, 10, 'Kvalita filmů')
    filmy["Mizerná"] = Term(Function.TrapMF(0, 0, 2, 4))
    filmy["Dobrá"] = Term(Function.TrapMF(3, 4, 7, 8))
    filmy["Vynikající"] = Term(Function.TrapMF(6, 8, 10, 10))

    av = FuzzyUniverse(0, 10, 'Kvalita AV')
    av["Mizerná"] = Term(Function.TrapMF(0, 0, 2, 4))
    av["Dobrá"] = Term(Function.TrapMF(3, 4, 6, 7))
    av["Vynikající"] = Term(Function.TrapMF(6, 8, 10, 10))

    # univerzum výsledků, fce příslušnosti pro výsledek ~ počty množin nemusejí být stejné
    kino = FuzzyUniverse(0, 10, 'Hodnocení kina')
    kino['Hrůza'] = Term(Function.TrapMF(0, 0, 1, 3))
    kino['Průměr'] = Term(Function.TrapMF(2, 3, 6, 7))
    kino['Dobré'] = Term(Function.TrapMF(6, 7, 8, 9))
    kino['Paráda'] = Term(Function.TrapMF(8, 9, 10, 10))

    # filmy.view()
    # av.view()
    # kino.view()

    rule1 = FuzzyRule(filmy['Mizerná'] & av['Mizerná'], kino['Hrůza'])
    rule2 = FuzzyRule(filmy['Mizerná'] & ~av['Mizerná'], kino['Průměr'])
    rule3 = FuzzyRule(filmy['Dobrá'] & av['Mizerná'], kino['Průměr'])
    rule4 = FuzzyRule(filmy['Dobrá'] & (av['Dobrá'] | av['Vynikající']), kino['Dobré'])
    rule5 = FuzzyRule(filmy['Vynikající'] & ~av['Vynikající'], kino['Dobré'])
    rule6 = FuzzyRule(filmy['Vynikající'] & av['Vynikající'], kino['Paráda'])

    rules_list = [rule1, rule2, rule3, rule4, rule5, rule6]
    fuzzy_system = FuzzySystem(fuzzy_universe_list=[filmy, av, kino], rule_list=rules_list)

    fuzzy_system.add_user_input("Kvalita filmů", 7)
    fuzzy_system.add_user_input("Kvalita AV", 1)

    print(fuzzy_system.generate_centroid(kino, 10000, True))
