import copy
from random import sample

class Agent:
    def __init__(self, state = 0, alpha = 0.25):
        self.state = state
        self.alpha = alpha
    
    def action(self, state, board, i, turn):
        # state recibe estado del juego actual, o sea una instancia de Env
        # board es el tablero temporal con las posibles jugadas
        # i sirve para determinar cuántos valores se toman en adelante
        # Se calcula la función de valor de cada acción que se pueda realizar
        
        # Se obtienen las opciones disponibles marcadas con '' por posición en ps
        ps = []
        for p in range(len(board)):
            if board[p] == '⊔':
                ps.append(p)
        # Lista de funciones de valor
        vs = []
        for p in ps:
            t_board = board.copy()
            # Se eligen por orden las posibles jugadas
            t_board[p] = str(turn % 2)
            # Se calcula la función de valor actual en v como la probabilidad de elegir cierta casilla por la recompensa de la misma
            # Descomentar el deseado
            # Puede ser tomando en cuenta que el siguiente será el turno del contringante:
            v = state.reward(t_board = t_board, turn = turn % 2) / len(ps)
            # O la siguiente jugada del mismo jugador
            #v = state.reward(t_board = t_board, turn = state.turn) / len(ps)
            # Si hay recursividad pendiente, se hace
            if i > 0:
                # Se actualiza de manera recursiva
                v = v + self.alpha * (self.action(state = state, board = t_board, i = i - 1, turn = turn + 1)[1] + v)
                #v = v + self.alpha * (self.action(state = state, board = t_board, i = i - 1, turn = state.turn)[1] + v)
            # Se agrega a la lista la tupla (posibiliad, valor)
            vs.append((p,v))

        if i == 2:
            p_board = t_board.copy()
        # Se regresa el valor mayor
        max_vs = [(-1, -1000)]
        for v in vs:
            if v[1] > max_vs[0][1]:
                max_vs.clear()
                max_vs.append(v)
            elif v[1] == max_vs[0][1]:
                max_vs.append(v)
            if i == 2:
                # Se agregan las probabilidades
                p_board[v[0]] = v[1]
        if i == 2:
            for n, i in enumerate(p_board):
                if i == '0':
                    p_board[n] = 'X'
                elif i == '1':
                    p_board[n] = 'O'
            print("\n {} | {} | {} \n {} | {} | {} \n {} | {} | {} \n".format(p_board[0], p_board[1], p_board[2], p_board[3],p_board[4], p_board[5], p_board[6] , p_board[7], p_board[8]))
        return sample(max_vs, 1)[0]
    
    def reset(self):
        self.state = 0
        self.reward = 0

class Env: # Juego del Gato
    def __init__(self, board = ['⊔'] * 9, turn = 0):
        self.board = board
        self.turn = turn
        self.playing = True

    def reward(self, t_board, turn):
        # t_board es el tablero con base en las posibles opciones
        # r es la recompensa
        r = 0
        # player es el jugador 0 o 1 con base en el turno. Es un simple módulo
        player = str(turn)

        # Una victoria se puede dar cuando las casillas verticales, horizontales y diagonales tienen el mismo símbolo, distinto de ''
        # Cada turno se revisa si se gana. En ese caso, la recompensa es 1 si el turno coincide con el símbolo ganador. Si se pierde, es -1, en otro caso, 0
        
        # Victorias horizontales
        if t_board[0] != '⊔' and t_board[0] == t_board[1] and t_board[0] == t_board[2]:
            if player == t_board[0]:
                r = 1
            else:
                r = -1
                
        elif t_board[3] != '⊔' and t_board[3] == t_board[4] and t_board[3] == t_board[5]:
            if player == t_board[3]:
                r = 1
            else:
                r = -1
                
        elif t_board[6] != '⊔' and t_board[6] == t_board[7] and t_board[6] == t_board[8]:
            if player == t_board[6]:
                r = 1
            else:
                r = -1
            
        # Victorias verticales
        elif t_board[0] != '⊔' and t_board[0] == t_board[3] and t_board[0] == t_board[6]:
            if player == t_board[0]:
                r = 1
            else:
                r = -1
                
        elif t_board[1] != '⊔' and t_board[1] == t_board[4] and t_board[1] == t_board[7]:
            if player == t_board[1]:
                r = 1
            else:
                r = -1
                
        elif t_board[2] != '⊔' and t_board[2] == t_board[5] and t_board[2] == t_board[8]:
            if player == t_board[2]:
                r = 1
            else:
                r = -1
        
        # Victorias diagonales
        elif t_board[0] != '⊔' and t_board[0] == t_board[4] and t_board[0] == t_board[8]:
            if player == t_board[0]:
                r = 1
        elif t_board[2] != '⊔' and t_board[2] == t_board[4] and t_board[2] == t_board[6]:
            if player == t_board[2]:
                r = 1

        return r

    def __str__(self):
        p_board = self.board.copy()
        for n, i in enumerate(p_board):
            if i == '0':
                p_board[n] = 'X'
            elif i == '1':
                p_board[n] = 'O'
        return "\n {} | {} | {} \n {} | {} | {} \n {} | {} | {} \n".format(p_board[0], p_board[1], p_board[2], p_board[3],p_board[4], p_board[5], p_board[6] , p_board[7], p_board[8])

    def reset(self):
        self.board = ['⊔'] * 9
        self.turn = 0

a = Agent()
e = Env()

reps = 10
ts = 10
while e.playing:
    print('-- TURNO {} --'.format(e.turn))
    player = 'X'
    if e.turn % 2 == 1:
        player = 'O'
    print('-- JUEGA {} --'.format(player))
    t = a.action(state = e, board = e.board, i = 2, turn = e.turn)
    e.board[t[0]] = str(e.turn % 2)
    # TODO: Revisar si ya se acabó el juego
    # Se incrementa un turno
    e.turn += 1
    print(e)
    print('-- FIN TURNO {} --\n'.format(e.turn -1))
    print('')