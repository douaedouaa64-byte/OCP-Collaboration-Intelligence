import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="OCP Collaboration Platform",
    page_icon="📊",
    layout="wide"
)
df = pd.read_csv("collaborations.csv")
st.title("📊 OCP Collaboration Intelligence Platform")

st.markdown("""
### Bienvenue

Cette plateforme permet :

- Gérer les collaborations
- Suivre les partenariats
- Détecter les collaborations à risque
- Générer des rapports RH
- Interagir avec un assistant IA
""")
actives = len(
    df[df["statut"] == "Active"]
)
en_attente = len(
    df[df["statut"] == "En attente"]
)

a_risque = len(
    df[df["risque"] >= 70]
)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
    "Collaborations",
    len(df)
)

with col2:
    st.metric(
    "Actives",
    actives
)
with col3:
    st.metric(
        "En attente",
        en_attente
    )

with col4:
    st.metric(
        "À risque",
        a_risque
    )
st.subheader("📋 Liste des collaborations")
st.subheader("🔎 Filtres")
type_counts = df["type"].value_counts()

fig = px.pie(
    values=type_counts.values,
    names=type_counts.index,
    title="Répartition des collaborations"
)

st.plotly_chart(fig)

type_selectionne = st.selectbox(
    "Type de partenariat",
    ["Tous"] + list(df["type"].unique())
)

if type_selectionne != "Tous":
    df_affiche = df[df["type"] == type_selectionne]
else:
    df_affiche = df
recherche = st.text_input(
    "🔍 Rechercher un partenaire"
)

if recherche:
    df_affiche = df_affiche[
        df_affiche["nom"].str.contains(
            recherche,
            case=False
        )
    ]
st.dataframe(df_affiche)
st.subheader("🚨 Top 10 collaborations les plus risquées")
st.subheader("📊 Répartition des niveaux de risque")

fig_risque = px.histogram(
    df,
    x="risque",
    nbins=20,
    title="Distribution des scores de risque"
)

st.plotly_chart(fig_risque)

top_risque = df.sort_values(
    by="risque",
    ascending=False
).head(10)

st.dataframe(top_risque)
st.dataframe(df)
# ================================================
# PHASE 1 — ANALYTICS AVANCÉS
# ================================================

st.markdown("---")
st.header("📊 Analytics avancés")

# --- Graphique 1 : Budget par type ---
st.subheader("💰 Budget total par type de partenariat")

budget_par_type = (
    df.groupby("type")["budget"]
    .sum()
    .reset_index()
    .sort_values("budget", ascending=False)
)

fig1 = px.bar(
    budget_par_type,
    x="type",
    y="budget",
    color="type",
    title="Budget total par type (DH)",
    labels={"budget": "Budget (DH)", "type": "Type"},
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(fig1, use_container_width=True)

# --- Graphique 2 : Top responsables par nombre de collaborations ---
st.subheader("👤 Top 10 responsables — Nombre de collaborations")

top_responsables = (
    df["responsable"]
    .value_counts()
    .head(10)
    .reset_index()
)
top_responsables.columns = ["responsable", "nb_collaborations"]

fig2 = px.bar(
    top_responsables,
    x="nb_collaborations",
    y="responsable",
    orientation="h",
    title="Top 10 responsables (nombre de collaborations)",
    color="nb_collaborations",
    color_continuous_scale="Blues"
)
fig2.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig2, use_container_width=True)

# --- Graphique 3 : Budget par responsable ---
st.subheader("💼 Top 10 responsables — Budget géré (DH)")

budget_par_resp = (
    df.groupby("responsable")["budget"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    budget_par_resp,
    x="budget",
    y="responsable",
    orientation="h",
    title="Top 10 responsables par budget total géré",
    color="budget",
    color_continuous_scale="Greens"
)
fig3.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig3, use_container_width=True)

# --- Graphique 4 : Risque moyen par type ET par statut ---
st.subheader("🚨 Risque moyen par type de partenariat")

col_g1, col_g2 = st.columns(2)

with col_g1:
    risque_par_type = (
        df.groupby("type")["risque"]
        .mean()
        .round(1)
        .sort_values(ascending=False)
        .reset_index()
    )
    fig4 = px.bar(
        risque_par_type,
        x="type",
        y="risque",
        color="risque",
        color_continuous_scale="Reds",
        title="Score de risque moyen par type",
        labels={"risque": "Risque moyen"}
    )
    st.plotly_chart(fig4, use_container_width=True)

