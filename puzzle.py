import argparse
import time
import timeit
from collections import deque


#Information/////////////////////////////////////////////////////////
class EightPuzzle:
    def __init__(self, state, parent, move, depth, cost, key):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost
        self.key = key
        if self.state:
            self.map = ''.join(str(e) for e in self.state)
    def __eq__(self, other):
        return self.map == other.map
    def __lt__(self, other):
        return self.map < other.map
    def __str__(self):
        return str(self.map)    

#Global variables***********************************************
GoalState = [0, 1, 2, 3, 4, 5, 6, 7, 8]
GoalNode = None # at finding solution
NodesExpanded = 0 #total nodes visited
MaxSearchDeep = 0 #max deep
MaxFrontier = 0 #max frontier


#BFS**************************************************************
def bfs(startState):

    global MaxFrontier, GoalNode, MaxSearchDeep

    boardVisited= set()
    Queue = deque([EightPuzzle(startState, None, None, 0, 0, 0)])

    while Queue:
        node = Queue.popleft()
        boardVisited.add(node.map)
        if node.state == GoalState:
            GoalNode = node
            return Queue
        posiblePaths = subNodes(node)
        for path in posiblePaths:
            if path.map not in boardVisited:
                Queue.append(path)
                boardVisited.add(path.map)
                if path.depth > MaxSearchDeep:
                    MaxSearchDeep = MaxSearchDeep + 1
        if len(Queue) > MaxFrontier:
            QueueSize = len(Queue)
            MaxFrontier = QueueSize
            
#DFS**************************************************************
def dfs(startState):

    global MaxFrontier, GoalNode, MaxSearchDeep

    boardVisited = set()
    stack = list([EightPuzzle(startState, None, None, 0, 0, 0)])
    while stack:
        node = stack.pop()
        boardVisited.add(node.map)
        if node.state == GoalState:
            GoalNode = node
            return stack
        #inverse the order of next paths for execution porpuses
        posiblePaths = reversed(subNodes(node))
        for path in posiblePaths:
            if path.map not in boardVisited:
                stack.append(path)
                boardVisited.add(path.map)
                if path.depth > MaxSearchDeep:
                    MaxSearchDeep = 1 + MaxSearchDeep
        if len(stack) > MaxFrontier:
            MaxFrontier = len(stack)
    

#AST**************************************************************
def ast(startState):
    
    global MaxFrontier, MaxSearchDeep, GoalNode
    
    #transform initial state to calculate Heuritic
    node1 = ""
    for poss in startState:
        node1 = node1 + str(poss)

    #calculate Heuristic and set initial node
    key = Heuristic(node1)
    boardVisited= set()
    Queue = []
    Queue.append(EightPuzzle(startState, None, None, 0, 0, key)) 
    boardVisited.add(node1)
    
    while Queue:
        Queue.sort(key=lambda o: o.key) 
        node = Queue.pop(0)
        if node.state == GoalState:
            GoalNode = node
            return Queue
        posiblePaths = subNodes(node)
        for path in posiblePaths:      
            thisPath = path.map[:]
            if thisPath not in boardVisited:
                key = Heuristic(path.map)
                path.key = key + path.depth
                Queue.append(path)               
                boardVisited.add(path.map[:])
                if path.depth > MaxSearchDeep:
                    MaxSearchDeep = 1 + MaxSearchDeep
        
        
#Heuristic: distance to root numbers
values_0 = [0,1,2,1,2,3,2,3,4]
values_1 = [1,0,1,2,1,2,3,2,3]
values_2 = [2,1,0,3,2,1,4,3,2]
values_3 = [1,2,3,0,1,2,1,2,3]
values_4 = [2,1,2,1,0,1,2,1,2]
values_5 = [3,2,1,2,1,0,3,2,1]
values_6 = [2,3,4,1,2,3,0,1,2]
values_7 = [3,2,3,2,1,2,1,0,1]
values_8 = [4,3,2,3,2,1,2,1,0]

def Heuristic(node):

    global values_0,values_1,values_2,values_3,values_4,values_5,values_6,value �k*�y߽�&�E���г����4��?����IRo�@ї����Lr���՗Uʸ	!|��%�J/��Rn�	�,>�6aS���#�F�l�om��'28��� ��X�=)]JȊ�L��Ewy�n/��/<�y4fT�'0�3W&zzY�K���+�}6=�7eH�!�w�N�.�M�P�'n[[�&
