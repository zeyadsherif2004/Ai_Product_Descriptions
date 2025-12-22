# backend/src/main.py
import os
import sys
import logging
import structlog
import uuid
import asyncio
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends, WebSocket, WebSocketDisconnect, Request
from sqlalchemy.orm import Session
from src.database.deps import get_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import json
import io
from dotenv import load_dotenv

# Rate limiting imports
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

try:
    import sentry_sdk
    from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
except Exception:
    sentry_sdk = None
    SentryAsgiMiddleware = None

# Add backend directory to path for imports
THIS_DIR = Path(__file__).resolve().parent
BACKEND_DIR = THIS_DIR.parent
sys.path.insert(0, str(BACKEND_DIR))

# Load environment BEFORE importing modules that need it
load_dotenv(BACKEND_DIR / ".env")

from utils.helpers import ensure_dir, timestamp, safe_extract_json, validate_and_ensure_compliance, generate_fallback_bullets
from src.ai_pipeline import load_env, call_gemini_generate, build_gemini_prompt, row_to_dict, CostTracker, SafetyFilter
from src.seo_check import seo_evaluate

from src.auth.firebase import get_current_user
from src.payments.endpoints import router as payment_router
from src.payments.credit_service import CreditService, OperationType

# Initialize logging (structured JSON)
def setup_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=getattr(logging, log_level, logging.INFO))
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, log_level, logging.INFO)),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

setup_logging()

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI app
app = FastAPI(
    title="AI Product Descriptions API",
    description="API for generating AI-powered product descriptions",
    version="1.0.0"
)

# Add rate limiting exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware (env-driven)
cors_origins_env = os.getenv(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:3000",
)
ALLOW_ORIGINS = [o.strip() for o in cors_origins_env.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    # attach a request id for tracing
    req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = req_id
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    response.headers.setdefault("X-XSS-Protection", "0")
    response.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'",
    )
    response.headers.setdefault("X-Request-ID", req_id)
    return response

# Optional Sentry setup
SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN and sentry_sdk is not None:
    sentry_sdk.init(dsn=SENTRY_DSN, traces_sample_rate=0.05)
    if SentryAsgiMiddleware is not None:
        app.add_middleware(SentryAsgiMiddleware)

# Include payment router
app.include_router(payment_router)

# Global variables for model and components
model = None
cost_tracker = None
safety_filter = None
credit_service = None

def find_column(columns, synonyms):
    """
    Find the best matching column for given synonyms.
    Normalizes column names and returns the first match.
    """
    normalized_columns = {}
    for col in columns:
        # Normalize: lowercase, remove spaces, hyphens, underscores
        normalized = col.lower().replace(' ', '').replace('-', '').replace('_', '')
        normalized_columns[normalized] = col
    
    for synonym in synonyms:
        normalized_synonym = synonym.lower().replace(' ', '').replace('-', '').replace('_', '')
        if normalized_synonym in normalized_columns:
            return normalized_columns[normalized_synonym]
    
    return None

def process_csv_row(row, target_audience, columns, language_code="en"):
    """
    Process a CSV row using automatic column mapping and dynamic feature generation.
    """
    # Define synonyms for automatic mapping
    product_name_synonyms = ['title', 'name', 'product', 'productname', 'item', 'model']
    category_synonyms = ['category', 'type', 'department', 'group', 'collection']
    
    # Blocklist for columns that shouldn't be used as features
    feature_blocklist = ['id', 'sku', 'price', 'cost', 'url', 'image', 'images']
    
    # Find mapped columns
    product_name_col = find_column(columns, product_name_synonyms)
    category_col = find_column(columns, category_synonyms)
    
    # Fallback logic
    if not product_name_col:
        product_name_col = columns[0] if columns else "Unknown"
    
    if not category_col:
        category_col = "General"
    
    # Extract values
    product_name = str(row.get(product_name_col, "")).strip()
    category = str(row.get(category_col, "")).strip() if category_col != "General" else "General"
    
    # Generate features from all other columns
    feature_parts = []
    for col in columns:
        if col not in [product_name_col, category_col] and col.lower() not in feature_blocklist:
            value = str(row.get(col, "")).strip()
            if value:  # Only include non-empty values
                feature_parts.append(f"{col}: {value}")
    
    features = ". ".join(feature_parts) if feature_parts else ""
    
    # Log mapping decisions for debugging
    logging.info(f"Mapped '{product_name_col}' to 'product_name', '{category_col}' to 'category'")
    
    return {
        "id": str(row.get("id", "")).strip(),
        "sku": str(row.get("sku", "")).strip(),
        "title": product_name,
        "category": category.lower(),
        "features": features,
        "primary_keyword": str(row.get("primary_keyword", "")).strip(),
        "tone": str(row.get("tone", "")).strip(),
        "price": row.get("price", ""),
        "images": str(row.get("images", "")).strip(),
        "audience": target_audience,
        "languageCode": language_code
    }