with col_g2:
    risque_par_statut = (
        df.groupby("statut")["risque"]
        .mean()
        .round(1)
        .sort_values(ascending=False)
        .reset_index()
    )
    fig5 = px.bar(
        risque_par_statut,
        x="statut",
        y="risque",
        color="risque",
        color_continuous_scale="Oranges",
        title="Score de risque moyen par statut",
        labels={"risque": "Risque moyen"}
    )
    st.plotly_chart(fig5, use_container_width=True)
    # ================================================
# PHASE 2 — ALERT CENTER
# ================================================

st.markdown("---")
st.header("🚨 Alert Center — Collaborations critiques")

# --- Calculs des alertes ---
critiques = df[df["risque"] >= 70]
nb_critiques = len(critiques)
budget_expose = critiques["budget"].sum()
nb_inactives = len(df[df["mois_depuis_activite"] > 12])
nb_sans_reunions = len(df[df["nb_reunions"] < 3])

# --- Bloc d'alerte principal ---
if nb_critiques > 0:
    st.error(f"""
    ⚠️ ALERTE CRITIQUE
    
    {nb_critiques} collaborations sont en état de risque élevé (score ≥ 70)
    Budget total exposé : {budget_expose:,.0f} DH
    """)
else:
    st.success("✅ Aucune collaboration en état critique actuellement.")

# --- KPIs d'alerte en colonnes ---
st.subheader("📊 Indicateurs de risque")

col_a1, col_a2, col_a3 = st.columns(3)

with col_a1:
    st.metric(
        label="🔴 Collaborations critiques",
        value=nb_critiques,
        delta=f"{round(nb_critiques / len(df) * 100, 1)}% du total",
        delta_color="inverse"
    )

with col_a2:
    st.metric(
        label="💸 Budget exposé (DH)",
        value=f"{budget_expose:,.0f}",
        delta="Score risque ≥ 70",
        delta_color="inverse"
    )

with col_a3:
    st.metric(
        label="😴 Partenariats inactifs",
        value=nb_inactives,
        delta="> 12 mois sans activité",
        delta_color="inverse"
    )

# --- Tableau des collaborations critiques ---
st.subheader("📋 Liste des collaborations critiques")

colonnes_affichees = ["nom", "type", "responsable", "budget", "statut", "nb_reunions", "mois_depuis_activite", "risque"]
critiques_affiches = critiques[colonnes_affichees].sort_values("risque", ascending=False)

st.dataframe(
    critiques_affiches.style.background_gradient(subset=["risque"], cmap="Reds"),
    use_container_width=True
)

# --- Recommandations automatiques ---
st.subheader("💡 Recommandations automatiques")

for _, row in critiques.head(5).iterrows():
    with st.expander(f"⚠️ {row['nom']} — Score : {row['risque']}/100"):

        recommandations = []

        if row["nb_reunions"] < 3:
            recommandations.append("📅 Planifier une réunion de suivi urgente — moins de 3 réunions enregistrées.")

        if row["mois_depuis_activite"] > 12:
            recommandations.append(f"⏰ Relancer le partenariat — {row['mois_depuis_activite']} mois d'inactivité.")

        if row["budget"] > 2000000:
            recommandations.append(f"💰 Audit budgétaire recommandé — {row['budget']:,.0f} DH exposés.")

        if row["statut"] in ["Suspendue", "En attente"]:
            recommandations.append(f"📌 Statut '{row['statut']}' à clarifier avec le responsable {row['responsable']}.")

        for rec in recommandations:
            st.warning(rec)

# --- Graphique : Distribution des scores de risque ---
st.subheader("📈 Distribution des scores de risque")

fig_dist = px.histogram(
    df,
    x="risque",
    nbins=20,
    color_discrete_sequence=["#E74C3C"],
    title="Distribution des scores de risque sur l'ensemble des collaborations",
    labels={"risque": "Score de risque", "count": "Nombre de collaborations"}
)
fig_dist.add_vline(
    x=70,
    line_dash="dash",
    line_color="darkred",
    annotation_text="Seuil critique (70)",
    annotation_position="top right"
)
st.plotly_chart(fig_dist, use_container_width=True)
# ================================================
# PHASE 3 — MACHINE LEARNING PRÉDICTIF
# ================================================

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

st.markdown("---")
st.header("🤖 Machine Learning — Prédiction des risques")

st.info("""
ℹ️ Ce module utilise un modèle **Random Forest** entraîné sur les données OCP
pour prédire si une collaboration est à risque élevé ou non.
""")

# --- Préparation des données ---
# On sélectionne les features (variables d'entrée)
features = ["nb_reunions", "mois_depuis_activite", "budget"]

