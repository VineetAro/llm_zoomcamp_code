from ingest import load_faq_data, build_index

documents = load_faq_data()
index = build_index(documents)