@app.on_event("startup")
async def startup_event():
    """Initialize the AI model and components on startup"""
    global model, cost_tracker, safety_filter, credit_service
    
    try:
        # Load environment and initialize model
        conf = load_env(dry_run=False)  # Use real API key
        model = conf["model"]
        cost_tracker = CostTracker()
        safety_filter = SafetyFilter()
        credit_service = CreditService()
        
        # TEMPORARILY DISABLED FOR TESTING - Rate limiting for API calls
        # last_api_call_time = 0
        # MIN_API_INTERVAL = 2.0  # Minimum 2 seconds between API calls
        
        print("✅ AI Product Descriptions API started successfully")
        if model is not None:
            print(f"🤖 Model: {conf['model_name']} (Live mode)")
            print(f"🌡️  Temperature: {conf['temperature']}")
            print("✅ API key configured - ready for AI generation")
        else:
            print(f"🤖 Model: {conf['model_name']} (Dry-run mode)")
            print(f"🌡️  Temperature: {conf['temperature']}")
            print("⚠️  Running in dry-run mode - API key not configured")
            print("🔧 To fix: Set GEMINI_API_KEY environment variable with a valid API key")
        
        print("💳 Credit service initialized - rate limiting enabled")
        
        # Initialize subscription plans
        try:
            from src.payments.init_subscription_plans import init_subscription_plans
            init_subscription_plans()
            logging.info("Subscription plans initialized")
        except Exception as e:
            logging.warning(f"Failed to initialize subscription plans: {str(e)}")
        
    except Exception as e:
        logging.error(f"Failed to start API: {str(e)}")
        raise

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": timestamp()
    }

# Liveness and readiness probes
@app.get("/healthz")
def liveness():
    return {"status": "ok"}

@app.get("/readyz")
def readiness():
    # Try DB connection
    try:
        from app.db.session import engine
        with engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")
        db_ok = True
    except Exception:
        db_ok = False
    return {"status": "ok" if db_ok else "degraded", "db": db_ok}

@app.get("/auth/me")
async def auth_me(user = Depends(get_current_user)):
    """Auth test endpoint that returns Firebase user claims"""
    logging.info("🔐 Auth endpoint called - user authenticated successfully")
    # return only safe fields
    safe = {k: user.get(k) for k in ("uid","email","email_verified","name","picture","auth_time")}
    return {"user": safe}

@app.get("/api/test-language/{language_code}")
@limiter.limit("5/minute")
def test_language_generation(request: Request, language_code: str, user = Depends(get_current_user)):
    """Test endpoint to debug language generation issues (requires authentication)"""
    if model is None:
        raise HTTPException(status_code=500, detail="AI model not initialized")
    
    # Validate language code
    SUPPORTED_LANGUAGES = ['en', 'es', 'fr', 'de', 'ja', 'zh']
    if language_code not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Unsupported language code: {language_code}")
    
    try:
        # Create a simple test prompt
        language_names = {
            "en": "English",
            "es": "Spanish", 
            "fr": "French",
            "de": "German",
            "ja": "Japanese",
            "zh": "Chinese"
        }
        target_language = language_names.get(language_code, "English")
        
        test_prompt = f"""Write a simple product description in {target_language} for a wireless headphone.

Return JSON:
{{
  "title": "title in {target_language}",
  "description": "description in {target_language}",
  "bullets": ["benefit 1 in {target_language}", "benefit 2 in {target_language}", "benefit 3 in {target_language}"],
  "meta": "meta description in {target_language}"
}}"""
        
        logging.info(f"Testing language generation for: {language_code}")
        
        ai_text, tokens_used, response_time = call_gemini_generate(
            model=model,
            prompt=test_prompt,
            temperature=0.8,
            cost_tracker=cost_tracker
        )
        
        # Try to parse the response
        ai_text = safety_filter.sanitize_output(ai_text)
        parsed = safe_extract_json(ai_text)
        
        return {
            "success": True,
            "language_code": language_code,
            "target_language": target_language,
            "raw_response": ai_text,
            "parsed_response": parsed,
            "tokens_used": tokens_used,
            "response_time": response_time
        }
        
    except Exception as e:
        logging.error(f"Test generation failed for {language_code}: {str(e)}")
        error_msg = str(e)
        
        # Enhanced error categorization
        if "QUOTA_EXCEEDED" in error_msg:
            error_type = "QUOTA_EXCEEDED"
        elif "SAFETY_FILTER" in error_msg:
            error_type = "SAFETY_FILTER"
        elif "NETWORK_ERROR" in error_msg:
            error_type = "NETWORK_ERROR"
        elif "RETRY_EXHAUSTED" in error_msg:
            error_type = "RETRY_EXHAUSTED"
        else:
            error_type = "UNKNOWN_ERROR"
        
        return {
            "success": False,
            "language_code": language_code,
            "error": error_msg,
            "error_type": error_type,
            "original_error_type": type(e).__name__
        }

