# === FILE: memory_store.py ===
def _text_to_embedding(self, text: str):
emb = embedder.encode([text], show_progress_bar=False, convert_to_numpy=True)
return emb[0]


def add_meeting(self, meeting_id: str, text: str, meta: Dict[str, Any] = None):
if meta is None:
meta = {}
timestamp = int(time.time())
embedding = self._text_to_embedding(text)
self.index.add(np.array([embedding]).astype('float32'))
self.embeddings.append(embedding)
self.metadatas.append({"meeting_id": meeting_id, "text": text, "meta": meta, "ts": timestamp})
return {"meeting_id": meeting_id}


def query(self, query_text: str, k: int = 3):
if len(self.metadatas) == 0:
return []
q_emb = self._text_to_embedding(query_text).astype('float32').reshape(1, -1)
D, I = self.index.search(q_emb, k)
results = []
for dist, idx in zip(D[0], I[0]):
if idx < 0 or idx >= len(self.metadatas):
continue
md = self.metadatas[idx]
results.append({"meeting_id": md["meeting_id"], "text": md["text"], "score": float(dist), "meta": md.get("meta", {})})
return results


def compact_old_meetings(self, keep_top_n: int = 5):
total = len(self.metadatas)
if total <= keep_top_n:
return {"compacted": 0, "total": total}
sorted_idx = sorted(range(total), key=lambda i: self.metadatas[i]["ts"])
to_compact = sorted_idx[: max(0, total - keep_top_n)]
compacted_count = 0
for idx in to_compact:
md = self.metadatas[idx]
orig_text = md["text"]
summary = self._extractive_summary(orig_text, n_sentences=2)
new_emb = self._text_to_embedding(summary)
self.metadatas[idx]["text"] = summary
self.embeddings[idx] = new_emb
compacted_count += 1
emb_arr = np.array(self.embeddings).astype('float32')
self.index = faiss.IndexFlatL2(self.dim)
if len(emb_arr) > 0:
self.index.add(emb_arr)
return {"compacted": compacted_count, "total": total}


def _extractive_summary(self, text: str, n_sentences: int = 2):
sents = re.split(r'(?<=[.!?])\s+', text.strip())
if len(sents) <= n_sentences:
return text.strip()
sent_embs = embedder.encode(sents, show_progress_bar=False, convert_to_numpy=True)
centroid = np.mean(sent_embs, axis=0, keepdims=True)
dists = np.linalg.norm(sent_embs - centroid, axis=1)
top_idx = np.argsort(dists)[:n_sentences]
chosen = [sents[i].strip() for i in sorted(top_idx)]
return " ".join(chosen)


def dump_index_summary(self):
return [{"meeting_id": md["meeting_id"], "text_preview": md["text"][:200], "ts": md["ts"]} for md in self.metadatas]


# instantiate a default memory store for convenience
memory = MemoryStore()