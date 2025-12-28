# =========================================================
# ARQUIVO: widgets.py
# Responsável pelos componentes visuais personalizados
# =========================================================

from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout, QLabel, QPushButton, QTextBrowser
)
from PyQt6.QtCore import Qt


class ExplainerPanel(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Contexto Científico", parent)

        # Estilização do Painel (Dark Theme)
        self.setStyleSheet("""
            QGroupBox {
                border: 1px solid #334155;
                border-radius: 6px;
                margin-top: 10px;
                font-weight: bold;
                color: #94a3b8;
                background-color: #0f172a;
            }
            QGroupBox::title { 
                subcontrol-origin: margin; 
                left: 10px; 
                padding: 0 3px; 
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(10, 15, 10, 10)

        # 1. Resumo (Sempre visível - Texto curto)
        self.lbl_summary = QLabel("Iniciando sistema...")
        self.lbl_summary.setWordWrap(True)
        self.lbl_summary.setStyleSheet("font-size: 13px; color: #e2e8f0; font-weight: 500;")
        layout.addWidget(self.lbl_summary)

        # 2. Botão de "Saiba Mais" (Interativo)
        self.btn_expand = QPushButton("▼ Explicar Fenômeno")
        self.btn_expand.setFlat(True)
        self.btn_expand.setStyleSheet("""
            text-align: left; 
            color: #58a6ff; 
            font-weight: bold; 
            border: none;
            padding: 5px 0;
        """)
        self.btn_expand.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_expand.clicked.connect(self._toggle_details)
        layout.addWidget(self.btn_expand)

        # 3. Detalhes (Oculto por padrão - Texto HTML rico)
        self.txt_details = QTextBrowser()
        self.txt_details.setOpenExternalLinks(True)
        self.txt_details.setStyleSheet("""
            QTextBrowser {
                background-color: #1e293b; 
                border: 1px solid #334155; 
                border-radius: 4px; 
                color: #cbd5e1; 
                font-size: 12px; 
                padding: 8px;
            }
        """)
        self.txt_details.setMaximumHeight(0)  # Começa fechado
        self.txt_details.setVisible(False)
        layout.addWidget(self.txt_details)

        # =====================================================
        # BASE DE CONHECIMENTO CIENTÍFICO
        # =====================================================
        self.texts = {
            "1D": {
                "short": "Uma partícula quântica encontra uma parede sólida. Diferente de uma bola de tênis, ela não bate e volta simplesmente.",
                "long": """
                <p style='color:#fff'><b>O Fenômeno do Tunelamento</b></p>
                <p>Na física clássica, se uma partícula não tem energia (E) suficiente para superar uma barreira (V), ela é refletida 100% das vezes.</p>
                <p>Na <b>Mecânica Quântica</b>, a partícula é descrita por uma <i>Função de Onda</i>. Quando a onda atinge a barreira, ela não para abruptamente; ela sofre um <b>decaimento exponencial</b> dentro da parede.</p>
                <p>Se a parede for fina o suficiente, a cauda da onda emerge do outro lado. Isso significa que há uma probabilidade real da partícula "atravessar" o muro sólido.</p>
                <p><i>Aplicações Reais:</i> Microscópios de Tunelamento (STM), Fusão Nuclear no Sol e Memórias Flash (SSD/Pen-drives).</p>
                """
            },
            "3D_RADIAL": {
                "short": "A onda se espalha em todas as direções a partir de um ponto central, como uma explosão ou som no ar.",
                "long": """
                <p style='color:#fff'><b>Simetria Esférica e Dispersão</b></p>
                <p>Aqui simulamos a equação de Schrödinger em coordenadas radiais. Imagine um átomo emitindo uma partícula.</p>
                <p>Observe que a amplitude da onda diminui à medida que ela se afasta do centro. Isso obedece à <b>Lei do Inverso do Quadrado</b>: como a mesma energia total deve se espalhar por uma casca esférica cada vez maior, a densidade de probabilidade em cada ponto deve diminuir.</p>
                <p>A barreira aqui atua como uma "casca" esférica envolvendo a partícula.</p>
                """
            },
            "3D_SURFACE": {
                "short": "Visualização Topográfica da Probabilidade. Picos altos indicam onde é mais provável encontrar a partícula.",
                "long": """
                <p style='color:#fff'><b>Mapeamento de Probabilidade |ψ|²</b></p>
                <p>Este gráfico converte a probabilidade em altura (Eixo Z). É a melhor forma de visualizar a <b>Interferência de Ondas</b>.</p>
                <p>Note a região 'agitada' antes da barreira (lado esquerdo). Isso ocorre porque a onda incidente (indo para a direita) colide com a onda refletida (voltando da barreira).</p>
                <p>Onde os picos se encontram, eles somam (interferência construtiva). Onde pico encontra vale, eles se anulam. Isso cria o padrão de <b>Onda Estacionária</b> que você vê.</p>
                """
            },
            "DOUBLE_BARRIER": {
                "short": "O equivalente 1D da Fenda Dupla. A onda fica presa e reflete entre dois muros, criando ressonância.",
                "long": """
                <p style='color:#fff'><b>Ressonância Quântica (Fabry-Pérot)</b></p>
                <p>Aqui temos duas barreiras separadas por um poço. A onda entra e fica 'batendo' de um lado para o outro no espaço entre os muros.</p>
                <p>Se a energia da partícula coincidir exatamente com um <b>Nível de Energia de Ressonância</b> do sistema, ocorre um fenômeno incrível: as reflexões se cancelam perfeitamente e a transmissão se torna 100%.</p>
                <p>Isso faz com que o sistema pareça transparente para a partícula, mesmo com barreiras altas. É o princípio dos <i>Diodos de Tunelamento Ressonante</i>.</p>
                """
            },
            "BIO_QUANTUM": {
                "short": "Como a natureza usa a física quântica para transportar energia da luz com eficiência quase perfeita?",
                "long": """
                <p style='color:#fff'><b>Biologia Quântica: Complexo FMO</b></p>
                <p>Na fotossíntese, um fóton cria um <i>éxciton</i> (pacote de energia). Ele precisa chegar ao Centro de Reação (caixa verde) antes de dissipar calor.</p>
                <p>Se a energia fizesse um "passeio aleatório" (como uma bola de pinball), ela se perderia. Em vez disso, a natureza usa <b>Coerência Quântica</b>.</p>
                <p>A onda de energia explora <b>todos os caminhos possíveis simultaneamente</b> (Superposição). Os caminhos ineficientes sofrem interferência destrutiva, e o caminho mais rápido é selecionado instantaneamente.</p>
                """
            }
        }

    def update_mode(self, mode):
        """Atualiza o texto baseado no modo selecionado no main.py"""
        # Pega o texto do dicionário, ou usa o 1D como padrão se não achar
        data = self.texts.get(mode, self.texts["1D"])

        self.lbl_summary.setText(data["short"])
        self.txt_details.setHtml(data["long"])

        # Se o usuário mudar de modo, podemos querer fechar o detalhe
        # ou mantê-lo aberto. Aqui optamos por manter o estado atual.

    def _toggle_details(self):
        """Abre e fecha a explicação detalhada com animação simples"""
        if self.txt_details.isVisible():
            self.txt_details.setVisible(False)
            self.txt_details.setMaximumHeight(0)
            self.btn_expand.setText("▼ Explicar Fenômeno")
        else:
            self.txt_details.setVisible(True)
            # Define uma altura máxima suficiente para ler o texto
            self.txt_details.setMaximumHeight(180)
            self.btn_expand.setText("▲ Ocultar Detalhes")