@app.post("/api/generate-description")
@limiter.limit("30/minute")
def generate_description(
    request: Request,
    title: str = Form(...),
    features: str = Form(...),
    category: str = Form("generic"),
    primary_keyword: str = Form(""),
    tone: str = Form("professional"),
    sku: str = Form(""),
    languageCode: str = Form("en"),
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a single product description"""
    if model is None or credit_service is None:
        raise HTTPException(status_code=500, detail="AI model or credit service not initialized")
    
    user_id = user.get("uid")
    
    # Check and refresh credits if needed (run sync version)
    import asyncio
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(credit_service.check_and_refresh_credits(user_id, session=db))
        
        # Check user credits before generation
        operation_type = OperationType.SINGLE_DESCRIPTION
        can_proceed, credit_info = loop.run_until_complete(credit_service.check_credits_and_limits(
            user_id, operation_type, product_count=1, session=db
        ))
    finally:
        loop.close()
    
    if not can_proceed:
        raise HTTPException(
            status_code=402,  # Payment Required
            detail={
                "error": credit_info.get("error"),
                "upgrade_required": credit_info.get("upgrade_required", False),
                "current_credits": credit_info.get("current_credits", 0),
                "required_credits": credit_info.get("required_credits", 1),
                "subscription_tier": credit_info.get("subscription_tier", "free"),
                "daily_usage_count": credit_info.get("daily_usage_count", 0),
                "daily_limit": credit_info.get("daily_limit", 0),
                "rate_limits": credit_info.get("rate_limits", {})
            }
        )
    
    # Validate language code
    SUPPORTED_LANGUAGES = ['en', 'es', 'fr', 'de', 'ja', 'zh']
    if languageCode not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Unsupported language code: {languageCode}")
    
    try:
        # Create row dict
        row = {
            "id": sku or timestamp(),
            "sku": sku,
            "title": title,
            "category": category,
            "features": features,
            "primary_keyword": primary_keyword,
            "tone": tone,
            "languageCode": languageCode
        }
        
        # Validate input
        is_valid, validation_msg = safety_filter.validate_input(title + " " + features)
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"Invalid input: {validation_msg}")
        
        # Build prompt
        prompt = build_gemini_prompt(row)
        
        # Call AI
        ai_text, tokens_used, response_time = call_gemini_generate(
            model=model,
            prompt=prompt,
            temperature=0.8,  # Increased for more creative and persuasive content
            cost_tracker=cost_tracker
        )
        
        # Sanitize output
        ai_text = safety_filter.sanitize_output(ai_text)
        
        # Parse response with compliance validation
        try:
            parsed = safe_extract_json(ai_text)
            validated = validate_and_ensure_compliance(parsed)
        except ValueError as validation_error:
            # If compliance validation fails, try to generate fallback bullets
            logging.warning(f"Compliance validation failed: {validation_error}")
            try:
                # Extract what we can from the response
                fallback_parsed = safe_extract_json(ai_text)
                if fallback_parsed.get("title") and fallback_parsed.get("description"):
                    # Generate fallback bullets
                    fallback_bullets = generate_fallback_bullets(
                        fallback_parsed.get("title", ""),
                        fallback_parsed.get("description", ""),
                        features
                    )
                    validated = {
                        "title": fallback_parsed.get("title", title),
                        "description": fallback_parsed.get("description", ""),
                        "bullets": fallback_bullets,
                        "meta": fallback_parsed.get("meta", "")
                    }
                    logging.info("Used fallback bullets due to compliance failure")
                else:
                    raise validation_error
            except Exception as fallback_error:
                logging.error(f"Fallback generation failed: {fallback_error}")
                raise HTTPException(status_code=500, detail=f"Description generation failed compliance validation: {validation_error}")
        
        # Extract fields from validated data
        generated_title = validated.get("title", title)
        description = validated.get("description", "").strip()
        bullets = validated.get("bullets", [])
        meta = validated.get("meta", "")
        
        # SEO evaluation
        seo = seo_evaluate(description, primary_keyword)
        
        # Deduct credits after successful generation
        loop = asyncio.new_event_loop()
        try:
            deduct_success, deduct_result = loop.run_until_complete(credit_service.deduct_credits(
                user_id, operation_type, product_count=1, request_id=row["id"], session=db
            ))
        finally:
            loop.close()
        if not deduct_success:
            logging.warning(f"Failed to deduct credits for user {user_id}: {deduct_result.get('error')}")
        
        return {
            "success": True,
            "data": {
                "id": row["id"],
                "sku": sku,
                "title": generated_title,
                "original_title": title,
                "description": description,
                "bullets": bullets,
                "meta": meta,
                "seo_score": seo,
                "languageCode": languageCode,
                "tokens_used": tokens_used,
                "response_time": response_time,
                "cost": cost_tracker.get_current_cost(),
                "credits_used": credit_info.get("required_credits", 1),
                "remaining_credits": deduct_result.get("remaining_credits", 0),
                "operation_type": operation_type.value,
                "subscription_tier": credit_info.get("subscription_tier", "free")
            }
        }
        
    except Exception as e:
        logging.error(f"Error generating description: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.post("/api/generate-batch")
@limiter.limit("10/minute")
def generate_batch_json(http_request: Request, request: Dict[str, Any], user = Depends(get_current_user), db: Session = Depends(get_db)):
    """Generate descriptions for multiple products from batch request"""
    logging.info(f"Generate batch endpoint called - user: {user.get('email', 'unknown')}")
    if model is None or credit_service is None:
        raise HTTPException(status_code=500, detail="AI model or credit service not initialized")
    
    user_id = user.get("uid")
    
    # Check and refresh credits if needed (run sync)
    import asyncio
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(credit_service.check_and_refresh_credits(user_id, session=db))
    finally:
        loop.close()
    
    # Handle both old format (array of products) and new format (batch request)
    if isinstance(request, list):
        # Legacy format - array of products
        products = request
        batch_tone = "professional"
        batch_style = "amazon"
        language_code = "en"
    else:
        # New format - batch request with tone and style
        products = request.get("products", [])
        batch_tone = request.get("batchTone", "professional")
        batch_style = request.get("batchStyle", "amazon")
        language_code = request.get("languageCode", "en")
    
    # Validate language code
    SUPPORTED_LANGUAGES = ['en', 'es', 'fr', 'de', 'ja', 'zh']
    if language_code not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Unsupported language code: {language_code}")
    
    # Determine operation type and check credits
    product_count = len(products)
    operation_type = credit_service.determine_operation_type(product_count, is_regeneration=False)
    
    loop = asyncio.new_event_loop()
    try:
        can_proceed, credit_info = loop.run_until_complete(credit_service.check_credits_and_limits(
            user_id, operation_type, product_count, session=db
        ))
    finally:
        loop.close()
    
    if not can_proceed:
        raise HTTPException(
            status_code=402,  # Payment Required
            detail={
                "error": credit_info.get("error"),
                "upgrade_required": credit_info.get("upgrade_required", False),
                "current_credits": credit_info.get("current_credits", 0),
                "required_credits": credit_info.get("required_credits", 1),
                "subscription_tier": credit_info.get("subscription_tier", "free"),
                "operation_type": operation_type.value,
                "product_count": product_count,
                "daily_usage_count": credit_info.get("daily_usage_count", 0),
                "daily_limit": credit_info.get("daily_limit", 0),
                "rate_limits": credit_info.get("rate_limits", {})
            }
        )
    
    try:
        results = []
        errors = []
        
        for idx, product in enumerate(products):
            try:
                # Convert to row dict format
                row_dict = {
                    "id": product.get("id", f"product_{idx}"),
                    "sku": product.get("sku", ""),
                    "title": product.get("product_name", ""),  # Frontend sends product_name
                    "category": product.get("category", "generic"),
                    "features": product.get("features", ""),
                    "primary_keyword": product.get("keywords", ""),  # Frontend sends keywords
                    "audience": product.get("audience", "general consumers"),  # Frontend sends audience
                    "tone": batch_tone,  # Use batch-level tone
                    "style_variation": batch_style,  # Use batch-level style
                    "languageCode": language_code  # Use batch-level language
                }
                
                # Basic validation for required fields
                if not row_dict["title"] or not row_dict["features"]:
                    errors.append({
                        "row": idx,
                        "id": row_dict.get("id", ""),
                        "error": "Missing required fields: product_name and features are required"
                    })
                    continue
                
                # Validate input
                is_valid, validation_msg = safety_filter.validate_input(
                    row_dict["title"] + " " + row_dict["features"]
                )
                if not is_valid:
                    errors.append({
                        "row": idx,
                        "id": row_dict.get("id", ""),
                        "error": f"Invalid input: {validation_msg}"
                    })
                    continue
                
                # Build prompt and generate
                prompt = build_gemini_prompt(row_dict)
                parsed = None
                tokens_used = 0
                response_time = 0
                
                try:
                    logging.info(f"Generating content for language: {language_code}")
                    
                    # Check if model is available before making API call
                    if model is None:
                        errors.append({
                            "row": idx,
                            "id": row_dict.get("id", ""),
                            "error": "AI model not initialized - check API key configuration"
                        })
                        logging.error(f"Model is None for product {row_dict.get('id', 'unknown')}")
                        continue
                    
                    # TEMPORARILY DISABLED FOR TESTING - rate_limit_api_call()  # Add rate limiting
                    ai_text, tokens_used, response_time = call_gemini_generate(
                        model=model,
                        prompt=prompt,
                        temperature=0.8,  # Increased for more creative and persuasive content
                        cost_tracker=cost_tracker
                    )
                    
                    logging.info(f"AI response received: {ai_text[:200]}...")
                    
                    # Parse and process with compliance validation
                    ai_text = safety_filter.sanitize_output(ai_text)
                    try:
                        parsed = safe_extract_json(ai_text)
                        validated = validate_and_ensure_compliance(parsed)
                    except ValueError as validation_error:
                        # If compliance validation fails, try to generate fallback bullets
                        logging.warning(f"Compliance validation failed for product {row_dict.get('id', 'Unknown')}: {validation_error}")
                        try:
                            # Extract what we can from the response
                            fallback_parsed = safe_extract_json(ai_text)
                            if fallback_parsed.get("title") and fallback_parsed.get("description"):
                                # Generate fallback bullets
                                fallback_bullets = generate_fallback_bullets(
                                    fallback_parsed.get("title", ""),
                                    fallback_parsed.get("description", ""),
                                    row_dict.get("features", "")
                                )
                                validated = {
                                    "title": fallback_parsed.get("title", row_dict.get("title", "")),
                                    "description": fallback_parsed.get("description", ""),
                                    "bullets": fallback_bullets,
                                    "meta": fallback_parsed.get("meta", "")
                                }
                                logging.info(f"Used fallback bullets for product {row_dict.get('id', 'Unknown')}")
                            else:
                                raise validation_error
                        except Exception as fallback_error:
                            logging.error(f"Fallback generation failed for product {row_dict.get('id', 'Unknown')}: {fallback_error}")
                            errors.append({
                                "row": idx,
                                "id": row_dict.get("id", ""),
                                "error": f"Description generation failed compliance validation: {validation_error}"
                            })
                            continue
                    
                    logging.info(f"Validated JSON: {validated}")
                    
                    # Validate that the generated content is in the requested language
                    if language_code != "en" and validated.get("description", ""):
                        # Basic check: if description contains mostly English words, flag as potential issue
                        english_words = ["the", "and", "for", "with", "this", "that", "product", "quality", "features"]
                        description_lower = validated.get("description", "").lower()
                        english_word_count = sum(1 for word in english_words if word in description_lower)
                        if english_word_count > 3:  # If more than 3 common English words, might be in English
                            logging.warning(f"Generated content for language {language_code} may contain English text")
                    
                except Exception as gen_error:
                    error_msg = str(gen_error)
                    logging.error(f"Generation error for product {row_dict.get('id', 'Unknown')}: {error_msg}")
                    logging.error(f"Error type: {type(gen_error).__name__}")
                    
                    # Enhanced error handling with specific error types
                    if "QUOTA_EXCEEDED" in error_msg:
                        logging.error("API quota exceeded - stopping batch processing")
                        errors.append({
                            "row": idx,
                            "id": row_dict.get("id", ""),
                            "error": "API quota exceeded - please try again later"
                        })
                        break  # Stop processing if quota exceeded
                    elif "SAFETY_FILTER" in error_msg:
                        logging.warning(f"Content blocked by safety filters for product: {row_dict.get('title', 'Unknown')}")
                        errors.append({
                            "row": idx,
                            "id": row_dict.get("id", ""),
                            "error": "Content blocked by safety filters - please review product details"
                        })
                        continue
                    elif "NETWORK_ERROR" in error_msg:
                        logging.warning(f"Network error for product: {row_dict.get('title', 'Unknown')} - will retry")
                        errors.append({
                            "row": idx,
                            "id": row_dict.get("id", ""),
                            "error": "Network error - please try again"
                        })
                        continue
                    elif "RETRY_EXHAUSTED" in error_msg:
                        logging.warning(f"All retry attempts exhausted for product: {row_dict.get('title', 'Unknown')}")
                        errors.append({
                            "row": idx,
                            "id": row_dict.get("id", ""),
                            "error": "API retry attempts exhausted - please try again later"
                        })
                        continue
                    
                    # Try a fallback with English if non-English fails
                    if language_code != "en":
                        logging.info(f"Attempting fallback to English for product: {row_dict.get('title', 'Unknown')}")
                        try:
                            # Create a simple English fallback
                            fallback_row = row_dict.copy()
                            fallback_row["languageCode"] = "en"
                            fallback_prompt = build_gemini_prompt(fallback_row)
                            
                            # TEMPORARILY DISABLED FOR TESTING - rate_limit_api_call()  # Add rate limiting
                            ai_text, tokens_used, response_time = call_gemini_generate(
                                model=model,
                                prompt=fallback_prompt,
                                temperature=0.8,  # Increased for more creative and persuasive content
                                cost_tracker=cost_tracker
                            )
                            
                            ai_text = safety_filter.sanitize_output(ai_text)
                            parsed = safe_extract_json(ai_text)
                            
                            logging.info(f"Fallback to English successful")
                            
                        except Exception as fallback_error:
                            logging.error(f"Fallback to English also failed: {str(fallback_error)}")
                            
                            # Try one more time with an even simpler approach
                            try:
                                logging.info(f"Attempting ultra-simple English generation")
                                simple_prompt = f"""Create a product description for: {row_dict.get('title', 'Product')}

Features: {row_dict.get('features', '')}
Audience: {row_dict.get('audience', 'general consumers')}

Return JSON:
{{
  "title": "Product title",
  "description": "Product description",
  "bullets": ["Benefit 1", "Benefit 2", "Benefit 3"],
  "meta": "Meta description"
}}"""
                                
                                # TEMPORARILY DISABLED FOR TESTING - rate_limit_api_call()  # Add rate limiting
                                ai_text, tokens_used, response_time = call_gemini_generate(
                                    model=model,
                                    prompt=simple_prompt,
                                    temperature=0.8,  # Increased for more creative and persuasive content
                                    cost_tracker=cost_tracker
                                )
                                
                                ai_text = safety_filter.sanitize_output(ai_text)
                                parsed = safe_extract_json(ai_text)
                                
                                logging.info(f"Ultra-simple English generation successful")
                                
                            except Exception as simple_error:
                                logging.error(f"Ultra-simple generation also failed: {str(simple_error)}")
                                errors.append({
                                    "row": idx,
                                    "id": row_dict.get("id", ""),
                                    "error": f"All generation attempts failed for language {language_code}: {str(gen_error)}"
                                })
                                continue
                    else:
                        errors.append({
                            "row": idx,
                            "id": row_dict.get("id", ""),
                            "error": f"Generation failed for language {language_code}: {str(gen_error)}"
                        })
                        continue
                
                result = {
                    "id": row_dict["id"],
                    "product_name": validated.get("title", row_dict["title"]),
                    "category": row_dict["category"],
                    "audience": row_dict.get("audience", "general consumers"),
                    "description": validated.get("description", ""),
                    "keywords": row_dict.get("primary_keyword", ""),
                    "features": row_dict["features"],  # Include original features
                    "tone": batch_tone,  # Include batch-level tone
                    "style_variation": batch_style,  # Include batch-level style variation
                    "languageCode": language_code,  # Include batch-level language
                    "bullets": validated.get("bullets", []),
                    "meta": validated.get("meta", ""),
                    "seo_score": seo_evaluate(validated.get("description", ""), row_dict.get("primary_keyword", "")),
                    "tokens_used": tokens_used,
                    "response_time": response_time
                }
                
                results.append(result)
                
            except Exception as e:
                errors.append({
                    "row": idx,
                    "id": product.get("id", ""),
                    "error": str(e)
                })
        
        # Deduct credits after successful batch generation
        batch_id = f"batch_{timestamp()}"
        loop = asyncio.new_event_loop()
        try:
            deduct_success, deduct_result = loop.run_until_complete(credit_service.deduct_credits(
                user_id, operation_type, product_count, batch_id=batch_id, session=db
            ))
        finally:
            loop.close()
        if not deduct_success:
            logging.warning(f"Failed to deduct credits for user {user_id}: {deduct_result.get('error')}")
        
        return {
            "success": True,
            "batch_id": batch_id,
            "items": results,
            "errors": errors,
            "total_processed": len(results),
            "total_errors": len(errors),
            "total_cost": cost_tracker.get_current_cost(),
            "credits_used": credit_info.get("required_credits", 1),
            "remaining_credits": deduct_result.get("remaining_credits", 0),
            "operation_type": operation_type.value,
            "subscription_tier": credit_info.get("subscription_tier", "free"),
            "product_count": product_count
        }
        
    except Exception as e:
        logging.error(f"Error processing JSON batch: {str(e)}")
        raise HTTPException(status_code=500, detail=f"JSON batch processing failed: {str(e)}")

@app.post("/api/generate-batch-csv")
@limiter.limit("5/minute")
async def generate_batch(http_request: Request, file: UploadFile = File(...), audience: str = Form(...), languageCode: str = Form("en"), user = Depends(get_current_user), db: Session = Depends(get_db)):
    """Generate descriptions for multiple products from CSV with automatic column mapping"""
    if model is None or credit_service is None:
        raise HTTPException(status_code=500, detail="AI model or credit service not initialized")
    
    user_id = user.get("uid")
    
    # Check and refresh credits if needed
    await credit_service.check_and_refresh_credits(user_id, session=db)
    
    # Validate language code
    SUPPORTED_LANGUAGES = ['en', 'es', 'fr', 'de', 'ja', 'zh']
    if languageCode not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Unsupported language code: {languageCode}")
    
    try:
        # Read CSV file
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Get column names for mapping
        columns = df.columns.tolist()
        
        # Check credits for CSV upload (1 credit per product)
        product_count = len(df)
        operation_type = OperationType.CSV_UPLOAD
        
        can_proceed, credit_info = await credit_service.check_credits_and_limits(
            user_id, operation_type, product_count, session=db
        )
        
        if not can_proceed:
            raise HTTPException(
                status_code=402,  # Payment Required
                detail={
                    "error": credit_info.get("error"),
                    "upgrade_required": credit_info.get("upgrade_required", False),
                    "current_credits": credit_info.get("current_credits", 0),
                    "required_credits": credit_info.get("required_credits", 1),
                    "subscription_tier": credit_info.get("subscription_tier", "free"),
                    "operation_type": operation_type.value,
                    "product_count": product_count,
                    "rate_limits": credit_info.get("rate_limits", {})
                }
            )
        
        results = []
        errors = []
        
        for idx, row in df.iterrows():
            try:
                # Use new automatic mapping function
                row_dict = process_csv_row(row, audience, columns, languageCode)
                
                # Validate input
                is_valid, validation_msg = safety_filter.validate_input(
                    row_dict["title"] + " " + row_dict["features"]
                )
                if not is_valid:
                    errors.append({
                        "row": idx,
                        "id": row_dict.get("id", ""),
                        "error": f"Invalid input: {validation_msg}"
                    })
                    continue
                
                # Build prompt and generate
                prompt = build_gemini_prompt(row_dict)
                
                # Check if model is available before making API call
                if model is None:
                    errors.append({
                        "row": idx,
                        "id": row_dict.get("id", ""),
                        "error": "AI model not initialized - check API key configuration"
                    })
                    logging.error(f"Model is None for product {row_dict.get('id', 'unknown')}")
                    continue
                
                ai_text, tokens_used, response_time = call_gemini_generate(
                    model=model,
                    prompt=prompt,
                    temperature=0.8,  # Increased for more creative and persuasive content
                    cost_tracker=cost_tracker
                )
                
                # Parse and process with compliance validation
                ai_text = safety_filter.sanitize_output(ai_text)
                try:
                    parsed = safe_extract_json(ai_text)
                    validated = validate_and_ensure_compliance(parsed)
                except ValueError as validation_error:
                    # If compliance validation fails, try to generate fallback bullets
                    logging.warning(f"Compliance validation failed for CSV product {row_dict.get('id', 'Unknown')}: {validation_error}")
                    try:
                        # Extract what we can from the response
                        fallback_parsed = safe_extract_json(ai_text)
                        if fallback_parsed.get("title") and fallback_parsed.get("description"):
                            # Generate fallback bullets
                            fallback_bullets = generate_fallback_bullets(
                                fallback_parsed.get("title", ""),
                                fallback_parsed.get("description", ""),
                                row_dict.get("features", "")
                            )
                            validated = {
                                "title": fallback_parsed.get("title", row_dict.get("title", "")),
                                "description": fallback_parsed.get("description", ""),
                                "bullets": fallback_bullets,
                                "meta": fallback_parsed.get("meta", "")
                            }
                            logging.info(f"Used fallback bullets for CSV product {row_dict.get('id', 'Unknown')}")
                        else:
                            raise validation_error
                    except Exception as fallback_error:
                        logging.error(f"Fallback generation failed for CSV product {row_dict.get('id', 'Unknown')}: {fallback_error}")
                        raise HTTPException(status_code=500, detail=f"CSV description generation failed compliance validation: {validation_error}")
                
                result = {
                    "id": row_dict["id"],
                    "product_name": validated.get("title", row_dict["title"]),
                    "category": row_dict["category"],
                    "audience": row_dict["audience"],
                    "description": validated.get("description", ""),
                    "keywords": row_dict.get("primary_keyword", ""),
                    "features": row_dict["features"],  # Include original features
                    "tone": "professional",  # Default tone for CSV batch
                    "style_variation": "standard",  # Default style for CSV batch
                    "languageCode": languageCode,  # Include language from CSV batch
                    "bullets": validated.get("bullets", []),
                    "meta": validated.get("meta", ""),
                    "seo_score": seo_evaluate(validated.get("description", ""), row_dict.get("primary_keyword", "")),
                    "tokens_used": tokens_used,
                    "response_time": response_time
                }
                
                results.append(result)
                
            except Exception as e:
                errors.append({
                    "row": idx,
                    "id": row_dict.get("id", ""),
                    "error": str(e)
                })
        
        # Deduct credits after successful CSV batch generation
        batch_id = f"batch_{timestamp()}"
        deduct_success, deduct_result = await credit_service.deduct_credits(
            user_id, operation_type, product_count, batch_id=batch_id, session=db
        )
        if not deduct_success:
            logging.warning(f"Failed to deduct credits for user {user_id}: {deduct_result.get('error')}")
        
        return {
            "success": True,
            "batch_id": batch_id,
            "items": results,
            "errors": errors,
            "total_processed": len(results),
            "total_errors": len(errors),
            "total_cost": cost_tracker.get_current_cost(),
            "credits_used": credit_info.get("required_credits", 1),
            "remaining_credits": deduct_result.get("remaining_credits", 0),
            "operation_type": operation_type.value,
            "subscription_tier": credit_info.get("subscription_tier", "free"),
            "product_count": product_count
        }
        
    except Exception as e:
        logging.error(f"Error processing batch: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Batch processing failed: {str(e)}")

@app.get("/api/usage-stats")
async def get_usage_stats():
    """Get current usage statistics"""
    if cost_tracker is None:
        raise HTTPException(status_code=500, detail="Cost tracker not initialized")
    
    return {
        "success": True,
        "data": cost_tracker.get_usage_stats()
    }

@app.get("/api/user/credits")
async def get_user_credit_info(user = Depends(get_current_user)):
    """Get user's credit information and subscription details"""
    if credit_service is None:
        raise HTTPException(status_code=500, detail="Credit service not initialized")
    
    user_id = user.get("uid")
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found in token")
    
    # Check and refresh credits if needed
    await credit_service.check_and_refresh_credits(user_id)
    
    # Get comprehensive credit information
    credit_info = await credit_service.get_user_credit_info(user_id)
    
    if "error" in credit_info:
        raise HTTPException(status_code=500, detail=credit_info["error"])
    
    return {
        "success": True,
        "data": credit_info
    }

@app.get("/batch/{batch_id}")
async def fetch_batch(batch_id: str):
    """Fetch a batch by ID (placeholder - in real implementation, store in database)"""
    # This is a placeholder. In a real implementation, you'd store batches in a database
    # and retrieve them by ID. For now, return a 404.
    raise HTTPException(status_code=404, detail="Batch not found. This is a placeholder endpoint.")

@app.get("/download/{batch_id}")
async def download_batch(batch_id: str):
    """Download a batch as a CSV file"""
    # For now, we'll return a simple CSV with the batch ID
    # In a real implementation, you'd store and retrieve the actual batch data
    
    csv_content = f"""id,sku,title,description,bullets,meta,status
{batch_id},,Generated Product,This is a placeholder download for batch {batch_id}.,"Placeholder bullet 1|Placeholder bullet 2",Placeholder meta description,completed"""
    
    from fastapi.responses import Response
    
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=batch_{batch_id}.csv"}
    )

