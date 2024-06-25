from collections import Counter

def analyze_chunk_size_overlap(chunks):
    sizes = []
    overlaps = []

    # Iterate through the chunks, ignoring the last one for overlap calculation
    for i in range(len(chunks) - 1):
        current_chunk = chunks[i]
        next_chunk = chunks[i + 1]

        # Calculate the size of the current chunk and add it to the list
        size_of_chunk = len(current_chunk)
        sizes.append(size_of_chunk)

        # Find the overlap by checking how many characters at the end of the current
        # chunk appear at the start of the next chunk
        overlap = 0
        # Set the maximum possible overlap to be the length of the shorter chunk
        max_overlap = min(size_of_chunk, len(next_chunk))

        # Check for overlap from 1 up to the maximum possible overlap
        for j in range(1, max_overlap + 1):
            if current_chunk[-j:] == next_chunk[:j]:
                overlap = j

        # Add the overlap size to the list
        overlaps.append(overlap)

    # Find the most common size and overlap
    chunk_size = Counter(sizes).most_common(1)[0][0]
    chunk_overlap = Counter(overlaps).most_common(1)[0][0]

    return chunk_size, chunk_overlap


# # Run the function and print the results
# common_size, common_overlap = analyze_chunk_size_overlap(list_sample_text)
# print(f"Most common chunk size: {common_size}")
# print(f"Most common overlap: {common_overlap}")