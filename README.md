# 📸 VS - Anti Shadow Ban pour Vinted

**VS** est une petite application codée en Python qui permet d’éviter le **shadow ban** ou le **rejet automatique** des annonces sur **Vinted**, lorsqu’on republie des articles avec **les mêmes photos**.

## 🛡️ Pourquoi l'utiliser ?

Lorsque tu repostes une annonce sur Vinted avec les **mêmes images**, l’algorithme de modération peut :
- détecter qu’il s’agit d’un **duplicata**,
- **masquer ton annonce** (shadow ban),
- ou même **supprimer la publication**.

**VS** règle ce problème en modifiant **très légèrement** les photos (rotation minime, recadrage subtil, bruit visuel imperceptible) afin de **tromper l’IA** de détection **tout en gardant la même apparence pour l'œil humain**.

## 🔧 Fonctionnement

1. Choisis un dossier contenant tes photos d’article.
2. L’application va générer plusieurs **variations très légères** de chaque photo.
3. Tu peux ensuite les réutiliser dans une nouvelle annonce Vinted **sans risquer d’être bloqué**.

## 🧠 Ce que l’appli fait techniquement :
- Rotation légère aléatoire
- Recadrage imperceptible
- Bruit subtil (pixels à peine modifiés)
- Ajustements de contraste/luminosité très fins
- Nom de fichier aléatoire

## 💻 Technologies

- Langage : Python 3.11
- Interface graphique : Tkinter
- Traitement d’images : Pillow, NumPy
- Emballée dans un `.exe` (aucune installation requise)

## 🚀 Utilisation

Télécharge le fichier `VS_Generator.exe`, double-clique, et utilise l’interface simple pour :
- Sélectionner tes images
- Choisir un dossier de sortie
- Générer automatiquement des variantes

---