# On crée la target : 1 = risque élevé (>= 70), 0 = risque normal
df["risque_critique"] = (df["risque"] >= 70).astype(int)

X = df[features]           # Les features — ce que le modèle analyse
y = df["risque_critique"]  # La target — ce qu'il doit prédire

# --- Train/Test Split ---
# 80% pour entraîner, 20% pour tester
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,       # 20% pour le test
    random_state=42      # Pour avoir les mêmes résultats à chaque fois
)

# --- Entraînement du modèle ---
modele = RandomForestClassifier(
    n_estimators=100,    # 100 arbres de décision
    random_state=42
)
modele.fit(X_train, y_train)  # Le modèle apprend

# --- Évaluation ---
y_pred = modele.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# --- Affichage des métriques ---
st.subheader("📊 Performance du modèle")

col_m1, col_m2, col_m3 = st.columns(3)

with col_m1:
    st.metric(
        label="🎯 Accuracy",
        value=f"{accuracy * 100:.1f}%",
        delta="sur le test set"
    )

with col_m2:
    st.metric(
        label="🌲 Arbres construits",
        value="100",
        delta="Random Forest"
    )

with col_m3:
    st.metric(
        label="📚 Données d'entraînement",
        value=f"{len(X_train)}",
        delta=f"{len(X_test)} pour le test"
    )

# --- Feature Importance ---
st.subheader("🔍 Feature Importance — Quelles variables influencent le risque ?")

importances = modele.feature_importances_
feature_importance_df = pd.DataFrame({
    "feature": features,
    "importance": importances
}).sort_values("importance", ascending=False)

fig_fi = px.bar(
    feature_importance_df,
    x="importance",
    y="feature",
    orientation="h",
    color="importance",
    color_continuous_scale="Purples",
    title="Importance de chaque variable dans la prédiction du risque",
    labels={"importance": "Importance", "feature": "Variable"}
)
fig_fi.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig_fi, use_container_width=True)

st.caption("""
💡 Plus une variable a une importance élevée, plus elle influence la décision du modèle.
Une importance de 0.6 signifie que cette variable explique 60% des décisions.
""")

# --- Prédictions sur toutes les collaborations ---
st.subheader("🔮 Prédictions IA sur toutes les collaborations")

# Le modèle prédit sur tout le dataset
df["prediction_risque"] = modele.predict(X)
df["probabilite_risque"] = modele.predict_proba(X)[:, 1]  # Probabilité entre 0 et 1

# Affichage des colonnes pertinentes
df_predictions = df[["nom", "type", "responsable", "budget", "risque", "probabilite_risque"]].copy()
df_predictions["probabilite_risque"] = (df_predictions["probabilite_risque"] * 100).round(1)
df_predictions = df_predictions.sort_values("probabilite_risque", ascending=False)
df_predictions.columns = ["Partenaire", "Type", "Responsable", "Budget (DH)", "Score règles", "Probabilité IA (%)"]

st.dataframe(df_predictions.head(20), use_container_width=True)

# --- Simulateur What-If ---
st.subheader("🧪 Simulateur What-If — Testez un scénario")

st.markdown("""
Modifiez les paramètres ci-dessous et l'IA prédit **instantanément** le niveau de risque.
""")

col_s1, col_s2, col_s3 = st.columns(3)

with col_s1:
    sim_reunions = st.slider(
        "📅 Nombre de réunions",
        min_value=0,
        max_value=20,
        value=5
    )

with col_s2:
    sim_inactivite = st.slider(
        "⏰ Mois d'inactivité",
        min_value=0,
        max_value=24,
        value=6
    )

with col_s3:
    sim_budget = st.number_input(
        "💰 Budget (DH)",
        min_value=50000,
        max_value=5000000,
        value=1000000,
        step=100000
    )

# Prédiction en temps réel
donnees_simulation = pd.DataFrame({
    "nb_reunions": [sim_reunions],
    "mois_depuis_activite": [sim_inactivite],
    "budget": [sim_budget]
})

probabilite = modele.predict_proba(donnees_simulation)[0][1]
prediction = modele.predict(donnees_simulation)[0]

# Affichage du résultat
st.markdown("### Résultat de la prédiction IA")

if prediction == 1:
    st.error(f"""
    🔴 RISQUE ÉLEVÉ — Probabilité : {probabilite * 100:.1f}%

    Ce partenariat présente un risque critique selon le modèle Random Forest.
    Une intervention est recommandée.
    """)
else:
    st.success(f"""
    🟢 RISQUE FAIBLE — Probabilité de risque : {probabilite * 100:.1f}%

    Ce partenariat ne présente pas de risque critique selon le modèle.
    """)

