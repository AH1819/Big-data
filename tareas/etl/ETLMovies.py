import pandas as pd

df = pd.read_csv('movie_metadata.csv')

average_gross = df['gross'].mean()
df['gross'].fillna(average_gross, inplace=True)

df['facenumber_in_poster'] = df['facenumber_in_poster'].apply(lambda x: 0 if pd.isnull(x) or x < 0 else x)

df['TitleCode'] = df['movie_imdb_link'].str.extract(r'(\d+)')

df['TitleCode'] = df['TitleCode'].apply(lambda x: 'tt' + x if pd.notnull(x) else x)

df['title_year'].fillna(0, inplace=True)

df = df[df['country'] == 'USA']

df.to_csv('FilmTV_USAMovies.csv', index=False)
