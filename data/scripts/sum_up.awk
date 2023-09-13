# BEGIN{diff=$1} : Au début du script, cette section initialise la variable
# diff avec la valeur de la première colonne ($1) de la première ligne d'entrée.
# Cela est fait pour calculer la différence entre les valeurs de la première colonne
# des lignes successives.
BEGIN{diff=$1}
{
	# Calcule la différence entre la première colonne actuelle ($1) et la valeur
	# stockée dans diff et la stocke dans step.
	step=$1-diff

	# Ajoute la valeur de la deuxième colonne ($2) à la variable quantity.
	quantity+=$2

	# Stocke la valeur de la deuxième colonne dans la variable len.
	len=$2
       	
	#printf("%Step = %20.19f\t %20.19f\t %20.19f\n",step,diff, $1)
	#printf("Granularity %d\n", TimeStep)

	# if(step>granularity) : Vérifie si la valeur de step (la différence entre les colonnes)
	# est supérieure à la valeur de granularity. Si c'est le cas, cela signifie
	# qu'une certaine condition est satisfaite (qui dépend de la valeur de granularity)
	# et le script effectue les étapes suivantes :
	if(step>granularity)
	{
		# Met à jour la valeur de diff avec la valeur actuelle de la première colonne.
		diff=$1-diff

       		#printf("%20.19f\t %20.19f\n ", quantity, diff)

		# Affiche la valeur de quantity (qui est une somme accumulée) suivie d'un retour à la ligne.
		printf("%d\n", quantity)

		# Réinitialise la variable quantity à zéro.
		quantity=0

		
		diff=$1
	}
}

