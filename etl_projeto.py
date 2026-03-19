import pandas as pd
import glob
from sqlalchemy import create_engine, text

engine = create_engine('postgresql://postgres:20042004@localhost:5433/BI')

def limpar_descricao(txt):
    import re
    return re.sub(r'^[A-Z0-9]{3,4}\*|^\s+', '', str(txt)).strip()

def processar_etp():
    arquivos = glob.glob("Fatura_*.csv")
    
    if not arquivos:
        print("Nenhum arquivo CSV encontrado! Verifique a pasta.")
        return

    for arquivo in arquivos:
        print(f"Lendo: {arquivo}")
        df = pd.read_csv(arquivo, sep=';', encoding='utf-8')

        df['Data de Compra'] = pd.to_datetime(df['Data de Compra'], dayfirst=True)
        df['Desc_Limpa'] = df['Descrição'].apply(limpar_descricao)
        
        df['num_parcela'] = df['Parcela'].apply(lambda x: int(x.split('/')[0]) if '/' in str(x) else 1)
        df['total_parcelas'] = df['Parcela'].apply(lambda x: int(x.split('/')[1]) if '/' in str(x) else 1)

        with engine.connect() as conn:
            for _, row in df.iterrows():
                conn.execute(text("""
                    INSERT INTO DIM_TITULAR (nome_titular, final_cartao) 
                    SELECT :nome, :final WHERE NOT EXISTS 
                    (SELECT 1 FROM DIM_TITULAR WHERE nome_titular = :nome AND final_cartao = :final)
                """), {"nome": row['Nome no Cartão'], "final": str(row['Final_Cartão'] if 'Final_Cartão' in df else row['Final do Cartão'])})

                conn.execute(text("""
                    INSERT INTO DIM_CATEGORIA (nome_categoria) 
                    SELECT :cat WHERE NOT EXISTS (SELECT 1 FROM DIM_CATEGORIA WHERE nome_categoria = :cat)
                """), {"cat": row['Categoria']})

                conn.execute(text("""
                    INSERT INTO DIM_ESTABELECIMENTO (nome_estabelec) 
                    SELECT :est WHERE NOT EXISTS (SELECT 1 FROM DIM_ESTABELECIMENTO WHERE nome_estabelec = :est)
                """), {"est": row['Desc_Limpa']})
                
                conn.execute(text("""
                    INSERT INTO DIM_DATA (id_data, dia, mes, ano) 
                    SELECT :dt, :d, :m, :a WHERE NOT EXISTS (SELECT 1 FROM DIM_DATA WHERE id_data = :dt)
                """), {
                    "dt": row['Data de Compra'], 
                    "d": row['Data de Compra'].day,
                    "m": row['Data de Compra'].month,
                    "a": row['Data de Compra'].year
                })

                
                res_titular = conn.execute(text("SELECT id_titular FROM DIM_TITULAR WHERE nome_titular = :n"), {"n": row['Nome no Cartão']}).fetchone()
                res_cat = conn.execute(text("SELECT id_categoria FROM DIM_CATEGORIA WHERE nome_categoria = :c"), {"c": row['Categoria']}).fetchone()
                res_est = conn.execute(text("SELECT id_estabelec FROM DIM_ESTABELECIMENTO WHERE nome_estabelec = :e"), {"e": row['Desc_Limpa']}).fetchone()

                conn.execute(text("""
                    INSERT INTO FATO_TRANSACAO (id_data, id_titular, id_categoria, id_estabelec, valor_brl, parcela_texto, num_parcela, total_parcelas)
                    VALUES (:dt, :tid, :cid, :eid, :val, :ptxt, :np, :tp)
                """), {
                    "dt": row['Data de Compra'], "tid": res_titular[0], "cid": res_cat[0], "eid": res_est[0],
                    "val": float(str(row['Valor (em R$)']).replace(',', '.')), "ptxt": row['Parcela'],
                    "np": row['num_parcela'], "tp": row['total_parcelas']
                })
            conn.commit()
    
    print("ETL Finalizado! Verifique o pgAdmin.")

if __name__ == "__main__":
    processar_etp()