# Barre de progression visuelle
st.progress(probabilite)
st.caption(f"Probabilité de risque élevé : {probabilite * 100:.1f}%")
# ================================================
# PHASE 4 — ASSISTANT IA CONVERSATIONNEL
# ================================================

from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()  # Charge les variables du fichier .env

st.markdown("---")
st.header("🤖 Assistant IA — OCP Collaboration Intelligence")

st.info("""
💬 Posez vos questions sur les collaborations OCP en langage naturel.
L'assistant connaît toutes vos données en temps réel.
""")

# --- Préparation du contexte des données pour l'IA ---
nb_total = len(df)
nb_actives = len(df[df["statut"] == "Active"])
nb_critiques = len(df[df["risque"] >= 70])
budget_total = df["budget"].sum()
budget_expose = df[df["risque"] >= 70]["budget"].sum()
top_responsable = df["responsable"].value_counts().idxmax()
top_budget_resp = df.groupby("responsable")["budget"].sum().idxmax()
type_plus_risque = df.groupby("type")["risque"].mean().idxmax()

contexte_donnees = f"""
Tu es un assistant IA expert en analyse de collaborations pour OCP (Office Chérifien des Phosphates).
Tu as accès aux données en temps réel de la plateforme OCP Collaboration Intelligence.

DONNÉES ACTUELLES :
- Total collaborations : {nb_total}
- Collaborations actives : {nb_actives}
- Collaborations critiques (risque ≥ 70) : {nb_critiques}
- Budget total géré : {budget_total:,.0f} DH
- Budget exposé (collaborations critiques) : {budget_expose:,.0f} DH
- Responsable avec le plus de collaborations : {top_responsable}
- Responsable gérant le plus grand budget : {top_budget_resp}
- Type de partenariat le plus risqué en moyenne : {type_plus_risque}

TOP 5 COLLABORATIONS LES PLUS RISQUÉES :
{df.nlargest(5, 'risque')[['nom', 'type', 'responsable', 'budget', 'risque']].to_string(index=False)}

RÉPARTITION PAR TYPE :
{df['type'].value_counts().to_string()}

RÉPARTITION PAR STATUT :
{df['statut'].value_counts().to_string()}

Réponds toujours en français, de manière professionnelle et concise.
Base tes réponses uniquement sur les données fournies ci-dessus.
Si on te pose une question hors contexte OCP, redirige poliment vers les données disponibles.
"""

# --- Initialisation de l'historique de conversation ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Affichage de l'historique ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Questions suggérées ---
if len(st.session_state.messages) == 0:
    st.markdown("**💡 Questions suggérées :**")
    col_q1, col_q2 = st.columns(2)

    with col_q1:
        if st.button("🔴 Combien de collaborations sont critiques ?"):
            st.session_state.messages.append({
                "role": "user",
                "content": "Combien de collaborations sont critiques et quel est le budget exposé ?"
            })
            st.rerun()

        if st.button("👤 Quel responsable gère le plus de budget ?"):
            st.session_state.messages.append({
                "role": "user",
                "content": "Quel responsable gère le plus grand budget total ?"
            })
            st.rerun()

    with col_q2:
        if st.button("📊 Quel type de partenariat est le plus risqué ?"):
            st.session_state.messages.append({
                "role": "user",
                "content": "Quel type de partenariat présente le risque moyen le plus élevé ?"
            })
            st.rerun()

        if st.button("💰 Quel est le budget total géré ?"):
            st.session_state.messages.append({
                "role": "user",
                "content": "Quel est le budget total géré par la plateforme OCP ?"
            })
            st.rerun()

# --- Input utilisateur ---
question = st.chat_input("Posez votre question sur les collaborations OCP...")

if question:
    # Ajouter la question à l'historique
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })
    with st.chat_message("user"):
        st.markdown(question)

    # --- Appel à l'API Groq ---
    with st.chat_message("assistant"):
        with st.spinner("L'IA analyse vos données..."):
            try:
               client = Groq(api_key=os.getenv("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"))
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",  # Llama 3 70B — le plus puissant de Groq
                    messages=[
                        {"role": "system", "content": contexte_donnees},
                        *[{"role": m["role"], "content": m["content"]}
                          for m in st.session_state.messages]
                    ],
                    temperature=0.3,   # Bas = réponses précises et factuelles
                    max_tokens=500     # Réponses concises
                )

                reponse_ia = response.choices[0].message.content
                st.markdown(reponse_ia)

                # Ajouter la réponse à l'historique
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reponse_ia
                })

            except Exception as e:
                st.error(f"Erreur de connexion à l'API : {str(e)}")

