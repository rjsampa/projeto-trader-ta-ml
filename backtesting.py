import numpy as np 
import pandas as pd

class Backtesting:
    def __init__(self, df, sinal, capital_inicial, preco_referencia='Close'):
        self.df = df[['Date', sinal, preco_referencia]]
        self.signal = sinal
        self.capital_inicial = capital_inicial
        self.capital = capital_inicial
        self.preco_referencia = 'Close'
        self.operacoes_compra = {}
        self.fluxo_venda = {}
        self.fluxo_venda[df.iloc[0]['Date']] = {
            'qtd_acoes_vendidas': 0,
            'valor_total_venda': 0,
            'preco': 0,
            'capital': capital_inicial,
            'lucro_bruto_operacao': 0
        }

    def buy_execute(self, prices):
        if self.status == 'vendido':
            preco_acao = prices[1][self.preco_referencia]
            self.qtd_de_acoes_compra = int(self.capital/preco_acao)
            self.capital_aportado = preco_acao*self.qtd_de_acoes_compra

            self.capital = self.capital-self.capital_aportado
            self.operacoes_compra[prices[1]['Date']] = {
                'preco_acao': round(prices[1]['Close'], 2),
                'qtd_acoes_comprada': self.qtd_de_acoes_compra,
                'capital_aportado': round(self.capital_aportado, 2),
                'capital': round(self.capital, 2)
            }
            self.status = 'comprado'

    def sell_execute(self, prices):
        if self.status == 'comprado':

            preco_acao = prices[1][self.preco_referencia]
            valor_venda = preco_acao*self.qtd_de_acoes_compra
            self.capital += valor_venda
            lucro = valor_venda-self.capital_aportado
            self.fluxo_venda[prices[1]['Date']] = {
                'qtd_acoes_vendidas': self.qtd_de_acoes_compra,
                'valor_total_venda': round(valor_venda, 2),
                'preco': preco_acao,
                'capital': round(self.capital, 2),
                'lucro_bruto_operacao': round(lucro, 2)
            }

            self.capital_aportado = 0
            self.qtd_de_acoes_compra = 0
            self.status = 'vendido'

    def backtesting(self):
        self.status = 'vendido'

        for day_info in self.df.iterrows():
            if day_info[1][self.signal] == 1:
                self.buy_execute(day_info)
            elif day_info[1][self.signal] == 2:
                self.sell_execute(day_info)

        if self.status == 'comprado':
            self.sell_execute(day_info)

        # final
        df_vendas = pd.DataFrame.from_dict(
            self.fluxo_venda,
            orient='index'
        ).reset_index().rename(columns={'index': 'Date'})

        df_vendas['flag_venda'] = 1
        self.df_result = self.df.merge(
            df_vendas[['Date', 'capital', 'flag_venda']],
            on='Date',
            how='left'
        )
        self.df_result['capital'].fillna(method='ffill', inplace=True)


def test_modelos(acao, df_val=None):
    signais = [i for i in df_val.columns if 'signal' in i]
    df_aux = df_val.loc[
        df_val['acao'] == acao,
        ['Date', 'Close']+signais
    ]

    performances = []

    for sinal in signais:
        bkt_l1 = Backtesting(
            df=df_aux,
            sinal=sinal,
            capital_inicial=1000
        )
        bkt_l1.backtesting()
        performance = round(bkt_l1.capital, 1)
        performances.append(performance)
    return performances, signais