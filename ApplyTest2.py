def get_node(v, F0, F1, h_table, m, nodes):

    # F0とF1が等しければF0をそのまま返す
    if F0 == F1:
        return F0

    # ハッシュテーブルを検査して、等価な接点が見つかればその番地を返す
    index = check_h_table(v, F0, F1, h_table, m, nodes)
    if(index != None):
        return index

    # 等価な接点がなければ新しい接点を作ってその番地を返す
    return make_node(v, F0, F1, h_table, m, nodes)


def check_h_table(v, F0, F1, h_table, m, nodes):  # ハッシュテーブルに要素が存在すれば格納されたインデックスを返す

    x = (v, F0, F1)
    # ハッシュ値からハッシュテーブルにある各Nodeのインデックスのリストを取得する
    indexes = h_table[hash(x) % m]

    if indexes != [None]:
        for index in indexes:
            if x == nodes[index]:
                return index

    return None


def make_node(v, F0, F1, h_table, m, nodes):  # 節テーブルとハッシュテーブルにそれぞれ情報を格納する

    len_nodes = len(nodes)
    index = "N" + str(len_nodes)
    x = (v, F0, F1)

    nodes[index] = x

    # ハッシュ値からハッシュテーブルにある各Nodeのインデックスのリストを取得する
    indexes = h_table[hash(x) % m]
    # ハッシュテーブルにインデックスを格納する
    if indexes[0] == None:
        indexes[0] = index
    else:
        indexes.append(index)

    return index


def apply(op, F, G, h_table, m, nodes, a_cache):

    # 各BDDが定数だった場合のとき
    if F == "N0":
        if op == "AND":
            return "N0"
        elif op == "OR":
            return G
        elif op == "XOR":
            return G
    elif F == "N1":
        if op == "AND":
            return G
        elif op == "OR":
            return "N1"
        elif op == "XOR":
            return get_node(nodes[G][0], nodes[G][2], nodes[G][1], h_table, m, nodes, a_cache)
    elif G == 0:
        if op == "AND":
            return "N0"
        elif op == "OR":
            return F
        elif op == "XOR":
            return F
    elif G == 1:
        if op == "AND":
            return F
        elif op == "OR":
            return "N1"
        elif op == "XOR":
            return get_node(nodes[F][0], nodes[F][2], nodes[F][1], h_table, m, nodes, a_cache)

    # FとGが同じとき
    if F == G:
        if op == "AND" or op == "OR":
            return F
        elif op == "XOR":
            return "N0"

    # op,F,Gの組み合わせがキャッシュに保存されている場合
    H = a_cache.get((op, F, G))
    if H != None:
        return H

    # 両者の最上位変数F.vとG.vが同じとき
    if nodes[F][0] == nodes[G][0]:
        H0 = apply(op, nodes[F][1], nodes[G][1], h_table, m, nodes, a_cache)
        a_cache[(op, nodes[F][1], nodes[G][1])] = H0
        H1 = apply(op, nodes[F][2], nodes[G][2], h_table, m, nodes, a_cache)
        a_cache[(op, nodes[F][2], nodes[G][2])] = H1
        return get_node(nodes[F][0], H0, H1, h_table, m, nodes)

    # F.vがG.vよりも上位の時
    if nodes[F][0] < nodes[G][0]:
        H0 = apply(op, nodes[F][1], G, h_table, m, nodes, a_cache)
        a_cache[(op, nodes[F][1], G)] = H0
        H1 = apply(op, nodes[F][2], G, h_table, m, nodes, a_cache)
        a_cache[(op, nodes[F][2], G)] = H0
        return get_node(nodes[F][0], H0, H1, h_table, m, nodes)

    # F.vがG.vよりも下位の時
    if nodes[F][0] > nodes[G][0]:
        H0 = apply(op, F, nodes[G][1], h_table, m, nodes, a_cache)
        a_cache[(op, F, nodes[G][1])] = H0
        H1 = apply(op, F, nodes[G][2], h_table, m, nodes, a_cache)
        a_cache[(op, F, nodes[G][2])] = H1
        return get_node(nodes[G][0], H0, H1, h_table, m, nodes)

    raise Exception("Something wrong...")


def print_nodes(entry, nodes):  # できた節テーブルを表示する

    print(" node_num | variable |  F0  |  F1 |")
    print("----------------------------------")

    for key, value in nodes.items():
        if key == "N0" or key == "N1":
            print("    {}    |   {}   | {} | {} |".format(
                key, value[0], value[1], value[2]))
            print("----------------------------------")
            continue

        if key == entry:
            print("    {}    |   {}      |  {}  |  {}  | <- entry_point".format(key,
                  value[0], value[1], value[2]))
        else:
            print("    {}    |   {}      |  {}  |  {}  |".format(
                key, value[0], value[1], value[2]))

        print("----------------------------------")


def main():

    # F = a * b + ~c をBDDとして出力することを目標とする

    # 各nodeの情報はtupleで(変数, F0のインデックス, F1のインデックス)と格納することとする
    # 変数は自然数を使い、現れる順に1から数を増やすことにする
    # 各インデックスは文字列で定義する

    # 0終端節と1終端節を定義
    nodes = {"N0": (None, None, None), "N1": (None, None, None)}

    # 変数の数
    num_v = 3

    # 最大節点数をハッシュ化時に使うため仮に定義
    m = num_v * num_v

    # ハッシュテーブルをサイズを指定して定義
    h_table = [[None] for i in range(m)]

    # 使われる変数を定義
    a = get_node(1, "N0", "N1", h_table, m, nodes)
    b = get_node(2, "N0", "N1", h_table, m, nodes)
    not_c = get_node(3, "N1", "N0", h_table, m, nodes)

    # Apply演算のキャッシュを格納する辞書を定義
    a_cache = {}

    a_and_b = apply("AND", a, b, h_table, m, nodes, a_cache)
    f = apply("OR", a_and_b, not_c, h_table, m, nodes, a_cache)

    print()
    print("BDDに対応する表")
    print_nodes(f, nodes)
    print()
    print("Node作成時のハッシュテーブル")
    print(h_table)
    print()
    print("Apply演算のキャッシュ")
    print(a_cache)


if __name__ == "__main__":
    main()