<S8o�c���cd�ioZ�.�V�@��ޫP[�P��:<=�u����Yِb��dR� �l�߃yw~=��g)ŏ+�w�vfI����9����XR^A���Ew����>a��r���K�c
F�7ANk��N�C��V8-bY5#h~�|-���=����N�3G�V�����H}λCuUtJ�4@(Ϯ�Q�5�*����!�C�o��X\	_
�IH��]�	�CG>��a��2��^K�����l�5
�t�v���/��]h���tIbZ�S��ÅO���������r��R��א�&�Jm�z��^�%<��C D9���v�W�J��ͣ����{y�xm��g&R��b�J����� � �0����d�׿a:�VA�:�_P^�a%�����V}s\]j��v�}�%�?ݑ)�-����K� --��H��˓����/|�ms�]��t��T�A�k�^J�)��;��|B��I���k�r�G��TJzS���V)�%��R9�3���h����B�hP���(ҝ�mq�0|;��R\m)[~O�%��P�׻t�푻��	�p�A�i:ͅ������A�c.���D2��Μ�'�6��� ��$���/���i{9�X�����x��1j��+��l�JL[k�Z���oQ�n�kי�,����a~���~h�y!�� �c���<v��q�w�@1L��&�L#}*+��RY����s�J���� ��O�Y�����.��BU��c���%^���o� \�r��w�6J��.��u����=ޜQe��[�>|.t�?��h���tҵ*�OX$����疂]���%36΄�ؘ,ð��ڦI�s�;�Z�i�d�!p�0������4,�!��f�B0�
)[N}4�xE�%�1NPc;ח�ɩ�H�`��[�O���d�te�����޷�Iw�IL�����n^�2��ȡu��b��tT�6�����į���	�%��4_\�����yb�E>T,�
�g�(ɕ,��mKZPņ� +.ݩ*'�z۲@r�'�ɧZ��Md�œ��}�J��~?���%�f��+B�L�Q�i�9�&��38o<����
VS�I��z�-�̄�Lv"J��(�'�M�d���-��-�ݍ�j�����l��r		���F]�>��U2����T��a�|S��ʌ�ģa�s�N�H�+�	 BA�����z�x�
a��n�g���^C����O=O�2�fG�\�O(���1��܋����_��C=�im��np�����P���K�d�MS����k`N�:3!M��$�/��\������O���v������t��&���\7��O�� �	�հ�X�[�ZAqnN�",���j4��ܤ*y�^$]�.�v�Bw©�ȕd6i�}����ȯ>Z{�/�� #��>`H�@��֭<�T���x"�����}��E��Ўd�L����UX�0���������4"�.��;������ܦE����"�@�}x9+��З�Q��o���&#ty�/�Tj�����Fj6�Mu��J�X�c�]�m�#@����KWFZ�
C�p�'��	��X��ez���4�fn:�sM��2�=�ng���x��ry���n��i���;�->'Ź�#�i�j��"�j�[��CM�ߓ�>�a_a~�1�@m�u�Ø��,��	��+٘o���ρ�3v*<z���9,Yc=Z��tU�kU�I���'k��4!�(u���^��*VgEm̬
֫	�e��5I�RA,��|�c�N'R��b�׸��xm�=65*5�mE"�xi"t4��>s����w$4�2Am�M��L���&P���������ن�'��VhMx��01��t���Ĵkd�GG-� �`��� Dʍ�P�Y	E"͍�ߎ7�qpu�ȝh2��+���u�@DY�b�i����zwI��-R�½��GH��`�	NmA	�J�=��~��&��%PnBɄ)B��8H��4�����d�cQ��(,x��0'Yp[��hU�������,1�`qbP���#�,�#asd�/v��NI"F�`�:��������Y�j]Sw0zӸtK��)����:&�=.I������
�x}�O�4ܽL�f��8B4��l���n;N��}��G��p�;M��~�S+���,�1��m~�DWT����X���K,��K@� �˱'&K���r�qC��)�QpV�>-+2|}e�~�^��`k<�9u��u��׵�U;8�0O�V߲:�ި$�K�Մ�k�{8�sY�u���<�n �<>\���٬�>`���"�+}U�r2���&:�ƮHA�5i���l���C1�+j��������A����`ڕ"e��jV�gm�մ��Q����e$G��Mǳ:���\r��=u�0�~}�#���@��-��d����(|��Tv���vPv�a�ڬ�Q��Q5As[�T��-�9*�Ց�Ǐ��k�FZ�>�t���r�Y�.�¹Et���x��������[�x��7�H��	�S�6����O�,=�}�g&�qX�n!�l9'���:=ۘغ�6l���ѱ��Z#fyy��A�XO L:2䭪����22�~����X8μr����X�@�9�6�as�z���v�#b5�I{O2HK�Y��H��)!.��p�<1�J���k�j�X�a'�l�>G]����p��0��[(�F��{�5�]���n�a2&p��>�wɲ6<E���&(��Z,����%�lK���.uԢ!���F���O)�� ��q��uR�.�����P���.j��j�~h(�j@�iW��D4��dXK+�HK���x���r})٣a�E�Ka!]�ƊL>&�)����΃�����~�gwG�Ɂ@�1�;!$�B�z0���@���f9��<����P�+��\��R/���u�E�H�7�Y�X?Q��	��.&��Q�#��Q7�ȥ�x3�����{f�`i}�a`������4���m"�����⼪�t>���q?}6���4�u3��hfh�:�'�`���BLCx,��]��5ݛ#S������aP�%(+)@�\��� 5�ڠ�5���UQ�i~R:�ʷyORP�e&e)Rfq��R5/�4m�A�� Aв�Z�N/=?����RI:zT\*{�]4��ĳmxIM#)X�0�eQ��0��.Ҷ��q�&b�< pe�(qu}޲�]���﫼�-׹����T�b�:h��:����}�9ӷ�\x�~���;Z+2���f�}O02$L�	Z���t�i(�_t�� �2�k�ψ���
�TsJ�[h״�%�o��%�\�JnU�70w��FA�L��Rq]x��!��ʉa�XHb"��)n8o��� �z���Z��!T�����;����������-��sz�r�U�����Cߚ�0rd��D�ʽ>��sj���[���j!�b�t,�kT���~����/s��7��e�������Ge�#I����W�x�9<1P�.,/`M*Od�f�����Oz|L7����	��-m9MG�.���n�v�a�[��mR�g�0�Ȩ`���" �(�o|��Ct� bu7����˗�Γ�G�ō������xP�C�Ǵ^���ww�rB��q0$wI��<��@��&{zX�v/�%�B����u�f���4E1�U���j�@��ѩ�   	�   (�<�   �  |!�(f��cgL�a,g�8�H_�u8t���T.V��u��p�'3ӎ4;>�!T	��٭�|����G�.hX��<�       if(direction==2):
            return None
        if(direction==3):
            return None
        if(direction==4):
            temp=newState[6]
            newState[6]=newState[7]
            newState[7]=temp
        return newState
    if(index==7):
        if(direction==1):
            temp=newState[7]
            newState[7]=newState[4]
            newState[4]=temp
        if(direction==2):
            return None
        if(direction==3):
            temp=newState[7]
            newState[7]=newState[6]
            newState[6]=temp
        if(direction==4):
            temp=newState[7]
            newState[7]=newState[8]
            newState[8]=temp
        return newState
    if(index==8):
        if(direction==1):
            temp=newState[8]
            newState[8]=newState[5]
            newState[5]=temp
        if(direction==2):
            return None
        if(direction==3):
            temp=newState[8]
            newState[8]=newState[7]
            newState[7]=temp
        if(direction==4):
            return None
        return newState
    
#MAIN**************************************************************
def main():

    global GoalNode

    #a = [1,8,2,3,4,5,6,7,0]
    #point=Heuristic(a)
    #print(point)
    #return
    
    #info = "6,1,8,4,0,2,7,3,5" #20
    #info = "8,6,4,2,1,3,5,7,0" #26
    
    #Obtain information from calling parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('method')
    parser.add_argument('initialBoard')
    args = parser.parse_args()
    data = args.initialBoard.split(",")

    #Build initial board state
    InitialState = []
    InitialState.append(int(data[0]))
    InitialState.append(int(data[1]))
    InitialState.append(int(data[2]))
    InitialState.append(int(data[3]))
    InitialState.append(int(data[4]))
    InitialState.append(int(data[5]))
    InitialState.append(int(data[6]))
    InitialState.append(int(data[7]))
    InitialState.append(int(data[8]))

    #Start operation
    start = timeit.default_timer()

    function = args.method
    if(function=="bfs"):
        bfs(InitialState)
    if(function=="dfs"):
        dfs(InitialState)  
    if(function=="ast"):
        ast(InitialState) 

    stop = timeit.default_timer()
    time = stop-start

    #Save total path result
    deep=GoalNode.depth
    moves = []
    while InitialState != GoalNode.state:
        if GoalNode.move == 1:
            path = 'Up'
        if GoalNode.move == 2:
            path = 'Down'
        if GoalNode.move == 3:
            path = 'Left'
        if GoalNode.move == 4:
            path = 'Right'
        moves.insert(0, path)
        GoalNode = GoalNode.parent

    #'''
    #Print results
    print("path: ",moves)
    print("cost: ",len(moves))
    print("nodes expanded: ",str(NodesExpanded))
    print("search_depth: ",str(deep))
    print("MaxSearchDeep: ",str(MaxSearchDeep))
    print("running_time: ",format(time, '.8f'))
    #'''

    #Generate output document for grade system
    #'''
    file = open('output.txt', 'w')
    file.write("path_to_goal: " + str(moves) + "\n")
    file.write("cost_of_path: " + str(len(moves)) + "\n")
    file.write("nodes_expanded: " + str(NodesExpanded) + "\n")
    file.write("search_depth: " + str(deep) + "\n")
    file.write("max_search_depth: " + str(MaxSearchDeep) + "\n")
    file.write("running_time: " + format(time, '.8f') + "\n")
    file.close()
    #'''

if __name__ == '__main__':
    main()