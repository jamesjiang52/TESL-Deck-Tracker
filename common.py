import json
from PyQt5 import QtCore


g_colors_attribute = {
    "Strength": QtCore.Qt.red,
    "Intelligence": QtCore.Qt.blue,
    "Willpower": QtCore.Qt.yellow,
    "Agility": QtCore.Qt.darkGreen,
    "Endurance": QtCore.Qt.darkMagenta,
    "Neutral": QtCore.Qt.gray
}

g_colors_rarity = {
    "Common": QtCore.Qt.lightGray,
    "Rare": QtCore.Qt.blue,
    "Epic": QtCore.Qt.darkMagenta,
    "Legendary": QtCore.Qt.yellow
}


def get_color_from_attributes_single(attributes):
    return g_colors_attribute[attributes[0]]


def get_color_from_attributes_multiple(attributes):
    colors = [*map(lambda x: g_colors_attribute[x], attributes)]

    try:
        colors.remove(g_colors_attribute["Neutral"])
    except ValueError:
        pass

    if not len(colors):
        colors = [g_colors_attribute["Neutral"]]

    return colors


def get_rarity_color(rarity):
    return g_colors_rarity[rarity]


class Card:
    def __init__(
        self, *,
        name,
        cost,
        attributes,
        type,
        rarity,
        prophecy
    ):
        self.Name = name
        self.Cost = cost
        self.Attributes = attributes
        self.Type = type
        self.Rarity = rarity
        self.Prophecy = prophecy

    def __lt__(self, other):
        if self.Cost < other.Cost:
            return True
        elif self.Cost == other.Cost:
            return self.Name < other.Name
        else:
            return False

    def __eq__(self, other):
        return self.Name == other.Name

    
class Deck:
    def __init__(self, cards):
        self.Cards = sorted(cards)
        self.Counts = {}
        self.Attributes = set()

        for card in self.Cards:
            if card.Name not in self.Counts:
                self.Counts[card.Name] = 1
                for attribute in card.Attributes:
                    self.Attributes.add(attribute)
            else:
                self.Counts[card.Name] += 1

        self.__get_class()

        attributes = list(self.Attributes)
        self.Attributes = []
        for attribute in ["Strength", "Intelligence", "Willpower", "Agility", "Endurance"]:
            if attribute in attributes:
                self.Attributes.append(attribute)
        if not len(self.Attributes):
            self.Attributes = ["Neutral"]
        

    def __get_class(self):
        try:
            self.Attributes.remove("Neutral")
        except KeyError:
            pass

        if not len(self.Attributes):
            self.Class = "Mono-Neutral"

        elif self.Attributes == set(["Strength"]):
            self.Class = "Mono-Red"
        elif self.Attributes == set(["Intelligence"]):
            self.Class = "Mono-Blue"
        elif self.Attributes == set(["Willpower"]):
            self.Class = "Mono-Yellow"
        elif self.Attributes == set(["Agility"]):
            self.Class = "Mono-Green"
        elif self.Attributes == set(["Endurance"]):
            self.Class = "Mono-Purple"

        elif self.Attributes == set(["Strength", "Intelligence"]):
            self.Class = "Battlemage"
        elif self.Attributes == set(["Strength", "Willpower"]):
            self.Class = "Crusader"
        elif self.Attributes == set(["Strength", "Agility"]):
            self.Class = "Archer"
        elif self.Attributes == set(["Strength", "Endurance"]):
            self.Class = "Warrior"
        elif self.Attributes == set(["Intelligence", "Willpower"]):
            self.Class = "Mage"
        elif self.Attributes == set(["Intelligence", "Agility"]):
            self.Class = "Assassin"
        elif self.Attributes == set(["Intelligence", "Endurance"]):
            self.Class = "Sorceror"
        elif self.Attributes == set(["Willpower", "Agility"]):
            self.Class = "Monk"
        elif self.Attributes == set(["Willpower", "Endurance"]):
            self.Class = "Spellsword"
        elif self.Attributes == set(["Agility", "Endurance"]):
            self.Class = "Scout"

        elif self.Attributes == set(["Strength", "Intelligence", "Agility"]):
            self.Class = "House Dagoth"
        elif self.Attributes == set(["Strength", "Willpower", "Agility"]):
            self.Class = "House Hlaalu"
        elif self.Attributes == set(["Strength", "Willpower", "Endurance"]):
            self.Class = "House Redoran"
        elif self.Attributes == set(["Intelligence", "Willpower", "Endurance"]):
            self.Class = "Tribunal Temple"
        elif self.Attributes == set(["Intelligence", "Agility", "Endurance"]):
            self.Class = "House Telvanni"

        elif self.Attributes == set(["Strength", "Intelligence", "Willpower"]):
            self.Class = "The Guildsworn"
        elif self.Attributes == set(["Strength", "Intelligence", "Endurance"]):
            self.Class = "Daggerfall Covenant"
        elif self.Attributes == set(["Strength", "Agility", "Endurance"]):
            self.Class = "Ebonheart Pact"
        elif self.Attributes == set(["Intelligence", "Willpower", "Agility"]):
            self.Class = "Aldmeri Dominion"
        elif self.Attributes == set(["Willpower", "Agility", "Endurance"]):
            self.Class = "Empire of Cyrodiil"


g_cards = {}

with open("cards.json", "r") as f:
    __cards = json.load(f)
    for __card in __cards:
        g_cards[__card["code"]] = Card(
            name=__card["name"],
            cost=__card["cost"],
            attributes=__card["attributes"],
            type=__card["type"],
            rarity=__card["rarity"],
            prophecy=__card["prophecy"]
        )
