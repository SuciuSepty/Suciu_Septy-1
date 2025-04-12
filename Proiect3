import json
import random
from collections import Counter

def plural_leu(val):
    return "leu" if val == 1 else "lei"

def calculeaza_rest(rest, bancnote):
    dp = [None] * (rest + 1)
    dp[0] = {}

    for i in range(1, rest + 1):
        for bancnota in bancnote:
            val = bancnota['valoare']
            stoc = bancnota['stoc']
            if i >= val:
                for k in range(1, stoc + 1):
                    if i - k * val >= 0 and dp[i - k * val] is not None:
                        nou = dict(dp[i - k * val])
                        nou[val] = nou.get(val, 0) + k
                        if nou[val] <= bancnota['stoc']:
                            if dp[i] is None or sum(nou.values()) < sum(dp[i].values()):
                                dp[i] = nou
                    else:
                        break
    return dp[rest]

def simuleaza_casa(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    bancnote = data["bancnote"]
    produse = data["produse"]

    client_id = 1
    while True:
        nr_produse = random.randint(1, 4)
        produse_cumparate = [random.choice(produse) for _ in range(nr_produse)]
        total = sum(p['pret'] for p in produse_cumparate)
        plata = total + random.randint(1, 20)
        rest = plata - total

        # Grupare produse dupa nume
        produse_counter = Counter(p['nume'] for p in produse_cumparate)
        preturi_dict = {p['nume']: p['pret'] for p in produse}

        print(f"Clientul {client_id}:")
        for nume, cantitate in produse_counter.items():
            pret = preturi_dict[nume]
            if cantitate == 1:
                print(f"  - {nume} ({pret} lei)")
            else:
                print(f"  - {cantitate} x {nume} ({pret} lei fiecare)")
        print(f"  Total: {total} lei")
        print(f"  Suma platita: {plata} lei")
        print(f"  Rest de oferit: {rest} lei")

        solutie = calculeaza_rest(rest, bancnote)
        if solutie is None:
            print("  Nu se poate oferi restul. Simularea se opreste.")
            break
        else:
            print("  Rest oferit:")
            for val, cnt in sorted(solutie.items(), reverse=True):
                leu_label = plural_leu(val)
                if cnt == 1:
                    print(f"    1 x bancnota de {val} {leu_label}")
                else:
                    print(f"    {cnt} x bancnote de {val} {leu_label}")
                for b in bancnote:
                    if b['valoare'] == val:
                        b['stoc'] -= cnt
                        break
        print("-" * 40)
        client_id += 1

simuleaza_casa("date_magazin.json")