# --- Bouton pour effacer la conversation ---
if len(st.session_state.messages) > 0:
    if st.button("🗑️ Effacer la conversation"):
        st.session_state.messages = []
        st.rerun()
# ================================================
# PHASE 5 — RAPPORT PDF PERSONNALISABLE + SQLite
# ================================================

import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import cm
import io
from datetime import datetime

st.markdown("---")
st.header("📄 Rapport PDF Personnalisable + Base de données SQL")

# ================================================
# PARTIE 1 — RAPPORT PDF PERSONNALISABLE
# ================================================

st.subheader("⚙️ Personnaliser votre rapport")

# --- APPARENCE ---
st.markdown("#### 🎨 Apparence du rapport")
col_app1, col_app2 = st.columns(2)

with col_app1:
    titre_rapport = st.text_input(
        "Titre du rapport",
        value="Rapport RH — Analyse des Collaborations OCP"
    )

with col_app2:
    editeur_rapport = st.text_input(
        "Nom de l'éditeur / département",
        value="Direction des Ressources Humaines — OCP"
    )

# --- FILTRES DES DONNÉES ---
st.markdown("#### 🔍 Filtrer les données du rapport")
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    # Filtre par type de partenariat
    types_disponibles = ["Tous"] + list(df["type"].unique())
    type_choisi = st.selectbox("Type de partenariat", types_disponibles, key="pdf_type")

with col_f2:
    # Filtre par responsable
    responsables_disponibles = ["Tous"] + sorted(df["responsable"].unique().tolist())
    responsable_choisi = st.selectbox("Responsable RH", responsables_disponibles, key="pdf_responsable")

with col_f3:
    # Seuil de risque personnalisable
    seuil_risque = st.slider(
        "Seuil de risque critique",
        min_value=0,
        max_value=100,
        value=70,
        step=5,
        help="Les collaborations avec un score >= ce seuil seront considérées critiques"
    )

# --- PÉRIODE ---
st.markdown("#### 📅 Période du rapport")
col_d1, col_d2 = st.columns(2)

with col_d1:
    date_debut = st.date_input("Date de début", value=datetime(2024, 1, 1))

with col_d2:
    date_fin = st.date_input("Date de fin", value=datetime.now())

# --- SECTIONS À INCLURE ---
st.markdown("#### 📋 Sections à inclure dans le rapport")
col_s1, col_s2, col_s3 = st.columns(3)

with col_s1:
    inclure_kpis = st.checkbox("✅ KPIs & indicateurs", value=True)
    inclure_top10 = st.checkbox("🔴 Top collaborations risquées", value=True)

with col_s2:
    inclure_repartition = st.checkbox("📊 Répartition par type", value=True)
    inclure_responsables = st.checkbox("👤 Analyse par responsable", value=True)

with col_s3:
    inclure_recommandations = st.checkbox("💡 Recommandations RH", value=True)
    inclure_liste_complete = st.checkbox("📋 Liste complète filtrée", value=False)

# --- Nombre de collaborations dans le Top ---
nb_top = st.slider("Nombre de collaborations dans le Top risques", 5, 20, 10)

# --- Aperçu des données filtrées ---
st.markdown("#### 👁️ Aperçu des données qui seront dans le rapport")

df_rapport = df.copy()
if type_choisi != "Tous":
    df_rapport = df_rapport[df_rapport["type"] == type_choisi]
if responsable_choisi != "Tous":
    df_rapport = df_rapport[df_rapport["responsable"] == responsable_choisi]

col_prev1, col_prev2, col_prev3 = st.columns(3)
with col_prev1:
    st.metric("Total collaborations filtrées", len(df_rapport))
with col_prev2:
    st.metric("Collaborations critiques", len(df_rapport[df_rapport["risque"] >= seuil_risque]))
with col_prev3:
    st.metric("Budget total filtré", f"{df_rapport['budget'].sum():,.0f} DH")

# ================================================
# FONCTION GÉNÉRATION PDF PERSONNALISABLE
# ================================================

