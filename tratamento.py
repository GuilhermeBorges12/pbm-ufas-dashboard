import pandas as pd
import re

df = pd.read_csv('leads_pbm_ufas.csv', sep=';', encoding='utf-8')
print(f"Lido: {df.shape[0]} linhas, {df.shape[1]} colunas")

def extrair_payload(texto):
    try:
        texto = texto.replace('""', '"')
        resultado = {}
        campos = ['source_platform','interesse_curso',
                  'nome_contato','email_contato']
        for campo in campos:
            padrao = rf'"{campo}"\s*:\s*"([^"]*?)"'
            match = re.search(padrao, texto)
            resultado[campo] = match.group(1).strip() if match else ''
        return resultado
    except:
        return {c:'' for c in ['source_platform','interesse_curso',
                               'nome_contato','email_contato']}

extraido = df['payload_json_banco_dados'].apply(extrair_payload)
df = pd.concat([df, pd.DataFrame(list(extraido))], axis=1)

df['data_hora_interacao'] = pd.to_datetime(df['data_hora_interacao'])
df['interesse_curso'] = df['interesse_curso'].replace(
    {',':'Não Informado','':'Não Informado'})

canal_map = {'site':'Site Institucional','ig':'Instagram',
             'fb':'Facebook','landing_page':'Landing Page / Google'}
df['canal'] = df['source_platform'].map(canal_map).fillna(
    df['source_platform'])

df['mes_ano']    = df['data_hora_interacao'].dt.to_period('M').astype(str)
df['mes_num']    = df['data_hora_interacao'].dt.month
df['hora_dia']   = df['data_hora_interacao'].dt.hour
df['dia_semana'] = df['data_hora_interacao'].dt.day_name()
df['tem_mensagem'] = df['mensagem_utilizador'].apply(
    lambda x: 'Com Mensagem'
    if pd.notna(x) and str(x).strip()!='' else 'Sem Mensagem')

contagem = df['email_contato'].value_counts()
df['tipo_lead'] = df['email_contato'].map(
    lambda e: 'Retorno' if contagem.get(e,1)>1 else 'Novo')

colunas_fato = ['id_transacao_web','data_hora_interacao','mes_ano',
    'mes_num','hora_dia','dia_semana','nome_contato','email_contato',
    'interesse_curso','canal','source_platform','tem_mensagem',
    'tipo_lead','referrer_origem']
fato = df[colunas_fato].copy()

dim_pessoas = (df.sort_values('data_hora_interacao')
    .drop_duplicates('email_contato',keep='first')
)[['email_contato','nome_contato','interesse_curso',
   'canal','mes_ano','data_hora_interacao','tipo_lead']]
dim_pessoas = dim_pessoas.rename(
    columns={'data_hora_interacao':'primeiro_contato'})

agg_mes = df.groupby('mes_ano').agg(
    total_interacoes=('id_transacao_web','count'),
    pessoas_unicas=('email_contato','nunique'),
    mestrado=('interesse_curso',lambda x:(x=='Mestrado').sum()),
    doutorado=('interesse_curso',lambda x:(x=='Doutorado').sum()),
    indeciso=('interesse_curso',lambda x:(x=='Indeciso').sum()),
    nao_informado=('interesse_curso',
        lambda x:(x=='Não Informado').sum()),
).reset_index()

fato.to_csv('fato_interacoes.csv',index=False,encoding='utf-8-sig')
dim_pessoas.to_csv('dim_pessoas.csv',index=False,encoding='utf-8-sig')
agg_mes.to_csv('agg_mes.csv',index=False,encoding='utf-8-sig')

print("Concluído!")
print(f"  fato_interacoes.csv → {len(fato)} linhas")
print(f"  dim_pessoas.csv     → {len(dim_pessoas)} linhas")
print(f"  agg_mes.csv         → {len(agg_mes)} linhas")