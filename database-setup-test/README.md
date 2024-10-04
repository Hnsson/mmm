# Project Title: Question Answer Application (RAG + Cassandra Vector Store)

## Overview

This project implements a retrieval-augmented generation (RAG) system using a Cassandra database to store embeddings, enabling efficient vector searches. It utilizes Docker for database setup and Python for data handling and embedding operations.

## Table of Contents
- [1. Setup Cassandra Database with Docker](#1-setup-cassandra-database-with-docker)
- [2. Requirements for python application](#2-requirements-for-python-application)
- [3. Usage](#3-usage)
- [4. Example output](#4-example-output)

## 1. Setup Cassandra Database with Docker

To set up a Cassandra database, follow these steps:

1. Run the Cassandra container:
    ```bash
    docker run --name <container_name> -d cassandra:5.0-alpha2
    ```
2. Retrieve the container's IP address:
    ```bash
    docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_name>
    ```
    <em>(Remember this IP address for the Python application.)</em>
3. Access Cassandra's CQL shell:
    ```bash
    docker exec -it my-cassandra cqlsh
    ```
4. Create a keyspace:
    ```bash
    CREATE KEYSPACE <keyspace_name> WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
    ```
5. Use the keyspace:
    ```bash
    USE <keyspace_name>
    ```
6. Crate the table (and add a SAI indexing for ANN):
    ```
    CREATE TABLE IF NOT EXISTS <table_name> (
        id UUID PRIMARY KEY,
        embedding VECTOR<FLOAT, 384>,
        document_chunk TEXT,
        source TEXT,
        embedding_type TEXT,
        metadata MAP<TEXT, TEXT>,
        created_at TIMESTAMP,
        document_id UUID
    );

    CREATE CUSTOM INDEX ON <table_name>(embedding) USING 'org.apache.cassandra.index.sai.StorageAttachedIndex';
    ```

## 2. Requirements for python application
The package dependencies are in the [requirements.txt](requirements.txt) file and can be installed using:
```bash
pip install -r requirements.txt
```

## 3. Usage
1. **Set Up Docker**: Ensure you have Docker installed and run the Cassandra container as describe in Section 1.
2. **Run the Python Script**: Modify the database connection details and document storage as needed, then execute the script to interact with the database and perform searches.
3. **Input Prompts**: Follow the prompts to search for similar document chunks based on your input.

## 4. Example output
Here is two example runs of the application:

```text
=====================================================================================
Type a prompt. For example 'How old is Emil?', 'What football team does Emil like?'
Enter your prompt: How old is Emil?

==================================================
Prompt: How old is Emil?
==================================================

Best Match:
Document ID    : 41a8ce84-2671-4026-a806-530b5cfc36c8
Document Chunk : 'My name is Emil and I'm 22 years old.'
Source         : 'emils_life.txt'
==================================================
```

```text
=====================================================================================
Type a prompt. For example 'How old is Emil?', 'What football team does Emil like?'
Enter your prompt: How old is Emil?

==================================================
Prompt: What football team does Emil like?
==================================================

Best Match:
Document ID    : 41a8ce84-2671-4026-a806-530b5cfc36c8
Document Chunk : 'I like to watch football and my favorite team is Arsenal.'
Source         : 'emils_life.txt'
==================================================
```