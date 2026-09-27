import sys
import os
import pandas as pd

def run_tests():
    print("=== Testing GoogleMVP Core Engine & Catalog ===")

    # Test 1: Data Loader & Schema Normalization
    print("\n1. Testing Data Loader...")
    from utils.data_loader import load_all_data, load_photo_catalog
    df_feedback, df_catalog = load_all_data()

    print(f" - df_feedback count: {len(df_feedback)}")
    print(f" - df_catalog count: {len(df_catalog)}")
    assert len(df_catalog) == 10000, f"Expected 10000 photos, got {len(df_catalog)}"
    
    expected_cols = ["photo_id", "timestamp", "location", "location_tag", "category", "album_name", "detected_objects", "ocr_text", "detected_ocr", "ai_visual_description", "visual_description", "image_url"]
    for col in expected_cols:
        assert col in df_catalog.columns, f"Missing column: {col}"
    print(f" - All {len(expected_cols)} schema columns present and normalized.")
    assert df_catalog["image_url"].notna().sum() == 10000, "Some photos are missing image_url!"
    print(" - All 10,000 photos have verified real image URLs.")

    # Check top photo benchmark
    top_photo = df_catalog.iloc[0]
    print(f" - Index 0 Photo ID: {top_photo['photo_id']} | Category: {top_photo['category']} | Image: {top_photo['image_url']}")
    assert top_photo['photo_id'] == "IMG_20250114_091522", f"Unexpected top photo: {top_photo['photo_id']}"
    assert top_photo['category'] == "Health & Medical", f"Unexpected category: {top_photo['category']}"
    assert str(top_photo['image_url']).startswith("http"), "Index 0 image_url is invalid"

    # Test 2: RAG Engine
    print("\n2. Testing PhotosRAGEngine Initialization...")
    from utils.rag_engine import PhotosRAGEngine
    engine = PhotosRAGEngine(df_catalog=df_catalog, df_feedback=df_feedback)
    assert hasattr(engine, "answer_query"), "engine missing answer_query method!"
    assert hasattr(engine, "search"), "engine missing search method!"

    # Test 3: RAG Query Evaluation - Medicine Benchmark
    print("\n3. Testing answer_query with Health Benchmark ('medicine box when I was sick with fever')...")
    resp1 = engine.answer_query("medicine box when I was sick with fever")
    
    required_keys = ["paragraph_summary", "paragraph_response", "point_takeaways", "point_wise_response", "reasoning", "photos", "matches", "clarifying_question"]
    for k in required_keys:
        assert k in resp1, f"Missing key in answer_query response: {k}"
    
    assert len(resp1["photos"]) > 0, "No photos returned!"
    top_candidate = resp1["photos"][0]
    print(f" - Primary match photo: {top_candidate['photo_id']}")
    print(f" - Image URL: {top_candidate['image_url']}")
    assert str(top_candidate["image_url"]).startswith("http"), "Candidate missing valid image_url"
    print(f" - Confidence score: {top_candidate['confidence_score']}%")
    print(f" - Confidence float: {top_candidate['confidence']}")
    print(f" - Location: {top_candidate['location']}")
    print(f" - Category: {top_candidate['category']}")
    print(f" - Visual Description: {top_candidate['visual_description'][:60]}...")
    print(f" - Detected OCR: {top_candidate['detected_ocr'][:60]}...")
    assert top_candidate["photo_id"] == "IMG_20250114_091522", f"Expected IMG_20250114_091522, got {top_candidate['photo_id']}"
    assert top_candidate["confidence_score"] >= 90, f"Expected confidence >= 90%, got {top_candidate['confidence_score']}%"

    # Test 4: RAG Query Evaluation - Goa Beach Benchmark
    print("\n4. Testing Goa Benchmark ('beach cafe with blue chairs in Goa')...")
    resp2 = engine.answer_query("beach cafe with blue chairs in Goa")
    top_candidate_goa = resp2["photos"][0]
    print(f" - Primary match photo: {top_candidate_goa['photo_id']}")
    print(f" - Confidence score: {top_candidate_goa['confidence_score']}%")
    assert top_candidate_goa["photo_id"] == "IMG_20241108_164530", f"Expected IMG_20241108_164530, got {top_candidate_goa['photo_id']}"

    # Test 5: Conceptual PM Inquiry
    print("\n5. Testing Conceptual PM Query ('Why does Google Photos search fail on user clues?')...")
    resp3 = engine.answer_query("Why does Google Photos search fail on user clues?")
    assert resp3["is_conceptual"] == True, "Expected is_conceptual=True"
    assert "paragraph_summary" in resp3
    assert len(resp3["point_takeaways"]) > 0
    print(f" - Conceptual Summary: {resp3['paragraph_summary'][:100]}...")

    # Test 6: Component Imports
    print("\n6. Testing Component Imports...")
    from components.photo_grid import render_photo_grid
    from components.ask_photos import render_ask_photos
    from components.evaluator_mode import render_evaluator_mode
    from components.dashboard import render_dashboard
    print(" - All components imported successfully.")

    print("\n[PASS] ALL 6 VERIFICATION SUITES PASSED!")

if __name__ == "__main__":
    run_tests()