def generer_rapport_pdf_perso(df_r, titre, editeur, seuil, nb_top_risques,
                               date_deb, date_fin,
                               inc_kpis, inc_top, inc_repartition,
                               inc_responsables, inc_recommandations, inc_liste):

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    elements = []

    style_titre = ParagraphStyle("titre", parent=styles["Title"],
        fontSize=20, textColor=colors.HexColor("#1B4F72"), spaceAfter=8)
    style_sous_titre = ParagraphStyle("sous_titre", parent=styles["Normal"],
        fontSize=11, textColor=colors.HexColor("#2E86C1"), spaceAfter=6)
    style_section = ParagraphStyle("section", parent=styles["Heading2"],
        fontSize=13, textColor=colors.HexColor("#1B4F72"), spaceBefore=12, spaceAfter=6)
    style_normal = ParagraphStyle("normal", parent=styles["Normal"],
        fontSize=9, spaceAfter=5)
    style_footer = ParagraphStyle("footer", parent=styles["Normal"],
        fontSize=8, textColor=colors.grey, alignment=1)

    def ligne_separation(couleur="#2E86C1", epaisseur=1.5):
        return Table([[""]],colWidths=[17*cm],
            style=TableStyle([("LINEABOVE",(0,0),(-1,-1),epaisseur,colors.HexColor(couleur))]))

    # ---- EN-TÊTE ----
    elements.append(Paragraph(titre, style_titre))
    elements.append(Paragraph(editeur, style_sous_titre))
    elements.append(Paragraph(
        f"Période : {date_deb.strftime('%d/%m/%Y')} — {date_fin.strftime('%d/%m/%Y')} | "
        f"Généré le : {datetime.now().strftime('%d/%m/%Y à %H:%M')} | "
        f"Seuil de risque : {seuil}/100",
        style_normal
    ))
    elements.append(Spacer(1, 0.3*cm))
    elements.append(ligne_separation())
    elements.append(Spacer(1, 0.4*cm))

    nb_total = len(df_r)
    if nb_total == 0:
        elements.append(Paragraph("Aucune donnée pour les filtres sélectionnés.", style_normal))
        doc.build(elements)
        buffer.seek(0)
        return buffer

    nb_critiques = len(df_r[df_r["risque"] >= seuil])
    budget_total = df_r["budget"].sum()
    budget_expose = df_r[df_r["risque"] >= seuil]["budget"].sum()

    # ---- SECTION KPIs ----
    if inc_kpis:
        elements.append(Paragraph("1. Indicateurs Clés de Performance", style_section))
        kpi_data = [
            ["Indicateur", "Valeur", "Analyse"],
            ["Total collaborations analysées", f"{nb_total}", "Périmètre du rapport"],
            ["Collaborations actives", f"{len(df_r[df_r['statut']=='Active'])}", f"{round(len(df_r[df_r['statut']=='Active'])/nb_total*100,1)}% du total"],
            ["Collaborations en attente", f"{len(df_r[df_r['statut']=='En attente'])}", f"{round(len(df_r[df_r['statut']=='En attente'])/nb_total*100,1)}% du total"],
            [f"Collaborations critiques (≥{seuil})", f"{nb_critiques}", f"{round(nb_critiques/nb_total*100,1)}% du total"],
            ["Budget total géré", f"{budget_total:,.0f} DH", "Portefeuille analysé"],
            ["Budget exposé", f"{budget_expose:,.0f} DH", f"{round(budget_expose/budget_total*100,1) if budget_total>0 else 0}% du budget total"],
        ]
        t = Table(kpi_data, colWidths=[7*cm, 4*cm, 6*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1B4F72")),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
            ("FONTSIZE",(0,0),(-1,0),10),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#EBF5FB"),colors.white]),
            ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#AED6F1")),
            ("FONTSIZE",(0,1),(-1,-1),9),
            ("TOPPADDING",(0,0),(-1,-1),5),
            ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.4*cm))

    # ---- SECTION TOP RISQUES ----
    if inc_top:
        elements.append(Paragraph(f"2. Top {nb_top_risques} Collaborations les Plus Risquées (seuil ≥ {seuil})", style_section))
        top_df = df_r.nlargest(nb_top_risques, "risque")[["nom","type","responsable","budget","statut","risque"]]
        top_data = [["Partenaire","Type","Responsable","Budget (DH)","Statut","Risque"]]
        for _, row in top_df.iterrows():
            top_data.append([str(row["nom"]), str(row["type"]), str(row["responsable"]),
                             f"{row['budget']:,.0f}", str(row["statut"]), f"{row['risque']}/100"])
        t2 = Table(top_data, colWidths=[3.5*cm,2.5*cm,3*cm,2.5*cm,2.5*cm,1.5*cm])
        t2.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#C0392B")),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
            ("FONTSIZE",(0,0),(-1,0),9),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#FDEDEC"),colors.white]),
            ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#F1948A")),
            ("FONTSIZE",(0,1),(-1,-1),8),
            ("TOPPADDING",(0,0),(-1,-1),4),
            ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ]))
        elements.append(t2)
        elements.append(Spacer(1, 0.4*cm))

    # ---- SECTION RÉPARTITION PAR TYPE ----
    if inc_repartition:
        elements.append(Paragraph("3. Répartition par Type de Partenariat", style_section))
        repartition = df_r.groupby("type").agg(
            nb=("nom","count"),
            budget=("budget","sum"),
            risque_moyen=("risque","mean")
        ).reset_index()
        rep_data = [["Type","Nb collaborations","Budget total (DH)","Risque moyen"]]
        for _, row in repartition.iterrows():
            rep_data.append([str(row["type"]), str(int(row["nb"])),
                            f"{row['budget']:,.0f}", f"{row['risque_moyen']:.1f}/100"])
        t3 = Table(rep_data, colWidths=[4*cm,4*cm,5*cm,4*cm])
        t3.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1B4F72")),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
            ("FONTSIZE",(0,0),(-1,0),10),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#EBF5FB"),colors.white]),
            ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#AED6F1")),
            ("FONTSIZE",(0,1),(-1,-1),9),
            ("TOPPADDING",(0,0),(-1,-1),5),
            ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ]))
        elements.append(t3)
        elements.append(Spacer(1, 0.4*cm))

    # ---- SECTION RESPONSABLES ----
    if inc_responsables:
        elements.append(Paragraph("4. Analyse par Responsable RH (Top 10)", style_section))
        resp_df = df_r.groupby("responsable").agg(
            nb=("nom","count"),
            budget=("budget","sum"),
            risque_moyen=("risque","mean")
        ).sort_values("budget", ascending=False).head(10).reset_index()
        resp_data = [["Responsable","Nb collaborations","Budget géré (DH)","Risque moyen"]]
        for _, row in resp_df.iterrows():
            resp_data.append([str(row["responsable"]), str(int(row["nb"])),
                             f"{row['budget']:,.0f}", f"{row['risque_moyen']:.1f}/100"])
        t4 = Table(resp_data, colWidths=[4*cm,4*cm,5*cm,4*cm])
        t4.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1B4F72")),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
            ("FONTSIZE",(0,0),(-1,0),10),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#EBF5FB"),colors.white]),
            ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#AED6F1")),
            ("FONTSIZE",(0,1),(-1,-1),9),
            ("TOPPADDING",(0,0),(-1,-1),5),
            ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ]))
        elements.append(t4)
        elements.append(Spacer(1, 0.4*cm))

    # ---- SECTION RECOMMANDATIONS ----
    if inc_recommandations:
        elements.append(Paragraph("5. Recommandations RH", style_section))
        recs = [
            f"• <b>{nb_critiques} collaborations</b> dépassent le seuil de risque fixé à {seuil}/100 — intervention urgente requise.",
            f"• Budget exposé : <b>{budget_expose:,.0f} DH</b> ({round(budget_expose/budget_total*100,1) if budget_total>0 else 0}% du portefeuille analysé).",
            "• Planifier des réunions de suivi pour tous les partenariats avec moins de 3 réunions enregistrées.",
            "• Relancer les partenariats inactifs depuis plus de 12 mois avec un plan d'action concret.",
            "• Effectuer un audit budgétaire pour les collaborations dont le budget dépasse 2 000 000 DH.",
            f"• Concentrer les efforts RH sur le type '{df_r.groupby('type')['risque'].mean().idxmax()}' — risque moyen le plus élevé.",
        ]
        for rec in recs:
            elements.append(Paragraph(rec, style_normal))
        elements.append(Spacer(1, 0.4*cm))

    # ---- SECTION LISTE COMPLÈTE ----
    if inc_liste:
        elements.append(Paragraph("6. Liste complète des collaborations filtrées", style_section))
        liste_df = df_r[["nom","type","responsable","budget","statut","risque"]].sort_values("risque", ascending=False)
        liste_data = [["Partenaire","Type","Responsable","Budget (DH)","Statut","Risque"]]
        for _, row in liste_df.iterrows():
            liste_data.append([str(row["nom"]), str(row["type"]), str(row["responsable"]),
                              f"{row['budget']:,.0f}", str(row["statut"]), f"{row['risque']}/100"])
        t5 = Table(liste_data, colWidths=[3.5*cm,2.5*cm,3*cm,2.5*cm,2.5*cm,1.5*cm])
        t5.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1B4F72")),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
            ("FONTSIZE",(0,0),(-1,0),9),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#EBF5FB"),colors.white]),
            ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#AED6F1")),
            ("FONTSIZE",(0,1),(-1,-1),7),
            ("TOPPADDING",(0,0),(-1,-1),3),
            ("BOTTOMPADDING",(0,0),(-1,-1),3),
        ]))
        elements.append(t5)

    # ---- PIED DE PAGE ----
    elements.append(Spacer(1, 0.5*cm))
    elements.append(ligne_separation(couleur="#AED6F1", epaisseur=1))
    elements.append(Spacer(1, 0.2*cm))
    elements.append(Paragraph(
        f"Document confidentiel — {editeur} — OCP Collaboration Intelligence Platform — Généré automatiquement",
        style_footer
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer

# --- Bouton de génération ---
st.markdown("---")
col_gen1, col_gen2 = st.columns([1, 2])

with col_gen1:
    generer = st.button("📥 Générer mon rapport PDF", type="primary", use_container_width=True)

with col_gen2:
    sections_selectionnees = []
    if inclure_kpis: sections_selectionnees.append("KPIs")
    if inclure_top10: sections_selectionnees.append(f"Top {nb_top} risques")
    if inclure_repartition: sections_selectionnees.append("Répartition")
    if inclure_responsables: sections_selectionnees.append("Responsables")
    if inclure_recommandations: sections_selectionnees.append("Recommandations")
    if inclure_liste_complete: sections_selectionnees.append("Liste complète")
    st.info(f"**Rapport actuel :** {len(df_rapport)} collaborations | Sections : {', '.join(sections_selectionnees) if sections_selectionnees else 'Aucune sélectionnée'}")

if generer:
    if not any([inclure_kpis, inclure_top10, inclure_repartition, inclure_responsables, inclure_recommandations, inclure_liste_complete]):
        st.warning("⚠️ Sélectionnez au moins une section à inclure dans le rapport.")
    else:
        with st.spinner("Génération du rapport personnalisé en cours..."):
            pdf_buffer = generer_rapport_pdf_perso(
                df_rapport, titre_rapport, editeur_rapport,
                seuil_risque, nb_top, date_debut, date_fin,
                inclure_kpis, inclure_top10, inclure_repartition,
                inclure_responsables, inclure_recommandations, inclure_liste_complete
            )
            nom_fichier = f"rapport_OCP_{type_choisi}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
            st.download_button(
                label="⬇️ Télécharger votre rapport personnalisé",
                data=pdf_buffer,
                file_name=nom_fichier,
                mime="application/pdf",
                use_container_width=True
            )
        st.success(f"✅ Rapport '{titre_rapport}' généré avec succès !")

# ================================================
# PARTIE 2 — BASE DE DONNÉES SQLite
# ================================================

st.markdown("---")
st.subheader("🗄️ Base de données SQL — SQLite")

st.info("ℹ️ Migration des données CSV vers une vraie base de données relationnelle SQLite.")

def creer_base_sqlite(df):
    conn = sqlite3.connect("ocp_collaborations.db")
    df.to_sql("collaborations", conn, if_exists="replace", index=False)
    conn.close()

def requete_sql(query):
    conn = sqlite3.connect("ocp_collaborations.db")
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result

if st.button("🗄️ Créer la base de données SQLite"):
    with st.spinner("Migration en cours..."):
        creer_base_sqlite(df)
    st.success("✅ Base SQLite créée — fichier : ocp_collaborations.db")

st.subheader("🔍 Requêtes SQL en temps réel")

requetes_exemples = {
    "Top 5 collaborations risquées": "SELECT nom, type, responsable, budget, risque FROM collaborations ORDER BY risque DESC LIMIT 5",
    "Budget total par type": "SELECT type, SUM(budget) as budget_total FROM collaborations GROUP BY type ORDER BY budget_total DESC",
    "Collaborations critiques (risque ≥ 70)": "SELECT nom, responsable, budget, risque FROM collaborations WHERE risque >= 70 ORDER BY risque DESC",
    "Nombre par statut": "SELECT statut, COUNT(*) as nombre FROM collaborations GROUP BY statut",
    "Top 5 responsables par budget": "SELECT responsable, SUM(budget) as budget_total, COUNT(*) as nb FROM collaborations GROUP BY responsable ORDER BY budget_total DESC LIMIT 5",
}

requete_choisie = st.selectbox("Choisir une requête exemple", list(requetes_exemples.keys()), key="sql_requete")
requete_sql_input = st.text_area("📝 Ou écrivez votre propre requête SQL :", value=requetes_exemples[requete_choisie], height=80)

if st.button("▶️ Exécuter la requête SQL"):
    try:
        creer_base_sqlite(df)
        resultat = requete_sql(requete_sql_input)
        st.success(f"✅ {len(resultat)} résultats trouvés")
        st.dataframe(resultat, use_container_width=True)
    except Exception as e:
        st.error(f"Erreur SQL : {str(e)}")
