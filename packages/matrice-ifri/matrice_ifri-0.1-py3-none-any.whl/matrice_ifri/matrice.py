class Matrice:
    # Constructeur
    def __init__(self, data: list):
        # Vérification du type de la donnée entrée par l'utilisateur
        if not isinstance(data, list):
            raise TypeError("La donnée entrée n'est pas une liste")

        # Gestion des dimensions 1D ou 2D
        is_2d = True
        for i in data:
            if not isinstance(i, list):
                is_2d = False
                break

        if is_2d:
            # 2D
            self.data = data
            self.shape = (len(data), len(data[0]))
        else:
            is_1d = True
            for i in data:
                if not isinstance(i, (int, float)):
                    is_1d = False
                    break

            if is_1d:
                # 1D
                self.data = data
                self.shape = (len(data),)
            else:
                raise TypeError("La donnée entrée n'est pas valide")

    # Calcul de la longueur
    def __len__(self):
        # Nombre d'éléments en 1D et nombre de lignes en 2D
        return self.shape[0]

    # Addition
    def __add__(self, new_array):
        if isinstance(new_array, Matrice):
            if self.shape != new_array.shape:
                raise ValueError("Erreur: Les dimensions ne sont pas les mêmes")

            # Addition 1D
            if len(self.shape) == 1:
                result = []
                for i in range(len(self.data)):
                    result.append(self.data[i] + new_array.data[i])
                return Matrice(result)
            # Addition 2D
            else:
                result = []
                for i in range(len(self.data)):
                    row = []
                    for j in range(len(self.data[0])):
                        row.append(self.data[i][j] + new_array.data[i][j])
                    result.append(row)
                return Matrice(result)
        elif isinstance(new_array, (int, float)):
            # Addition 1D avec un scalaire
            if len(self.shape) == 1:
                result = []
                for i in range(len(self.data)):
                    result.append(self.data[i] + new_array)
                return Matrice(result)
            # Addition 2D avec un scalaire
            else:
                result = []
                for i in range(len(self.data)):
                    row = []
                    for j in range(len(self.data[0])):
                        row.append(self.data[i][j] + new_array)
                    result.append(row)
                return Matrice(result)
        else:
            raise TypeError("Désolé! Calcul impossible")

    # Soustraction
    def __sub__(self, new_array):
        if isinstance(new_array, Matrice):
            if self.shape != new_array.shape:
                raise ValueError("Erreur: Les dimensions ne sont pas les mêmes")

            # Soustraction 1D
            if len(self.shape) == 1:
                result = []
                for i in range(len(self.data)):
                    result.append(self.data[i] - new_array.data[i])
                return Matrice(result)
            # Soustraction 2D
            else:
                result = []
                for i in range(len(self.data)):
                    row = []
                    for j in range(len(self.data[0])):
                        row.append(self.data[i][j] - new_array.data[i][j])
                    result.append(row)
                return Matrice(result)
        elif isinstance(new_array, (int, float)):
            # Soustraction 1D avec un scalaire
            if len(self.shape) == 1:
                result = []
                for i in range(len(self.data)):
                    result.append(self.data[i] - new_array)
                return Matrice(result)
            # Soustraction 2D avec un scalaire
            else:
                result = []
                for i in range(len(self.data)):
                    row = []
                    for j in range(len(self.data[0])):
                        row.append(self.data[i][j] - new_array)
                    result.append(row)
                return Matrice(result)
        else:
            raise TypeError("Désolé! Calcul impossible")

    # Multiplication
    def __mul__(self, new_array):
        if isinstance(new_array, Matrice):
            if self.shape != new_array.shape:
                raise ValueError("Erreur: Les dimensions ne sont pas les mêmes")

            # Multiplication 1D
            if len(self.shape) == 1:
                result = []
                for i in range(len(self.data)):
                    result.append(self.data[i] * new_array.data[i])
                return Matrice(result)
            # Multiplication 2D
            else:
                result = []
                for i in range(len(self.data)):
                    row = []
                    for j in range(len(self.data[0])):
                        row.append(self.data[i][j] * new_array.data[i][j])
                    result.append(row)
                return Matrice(result)
        elif isinstance(new_array, (int, float)):
            # Multiplication 1D avec un scalaire
            if len(self.shape) == 1:
                result = []
                for i in range(len(self.data)):
                    result.append(self.data[i] * new_array)
                return Matrice(result)
            # Multiplication 2D avec un scalaire
            else:
                result = []
                for i in range(len(self.data)):
                    row = []
                    for j in range(len(self.data[0])):
                        row.append(self.data[i][j] * new_array)
                    result.append(row)
                return Matrice(result)
        else:
            raise TypeError("Désolé! Calcul impossible")

    # Division
    def __truediv__(self, new_array):
        if isinstance(new_array, Matrice):
            if self.shape != new_array.shape:
                raise ValueError("Erreur: Les dimensions ne sont pas les mêmes")

            # Division 1D
            if len(self.shape) == 1:
                result = []
                for i in range(len(self.data)):
                    if new_array.data[i] == 0:
                        raise ZeroDivisionError("Division par zéro détectée")
                    result.append(self.data[i] / new_array.data[i])
                return Matrice(result)
            # Division 2D
            else:
                result = []
                for i in range(len(self.data)):
                    row = []
                    for j in range(len(self.data[0])):
                        if new_array.data[i][j] == 0:
                            raise ZeroDivisionError("Division par zéro détectée")
                        row.append(self.data[i][j] / new_array.data[i][j])
                    result.append(row)
                return Matrice(result)
        elif isinstance(new_array, (int, float)):
            if new_array == 0:
                raise ZeroDivisionError("Division par zéro détectée")
            # Division 1D avec un scalaire
            if len(self.shape) == 1:
                result = []
                for i in range(len(self.data)):
                    result.append(self.data[i] / new_array)
                return Matrice(result)
            # Division 2D avec un scalaire
            else:
                result = []
                for i in range(len(self.data)):
                    row = []
                    for j in range(len(self.data[0])):
                        row.append(self.data[i][j] / new_array)
                    result.append(row)
                return Matrice(result)
        else:
            raise TypeError("Désolé! Calcul impossible")

    # Multiplication avec un scalaire (utilisation de @)
    def __matmul__(self, new_array):
        if isinstance(new_array, (int, float)):
            # Multiplication 1D avec un scalaire
            if len(self.shape) == 1:
                result = []
                for i in range(len(self.data)):
                    result.append(self.data[i] * new_array)
                return Matrice(result)
            # Multiplication 2D avec un scalaire (bonus)
            else:
                result = []
                for i in range(len(self.data)):
                    row = []
                    for j in range(len(self.data[0])):
                        row.append(self.data[i][j] * new_array)
                    result.append(row)
                return Matrice(result)
        else:
            raise TypeError("Désolé! Calcul impossible")
    
    # Recherche d'un élément
    def __contains__(self, element):
        # Recherche 1D
        if len(self.shape) == 1:
            for item in self.data:
                if item == element:
                    return True
        # Recherche 2D
        else:
            for row in self.data:
                for item in row:
                    if item == element:
                        return True
        return False

    # Représentation de la matrice sous forme de chaîne
    def __str__(self):
        return str(self.data)
