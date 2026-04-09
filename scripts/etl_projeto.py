import pandas as pd
import glob
from sqlalchemy import create_engine, text
import re

engine = create_engine('postgresql://postgres:20042004@localhost:5433/BI')

def limpar_descricao(txt):
    return re.sub(r'^[A-Z0-9]{3,4}\*|^\s+', '', str(txt)).strip()

def processar_etp():
    arquivos = glob.glob("Fatura_*.csv")
    
    if not arquivos:
        print("Nenhum arquivo CSV encontrado! Verifique se os arquivos estão na mesma pasta do script.")
        return

    for arquivo in arquivos:
        print(f"Processando: {arquivo}")
        
        try:
            df = pd.read_csv(arquivo, sep=';', encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(arquivo, sep=';', encoding='latin1')

        df['Data de Compra'] = pd.to_datetime(df['Data de Compra'], dayfirst=True)
        
        df['Desc_Limpa'] = df['Descrição'].apply(limpar_descricao)
        
        df['num_parcela'] = df['Parcela'].apply(lambda x: int(str(x).split('/')[0]) if '/' in str(x) else 1)
        df['total_parcelas'] = df['Parcela'].apply(lambda x: int(str(x).split('/')[1]) if '/' in str(x) else 1)

        with engine.connect() as conn:
            for _, row in df.iterrows():
                
                final_cartao = str(row['Final_Cartão'] if 'Final_Cartão' in df.columns else row['Final do Cartão'])
                conn.execute(text("""
                    INSERT INTO DIM_TITULAR (nome_titular, final_cartao) 
                    SELECT :nome, :final WHERE NOT EXISTS 
                    (SELECT 1 FROM DIM_TITULAR WHERE nome_titular = :nome AND final_cartao = :final)
                """), {"nome": row['Nome no Cartão'], "final": final_cartao})

                conn.execute(text("""
                    INSERT INTO DIM_CATEGORIA (nome_categoria) 
                    SELECT :cat WHERE NOT EXISTS (SELECT 1 FROM DIM_CATEGORIA WHERE nome_categoria = :cat)
                """), {"cat": str(row['Categoria']).upper()})

                conn.execute(text("""
                    INSERT INTO DIM_ESTABELECIMENTO (nome_estabelecimento) 
                    SELECT :est WHERE NOT EXISTS (SELECT 1 FROM DIM_ESTABELECIMENTO WHERE nome_estabelecimento = :est)
                """), {"est": row['Desc_Limpa'].upper()})
                
                dt = row['Data de Compra']
                conn.execute(text("""
                    INSERT INTO DIM_DATA (id_data, dia, mes, ano, nome_mes, dia_semana_nome, dia_semana_num) 
                    SELECT :id, :d, :m, :a, :n_mes, :d_nome, :d_num
                    WHERE NOT EXISTS (SELECT 1 FROM DIM_DATA WHERE id_data = :id)
                """), {
                    "id": dt, "d": dt.day, "m": dt.month, "a": dt.year,
                    "n_mes": dt.strftime('%B'), "d_nome": dt.strftime('%A'), "d_num": dt.weekday()
                })

                res_titular = conn.execute(text("SELECT id_titular FROM DIM_TITULAR WHERE nome_titular = :n"), {"n": row['Nome no Cartão']}).fetchone()
                res_cat = conn.execute(text("SELECT id_categoria FROM DIM_CATEGORIA WHERE nome_categoria = :c"), {"c": str(row['Categoria']).upper()}).fetchone()
                res_est = conn.execute(text("SELECT id_estabelecimento FROM DIM_ESTABELECIMENTO WHERE nome_estabelecimento = :e"), {"e": row['Desc_Limpa'].upper()}).fetchone()

                valor_brl = float(str(row['Valor (em R$)']).replace('.', '').replace(',', '.'))
                
                valor_usd = None
                cotacao = None
                if 'Valor (em US$)' in row and pd.notna(row['Valor (em US$)']):
                    try:
                        valor_usd = float(str(row['Valor (em US$)']).replace('.', '').replace(',', '.'))
                        if 'Cotação' in row and pd.notna(row['Cotação']):
                            cotacao = float(str(row['Cotação']).replace('.', '').replace(',', '.'))
                    except:
                        pass

                conn.execute(text("""
                    INSERT INTO FATO_TRANSACAO 
                    (id_data, id_titular, id_categoria, id_estabelecimento, 
                     valor_brl, valor_usd, cotacao, parcela_texto, 
                     num_parcela, total_parcelas, arquivo_origem)
                    VALUES (:dt, :tid, :cid, :eid, :val, :v_usd, :cot, :ptxt, :np, :tp, :arq)
                """), {
                    "dt": dt, "tid": res_titular[0], "cid": res_cat[0], "eid": res_est[0],
                    "val": valor_brl, "v_usd": valor_usd, "cot": cotacao,
                    "ptxt": row['Parcela'], "np": row['num_parcela'], "tp": row['total_parcelas'],
                    "arq": arquivo
                })
            
            conn.commit()
    
    print("\nETL FINALIZADO COM SUCESSO!")

if __name__ == "__main__":
    processar_etp()