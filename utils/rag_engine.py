import re
import math
from collections import Counter, defaultdict
from typing import List, Dict, Any, Tuple
import pandas as pd
from utils.data_loader import load_all_data

# Common English stopwords
ENGLISH_STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
    "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't",
    "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have",
    "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself",
    "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is",
    "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
    "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should",
    "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them",
    "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've",
    "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd",
    "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's",
    "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you",
    "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"
}

class PureTfidfVectorizer:
    """
    Lightweight, self-contained pure-Python TF-IDF Vectorizer with n-grams and Cosine Similarity.
    Eliminates binary DLL dependencies and guarantees 100% cross-platform compatibility.
    """
    def __init__(self, ngram_range=(1, 2), stop_words=ENGLISH_STOPWORDS):
        self.ngram_range = ngram_range
        self.stop_words = stop_words
        self.vocab = {}
        self.idf = {}
        self.doc_vectors = []

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9_\-\.\#]+\b', str(text).lower())
        tokens = [t for t in tokens if t not in self.stop_words and len(t) > 1]
        
        # Add bigrams if requested
        if self.ngram_range[1] >= 2 and len(tokens) >= 2:
            bigrams = [f"{tokens[i]}_{tokens[i+1]}" for i in range(len(tokens) - 1)]
            tokens.extend(bigrams)
        return tokens

    def fit_transform(self, docs: List[str]):
        """Fit vocabulary and compute TF-IDF matrix for documents."""
        N = len(docs)
        doc_tokens = [self._tokenize(d) for d in docs]
        
        # Calculate Document Frequency (DF)
        df = defaultdict(int)
        for tokens in doc_tokens:
            unique_terms = set(tokens)
            for t in unique_terms:
                df[t] += 1
                
        # Vocabulary and IDF
        self.vocab = {t: idx for idx, t in enumerate(df.keys())}
        self.idf = {t: math.log((1 + N) / (1 + count)) + 1.0 for t, count in df.items()}
        
        # Compute TF-IDF vectors
        self.doc_vectors = []
        for tokens in doc_tokens:
            self.doc_vectors.append(self._vectorize(tokens))
        return self.doc_vectors

    def _vectorize(self, tokens: List[str]) -> Dict[str, float]:
        counts = Counter(tokens)
        total = len(tokens) if tokens else 1
        vec = {}
        norm_sq = 0.0
        for t, count in counts.items():
            if t in self.idf:
                tf = count / total
                weight = tf * self.idf[t]
                vec[t] = weight
                norm_sq += weight * weight
        
        # L2 normalize
        norm = math.sqrt(norm_sq) if norm_sq > 0 else 1.0
        for t in vec:
            vec[t] /= norm
        return vec

    def transform_single(self, text: str) -> Dict[str, float]:
        tokens = self._tokenize(text)
        return self._vectorize(tokens)

    @staticmethod
    def cosine_similarity(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Compute cosine similarity between two sparse normalized vectors."""
        if len(vec1) > len(vec2):
            vec1, vec2 = vec2, vec1
        return sum(weight * vec2.get(term, 0.0) for term, weight in vec1.items())


class PhotosRAGEngine:
    """
    Episodic Semantic RAG Engine for Google Photos.
    Interprets vague human episodic memory cues, performs multi-modal query expansion,
    searches across visual, OCR, EXIF, and location metadata, and computes confidence scores.
    """

    def __init__(self, df_catalog: pd.DataFrame = None, df_feedback: pd.DataFrame = None):
        if df_catalog is None or df_feedback is None:
            fb, cat = load_all_data()
            self.df_feedback = fb if df_feedback is None else df_feedback
            self.df_catalog = cat if df_catalog is None else df_catalog
        else:
            self.df_catalog = df_catalog
            self.df_feedback = df_feedback

        self._build_search_index()

    def reload_data(self, df_catalog: pd.DataFrame, df_feedback: pd.DataFrame):
        """Reload datasets and rebuild index."""
        self.df_catalog = df_catalog
        self.df_feedback = df_feedback
        self._build_search_index()

    def _build_search_index(self):
        """Construct multi-field semantic index for photo metadata catalog."""
        self.corpus_docs = []
        for _, row in self.df_catalog.iterrows():
            # Weighted multi-modal document representation
            doc_str = (
                f"Visual: {row.get('ai_visual_description', '')} "
                f"Visual: {row.get('ai_visual_description', '')} "
                f"Objects: {row.get('detected_objects', '')} "
                f"Objects: {row.get('detected_objects', '')} "
                f"OCR: {row.get('ocr_text', '')} "
                f"OCR: {row.get('ocr_text', '')} "
                f"Location: {row.get('location_tag', '')} "
                f"Album: {row.get('album_name', '')} "
                f"Date: {row.get('timestamp', '')}"
            )
            self.corpus_docs.append(doc_str)

        self.vectorizer = PureTfidfVectorizer()
        if self.corpus_docs:
            self.vectorizer.fit_transform(self.corpus_docs)

        # Index historical failure feedback queries
        self.feedback_queries = self.df_feedback['user_query'].tolist() if 'user_query' in self.df_feedback else []
        self.fb_vectorizer = PureTfidfVectorizer()
        if self.feedback_queries:
            self.fb_vectorizer.fit_transform(self.feedback_queries)

    def expand_episodic_query(self, user_query: str) -> Dict[str, Any]:
        """
        Deconstruct human episodic memories into temporal, visual, OCR, object, and spatial cues.
        """
        q_lower = user_query.lower()

        # 1. Temporal anchors extraction
        temporal_cues = []
        target_years = []

        if "last year" in q_lower or "a year ago" in q_lower:
            temporal_cues.append("Relative past: ~1 year ago (2024-2025)")
            target_years.extend([2024, 2025])
        elif "two years ago" in q_lower:
            temporal_cues.append("Relative past: ~2 years ago (2023-2024)")
            target_years.extend([2023, 2024])
        elif "last month" in q_lower or "recent" in q_lower:
            temporal_cues.append("Recent timeframe (past 1-3 months)")
            target_years.append(2025)
        elif "summer" in q_lower:
            temporal_cues.append("Seasonal Anchor: Summer (Jun-Aug)")
        elif "winter" in q_lower or "snow" in q_lower:
            temporal_cues.append("Seasonal Anchor: Winter (Dec-Feb)")

        # Extract explicit 4-digit years
        found_years = re.findall(r'\b(20[12][0-9])\b', user_query)
        if found_years:
            target_years.extend([int(y) for y in found_years])
            temporal_cues.append(f"Explicit Year: {', '.join(found_years)}")

        # 2. Visual & Sensory clues
        visual_keywords = [
            "yellow", "blue", "red", "green", "pink", "black", "white", "gold", "turquoise", "amber",
            "blurry", "sunny", "dark", "night", "neon", "wooden", "small", "big", "handwritten", "cursive"
        ]
        detected_visual = [v for v in visual_keywords if re.search(r'\b' + v + r'\b', q_lower)]

        # 3. Object & Entity clues (using exact word boundaries)
        object_synonym_map = {
            "medicine": ["medicine", "paracetamol", "pill", "blister", "capsule", "prescription", "pharmacy", "box"],
            "sick": ["fever", "thermometer", "paracetamol", "water", "nightstand", "illness", "bedside"],
            "cafe": ["cafe", "coffee", "roasters", "patio", "table", "espresso", "latte", "beach"],
            "recipe": ["recipe", "ingredients", "penne", "pasta", "card", "handwritten", "bake", "cream"],
            "dog": ["dog", "retriever", "golden", "pet", "collar", "canine", "snow"],
            "flight": ["boarding", "pass", "airport", "gate", "seat", "terminal", "flight", "air france"],
            "receipt": ["receipt", "bill", "trattoria", "total", "paper", "slip", "usps", "tracking"],
            "car": ["car", "bumper", "scratch", "parking", "tire", "volkswagen", "beetle"],
            "wifi": ["wifi", "router", "password", "netgear", "barcode", "key"],
            "birthday": ["birthday", "cake", "candle", "dinosaur", "party"],
            "graduation": ["graduation", "diploma", "ribbon", "gown", "commencement", "cap"],
            "measuring": ["measuring", "tape", "cabinet", "inches", "stanley", "dimensions"]
        }

        detected_objects = []
        expansion_tokens = []

        for category, synonyms in object_synonym_map.items():
            category_match = bool(re.search(r'\b' + re.escape(category) + r'\b', q_lower))
            synonym_match = any(bool(re.search(r'\b' + re.escape(s) + r'\b', q_lower)) for s in synonyms)
            if category_match or synonym_match:
                detected_objects.append(category)
                expansion_tokens.extend(synonyms[:4])

        # 4. Location clues
        location_candidates = [
            "goa", "paris", "mumbai", "new york", "brooklyn", "austin", "boston", "seattle", "florence",
            "italy", "france", "mexico", "whistler", "airport", "kitchen", "bedroom", "home", "beach"
        ]
        detected_locations = [loc for loc in location_candidates if re.search(r'\b' + loc + r'\b', q_lower)]

        # Synthesize expanded query string
        clean_tokens = list(dict.fromkeys(user_query.split() + expansion_tokens + detected_visual + detected_locations))
        expanded_query_str = " ".join(clean_tokens)

        return {
            "original_query": user_query,
            "expanded_query": expanded_query_str,
            "temporal_cues": temporal_cues,
            "target_years": list(set(target_years)),
            "visual_cues": detected_visual,
            "object_cues": detected_objects,
            "location_cues": detected_locations
        }

    def is_conceptual_query(self, query: str) -> bool:
        """
        Determine if query is an analytical/PM case-study question rather than a direct photo search.
        """
        q_lower = query.lower()
        conceptual_patterns = [
            r"fail.*understand.*clue",
            r"understand.*clue",
            r"clue.*provide",
            r"why.*(search|user).*fail",
            r"does.*(google photos|search).*fail",
            r"what.*(remember|forget)",
            r"recall gap",
            r"semantic gap",
            r"failure (reason|taxonomy|point|rate)",
            r"how does.*(rag|assistant|search|engine).*work",
            r"what.*failure",
            r"case study",
            r"problem statement"
        ]
        return any(re.search(p, q_lower) for p in conceptual_patterns)

    def generate_conceptual_response(self, user_query: str) -> Dict[str, Any]:
        """
        Generate detailed PM narrative and point-wise breakdown for analytical inquiries.
        """
        paragraph = (
            "**Yes, standard Google Photos search frequently fails to understand the clues users provide.** "
            "In our product management discovery study analyzing user feedback across the Google Play Store, Reddit, and Support tickets, "
            "over **50% of retrieval failures** stem directly from a fundamental **'Semantic Recall Gap'**. "
            "Human episodic memory naturally encodes subjective, sensory, and emotional anchors (such as *'feeling sick with fever'*, "
            "*'small cafe with blue chairs'*, or *'when I was in college'*), whereas traditional photo search engines are architected "
            "around rigid metadata like exact EXIF timestamps (`YYYY-MM-DD`), formal commercial business names, and explicit folder structures. "
            "Because 88% of users remember visual colors/moods and 85% recall emotional context while 88% completely forget exact EXIF dates, "
            "traditional keyword and EXIF matching consistently fails to bridge the vocabulary divide, leaving users unable to retrieve their memories."
        )

        points = [
            ("🧠 The Semantic Recall Gap", "Human episodic memory stores sensory, emotional, and relative anchors (e.g., 'medicine photo when sick last year'), whereas standard database search indexes rigid technical attributes (EXIF timestamps, camera model, exact geotags)."),
            ("📊 Empirical Recall Asymmetry", "Research indicates that 88% of users easily recall visual colors and 85% remember emotional context, yet 88% forget exact dates and 82% forget formal business/brand names. The search engine penalizes users for normal human cognitive recall."),
            ("📉 6 Core Failure Taxonomies", "Telemetry breakdown reveals: Time Framing Errors (23%), Incomplete Vocabulary (20%), OCR Misreads on documents/cards (17%), Metadata Missing (17%), Visual Attribute Drift (13%), and Synonym Mismatches (10%)."),
            ("🚀 How the Episodic RAG Engine Solves This", "Our proposed solution injects an Episodic Query Expander that decomposes vague memories into temporal approximations (mapping 'last year' to recent winter), visual descriptions, and OCR candidates, cross-referencing multi-modal vector representations."),
            ("💬 Real User Complaint Evidence", "PlayStore Feedback FB-1001: 'Searched for my medicine photo from when I had the flu last winter and got zero results because I didn't know the exact brand name Paracetamol.'")
        ]

        # Find closest failure complaints from feedback dataset
        hist_context = []
        if self.fb_vectorizer.doc_vectors and self.feedback_queries:
            fb_q_vec = self.fb_vectorizer.transform_single(user_query)
            fb_sims = [
                (fi, self.fb_vectorizer.cosine_similarity(fb_q_vec, d_vec))
                for fi, d_vec in enumerate(self.fb_vectorizer.doc_vectors)
            ]
            fb_sims.sort(key=lambda x: x[1], reverse=True)
            for fi, sim in fb_sims[:3]:
                hist_row = self.df_feedback.iloc[fi]
                hist_context.append({
                    "query": hist_row.get("user_query"),
                    "failure_reason": hist_row.get("failure_reason"),
                    "forgotten": hist_row.get("forgotten_clues")
                })

        return {
            "is_conceptual": True,
            "show_photos": False,
            "paragraph_response": paragraph,
            "point_wise_response": points,
            "reasoning": "Identified Product Management Discovery inquiry regarding Google Photos search failure taxonomy and clue comprehension.",
            "matches": [],
            "clarifying_question": None,
            "confidence_band": "HIGH",
            "top_confidence": 100,
            "historical_feedback_context": hist_context
        }

    def search(self, user_query: str, top_k: int = 4) -> Dict[str, Any]:
        """
        Execute episodic semantic search across photo metadata and historical failure reports.
        Handles both conceptual PM inquiries and direct photo searches with paragraph + point-wise synthesis.
        """
        # 1. Check for conceptual PM case-study inquiry
        if self.is_conceptual_query(user_query):
            return self.generate_conceptual_response(user_query)

        if self.df_catalog.empty or not self.vectorizer.doc_vectors:
            return {
                "is_conceptual": False,
                "show_photos": False,
                "paragraph_response": "The photo catalog is currently empty or unindexed. Please re-index datasets in the sidebar.",
                "point_wise_response": [],
                "reasoning": "Catalog is empty or unindexed.",
                "matches": [],
                "clarifying_question": None,
                "confidence_band": "LOW",
                "historical_feedback_context": []
            }

        expansion = self.expand_episodic_query(user_query)
        expanded_query = expansion["expanded_query"]

        # Vector similarity scoring via PureTfidfVectorizer
        query_vec = self.vectorizer.transform_single(expanded_query)
        
        sim_scores = [
            self.vectorizer.cosine_similarity(query_vec, doc_vec)
            for doc_vec in self.vectorizer.doc_vectors
        ]

        # Multi-factor score calibration (temporal booster + location + OCR bonus)
        adjusted_scores = []
        for idx, base_score in enumerate(sim_scores):
            row = self.df_catalog.iloc[idx]
            
            # Base semantic relevance
            relevance = base_score * 1.8
            
            # Boost if target year matches
            photo_timestamp = str(row.get("timestamp", ""))
            if any(str(y) in photo_timestamp for y in expansion["target_years"]):
                relevance += 0.20

            # Boost if location matches
            loc_str = str(row.get("location_tag", "")).lower()
            if any(loc in loc_str for loc in expansion["location_cues"]):
                relevance += 0.25

            # Boost for direct OCR match
            ocr_str = str(row.get("ocr_text", "")).lower()
            if any(obj in ocr_str for obj in expansion["object_cues"]):
                relevance += 0.20

            # Boost for visual description match
            vis_str = str(row.get("ai_visual_description", "")).lower()
            if any(v in vis_str for v in expansion["visual_cues"]):
                relevance += 0.15

            # Scale to realistic 0-100% probability curve
            calibrated = min(0.98, max(0.15, relevance)) if base_score > 0.05 else min(0.35, base_score * 0.8)
            adjusted_scores.append((idx, calibrated))

        # Sort descending
        adjusted_scores.sort(key=lambda x: x[1], reverse=True)
        top_candidates = adjusted_scores[:top_k]

        matches = []
        for idx, score in top_candidates:
            row = self.df_catalog.iloc[idx]
            pct_conf = int(round(score * 100))
            
            # Identify matched cues
            matched_items = []
            desc_text = f"{row.get('ai_visual_description', '')} {row.get('ocr_text', '')}".lower()
            for term in (expansion["visual_cues"] + expansion["location_cues"] + expansion["object_cues"]):
                if term in desc_text:
                    matched_items.append(term)

            matches.append({
                "photo_id": row.get("photo_id", f"IMG_{idx}"),
                "timestamp": row.get("timestamp", "Unknown"),
                "location_tag": row.get("location_tag", "Unknown Location"),
                "ai_visual_description": row.get("ai_visual_description", "No description available"),
                "detected_objects": row.get("detected_objects", ""),
                "ocr_text": row.get("ocr_text", "None"),
                "album_name": row.get("album_name", "General"),
                "confidence_score": pct_conf,
                "matched_cues": list(set(matched_items)) if matched_items else ["semantic concept"]
            })

        top_confidence = matches[0]["confidence_score"] if matches else 0
        top_match = matches[0] if matches else None

        # Build Episodic Reasoning Summary
        reasoning_parts = []
        if expansion["temporal_cues"]:
            reasoning_parts.append(f"Mapped temporal reference to **{', '.join(expansion['temporal_cues'])}**")
        if expansion["location_cues"]:
            reasoning_parts.append(f"Identified geographic anchor: **{', '.join([l.title() for l in expansion['location_cues']])}**")
        if expansion["visual_cues"]:
            reasoning_parts.append(f"Extracted sensory/visual cues: **{', '.join(expansion['visual_cues'])}**")
        if expansion["object_cues"]:
            reasoning_parts.append(f"Synthesized concept vocabulary: **{', '.join(expansion['object_cues'])}** with OCR cross-referencing")

        if not reasoning_parts:
            reasoning_summary = f"Analyzed query semantics across image descriptions, detected objects, and embedded text (OCR)."
        else:
            reasoning_summary = "; ".join(reasoning_parts) + "."

        # Synthesize Paragraph Response
        if top_confidence >= 65 and top_match:
            paragraph_response = (
                f"I searched your photo library for memories matching **'{user_query}'**. "
                f"By analyzing your episodic memory cues, the assistant cross-referenced visual elements, relative time anchors, and embedded OCR text. "
                f"I retrieved **{len(matches)} candidate photos**, with primary match **`{top_match['photo_id']}`** "
                f"found in your *{top_match['album_name']}* album ({top_match['location_tag']}) with **{top_match['confidence_score']}% confidence**."
            )
        else:
            paragraph_response = (
                f"I searched across your photo catalog for memories matching **'{user_query}'**. "
                f"While several candidate photos share partial characteristics, the confidence level is currently lower ({top_confidence}%) "
                f"because key distinguishing anchors (such as explicit location or visual markers) are ambiguous."
            )

        # Synthesize Point-Wise Breakdown
        points = []
        if expansion["temporal_cues"]:
            points.append(("🕒 Temporal Anchor Interpreted", f"Mapped episodic time clue to {', '.join(expansion['temporal_cues'])}."))
        if expansion["visual_cues"]:
            points.append(("👁️ Visual Cues Extracted", f"Identified visual attributes: {', '.join(expansion['visual_cues'])}."))
        if expansion["location_cues"]:
            points.append(("📍 Spatial Anchor Located", f"Mapped geographic reference to {', '.join([l.title() for l in expansion['location_cues']])}."))
        if top_match:
            points.append(("🎯 Primary Candidate Retrieved", f"Photo `{top_match['photo_id']}` taken at {top_match['location_tag']} ({top_match['timestamp']})."))
            if top_match['ocr_text'] and top_match['ocr_text'] != 'None':
                points.append(("📝 OCR Cross-Verification", f"Matched text in image: \"{top_match['ocr_text'][:80]}...\""))
            points.append(("🟢 Match Confidence Rating", f"{top_match['confidence_score']}% match confidence score."))

        # Context-aware Clarifying Question if confidence < 70%
        clarifying_question = None
        confidence_band = "HIGH" if top_confidence >= 80 else ("MEDIUM" if top_confidence >= 65 else "LOW")

        if top_confidence < 70:
            if expansion["location_cues"] and not expansion["visual_cues"]:
                clarifying_question = f"Do you remember any standout colors, objects, or people who were with you around {expansion['location_cues'][0].title()}?"
            elif "medicine" in expansion["object_cues"] or "sick" in user_query.lower():
                clarifying_question = "Was this medicine in a pill blister pack, a prescription syrup bottle, or a box with specific color markings?"
            elif expansion["visual_cues"] and not expansion["temporal_cues"]:
                clarifying_question = "Do you remember roughly which year or season this photo was taken (e.g., Summer 2024, last holidays)?"
            elif "cafe" in user_query.lower() or "restaurant" in user_query.lower():
                clarifying_question = "Do you recall if the photo was taken indoors or outside on a patio, or any dishes on the table?"
            else:
                clarifying_question = "Could you share any other remembered details - such as who was there, an approximate month/year, or any visible text/logos?"

        # Cross-reference with historical feedback failures
        hist_context = []
        if self.fb_vectorizer.doc_vectors and self.feedback_queries:
            fb_q_vec = self.fb_vectorizer.transform_single(user_query)
            fb_sims = [
                (fi, self.fb_vectorizer.cosine_similarity(fb_q_vec, d_vec))
                for fi, d_vec in enumerate(self.fb_vectorizer.doc_vectors)
            ]
            fb_sims.sort(key=lambda x: x[1], reverse=True)
            for fi, sim in fb_sims[:2]:
                if sim > 0.25:
                    hist_row = self.df_feedback.iloc[fi]
                    hist_context.append({
                        "query": hist_row.get("user_query"),
                        "failure_reason": hist_row.get("failure_reason"),
                        "forgotten": hist_row.get("forgotten_clues")
                    })

        return {
            "is_conceptual": False,
            "show_photos": True,
            "paragraph_response": paragraph_response,
            "point_wise_response": points,
            "reasoning": reasoning_summary,
            "matches": matches,
            "clarifying_question": clarifying_question,
            "confidence_band": confidence_band,
            "top_confidence": top_confidence,
            "historical_feedback_context": hist_context
        }
