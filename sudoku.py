import random
import time
import copy

def generer_grille_complete():
    grille = [[0 for _ in range(9)] for _ in range(9)]
    
    def est_valide_generation(grille, num, pos):
        for i in range(9):
            if grille[pos[0]][i] == num or grille[i][pos[1]] == num:
                return False
        box_x, box_y = pos[1] // 3, pos[0] // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if grille[i][j] == num:
                    return False
        return True
    
    def remplir_grille(grille):
        for i in range(9):
            for j in range(9):
                if grille[i][j] == 0:
                    nombres = list(range(1, 10))
                    random.shuffle(nombres)
                    for num in nombres:
                        if est_valide_generation(grille, num, (i, j)):
                            grille[i][j] = num
                            if remplir_grille(grille):
                                return True
                            grille[i][j] = 0
                    return False
        return True
    
    remplir_grille(grille)
    return grille

def generer_grille_jeu(grille_complete, difficulte):
    grille = copy.deepcopy(grille_complete)
    cases_a_vider = {
        'easy': 30,
        'medium': 40,
        'hard': 50
    }
    
    cases_vides = cases_a_vider.get(difficulte, 40)
    
    positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(positions)
    
    for i in range(cases_vides):
        row, col = positions[i]
        grille[row][col] = 0
    
    return grille

def afficher_grille(grille):
    for i in range(len(grille)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        for j in range(len(grille[0])):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            if j == 8:
                print(grille[i][j])
            else:
                print(str(grille[i][j]) + " ", end="")

def est_valide(grille, num, pos):
    for j in range(len(grille[0])):
        if grille[pos[0]][j] == num and pos[1] != j:
            return False

    for i in range(len(grille)):
        if grille[i][pos[1]] == num and pos[0] != i:
            return False

    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if grille[i][j] == num and (i, j) != pos:
                return False

    return True

def trouver_vide(grille):
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if grille[i][j] == 0:
                return (i, j)
    return None

def jouer_sudoku(difficulte):
    grille_complete = generer_grille_complete()
    grille = generer_grille_jeu(grille_complete, difficulte)
    grille_solution = copy.deepcopy(grille_complete)
    score = 1000
    debut = time.time()

    while True:
        afficher_grille(grille)
        print("Entrez 'stop' à tout moment pour arrêter le jeu.")
        ligne = input("Entrez la ligne (1-9): ")
        if ligne.lower() == 'stop':
            break
        ligne = int(ligne) - 1
        colonne = int(input("Entrez la colonne (1-9): ")) - 1
        valeur = int(input("Entrez la valeur (1-9): "))

        if grille[ligne][colonne] != 0:
            print("Cette case est déjà remplie!")
            continue

        if est_valide(grille, valeur, (ligne, colonne)):
            grille[ligne][colonne] = valeur
            score += 10
        else:
            print("Mouvement invalide!")
            score -= 5

        if trouver_vide(grille) is None:
            print("Félicitations! Vous avez terminé le Sudoku!")
            fin = time.time()
            temps = int(fin - debut)
            score_final = score - temps
            print(f"Votre score final est: {score_final}")
            return score_final

    fin = time.time()
    temps = int(fin - debut)
    score_final = score - temps
    print("\nVoici la solution correcte:")
    afficher_grille(grille_solution)
    print(f"\nVotre score actuel: {score_final}")
    return score_final

def main():
    while True:
        print("Choisissez un niveau de difficulté:")
        print("1. Facile")
        print("2. Moyen")
        print("3. Difficile")
        choix = input("Entrez votre choix (1-3): ")
        
        difficulte = {
            '1': 'easy',
            '2': 'medium',
            '3': 'hard'
        }.get(choix, 'medium')
        
        score = jouer_sudoku(difficulte)
        rejouer = input("Voulez-vous rejouer? (o/n): ")
        if rejouer.lower() != 'o':
            break
    print("Merci d'avoir joué!")

if __name__ == "__main__":
    main()