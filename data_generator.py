import pandas as pd
import random

collaborations = []

types = [
    "Université",
    "Entreprise",
    "Institution",
    "Association"
]

statuts = [
    "Active",
    "En attente",
    "Terminée",
    "Suspendue"
]

for i in range(1, 3501):

    nb_reunions = random.randint(0, 20)

    mois_depuis_activite = random.randint(0, 24)

    budget = random.randint(
        50000,
        5000000
    )

    risque = 0

    if nb_reunions < 3:
        risque += 30

    if mois_depuis_activite > 12:
        risque += 40

    if budget > 3000000:
        risque += 20

    risque = min(risque, 100)

    collaboration = {

        "id": i,

        "nom": f"Partenaire_{i}",

        "type": random.choice(types),

        "responsable": f"Responsable_{random.randint(1,50)}",

        "budget": budget,

        "statut": random.choice(statuts),

        "nb_reunions": nb_reunions,

        "mois_depuis_activite": mois_depuis_activite,

        "risque": risque
    }

    collaborations.append(collaboration)

df = pd.DataFrame(collaborations)

df.to_csv(
    "collaborations.csv",
    index=False
)

print("3500 collaborations générées")