@app.post("/api/regenerate")
@limiter.limit("30/minute")
def regenerate_description(http_request: Request, item: Dict[str, Any], user = Depends(get_current_user)):
    """Regenerate a single product description"""
    logging.info(f"Regenerate endpoint called - user: {user.get('email', 'unknown')}")
    if model is None or credit_service is None:
        raise HTTPException(status_code=500, detail="AI model or credit service not initialized")
    
    if safety_filter is None or cost_tracker is None:
        raise HTTPException(status_code=500, detail="AI components not initialized")
    
    user_id = user.get("uid")
    
    # Check and refresh credits if needed (run sync)
    import asyncio
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(credit_service.check_and_refresh_credits(user_id))
        
        # Check credits for regeneration (1 credit)
        operation_type = OperationType.REGENERATION
        can_proceed, credit_info = loop.run_until_complete(credit_service.check_credits_and_limits(
            user_id, operation_type, product_count=1
        ))
    finally:
        loop.close()
    
    if not can_proceed:
        raise HTTPException(
            status_code=402,  # Payment Required
            detail={
                "error": credit_info.get("error"),
                "upgrade_required": credit_info.get("upgrade_required", False),
                "current_credits": credit_info.get("current_credits", 0),
                "required_credits": credit_info.get("required_credits", 1),
                "subscription_tier": credit_info.get("subscription_tier", "free"),
                "operation_type": operation_type.value,
                "daily_usage_count": credit_info.get("daily_usage_count", 0),
                "daily_limit": credit_info.get("daily_limit", 0),
                "rate_limits": credit_info.get("rate_limits", {})
            }
        )
    
    try:
        # Convert the item to row dict format
        row_dict = {
            "id": item.get("id", timestamp()),
            "sku": item.get("sku", ""),
            "title": item.get("product_name", ""),
            "category": item.get("category", "generic"),
            "features": item.get("features", ""),
            "primary_keyword": item.get("keywords", ""),
            "audience": item.get("audience", "general consumers"),
            "tone": item.get("tone", "professional"),
            "style_variation": item.get("style_variation", "amazon"),
            "languageCode": item.get("languageCode", "en")
        }
        
        # Basic validation
        if not row_dict["title"] or not row_dict["features"]:
            raise HTTPException(status_code=400, detail="Missing required fields: product_name and features are required")
        
        # Validate input
        is_valid, validation_msg = safety_filter.validate_input(
            row_dict["title"] + " " + row_dict["features"]
        )
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"Invalid input: {validation_msg}")
        
        # Build prompt and generate
        prompt = build_gemini_prompt(row_dict)
        ai_text, tokens_used, response_time = call_gemini_generate(
            model=model,
            prompt=prompt,
            temperature=0.8,  # Increased for more creative and persuasive content
            cost_tracker=cost_tracker
        )
        
        # Parse and process with compliance validation
        ai_text = safety_filter.sanitize_output(ai_text)
        try:
            parsed = safe_extract_json(ai_text)
            validated = validate_and_ensure_compliance(parsed)
        except ValueError as validation_error:
            # If compliance validation fails, try to generate fallback bullets
            logging.warning(f"Compliance validation failed for regenerate product {row_dict.get('id', 'Unknown')}: {validation_error}")
            try:
                # Extract what we can from the response
                fallback_parsed = safe_extract_json(ai_text)
                if fallback_parsed.get("title") and fallback_parsed.get("description"):
                    # Generate fallback bullets
                    fallback_bullets = generate_fallback_bullets(
                        fallback_parsed.get("title", ""),
                        fallback_parsed.get("description", ""),
                        row_dict.get("features", "")
                    )
                    validated = {
                        "title": fallback_parsed.get("title", row_dict.get("title", "")),
                        "description": fallback_parsed.get("description", ""),
                        "bullets": fallback_bullets,
                        "meta": fallback_parsed.get("meta", "")
                    }
                    logging.info(f"Used fallback bullets for regenerate product {row_dict.get('id', 'Unknown')}")
                else:
                    raise validation_error
            except Exception as fallback_error:
                logging.error(f"Fallback generation failed for regenerate product {row_dict.get('id', 'Unknown')}: {fallback_error}")
                raise HTTPException(status_code=500, detail=f"Regenerate description failed compliance validation: {validation_error}")
        
        # Deduct credits after successful regeneration
        loop = asyncio.new_event_loop()
        try:
            deduct_success, deduct_result = loop.run_until_complete(credit_service.deduct_credits(
                user_id, operation_type, product_count=1, request_id=row_dict["id"]
            ))
        finally:
            loop.close()
        if not deduct_success:
            logging.warning(f"Failed to deduct credits for user {user_id}: {deduct_result.get('error')}")
        
        result = {
            "id": row_dict["id"],
            "product_name": validated.get("title", row_dict["title"]),
            "category": row_dict["category"],
            "audience": row_dict["audience"],
            "description": validated.get("description", ""),
            "keywords": row_dict["primary_keyword"],
            "features": row_dict["features"],  # Include original features
            "tone": row_dict["tone"],  # Include original tone
            "style_variation": row_dict["style_variation"],  # Include original style variation
            "languageCode": row_dict["languageCode"],  # Include original language
            "bullets": validated.get("bullets", []),
            "meta": validated.get("meta", ""),
            "seo_score": seo_evaluate(validated.get("description", ""), row_dict["primary_keyword"]),
            "tokens_used": tokens_used,
            "response_time": response_time,
            "regenerating": False,
            "credits_used": credit_info.get("required_credits", 1),
            "remaining_credits": deduct_result.get("remaining_credits", 0),
            "operation_type": operation_type.value,
            "subscription_tier": credit_info.get("subscription_tier", "free")
        }
        
        return result
        
    except Exception as e:
        logging.error(f"Error regenerating description: {str(e)}")
        logging.error(f"Item data: {item}")
        logging.error(f"Model status: {model is not None}")
        logging.error(f"Safety filter status: {safety_filter is not None}")
        logging.error(f"Cost tracker status: {cost_tracker is not None}")
        raise HTTPException(status_code=500, detail=f"Regeneration failed: {str(e)}")

@app.get("/api/health")
async def health():
    """Health check endpoint to verify the app is running"""
    return {"status": "ok"}

@app.websocket("/ws/payments")
async def websocket_payments(websocket: WebSocket):
    """WebSocket endpoint for payment notifications"""
    logging.info("WebSocket connection attempt received")
    await websocket.accept()
    logging.info("WebSocket connection accepted")
    try:
        while True:
            # Keep connection alive and send periodic heartbeats
            await asyncio.sleep(30)  # Send heartbeat every 30 seconds
            await websocket.send_json({
                "type": "heartbeat",
                "timestamp": time.time(),
                "status": "connected"
            })
    except WebSocketDisconnect:
        logging.info("WebSocket client disconnected")
    except Exception as e:
        logging.error(f"WebSocket error: {str(e)}")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
