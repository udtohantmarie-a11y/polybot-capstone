# Distance Metric Comparison Report
**Project:** PolyBot: A RAG-based Campus Tourism & History Guide
**Dataset:** TPC Student Handbook v.04

## Overview
A vector database requires a precise mathematical definition of "similar" to retrieve the correct document chunks for a Retrieval-Augmented Generation (RAG) pipeline[cite: 3]. This report compares three distance metrics applied to our TPC Student Handbook dataset to determine the most effective method for semantic retrieval.

## 1. Cosine Similarity
Cosine similarity measures the angle between two vectors, ignoring their magnitude[cite: 3].
*   **Formula:** $cosine\_similarity(A,B)=(A\cdot B)/(||A||\times||B||)$[cite: 5]
*   **Characteristics:** The result ranges from -1 (opposite direction/meaning) to 1 (identical direction/meaning), with values near 0 indicating unrelated content[cite: 3, 5].
*   **Analysis on Dataset:** When querying "What is the uniform policy?", this metric accurately retrieves the section detailing the "TALIBON POLYTECHNIC COLLEGE SCHOOL UNIFORM" regardless of whether the handbook chunk is a short sentence or a long paragraph.
*   **Best For:** It is the standard default for text embeddings and semantic search because it measures meaning-similarity independent of how "strongly worded" or long a passage is[cite: 3].

## 2. Euclidean Distance (L2)
This metric calculates the straight-line distance between two vector endpoints in space[cite: 3].
*   **Formula:** $d(A,B)=\sqrt{\sum_{i=1}^{n}(A_i-B_i)^2}$
*   **Characteristics:** A smaller value indicates that the vectors are more similar[cite: 3]. It is highly sensitive to the magnitude (overall length) of the vectors.
*   **Analysis on Dataset:** Querying "grading system" might artificially favor shorter, densely packed text chunks over the longer, comprehensive explanations of the TPC grading matrix, occasionally missing the best context.
*   **Best For:** Cases where vector magnitude carries meaningful information, rather than just semantic text retrieval[cite: 3].

## 3. Dot Product
The dot product is the raw product of two vectors' magnitudes and the cosine of the angle between them[cite: 3].
*   **Formula:** $A\cdot B=\sum_{i=1}^{n}A_i B_i$
*   **Characteristics:** It is highly sensitive to vector length[cite: 3]. If the embeddings are already normalized to unit length, the dot product will yield the exact same ranking as cosine similarity.
*   **Analysis on Dataset:** Without normalization, this metric might skew results toward longer document chunks in the handbook, even if they are only marginally related to a user's short query.
*   **Best For:** Recommendation systems or when embeddings are strictly normalized to unit length[cite: 3].

## Recommendation
For PolyBot, **Cosine Similarity** is the recommended distance metric. Since our RAG knowledge base relies on the TPC Student Handbook, the chunks vary significantly in length. Cosine similarity normalizes these differences, ensuring that retrieval is based strictly on the semantic meaning of the student's query rather than the length of the text chunk[cite: 3, 5].