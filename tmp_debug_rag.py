from src.rag.pipeline import initialize_rag
from src.rag.rag_service import rag_query

try:
    qa_chain, _ = initialize_rag(document_id=None)
    print('initialized', type(qa_chain))
    print(rag_query(qa_chain, 'what is accuracy and interpretability in machine learning'))
except Exception as e:
    import traceback
    traceback.print_exc()
