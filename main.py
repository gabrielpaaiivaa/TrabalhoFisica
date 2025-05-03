import sqlite3

class MenuPrincipal:
    def __init__(self):
        self.opcoes = {
            "1": self.fazer_calculos,
            "2": self.explicacao_teorias,
            "3": self.acessar_historico,
            "4": self.encerrar_processo
        }
        self.conectar_banco()

    def conectar_banco(self):
        self.conn = sqlite3.connect('historico_calculos.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS historico (
                               id INTEGER PRIMARY KEY,
                               delta_fluxo REAL,
                               delta_tempo REAL,
                               epsilon REAL)''')
        self.conn.commit()

    def mostrar_menu(self):
        print("\n--BEM VINDO AO MENU---\nDIGITE:")
        print("1: FAZER CÁLCULOS")
        print("2: EXPLICAÇÃO DAS TEORIAS")
        print("3: ACESSAR O HISTÓRICO")
        print("4: ENCERRAR O PROCESSO")

    def executar(self):
        while True:
            self.mostrar_menu()
            escolha = input("Escolha uma opção: ")
            acao = self.opcoes.get(escolha)
            if acao:
                acao()
            else:
                print(f"'{escolha}' não é uma opção válida.")

    def fazer_calculos(self):
        print("Você escolheu FAZER CÁLCULOS.")
        print("A fórmula é: ε = – ΔΦ / Δt")

        try:
            delta_fluxo = float(input("Digite a variação do fluxo magnético (ΔΦ): "))
            delta_tempo = float(input("Digite a variação do tempo (Δt): "))
            if delta_tempo == 0:
                raise ZeroDivisionError("A variação do tempo não pode ser zero.")
            epsilon = - delta_fluxo / delta_tempo
            print("O resultado da equação é: ε = {} V".format(epsilon))
            self.salvar_historico(delta_fluxo, delta_tempo, epsilon)
        except ValueError:
            print("Por favor, digite um número válido.")
        except ZeroDivisionError as e:
            print(e)

    def salvar_historico(self, delta_fluxo, delta_tempo, epsilon):
        self.cursor.execute("INSERT INTO historico (delta_fluxo, delta_tempo, epsilon) VALUES (?, ?, ?)",
                            (delta_fluxo, delta_tempo, epsilon))
        self.conn.commit()

    def explicacao_teorias(self):
        menu_teorias = MenuTeorias()
        menu_teorias.executar()

    def acessar_historico(self):
        print("Você escolheu ACESSAR O HISTÓRICO.")
        self.cursor.execute("SELECT * FROM historico")
        historico = self.cursor.fetchall()
        if historico:
            for registro in historico:
                print("ID: {}, ΔΦ: {}, Δt: {}, ε: {:.2f} V".format(registro[0], registro[1], registro[2], registro[3]))
        else:
            print("Nenhum histórico de cálculos encontrado.")

    def encerrar_processo(self):
        print("Encerrando o processo. Até logo!")
        self.conn.close()
        exit(0)


class MenuTeorias:
    def __init__(self):
        self.opcoes = {
            "1": self.mostrar_formulas,
            "2": self.teoria_inducao,
            "3": self.voltar
        }

    def mostrar_menu(self):
        print("\n--MENU DE TEORIAS---\nDIGITE:")
        print("1: MOSTRAR FÓRMULAS")
        print("2: TEORIA - INDUÇÃO")
        print("3: VOLTAR")

    def executar(self):
        while True:
            self.mostrar_menu()
            escolha = input("Escolha uma opção: ")
            acao = self.opcoes.get(escolha)
            if acao:
                acao()
                if escolha == "3":
                    break
            else:
                print(f"'{escolha}' não é uma opção válida.")

    def mostrar_formulas(self):
        print("Atualmente, a fórmula que melhor descreve a indução eletromagnética é a Lei de Faraday-Lenz:\n")
        print("ε = – ΔΦ / Δt\n")
        print("ε é a força eletromotriz induzida (também chamada de diferença de potencial), medida em V, volts;")
        print("ΔΦ representa a variação do fluxo magnético no tempo em questão, de maneira que:  ΔΦ = Φf – Φi;")
        print("Δt é a variação do tempo no momento observada, medida em segundos; e")
        print("O sinal negativo que aparece no início da fórmula indica a inversão de sentido que ocorre na lei de Faraday complementada pelas ideias de Lenz.")

    def teoria_inducao(self):
        print("Você escolheu TEORIA - INDUÇÃO.")
        print("A indução eletromagnética, descoberta por Michael Faraday em 1831, é o")
        print("processo pelo qual uma corrente elétrica é gerada em um condutor ")
        print('exposto a uma variação de campo magnético. A Lei de Faraday afirma que')
        print('a força eletromotriz (FEM) induzida é proporcional à taxa de variação ')
        print('do fluxo magnético, e a Lei de Lenz determina que a corrente induzida ')
        print('se opõe à mudança no fluxo magnético. Este fenômeno é crucial para o')
        print('funcionamento de geradores elétricos, transformadores e motores')
        print('elétricos. A indução eletromagnética é fundamental para a geração e')
        print('transmissão de energia elétrica e é amplamente utilizada em ')
        print('dispositivos eletrônicos e sistemas de energia modernos.')

    def voltar(self):
        print("Voltando ao menu principal...")


if __name__ == "__main__":
    menu_principal = MenuPrincipal()
    menu_principal.executar()