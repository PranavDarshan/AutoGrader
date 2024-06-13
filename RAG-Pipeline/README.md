# Creating the RAG pipeline

This repository contains a Retrieval-Augmented Generation (RAG) pipeline that is trained using the `all-MiniLM-L6-v2` model. The pipeline stores the embeddings of an operating system textbook in a FAISS vector store, chunked page-wise.

## Introduction

The RAG pipeline is designed to enhance the capabilities of a language model by combining it with a retrieval mechanism. The `all-MiniLM-L6-v2` model is used to generate embeddings for each page of an operating system textbook. These embeddings are then stored in a FAISS vector store, allowing for efficient similarity search and retrieval.\

The pdf version of the textbook used for this purpose is also enclosed withing this repository!
