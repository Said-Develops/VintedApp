# Installation des dépendances
# pip install Pillow numpy

from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import random
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import numpy as np
import os
import datetime
import hashlib
import time
import threading

class ImageDuplicatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Générateur d'Images - Ultra Aléatoire v4.0")
        self.root.geometry("600x500")
        self.root.configure(bg='#2c3e50')
        

        self.dossier_entree = tk.StringVar()
        self.dossier_sortie = tk.StringVar()
        self.nb_variations = tk.IntVar(value=5)
        self.processing = False
        
        self.setup_ui()
    
    def setup_ui(self):

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#2c3e50', foreground='white', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('TButton', font=('Arial', 10, 'bold'))
        style.configure('TEntry', font=('Arial', 10))
        

        title_frame = tk.Frame(self.root, bg='#2c3e50', pady=20)
        title_frame.pack(fill='x')
        
        title_label = ttk.Label(title_frame, text="🎨 GÉNÉRATEUR D'IMAGES ULTRA-ALÉATOIRE", 
                               style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="📁 Chaque variation dans son propre dossier • 🎲 Noms 100% aléatoires")
        subtitle_label.pack(pady=5)
        

        main_frame = tk.Frame(self.root, bg='#34495e', padx=30, pady=20)
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        

        self.create_folder_section(main_frame, "📂 DOSSIER SOURCE (images à traiter)", 
                                 self.dossier_entree, self.choisir_dossier_entree, 0)
        

        self.create_folder_section(main_frame, "📁 DOSSIER DE SORTIE (résultats)", 
                                 self.dossier_sortie, self.choisir_dossier_sortie, 2)
        

        variations_frame = tk.Frame(main_frame, bg='#34495e', pady=15)
        variations_frame.grid(row=4, column=0, columnspan=3, sticky='ew', pady=10)
        
        ttk.Label(variations_frame, text="🔢 NOMBRE DE VARIATIONS À CRÉER", 
                 font=('Arial', 11, 'bold')).pack(anchor='w')
        
        scale_frame = tk.Frame(variations_frame, bg='#34495e')
        scale_frame.pack(fill='x', pady=5)
        
        self.scale = tk.Scale(scale_frame, from_=1, to=20, orient='horizontal',
                             variable=self.nb_variations, bg='#3498db', fg='white',
                             font=('Arial', 10, 'bold'), length=400, sliderlength=30)
        self.scale.pack(side='left')
        
        self.variations_label = ttk.Label(scale_frame, text="5 variations", 
                                         font=('Arial', 12, 'bold'))
        self.variations_label.pack(side='right', padx=20)
        
        self.scale.configure(command=self.update_variations_label)
        
 
        info_frame = tk.Frame(main_frame, bg='#34495e', pady=10)
        info_frame.grid(row=5, column=0, columnspan=3, sticky='ew')
        
        info_text = """ℹ️  Ce Logiciel a été crée par Kraimbah Saïd, Développeur C# .Net :
• GitHub : https://github.com/Said-Develops
• LinkedIn : https://www.linkedin.com/in/said-kraimbah-/"""
        
        info_label = tk.Label(info_frame, text=info_text, bg='#34495e', fg='#ecf0f1',
                             font=('Arial', 9), justify='left', wraplength=500)
        info_label.pack(anchor='w')
        

        buttons_frame = tk.Frame(main_frame, bg='#34495e', pady=20)
        buttons_frame.grid(row=6, column=0, columnspan=3)
        
        self.start_button = tk.Button(buttons_frame, text="🚀 DÉMARRER LE TRAITEMENT", 
                                     command=self.demarrer_traitement, bg='#27ae60', fg='white',
                                     font=('Arial', 12, 'bold'), padx=20, pady=10,
                                     relief='raised', bd=3)
        self.start_button.pack(side='left', padx=10)
        
        quit_button = tk.Button(buttons_frame, text="❌ QUITTER", 
                               command=self.root.quit, bg='#e74c3c', fg='white',
                               font=('Arial', 12, 'bold'), padx=20, pady=10,
                               relief='raised', bd=3)
        quit_button.pack(side='right', padx=10)
        

        self.progress_frame = tk.Frame(main_frame, bg='#34495e')
        self.progress_frame.grid(row=7, column=0, columnspan=3, sticky='ew', pady=10)
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='indeterminate')
        self.progress_label = ttk.Label(self.progress_frame, text="")
        

        console_frame = tk.Frame(main_frame, bg='#34495e', pady=10)
        console_frame.grid(row=8, column=0, columnspan=3, sticky='ew')
        
        ttk.Label(console_frame, text="📋 CONSOLE DE SORTIE", 
                 font=('Arial', 10, 'bold')).pack(anchor='w')
        
        self.console = tk.Text(console_frame, height=8, bg='#2c3e50', fg='#00ff00',
                              font=('Consolas', 9), wrap='word')
        scrollbar = tk.Scrollbar(console_frame, orient='vertical', command=self.console.yview)
        self.console.configure(yscrollcommand=scrollbar.set)
        
        self.console.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        

        main_frame.grid_columnconfigure(1, weight=1)
    
    def create_folder_section(self, parent, title, var, command, row):
        frame = tk.Frame(parent, bg='#34495e', pady=10)
        frame.grid(row=row, column=0, columnspan=3, sticky='ew', pady=5)
        
        ttk.Label(frame, text=title, font=('Arial', 11, 'bold')).pack(anchor='w')
        
        path_frame = tk.Frame(frame, bg='#34495e')
        path_frame.pack(fill='x', pady=5)
        
        entry = tk.Entry(path_frame, textvariable=var, font=('Arial', 10), 
                        bg='white', relief='sunken', bd=2)
        entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        button = tk.Button(path_frame, text="📁 Parcourir", command=command,
                          bg='#3498db', fg='white', font=('Arial', 9, 'bold'),
                          padx=15, relief='raised', bd=2)
        button.pack(side='right')
    
    def update_variations_label(self, value):
        nb = int(float(value))
        self.variations_label.configure(text=f"{nb} variation{'s' if nb > 1 else ''}")
    
    def choisir_dossier_entree(self):
        dossier = filedialog.askdirectory(title="Choisir le dossier contenant vos images")
        if dossier:
            self.dossier_entree.set(dossier)
    
    def choisir_dossier_sortie(self):
        dossier = filedialog.askdirectory(title="Choisir le dossier de sortie")
        if dossier:
            self.dossier_sortie.set(dossier)
    
    def log_console(self, message):
        """Ajoute un message à la console"""
        self.console.insert('end', message + '\n')
        self.console.see('end')
        self.root.update_idletasks()
    
    def demarrer_traitement(self):
        if not self.dossier_entree.get():
            messagebox.showerror("Erreur", "Veuillez sélectionner un dossier d'entrée")
            return
        
        if not self.dossier_sortie.get():
            messagebox.showerror("Erreur", "Veuillez sélectionner un dossier de sortie")
            return
        
        if self.processing:
            messagebox.showwarning("Attention", "Un traitement est déjà en cours")
            return
        

        self.processing = True
        self.start_button.configure(state='disabled', text="⏳ TRAITEMENT EN COURS...")
        
        self.progress_bar.pack(fill='x', pady=5)
        self.progress_label.pack()
        self.progress_bar.start(10)
        
        self.console.delete(1.0, 'end')
        
        thread = threading.Thread(target=self.traiter_images_thread)
        thread.daemon = True
        thread.start()
    
    def traiter_images_thread(self):
        """Traite les images dans un thread séparé"""
        try:
            self.traiter_images_simple(self.dossier_entree.get(), 
                                     self.dossier_sortie.get(), 
                                     self.nb_variations.get())
        except Exception as e:
            self.log_console(f"❌ Erreur: {str(e)}")
        finally:
            self.root.after(0, self.fin_traitement)
    
    def fin_traitement(self):
        """Appelé à la fin du traitement"""
        self.processing = False
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.progress_label.pack_forget()
        self.start_button.configure(state='normal', text="🚀 DÉMARRER LE TRAITEMENT")
        messagebox.showinfo("Terminé", "Traitement terminé avec succès !")


    
    def creer_structure_dossiers(self, dossier_sortie, nb_variations):
        """Crée les dossiers pour chaque variation"""
        dossiers_variations = {}
        
        for num_variation in range(1, nb_variations + 1):
            nom_dossier = f"Variation_{num_variation:02d}"
            chemin_dossier = os.path.join(dossier_sortie, nom_dossier)
            
            try:
                os.makedirs(chemin_dossier, exist_ok=True)
                dossiers_variations[num_variation] = chemin_dossier
                self.log_console(f"📁 Dossier créé : {nom_dossier}")
            except Exception as e:
                self.log_console(f"❌ Erreur création dossier {nom_dossier}: {e}")
                return None
        
        return dossiers_variations

    def rotation_puis_recadrage(self, img, intensite=1.0):
        """📐 ROTATION LÉGÈRE + RECADRAGE pour masquer le fond"""
        w, h = img.size
        
        if w < 100 or h < 100:
            return img
        
        try:

            angle_max = min(3.0, 1.0 * intensite)
            angle = random.uniform(-angle_max, angle_max)
            

            img_rotated = img.rotate(angle, expand=True, fillcolor=(0,0,0,0) if img.mode == 'RGBA' else (255,255,255))
            

            w_rot, h_rot = img_rotated.size
            

            facteur_rotation = abs(angle) / angle_max if angle_max > 0 else 0
            marge_rotation = int(min(w_rot, h_rot) * 0.02 * (1 + facteur_rotation))
            

            marge_extra = int(min(w_rot, h_rot) * random.uniform(0.005, 0.02) * intensite)
            

            marge_gauche = random.randint(marge_rotation, marge_rotation + marge_extra)
            marge_droite = random.randint(marge_rotation, marge_rotation + marge_extra)
            marge_haut = random.randint(marge_rotation, marge_rotation + marge_extra)
            marge_bas = random.randint(marge_rotation, marge_rotation + marge_extra)
            

            marge_max = min(w_rot * 0.05, h_rot * 0.05)
            marge_gauche = min(marge_gauche, marge_max)
            marge_droite = min(marge_droite, marge_max)
            marge_haut = min(marge_haut, marge_max)
            marge_bas = min(marge_bas, marge_max)
            

            left = int(marge_gauche)
            top = int(marge_haut)
            right = int(w_rot - marge_droite)
            bottom = int(h_rot - marge_bas)
            

            if right > left + 50 and bottom > top + 50:
                img_final = img_rotated.crop((left, top, right, bottom))
                return img_final
            else:
                return img  
                
        except Exception as e:
            self.log_console(f"    ⚠️  Erreur rotation+recadrage: {e}")
            return img

    def bruit_intelligent(self, img, intensite=1.0):
        """Ajoute un bruit subtil pour différencier"""
        try:
            if random.random() < 0.7:

                pixels = np.array(img)
                h, w = pixels.shape[:2]
                
                nb_pixels = int(h * w * 0.001 * intensite)
                nb_pixels = min(nb_pixels, h * w // 100)
                
                for _ in range(nb_pixels):
                    x = random.randint(0, w-1)
                    y = random.randint(0, h-1)
                    if len(pixels.shape) == 3:
                        variation = random.randint(-15, 15)
                        pixels[y, x] = np.clip(pixels[y, x] + variation, 0, 255)
                    
                return Image.fromarray(pixels)
        except Exception:
            pass
        return img

    def modifications_avancees_douces(self, img, intensite=1.0):
        """Applique des modifications douces mais efficaces"""
        try:

            img = self.rotation_puis_recadrage(img, intensite)
            
            # 2. Ajustements de couleur très légers
            if random.random() < 0.8:

                enhancer = ImageEnhance.Brightness(img)
                facteur = random.uniform(0.95 + intensite*0.02, 1.05 + intensite*0.02)
                img = enhancer.enhance(facteur)
                

                enhancer = ImageEnhance.Contrast(img)
                facteur = random.uniform(0.95 + intensite*0.02, 1.05 + intensite*0.02)
                img = enhancer.enhance(facteur)
            

            if random.random() < 0.5:
                img = self.bruit_intelligent(img, intensite)
                

            if random.random() < 0.3:
                if random.random() < 0.5:
                    img = img.filter(ImageFilter.GaussianBlur(radius=0.2 * intensite))
                else:
                    img = img.filter(ImageFilter.UnsharpMask(radius=0.5, percent=100 + int(10*intensite)))
            
            return img
            
        except Exception as e:
            self.log_console(f"    ⚠️  Erreur modifications: {e}")
            return img

    def generer_nom_ultra_aleatoire(self):
        """Génère un nom de fichier ULTRA-ALÉATOIRE et unique"""

        consonnes = "bcdfghjklmnpqrstvwxyz"
        voyelles = "aeiou"
        chiffres = "0123456789"

        nom = ""
        longueur = random.randint(8, 12)
        for i in range(longueur):
            if i % 2 == 0:
                nom += random.choice(consonnes)
            else:
                nom += random.choice(voyelles)
        

        nom += "".join([random.choice(chiffres) for _ in range(random.randint(2, 4))])
        

        timestamp = str(int(time.time() * 1000000))
        nom += "_" + timestamp[-8:]  

        random_seed = str(random.random() * time.time())
        hash_court = hashlib.md5(random_seed.encode()).hexdigest()[:6]
        nom += hash_court
        
        return nom

    def traiter_images_simple(self, dossier_entree, dossier_sortie, nb_variations):
        """Traite les images avec noms 100% aléatoires - SIMPLE ET RAPIDE"""
        extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')
        
        fichiers = [f for f in os.listdir(dossier_entree) 
                    if f.lower().endswith(extensions)]
        
        if not fichiers:
            self.log_console("❌ Aucune image trouvée")
            return
        

        self.log_console(f"📁 Création de la structure de dossiers...")
        dossiers_variations = self.creer_structure_dossiers(dossier_sortie, nb_variations)
        
        if not dossiers_variations:
            self.log_console("❌ Impossible de créer les dossiers")
            return
        
        total_reussites = 0
        
        self.log_console(f"\n📸 Trouvé {len(fichiers)} image(s) à traiter")
        
        for num_variation in range(1, nb_variations + 1):
            dossier_variation = dossiers_variations[num_variation]
            self.log_console(f"\n📁 === VARIATION {num_variation:02d} === (dans {os.path.basename(dossier_variation)})")
            images_reussies = 0
            
            for fichier in fichiers:
                nom_fichier = os.path.splitext(fichier)[0]
                chemin_entree = os.path.join(dossier_entree, fichier)
                
                try:
                    with Image.open(chemin_entree) as img:

                        intensite = 0.5 + (num_variation - 1) * 0.3
                        

                        img_modifiee = self.modifications_avancees_douces(img.copy(), intensite)
                        

                        nom_ultra_aleatoire = self.generer_nom_ultra_aleatoire()
                        extension = random.choice(['.jpg', '.jpeg'])
                        nom_sortie = nom_ultra_aleatoire + extension
                        chemin_sortie = os.path.join(dossier_variation, nom_sortie)
                        

                        qualite = random.randint(90, 98)
                        img_modifiee.save(chemin_sortie, quality=qualite, optimize=True)
                        
                        self.log_console(f"  ✅ {nom_fichier} → {nom_sortie}")
                        images_reussies += 1
                        
                except Exception as e:
                    self.log_console(f"  ❌ Erreur avec {nom_fichier}: {e}")
            
            self.log_console(f"  💚 {images_reussies} images créées dans Variation_{num_variation:02d}/")
            total_reussites += images_reussies
        
        self.log_console(f"\n🎉 === TRAITEMENT TERMINÉ ===")
        self.log_console(f"📁 Résultats organisés dans : {dossier_sortie}")
        self.log_console(f"📂 {nb_variations} dossiers de variations créés")
        self.log_console(f"💾 Total : {total_reussites} images générées")
        self.log_console(f"🎲 Tous les noms sont 100% aléatoires et uniques !")
        
        self.log_console(f"\n📁 Structure finale :")
        for i in range(1, nb_variations + 1):
            nb_fichiers = len([f for f in os.listdir(dossiers_variations[i]) 
                              if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            self.log_console(f"   📂 Variation_{i:02d}/ → {nb_fichiers} images")

def main():
    root = tk.Tk()
    app = ImageDuplicatorGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n⏹️  Arrêt par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()