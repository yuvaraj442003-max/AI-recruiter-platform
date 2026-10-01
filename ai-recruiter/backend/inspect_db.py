import psycopg2
conn = psycopg2.connect(host='localhost', port=5432, database='ai_recruiter', user='postgres', password='postgres234')
c = conn.cursor()
for t in ['screening_questions', 'candidate_invitations', 'candidate_shortlists', 'candidate_search_history', 'saved_candidate_searches']:
    c.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{t}' ORDER BY ordinal_position")
    print(f"{t}: {[r[0] for r in c.fetchall()]}")
conn.close()
