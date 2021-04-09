def main():
    # 0定数接点と1定数接点を節テーブルに定義する
    nodes = [Node(index=0), Node(index=1)]
    a = get_node(1, 0, 1, nodes)
    b = get_node(2, 0, 1, nodes)
    not_c = get_node(3, 1, 0, nodes)

    a_and_b = apply("AND", a, b, nodes)

    f = apply("OR", a_and_b, not_c, nodes)

    print_nodes(f, nodes)


class Node:
    def __init__(self, index=None, v=None, F0=None, F1=None):
        self.index = index
        self.v = v
        self.F0 = F0
        self.F1 = F1


# 変数番号v, 0枝の番地F0, 1枝の番地F1
def get_node(v, F0, F1, nodes):
    # F0とF1が等しければF0をそのまま返す
    if F0 == F1:
        return F0

    # 節テーブルを検査して、等価な接点が見つかればその番地を返す
    for node in nodes:
        if v == node.v:
            if node.F0 == F0 and node.F1 == F1:
                return node.index

    # 等価な接点がなければ新しい接点を作ってその番地を返す
    node = Node(len(nodes), v, F0, F1)
    nodes.append(node)
    return len(nodes) - 1


def apply(op, F, G, nodes):

    # 各BDDが定数だった場合のとき演算子の種類に応じた演算結果の接点の番地を返す
    if F == 0:
        return const_cal(op, G, 0)
    elif F == 1:
        return const_cal(op, G, 1)
    elif G == 0:
        return const_cal(op, F, 0)
    elif G == 1:
        return const_cal(op, F, 1)

    # F=GのときはFを返す
    if F == G:
        return F

    # 両者の最上位変数F.vとG.vが同じとき
    if nodes[F].v == nodes[G].v:
        H0 = apply(op, nodes[F].F0, nodes[G].F0, nodes)
        H1 = apply(op, nodes[F].F1, nodes[G].F1, nodes)
        if H0 == H1:
            return H0
        else:
            return get_node(nodes[F].v, H0, H1, nodes)

    # F.vがG.vよりも上位の時
    if nodes[F].v < nodes[G].v:
        H0 = apply(op, nodes[F].F0, G, nodes)
        H1 = apply(op, nodes[F].F1, G, nodes)
        if H0 == H1:
            return H0
        else:
            return get_node(nodes[F].v, H0, H1, nodes)

    # F.vがG.vよりも下位の時
    if nodes[F].v > nodes[G].v:
        H0 = apply(op, nodes[G].F0, F, nodes)
        H1 = apply(op, nodes[G].F1, F, nodes)
        if H0 == H1:
            return H0
        else:
            return get_node(nodes[G].v, H0, H1, nodes)


def const_cal(op, F, const):
    if const == 0:
        if op == "AND":
            return 0
        elif op == "OR":
            return F
        else:
            print("想定されていないオペランドです。")
    elif const == 1:
        if op == "AND":
            return F
        if op == "OR":
            return 1
        else:
            print("想定されていないオペランドです。")
    else:
        print("想定されていない定数です。")

# できた節テーブルを表示する


def print_nodes(index, nodes):

    print(" node_num | variable |  F0  |  F1 |")
    print("----------------------------------")

    for i in range(len(nodes)):
        if i <= 1:
            print("    N{}    |   {}   | {} | {} |".format(
                i, nodes[i].v, nodes[i].F0, nodes[i].F1))
            print("----------------------------------")
            continue

        if i == index:
            print("    N{}    |   {}      |  N{}  |  N{}  | <- entry_point".format(i,
                  nodes[i].v, nodes[i].F0, nodes[i].F1))
        else:
            print("    N{}    |   {}      |  N{}  |  N{}  |".format(
                i, nodes[i].v, nodes[i].F0, nodes[i].F1))

        print("----------------------------------")


if __name__ == "__main__":
    main()
