import streamlit as st
import pandas as pd
import numpy as np
import lightfm
import nmslib
import pickle
import scipy.sparse as sparse


def get_titles(items_list, items):
    result = pd.DataFrame(items[items.item_id.isin(items_list)].title)
    result.index = [i + 1 for i in range(len(items_list))]
    return result


def nearest(id, embeddings, graph, n=5):
    # n+1 because id includes in nearest list too
    return graph.knnQuery(embeddings[id], k=n+1)[0][1:]


@st.cache(suppress_st_warning=True)
def load_embeddings(name):
    # load embeddings
    with open(name, 'rb') as file:
        embeddings = pickle.load(file)
        file.close()
    return embeddings


@st.cache(suppress_st_warning=True)
def load_items():
    # load items
    return pd.read_csv('items.csv')


item_embeddings = load_embeddings('item_embeddings.pkl')
items = load_items()
search_graph_item = nmslib.init()
search_graph_item.loadIndex("item_graph.hnsw")

# number of recommendations
n_recommends = 10

# find nearest items
st.title("Recommender for items")
item_values = list(items.item_id)
input_str = st.text_input('Item_id (0 - 41319)', '100')
item_for_search = int(input_str)
if item_for_search in item_values:
    title = get_titles([item_for_search], items)
    st.write("Item title:")
    st.write(title.title)
    nearest_item = nearest(int(item_for_search),
                           item_embeddings, search_graph_item, n_recommends)
    answer = get_titles(nearest_item, items)
    "Recommendations: "
    st.write(answer)
else:
    st.write("Sorry, item_id =" + " {" + input_str + "} " + "not found")
