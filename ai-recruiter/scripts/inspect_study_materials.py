with open('ai-recruiter/backend/app/services/textbooks/dsa_master.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("DSA_TEXTBOOK_MARKDOWN =")
print("Found DSA_TEXTBOOK_MARKDOWN at:", idx)
chunk = text[idx:idx+2000]
print(chunk.encode('ascii', errors='replace').decode('ascii'))
