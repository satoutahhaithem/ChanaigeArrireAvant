file = open("base-de-regles.txt", "r")
rules = file.readlines()
cleaned_rules = []

# base_de_faits = ["pommes", "œufs", "abricots", "farine", "beurre", "sucre", "sel"]
# base_de_faits = ["B", "C"]
base_de_faits = ["E", "F"]

# Filtering out whitespace from input file
for rule in rules:
    cleaned_rules.append(rule.strip())


def get_premise_facts(rule):
    premise_start_position = 7
    premise_end_position = rule.find("ALORS")
    premise = rule[premise_start_position:premise_end_position]
    premise_facts = premise.replace(" ", "").split("ET")

    return premise_facts

def get_conclusion(rule):
    premise_end_position = rule.find("ALORS")
    conclusion = rule[premise_end_position + 6:].replace(" ", "")

    return conclusion

def avant(rules):
    rule_stack = []
    for rule in rules:
        premise_start_position = 7
        premise_end_position = rule.find("ALORS")
        premise = rule[premise_start_position:premise_end_position]
        premise_facts = premise.replace(" ", "").split("ET")
        conclusion = rule[premise_end_position + 6:].replace(" ", "")

        premise_fact_known = True
        for premise_fact in premise_facts:
            premise_fact_known = premise_fact in base_de_faits
            if not premise_fact_known:
                print(f"Fait inconnu dans {rule[:2]}: {premise_fact}")
                rule_stack.append(rule)
                break

        if premise_fact_known and conclusion not in base_de_faits:
            print(f"Le fait {conclusion} est demontré par la règle {rule[:2]}")
            base_de_faits.append(conclusion)

    for rule in reversed(rule_stack):
        premise_start_position = 7
        premise_end_position = rule.find("ALORS")
        premise = rule[premise_start_position:premise_end_position]
        premise_facts = premise.replace(" ", "").split("ET")
        conclusion = rule[premise_end_position + 6:].replace(" ", "")

        premise_fact_known = True
        for premise_fact in premise_facts:
            premise_fact_known = premise_fact in base_de_faits
            if not premise_fact_known:
                print(f"Fait inconnu dans {rule[:2]}: {premise_fact}")
                break

        if premise_fact_known and conclusion not in base_de_faits:
            print(f"Le fait {conclusion} est demontré par la règle {rule[:2]}")
            base_de_faits.append(conclusion)




    print("La nouvelle base de faits:", base_de_faits)


def clean_up(rules):
    new_rules = []
    premise_facts_set = set([])
    conclusions_set = set([])
    not_verified = set([])

    for rule in rules:
        premise_start_position = 7
        premise_end_position = rule.find("ALORS")
        premise = rule[premise_start_position:premise_end_position]
        premise_facts = premise.replace(" ", "").split("ET")
        conclusion = rule[premise_end_position + 6:].replace(" ", "")

        for premise_fact in premise_facts:
            premise_facts_set.add(premise_fact)
        conclusions_set.add(conclusion)


    for premise_fact in premise_facts_set:
        if premise_fact not in conclusions_set and premise_fact not in base_de_faits:
            not_verified.add(premise_fact)


    for rule in rules:
        premise_facts = get_premise_facts(rule)
        all_premise_facts_verified = True
        for premise_fact in premise_facts:
            if premise_fact in not_verified:
                all_premise_facts_verified = False
                break

        if all_premise_facts_verified:
            new_rules.append(rule)

    return new_rules


def get_rule_with_conclusion(rules, conclusion):
    for rule in rules:
        if conclusion == get_conclusion(rule):
            return rule


def arriere(rules, wanted_conclusion):
    new_rules = clean_up(rules)
    init_rule = get_rule_with_conclusion(new_rules, wanted_conclusion)
    rule_stack = [init_rule]

    rules_flow = []
    while rule_stack:
        premise_facts_verified = True
        premise_facts = get_premise_facts(rule_stack[-1])

        for premise_fact in premise_facts:
            if premise_fact not in base_de_faits:
                premise_facts_verified = False
                print("premise_fact", premise_fact)
                rule_stack.append(get_rule_with_conclusion(new_rules, premise_fact))
                break

        if premise_facts_verified:
            new_conclusion = get_conclusion(rule_stack[-1])
            base_de_faits.append(new_conclusion)
            print("new conclusion added:", new_conclusion, "from", rule_stack[-1][:2])
            rules_flow.append(rule_stack[-1][:2])
            rule_stack.pop()

    print(rules_flow)
    print("nouvelle base de faits", base_de_faits)


type_chainage = input("Quel type de chaı̂nage?\n")

if type_chainage == "avant":
    avant(cleaned_rules)
elif type_chainage == "arriere":
    wanted_conclusion = input("Quelle conclusion voulez vous?\n")
    arriere(cleaned_rules, wanted_conclusion)
else:
    print("type inconnu")
