import numpy as np

def add_ramo(Y, de, para, r_pct, x_pct, b_pct=0.0, tap=1.0, shift_deg=0.0, status=1):
    if status == 0: return
    i, k = de - 1, para - 1
    r, x, b = r_pct / 100.0, x_pct / 100.0, b_pct / 100.0
    z = complex(r, x)
    y = 1 / z
    ysh = 1j * (b / 2.0)
    a = tap * np.exp(1j * np.deg2rad(shift_deg))
    
    Y[i, i] += (y + ysh) / (abs(a) ** 2)
    Y[k, k] += (y + ysh)
    Y[i, k] += -y / np.conj(a)
    Y[k, i] += -y / a

def montar_ybus(n_barras, linhas, transformadores):
    Y = np.zeros((n_barras, n_barras), dtype=complex)
    for ln in linhas: add_ramo(Y, **ln)
    for tr in transformadores: add_ramo(Y, **tr)
    return Y

def fmt_val(z, tol=1e-8):
    re = z.real if abs(z.real) > tol else 0.0
    im = z.imag if abs(z.imag) > tol else 0.0
    
    re_str = f"{re:,.5f}".replace(".", "X").replace(",", ".").replace("X", ",")
    im_str = f"{abs(im):,.5f}".replace(".", "X").replace(",", ".").replace("X", ",")
    sinal = " + j" if im >= 0 else " - j"
    
    if abs(z) < tol:
        return " " * 20
    return f"{re_str}{sinal}{im_str}"

def imprimir_padrao_imagem(Y):
    n = Y.shape[0]
    print("Ybus (pu):\n")
    for col_inicio in range(0, n, 3):
        col_fim = min(col_inicio + 3, n)
        headers = " " * 10
        for j in range(col_inicio, col_fim):
            headers += f"{'Barra ' + str(j+1):>21}"
        print(headers)
        
        for i in range(n):
            linha_str = f"Barra {i+1:<2}"
            tem_valor = False
            vals_str = ""
            for j in range(col_inicio, col_fim):
                val = fmt_val(Y[i, j])
                vals_str += f"{val:>21}"
                if val.strip(): tem_valor = True
            if tem_valor:
                print(f"{linha_str}{vals_str}")
        print("\n" + "-" * 80 + "\n")

if __name__ == "__main__":
    n_barras = 9
    
    # Dados de linha conforme Adendo I [cite: 68] e requisitos da tarefa 
    linhas = [
        {"de": 3, "para": 5, "r_pct": 1.7, "x_pct": 9.2, "b_pct": 15.8},
        {"de": 3, "para": 8, "r_pct": 1.0, "x_pct": 8.5, "b_pct": 17.6},
        {"de": 4, "para": 6, "r_pct": 0.85, "x_pct": 7.2, "b_pct": 14.9},
        {"de": 4, "para": 7, "r_pct": 0.9, "x_pct": 7.9, "b_pct": 16.2},
        {"de": 5, "para": 7, "r_pct": 3.2, "x_pct": 16.1, "b_pct": 30.6},
        {"de": 6, "para": 8, "r_pct": 1.1, "x_pct": 8.4, "b_pct": 25.6},
        {"de": 7, "para": 9, "r_pct": 1.19, "x_pct": 10.08, "b_pct": 20.9},
        {"de": 8, "para": 9, "r_pct": 3.9, "x_pct": 17.0, "b_pct": 35.8},
        {"de": 3, "para": 9, "r_pct": 1.7, "x_pct": 9.2, "b_pct": 15.8},
    ]
    
    # Dados de transformadores conforme Adendo I [cite: 73]
    transformadores = [
        {"de": 1, "para": 3, "r_pct": 0.0, "x_pct": 5.34},
        {"de": 2, "para": 4, "r_pct": 0.0, "x_pct": 7.68},
    ]

    Ybus = montar_ybus(n_barras, linhas, transformadores)
    imprimir_padrao_imagem(Ybus)
