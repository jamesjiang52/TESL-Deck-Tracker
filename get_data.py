import json
from elderscrollslegendssdk import Card


with open("codes.json", "r") as f:
    __codes = json.load(f)

__card_ids = [*map(lambda x: x["id"], __codes)]

with open("cards.json", "w") as f:
    __cards = Card.all()
    cards_json_all = []
    for __card in __cards:
        try:
            cards_json_all.append({
                "code": __codes[__card_ids.index(__card.id)]["code"],
                "name": __card.name,
                "cost": __card.cost,
                "attributes": __card.attributes,
                "type": __card.type,
                "rarity": __card.rarity,
                "prophecy": "Prophecy" in __card.keywords
            })
        except ValueError as e:
            print(__card.name, e)
    json.dump(cards_json_all, f, indent=2)
