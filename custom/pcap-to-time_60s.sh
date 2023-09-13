#!/bin/bash

# Couleurs de la police
red="\e[31m"
green="\e[32m"
blue="\e[34m"
magenta="\e[35m"
cyan="\e[36m"

# Réinitialisation de la couleur à la fin du texte
reset_color="\e[0m"

# Obtenir la date actuelle
current_date=$(date +"%Y-%m-%d %H:%M:%S")

# Début du script
echo -e "${green}Début du script : $current_date${reset_color}"

# Vérification des arguments
if [ "$#" -ne 2 ]; then
  echo -e "${magenta}Utilisation du script : $0 chemin_vers_fichier_pcap chemin_de_sauvegarde${reset_color}"
  exit 1
fi

# Chemin vers le répertoire contenant les fichiers PCAP
# pcap_directory="/chemin/vers/les/fichiers/pcap"
pcap_directory=$1

# Chemin vers le répertoire de sortie pour les fichiers sans extension
# output_directory="/chemin/vers/le/repertoire/de/sortie"
output_directory=$2

# Liste des fichiers PCAP dans le répertoire
pcap_files=("$pcap_directory"/*.pcap)

# Initialiser le compteur à zéro
count=0

# Parcourir tous les fichiers dans le répertoire
for file in "${pcap_files[@]}"; do
    # Vérifier si le fichier est un fichier PCAP
    if [ -f "$file" ]; then
        # Incrémenter le compteur
        count=$((count + 1))
    fi
done

# Créez le répertoire de sortie s'il n'existe pas déjà
mkdir -p "$output_directory"

# Parcours de chaque fichier PCAP
for pcap_file in "${pcap_files[@]}"; do
    # Nom du fichier sans extension
    filename_without_extension=$(basename -- "$pcap_file" .pcap)

    # Chemin de sortie pour le fichier sans extension
    output_file="$output_directory/$filename_without_extension"

    # Utilisation de tshark pour extraire la longueur des paquets par minute et sauvegarder dans un fichier sans extension
    # awk '{print $8}' imprime le nombre d'octets de données dans les frames capturées dans le fichier pcap
    tshark -r "$pcap_file" -q -z "io,stat,60,frame.len" | grep -v "^===" | awk '{print $8}' > "$output_file"

    echo -e "${cyan}Traitement terminé pour $pcap_file. Résultats sauvegardés dans $output_file ${reset_color}"
done

echo -e "${blue}Tous les fichiers PCAP ont été traités.${reset_color}"

# Obtenir la date actuelle
current_date=$(date +"%Y-%m-%d %H:%M:%S")

# Fin du script
echo -e "${green}Fin du script : $current_date${reset_color}"
