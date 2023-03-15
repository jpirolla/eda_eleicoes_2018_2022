#!/usr/bin/env python
# coding: utf-8

# # Análise exploratória eleições Brasileiras 2016 - 2022

# ## Importação das bibliotecas e dataset

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt
import plotly.express as px
# plt.style.use('ggplot')


# In[2]:


df = pd.read_csv('br_tse_eleicoes_2018_2022.csv')
df.head(5)


# In[8]:


palette = sns.color_palette("Spectral")


# ## 1. Análise inicial - Conhecendo o dataset

# #### Analisando o tamanho do dataset

# In[11]:


df.shape


# #### Verificando qual a configuração dos dados

# In[3]:


df.columns


# In[13]:


df.info()


# Uma vez que não há valores nulos, não precisamos nos preocuparar como tratar os dados nesse sentido. Caso houvesse, poderíamos optar por fazer uma normalização, por exemplo. Além disso, o dataset é composto por **variáveis qualitativas e quantitativas**, 

# **Tipos de cargos**

# In[96]:


df.loc[:,'cargo'].drop_duplicates()


# #### Análise estatística básica do dataset 

# In[14]:


df.describe()


# # 3. Filtragem de informações relevantes

# **Tipos de eleições**

# In[5]:


df.loc[:,'tipo_eleicao'].drop_duplicates()


# ## Análises

# ### Idade dos candidatos 

# In[3]:


fig = px.histogram(df, nbins=11, title="Histograma de idades", x='idade')
fig.show()


# In[4]:


fig = px.box(df, title="Box plot de idades", x='idade')

# Exibir o gráfico
fig.show()


# Note que o bloxplot referente às idades evidencia a presença de muitos outliers que elevam a média das idades, visto que esta é uma medida sensível à valores discrepantes. Vamos eliminar os valores maiores que 80 anos.

# In[5]:


df_filtered = df[df.idade < 80]
fig = px.box(df_filtered, title="Box plot de idades sem candidatos com mais de 80", x="idade")
fig.show()


# In[3]:


media = np.mean(df)
media_atualizada = np.mean(df_filtered)
print(media)
print(media_atualizada)


# ### Gênero

# In[12]:


# distribuição de genero
df.genero.value_counts(1)


# In[24]:


fig = px.histogram(df, nbins=11, title="Histograma de idades", x='genero')
fig.show()


# In[90]:


genero = df.genero.value_counts()
genero.plot.bar()
plt.title('Histograma do gênero dos candidatos')
plt.xticks(rotation=360)


# In[80]:


# Definir a paleta de cores
palette = sns.color_palette('Set2', 8)
sns.set_palette(palette)


# In[93]:


# Contar a frequência de gênero para cada estado
df_grouped = df.groupby(['sigla_uf', 'genero']).size().reset_index(name='counts')

# Plotar o gráfico de barras usando o Seaborn
sns.catplot(x='sigla_uf', y='counts', hue='genero', kind='bar', data=df_grouped)

# Adicionar título e rótulos de eixo
plt.title('Frequência de gênero por estado')
plt.xlabel('Estados')
plt.ylabel('Frequência')

# Rotacionar a legenda dos estados
plt.xticks(rotation=90)

# Aumentar o tamanho da figura
plt.gcf().set_size_inches(8, 6)
# Mostrar o gráfico
plt.show()


# Normalizando os dados pela quantidade de eleitores em cada estado 

# In[92]:


# Contar a frequência de gênero para cada estado
df_grouped = df.groupby(['sigla_uf', 'genero']).size().reset_index(name='counts')

# Calcular o número total de eleitores por estado
total_counts = df.groupby('sigla_uf').size().reset_index(name='total_counts')

# Juntar os dados com o número total de eleitores por estado
df_grouped = df_grouped.merge(total_counts, on='sigla_uf')

# Normalizar os dados pela quantidade de eleitores por estado
df_grouped['counts'] = df_grouped['counts'] / df_grouped['total_counts']

# Plotar o gráfico de barras usando o Seaborn
sns.catplot(x='sigla_uf', y='counts', hue='genero', kind='bar', data=df_grouped)

# Adicionar título e rótulos de eixo
plt.title('Frequência de gênero por estado (normalizada)')
plt.xlabel('Estado')
plt.ylabel('Frequência (normalizada)')

# Rotacionar a legenda dos estados
plt.xticks(rotation=90)

# Aumentar o tamanho da figura
plt.gcf().set_size_inches(8, 6)

# Mostrar o gráfico
plt.show()


# ### Para vereador

# In[ ]:


#  palette={"feminino": "red", "masculino": "darkblue"}


# In[108]:


# Filtrar os dados para eleições para vereadores
df_filtered = df[df['cargo'] == 'vereador'].dropna()

# Contar a frequência de gênero para cada estado
df_grouped = df_filtered.groupby(['sigla_uf', 'genero']).size().reset_index(name='counts')

# Plotar o gráfico de barras usando o Seaborn
sns.catplot(x='sigla_uf', y='counts', hue='genero', kind='bar', data=df_grouped)

# Adicionar título e rótulos de eixo
plt.title('Frequência de gênero por estado para Vereador')
plt.xlabel('Estado')
plt.ylabel('Frequência')


# Aumentar o tamanho da figura
plt.gcf().set_size_inches(8, 6)

plt.xticks(rotation=90)

# Mostrar o gráfico
plt.show()


# #### Dando erro mas queria comparar os de deputados tb

# In[113]:


# Filtrar os dados para eleições para vereadores
df_filtered = df[df['cargo'] == 'deputado federal'].dropna()

# Contar a frequência de gênero para cada estado
df_grouped = df_filtered.groupby(['sigla_uf', 'genero']).size().reset_index(name='counts')

# Plotar o gráfico de barras usando o Seaborn
sns.catplot(x='sigla_uf', y='counts', hue='genero', kind='bar', data=df_grouped)

# Adicionar título e rótulos de eixo
plt.title('Frequência de gênero por estado para Vereador')
plt.xlabel('Estado')
plt.ylabel('Frequência')


# Aumentar o tamanho da figura
plt.gcf().set_size_inches(8, 6)

plt.xticks(rotation=90)

# Mostrar o gráfico
plt.show()


# ### Ocupação

# In[24]:


df.ocupacao.value_counts(1)


# In[16]:


df.instrucao.value_counts(1)


# In[84]:


escolaridade = df.instrucao.value_counts(1)
escolaridade.plot.bar()
plt.title('Histograma da escolaridade dos candidatos')


# In[17]:


df.cargo.value_counts()


# In[18]:


df.raca.value_counts()


# 2. Análise bivariada

# In[30]:


_ = sns.boxplot(x='idade', y='raca', data=df)


# In[32]:


_ = sns.boxplot(x='idade', y='instrucao', data=df)

