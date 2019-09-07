from common import Card, Deck, g_cards


def decode(deck_code):
    if deck_code == "":
        return Deck([])
    
    cards = []

    try:
        index_curr = 2  # skip "SP" prefix in every deck code

        for i in [1, 2, 3]:
            # get number of i-ofs (AA=0, AB=1, AC=2, ...)
            num_i_ofs = 26*(ord(deck_code[index_curr]) - ord("A")) + \
                ord(deck_code[index_curr + 1]) - ord("A")
            index_curr += 2

            for j in range(num_i_ofs):
                for k in range(i):
                    cards.append(g_cards[deck_code[index_curr:index_curr + 2]])
                index_curr += 2            

    except Exception as e:
        print("Deck code is invalid: \n{}\n".format(e))

    return Deck(cards)
