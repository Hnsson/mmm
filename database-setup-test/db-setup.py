from cassandra.cluster import Cluster
import cassio
from sentence_transformers import SentenceTransformer

from chunkers.chunker_1 import chunk_pdf

import uuid

cluster = Cluster(["172.17.0.2"])
session = cluster.connect('my_keyspace')


# Load HuggingModel (e.g., 'all'MiniLM-L6-v2')
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')






# Maybe used in chunking where the same bytes (same string i.e. source) will always return the same UUID
def get_id_from_source(source_url):
    return uuid.uuid5(uuid.NAMESPACE_DNS, source_url)

def embed_prompt(prompt):
    return model.encode(prompt).tolist()



# Method to insert data into cassandra
def insert_into_cassandra(document_id, chunk, embedding, source_url):
    query = """
        INSERT INTO embeddings (id, new_embedding, document_chunk, source, embedding_type, metadata, created_at, document_id)
        VALUES (uuid(), %s, %s, %s, 'text', {'source': %s, 'author': 'Emil'}, toTimestamp(now()), %s)
        """

    session.execute(query, (embedding, chunk, source_url, source_url, document_id))
    print(f"Stored chunk: '{chunk}' with embedding: {embedding[:5]}...")





# Will be replaced with a real chunker. This just adds manual chunks to the database and sources that doesn't exists
def store_document_in_cassandra(source_url):
    document_id = get_id_from_source(source_url)
    chunks = chunk_pdf(source_url)
    for chunk in chunks:
        embedding = model.encode(chunk).tolist()

        insert_into_cassandra(document_id, chunk, embedding, source_url)

# store_document_in_cassandra('assets/harry_potter_1.pdf')




def search_similar_documents(prompt, keyspace='my_keyspace', table="embeddings",top_k=3):
    # Step 1: Embed the search prompt
    query_embedding = embed_prompt(prompt)

    # Step 2: Perform vector search using cosine similarity
    query = f"""
        SELECT id, document_chunk, source, new_embedding
        FROM {keyspace}.{table}
        ORDER BY new_embedding ANN OF {query_embedding}
        LIMIT {top_k};
    """

    rows = session.execute(query)

    results = []
    for row in rows:
        result = {
            'id': row.id,
            'document_chunk': row.document_chunk,
            'source': row.source
        }
        results.append(result)


    return results



if __name__ == '__main__':
    #-- Define the prompt
    print("\n" + "="*85)
    # print("Type a prompt. For example \x1B[3m'How old is Emil?', 'What football team does Emil like?'\x1B[0")
    # print("="*85)
    prompt = input("Enter your prompt: ")
    # What was Rons result on the exam?

    #-- Perform the search
                                    #  prompt, keyspace, table, number of nearest neighbors
    results = search_similar_documents(prompt, 'my_keyspace', 'embeddings', 3)

    #-- Print the prompt and result with improved formatting
    print("\n" + "="*50)
    print(f"Prompt: {prompt}")
    print("="*50)

    if results:
        for result in results:
            print(f"Document ID    : {result['id']}")
            print(f"Document Chunk : {result['document_chunk']}")
            print(f"Source         : {result['source']}")
            print("="*50)
        # top_result = results[0]
        # print(f"\nBest Match:")
        # print(f"Document ID    : {top_result['id']}")
        # print(f"Document Chunk : {top_result['document_chunk']}")
        # print(f"Source         : {top_result['source']}")
        # print("="*50)


        # print(f"\nSecond Result:")
        # print(f"Document ID    : {results[1]['id']}")
        # print(f"Document Chunk : {results[1]['document_chunk']}")
        # print(f"Source         : {results[1]['source']}")
        # print("="*50)
    else:
        print("\nNo matching results found.")
        print("="*50)
