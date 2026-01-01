# 🚀 Guide d'Installation et d'Utilisation

## 📋 Table des Matières
1. [Prérequis](#prérequis)
2. [Choix de la Configuration](#choix-de-la-configuration)
3. [Installation](#installation)
4. [Lancement de l'Application](#lancement)
5. [Utilisation](#utilisation)
6. [Dépannage](#dépannage)

---

## 🔧 Prérequis

Avant de commencer, assurez-vous d'avoir:

### **Obligatoire:**
- ✅ **Python 3.8 ou supérieur**
  - Télécharger sur: https://python.org
  - Vérifier: Ouvrir un terminal et taper `python --version`

### **Recommandé:**
- ✅ **Git** (pour une meilleure compatibilité Real-ESRGAN)
  - Télécharger sur: https://git-scm.com/
  - Vérifier: Taper `git --version` dans un terminal

### **Système:**
- **OS:** Windows 10/11, macOS, ou Linux
- **RAM:** 4 GB minimum (8 GB recommandé)
- **Espace disque:** 2-4 GB pour les dépendances
- **Internet:** Requis pour l'installation initiale

---

## ⚡ Choix de la Configuration

Deux versions d'installation sont disponibles selon votre matériel:

### **📊 Comparaison des Configurations:**

| Critère | Version CPU | Version GPU |
|---------|-------------|-------------|
| **Fichier de setup** | `setup_cpu.bat` | `setup_gpu.bat` |
| **Fonctionne sur** | Tous les ordinateurs | NVIDIA GPU uniquement |
| **Téléchargement** | ~500 MB | ~3 GB |
| **Temps d'installation** | 5-8 minutes | 8-12 minutes |
| **Vitesse de traitement** | 15-30 secondes | 8-12 secondes |
| **Qualité des résultats** | Identique | Identique |
| **Recommandé pour** | Compatibilité maximale | Performance maximale |

---

### **🤔 Comment Choisir?**

#### **Utilisez `setup_cpu.bat` si:**
- ❓ Vous n'êtes pas sûr de votre configuration
- 💻 Vous avez un ordinateur portable sans carte graphique dédiée
- 🍎 Vous utilisez un Mac
- 🔵 Vous avez une carte graphique AMD ou Intel
- ✅ Vous voulez la solution la plus simple et garantie

**→ C'est le choix par défaut et recommandé**

---

#### **Utilisez `setup_gpu.bat` si:**
- 🎮 Vous avez une carte graphique NVIDIA (GeForce GTX/RTX)
- ⚡ Vous voulez le traitement le plus rapide possible
- 💾 Vous avez au moins 2 GB de VRAM
- 🪟 Vous êtes sur Windows avec les pilotes NVIDIA installés

---

### **🔍 Vérifier Votre Carte Graphique (Windows):**

**Méthode 1 - Gestionnaire des Tâches:**
1. Appuyez sur `Ctrl + Shift + Échap`
2. Cliquez sur l'onglet "Performance"
3. Cherchez "GPU" dans la liste
4. Si vous voyez "NVIDIA GeForce", vous pouvez utiliser la version GPU

**Méthode 2 - Gestionnaire de Périphériques:**
1. Appuyez sur `Win + X`
2. Sélectionnez "Gestionnaire de périphériques"
3. Développez "Cartes graphiques"
4. Vérifiez le nom de votre GPU

**Méthode 3 - Ligne de Commande:**
```bash
nvidia-smi
```
Si cette commande affiche des informations, vous avez NVIDIA avec pilotes ✅

---

### **💡 Exemples de Cartes Graphiques Compatibles:**

#### **✅ Compatible (Version GPU):**
- NVIDIA GeForce RTX 4090, 4080, 4070, 4060, 4050
- NVIDIA GeForce RTX 3090, 3080, 3070, 3060, 3050
- NVIDIA GeForce RTX 2080, 2070, 2060
- NVIDIA GeForce GTX 1660, 1650, 1080, 1070, 1060
- NVIDIA GeForce GTX 980, 970, 960

#### **❌ Non Compatible (Utilisez Version CPU):**
- AMD Radeon (toutes versions)
- Intel UHD Graphics / Iris
- Apple M1 / M2 / M3
- Cartes graphiques intégrées

---

## 📥 Installation

### **Étape 1: Choisir et Lancer le Setup**

Selon votre choix ci-dessus, double-cliquez sur:
- `setup_cpu.bat` (version universelle - recommandée) **OU**
- `setup_gpu.bat` (version rapide - NVIDIA uniquement)

### **Étape 2: Patienter**

Le script va automatiquement:
1. ✅ Créer un environnement virtuel Python
2. ✅ Installer NumPy (version compatible)
3. ✅ Installer PyTorch (CPU ou GPU selon votre choix)
4. ✅ Installer OpenCV, Flask, et autres dépendances
5. ✅ Installer Real-ESRGAN et ses composants
6. ✅ Tester l'installation

**⏱️ Durée estimée:**
- Version CPU: 5-8 minutes
- Version GPU: 8-12 minutes (téléchargement plus volumineux)

### **Étape 3: Vérification**

À la fin, vous verrez:
```
============================================================
Setup Complete!
============================================================

Next steps:
  1. Ensure trainedYOLO.pt is in models/ folder
  2. Run: run.bat
  3. Open: http://localhost:5000
```

**⚠️ Important:** Vérifiez que le fichier `trainedYOLO.pt` est bien dans le dossier `models/`

---

## 🎯 Lancement de l'Application

### **Méthode Simple:**
Double-cliquez sur: **`run.bat`**

### **Méthode Manuelle (Alternative):**
```bash
# Ouvrir un terminal dans le dossier du projet
venv\Scripts\activate
python app.py
```

### **Confirmation de Lancement:**
Vous devriez voir dans le terminal:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
```

✅ **L'application est maintenant lancée!**

---

## 🌐 Utilisation de l'Application

### **Étape 1: Ouvrir le Navigateur**
Accédez à: **http://localhost:5000**

### **Étape 2: Upload du Document**
Deux méthodes possibles:

**Méthode A - Glisser-Déposer:**
1. Prenez une photo de votre document
2. Glissez-la directement sur la zone de dépôt
3. Relâchez

**Méthode B - Parcourir:**
1. Cliquez sur "Browse Files"
2. Sélectionnez votre image
3. Cliquez sur "Ouvrir"

**📝 Formats acceptés:** PNG, JPG, JPEG, BMP, TIFF, WEBP  
**📏 Taille maximale:** 16 MB

### **Étape 3: Aperçu**
Vous verrez un aperçu de votre image avec:
- Le nom du fichier
- Un bouton "Process Document" (vert)
- Un bouton "Cancel" (gris)

### **Étape 4: Traitement**
Cliquez sur **"Process Document"**

L'interface affiche les 4 étapes en temps réel:
1. 🔍 **Détection du document...** (YOLO analyse l'image)
2. ✂️ **Extraction et nettoyage...** (Suppression de l'arrière-plan)
3. 📐 **Redressement des bordures...** (Correction de perspective)
4. ⬆️ **Amélioration de la qualité...** (Upscaling avec Real-ESRGAN/OpenCV)

**⏱️ Durée du traitement:**
- Version CPU: 15-30 secondes
- Version GPU: 8-12 secondes

### **Étape 5: Résultats**
Une fois terminé, vous verrez:
- ✅ Icône de succès
- "Processing Complete!"
- Aperçu du document traité
- Deux boutons:
  - **⬇️ Download Processed Document** (télécharger le résultat)
  - **🔄 Process Another Document** (traiter un autre document)

### **Étape 6: Téléchargement**
Cliquez sur **"Download Processed Document"**

Le fichier sera téléchargé avec le nom: `processed_document.png`

---

## ⚙️ Différences de Performance

### **Vitesse de Traitement par Étape:**

| Étape | Version CPU | Version GPU | Différence |
|-------|-------------|-------------|------------|
| Détection YOLO | 50-150 ms | 50-150 ms | Similaire |
| Extraction | 1-2 sec | 1-2 sec | Similaire |
| Dewarping | 1-2 sec | 1-2 sec | Similaire |
| **Upscaling** | **12-25 sec** | **4-8 sec** | **3x plus rapide** |
| **TOTAL** | **15-30 sec** | **8-12 sec** | **2-3x plus rapide** |

**💡 Note:** La différence principale se situe au niveau de l'upscaling. Les autres étapes utilisent déjà des algorithmes optimisés.

---

## 🔄 Traiter Plusieurs Documents

### **Méthode Simple:**
1. Après avoir téléchargé votre premier document
2. Cliquez sur "Process Another Document"
3. Répétez le processus d'upload et traitement

### **Astuce:**
L'application nettoie automatiquement les fichiers temporaires après chaque téléchargement pour économiser de l'espace disque.

---

## 🛠️ Dépannage

### **Problème 1: "Real-ESRGAN not properly installed"**

**Message dans le terminal:**
```
Real-ESRGAN not properly installed: ...
Falling back to OpenCV upscaling...
```

**Solution:**
- ✅ Ce n'est **PAS une erreur bloquante**
- ✅ L'application fonctionne avec OpenCV (qualité excellente)
- ✅ Pour activer Real-ESRGAN:
  ```bash
  venv\Scripts\activate
  pip install git+https://github.com/XPixelGroup/BasicSR.git
  ```

**💡 Important:** Même avec OpenCV, la qualité est très bonne. Real-ESRGAN est une optimisation, pas une nécessité.

---

### **Problème 2: "Port 5000 already in use"**

**Erreur:**
```
OSError: [Errno 48] Address already in use
```

**Solution 1 - Tuer le processus:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID [NUMERO_PID] /F
```

**Solution 2 - Changer le port:**
Éditez `app.py`, dernière ligne:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changé à 5001
```
Puis accédez à: http://localhost:5001

---

### **Problème 3: "Model not found"**

**Erreur:**
```
Error: Could not find model at models/trainedYOLO.pt
```

**Solution:**
- Vérifiez que `trainedYOLO.pt` est dans le dossier `models/`
- Le nom doit être exactement: `trainedYOLO.pt` (sensible à la casse)

---

### **Problème 4: Erreur NumPy**

**Erreur:**
```
AttributeError: _ARRAY_API not found
```

**Solution:**
```bash
venv\Scripts\activate
pip uninstall numpy -y
pip install "numpy<2.0.0"
```

---

### **Problème 5: Le Setup Échoue**

**Si `setup_cpu.bat` ou `setup_gpu.bat` ne fonctionne pas:**

**Installation manuelle:**
```bash
# 1. Créer l'environnement virtuel
python -m venv venv
venv\Scripts\activate

# 2. Installer les dépendances
pip install "numpy<2.0.0"
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install opencv-python flask werkzeug pillow ultralytics

# 3. Installer Real-ESRGAN (optionnel)
pip install git+https://github.com/XPixelGroup/BasicSR.git
pip install facexlib realesrgan gfpgan

# 4. Lancer l'application
python app.py
```

---

### **Problème 6: GPU Non Détecté (Version GPU)**

**Si vous avez installé la version GPU mais elle utilise le CPU:**

**Vérification:**
```bash
venv\Scripts\activate
python -c "import torch; print(torch.cuda.is_available())"
```

**Si résultat = False:**
1. Vérifiez que vous avez une carte NVIDIA
2. Installez/mettez à jour les pilotes NVIDIA
3. Réinstallez PyTorch:
   ```bash
   pip uninstall torch torchvision -y
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

---

## 📊 Commandes Utiles

### **Vérifier l'Installation:**
```bash
# Activer l'environnement
venv\Scripts\activate

# Vérifier Python
python --version

# Vérifier les packages installés
pip list

# Tester PyTorch
python -c "import torch; print(torch.__version__)"

# Tester GPU (si version GPU)
python -c "import torch; print(torch.cuda.is_available())"

# Tester Real-ESRGAN
python -c "from realesrgan import RealESRGANer; print('OK')"
```

---

## 🔄 Changer de Version (CPU ↔ GPU)

**Pour passer de CPU à GPU (ou inversement):**

1. Supprimez le dossier `venv`:
   ```bash
   rmdir /s venv
   ```

2. Relancez le setup souhaité:
   - `setup_cpu.bat` ou `setup_gpu.bat`

3. Relancez l'application:
   ```bash
   run.bat
   ```

---

## 📝 Notes Importantes

### **Performance:**
- ⚡ La version GPU est 2-3x plus rapide mais requiert NVIDIA
- ✅ La version CPU fonctionne partout mais est plus lente
- 🎨 **La qualité est identique** entre les deux versions

### **Qualité:**
- Real-ESRGAN: Qualité optimale (si installation réussie)
- OpenCV: Qualité excellente (fallback automatique)
- Les deux produisent des résultats professionnels

### **Compatibilité:**
- Windows 10/11: Entièrement supporté
- macOS: Utilisez version CPU uniquement
- Linux: Les deux versions fonctionnent

---

## 🎓 Conseils d'Utilisation

### **Pour de Meilleurs Résultats:**
1. 📸 Prenez la photo dans un endroit bien éclairé
2. 📏 Essayez de cadrer le document entièrement
3. 🎯 L'angle n'est pas important (l'IA corrige automatiquement)
4. 📱 Les photos de smartphone fonctionnent parfaitement
5. 🖼️ Évitez les images trop floues ou surexposées

### **Types de Documents Supportés:**
- ✅ Feuilles A4, lettres, notes
- ✅ Reçus, factures
- ✅ Certificats, diplômes
- ✅ Contrats, formulaires
- ✅ Cartes, documents d'identité
- ✅ Livres, magazines (pages individuelles)

---

## 🆘 Besoin d'Aide?

### **Ressources Disponibles:**
- 📖 `DESCRIPTION_PROJET.md` - Description complète du projet
- 🔧 `TROUBLESHOOTING.md` - Guide de dépannage détaillé
- 📋 `WHICH_SETUP.md` - Aide au choix de configuration
- 🚀 `EXAMINER_QUICKSTART.md` - Guide rapide pour l'examinateur

### **En Cas de Problème Persistant:**
1. Vérifiez que Python 3.8+ est installé
2. Vérifiez que `trainedYOLO.pt` est dans `models/`
3. Essayez la version CPU (plus compatible)
4. Consultez le fichier `TROUBLESHOOTING.md`
5. Vérifiez les messages d'erreur dans le terminal

---

## ✅ Check-list Avant Utilisation

- [ ] Python 3.8+ installé
- [ ] Git installé (recommandé)
- [ ] `trainedYOLO.pt` dans le dossier `models/`
- [ ] Setup exécuté avec succès
- [ ] Pas de messages d'erreur lors du lancement
- [ ] Navigateur ouvert sur http://localhost:5000
- [ ] Image de test prête à être uploadée

---

## 🎉 Résumé Rapide

1. **Installer:** Double-clic sur `setup_cpu.bat` ou `setup_gpu.bat`
2. **Attendre:** 5-12 minutes selon la version
3. **Lancer:** Double-clic sur `run.bat`
4. **Ouvrir:** http://localhost:5000 dans le navigateur
5. **Utiliser:** Glisser-déposer → Process → Download
6. **Profiter:** Documents numérisés de qualité professionnelle!

---

*Développé dans le cadre d'un projet de Computer Vision*  
*Pour toute question technique, consultez les fichiers de documentation fournis.*