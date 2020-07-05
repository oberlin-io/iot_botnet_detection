# Drop features that are all 0 or 1
#edit move this into to_vecspace
drops = list()
for col in df.columns:
    if df[col].value_counts().shape[0]==1:
        drops.append(col)

df.drop(columns=drops, inplace=True)

# Infected|not counts normalized
notinf = df[df.infected==0].sum() / df[df.infected==0].count()
inf = df[df.infected==1].sum() / df[df.infected==1].count()
sums = pd.DataFrame({'infected':inf,'not_infected':notinf})
sums.drop(index='infected', inplace=True)
sums = sums.reset_index().rename(columns={'index':'feature'})