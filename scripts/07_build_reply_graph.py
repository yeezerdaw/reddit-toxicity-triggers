import networkx as nx

def build_interaction_graph(df):
    df = df[['comment_id', 'parent_id', 'author', 'subreddit']].dropna()
    df = df[~df['author'].isin(['[deleted]', 'AutoModerator'])]
    comment_to_author = dict(zip(df['comment_id'], df['author']))

    G = nx.DiGraph()
    G.add_nodes_from(df['author'].unique())

    for _, row in df.iterrows():
        if row['parent_id'].startswith('t1_'):
            parent_id = row['parent_id'][3:]
            if parent_id in comment_to_author:
                replier = row['author']
                replied_to = comment_to_author[parent_id]
                if replier != replied_to:
                    G.add_edge(replier, replied_to, subreddit=row['subreddit'])

    return G

