"""
Apex ML API - Autonomous ML Operations Agent

This module implements a senior autonomous ML operations agent with:
- OODA Loop (Observe, Orient, Decide, Act)
- Auto-debugging capabilities
- Contextual memory (Knowledge Ledger)
- Security and efficiency constraints
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime, UTC
import logging
import re

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, field_validator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security: Mask sensitive data in logs
def mask_sensitive_data(data: str) -> str:
    """Mask API keys and sensitive user IDs in logs"""
    # Mask API keys (pattern: api_key, apikey, token)
    data = re.sub(r'(api[_-]?key|token)[\s:=]+["\']?[\w\-]+["\']?', r'\1: ***REDACTED***', data, flags=re.IGNORECASE)
    # Mask user IDs (pattern: user_id, userId)
    data = re.sub(r'(user[_-]?id)[\s:=]+["\']?[\w\-]+["\']?', r'\1: ***REDACTED***', data, flags=re.IGNORECASE)
    return data


# Initialize FastAPI app
app = FastAPI(
    title="Apex ML API",
    description="Autonomous ML Operations Agent with OODA Loop",
    version="1.0.0"
)

# ===========================
# MODELS & SCHEMAS
# ===========================

class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class RiskLevel(str, Enum):
    RISK = "risk"
    GROWTH = "growth"
    NEUTRAL = "neutral"

class ChurnPredictionRequest(BaseModel):
    user_id: str = Field(..., description="User identifier")
    usage_metrics: Dict[str, float] = Field(..., description="Usage metrics for prediction")
    
    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, v):
        if not v or len(v) < 3:
            raise ValueError('user_id must be at least 3 characters')
        return v

class ChurnPredictionResponse(BaseModel):
    prediction: str = Field(..., description="Churn prediction: 'will_churn' or 'will_retain'")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    risk_level: RiskLevel = Field(..., description="Risk assessment")

class SentimentAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to analyze")
    
class SentimentAnalysisResponse(BaseModel):
    sentiment: str = Field(..., description="Sentiment: 'positive', 'negative', or 'neutral'")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    risk_level: RiskLevel = Field(..., description="Risk assessment based on sentiment")

class ValidationRequest(BaseModel):
    logic_data: Dict[str, Any] = Field(..., description="Logic to validate")
    
class ValidationResponse(BaseModel):
    is_valid: bool = Field(..., description="Whether the logic is valid")
    message: str = Field(..., description="Validation message")
    verified_at: str = Field(..., description="Timestamp of verification")

class SecurityAuditRequest(BaseModel):
    data_source: str = Field(..., description="Data source to audit")
    risk_indicators: List[str] = Field(..., description="Risk indicators detected")
    
class SecurityAuditResponse(BaseModel):
    audit_status: str = Field(..., description="Audit status")
    recommendations: List[str] = Field(..., description="Security recommendations")
    severity: str = Field(..., description="Severity level")

class MarketingGeneratorRequest(BaseModel):
    growth_indicators: List[str] = Field(..., description="Growth indicators")
    target_audience: str = Field(..., description="Target audience")
    
class MarketingGeneratorResponse(BaseModel):
    campaign_ideas: List[str] = Field(..., description="Marketing campaign ideas")
    estimated_reach: int = Field(..., description="Estimated reach")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in recommendations")

# ===========================
# KNOWLEDGE LEDGER
# ===========================

class KnowledgeLedger:
    """Contextual memory for storing successful tool results"""
    
    def __init__(self):
        self.ledger: Dict[str, Any] = {}
        self.iteration_count: int = 0
        self.max_iterations: int = 5
        
    def store(self, key: str, value: Any):
        """Store a result in the knowledge ledger"""
        self.ledger[key] = {
            "value": value,
            "timestamp": datetime.now(UTC).isoformat(),
            "iteration": self.iteration_count
        }
        logger.info(f"Stored in ledger: {key}")
        
    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve a result from the knowledge ledger"""
        entry = self.ledger.get(key)
        return entry["value"] if entry else None
        
    def increment_iteration(self):
        """Increment the iteration counter"""
        self.iteration_count += 1
        if self.iteration_count >= self.max_iterations:
            logger.warning(f"Reached maximum iterations: {self.max_iterations}")
            
    def reset(self):
        """Reset the ledger for a new task"""
        self.ledger.clear()
        self.iteration_count = 0
        
    def is_at_max_iterations(self) -> bool:
        """Check if at maximum iterations"""
        return self.iteration_count >= self.max_iterations
        
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the ledger"""
        return {
            "entries": len(self.ledger),
            "iterations": self.iteration_count,
            "keys": list(self.ledger.keys())
        }

# Global knowledge ledger instance
knowledge_ledger = KnowledgeLedger()

# ===========================
# OODA LOOP IMPLEMENTATION
# ===========================

class OODALoop:
    """
    Autonomous decision-making loop:
    1. OBSERVE: Collect data from ML tools
    2. ORIENT: Analyze confidence and risk
    3. DECIDE: Choose next action
    4. ACT: Execute the action
    """
    
    @staticmethod
    def observe(data: Any, tool_name: str) -> Dict[str, Any]:
        """Observe: Collect and log incoming data"""
        observation = {
            "tool": tool_name,
            "data": data,
            "timestamp": datetime.now(UTC).isoformat()
        }
        # Security: Mask sensitive data before logging
        safe_log = mask_sensitive_data(str(observation))
        logger.info(f"OBSERVE: {safe_log}")
        return observation
    
    @staticmethod
    def orient(confidence: float, risk_level: RiskLevel) -> Dict[str, Any]:
        """Orient: Analyze the data and determine confidence level"""
        confidence_category = (
            ConfidenceLevel.HIGH if confidence >= 0.7
            else ConfidenceLevel.MEDIUM if confidence >= 0.5
            else ConfidenceLevel.LOW
        )
        
        orientation = {
            "confidence": confidence,
            "confidence_category": confidence_category,
            "risk_level": risk_level,
            "proceed_with_standard_path": confidence >= 0.7
        }
        logger.info(f"ORIENT: Confidence={confidence}, Risk={risk_level}, Proceed={orientation['proceed_with_standard_path']}")
        return orientation
    
    @staticmethod
    def decide(orientation: Dict[str, Any], risk_level: RiskLevel) -> str:
        """Decide: Choose the next tool based on analysis"""
        # If low confidence, return "manual_review"
        if not orientation["proceed_with_standard_path"]:
            decision = "manual_review"
            logger.info(f"DECIDE: Low confidence (<0.7), routing to {decision}")
            return decision
        
        # Route based on risk level
        if risk_level == RiskLevel.RISK:
            decision = "security_audit"
        elif risk_level == RiskLevel.GROWTH:
            decision = "marketing_generator"
        else:
            decision = "standard_processing"
            
        logger.info(f"DECIDE: Risk level {risk_level}, routing to {decision}")
        return decision
    
    @staticmethod
    def act(decision: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Act: Execute the chosen action"""
        action_result = {
            "decision": decision,
            "executed_at": datetime.now(UTC).isoformat(),
            "context": context
        }
        logger.info(f"ACT: Executing {decision}")
        return action_result

# ===========================
# AUTO-DEBUGGING MIDDLEWARE
# ===========================

from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Auto-debugging for validation errors (422)"""
    errors = exc.errors()
    logger.error(f"Validation Error (422): {errors}")
    
    # Clean up errors to be JSON serializable
    clean_errors = []
    for error in errors:
        clean_error = {
            "type": error.get("type"),
            "loc": error.get("loc"),
            "msg": error.get("msg"),
            "input": error.get("input")
        }
        # Add URL if present
        if "url" in error:
            clean_error["url"] = error["url"]
        clean_errors.append(clean_error)
    
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "detail": clean_errors,
            "debug_hint": "Check your JSON schema. Ensure all required fields are present and have correct types.",
            "documentation": f"{request.url.path}/docs"
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """General exception handler with auto-debugging hints"""
    error_message = str(exc)
    safe_error = mask_sensitive_data(error_message)
    logger.error(f"Error in {request.url.path}: {safe_error}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": safe_error,
            "debug_hint": "Check logs for traceback. Verify input data format.",
            "path": str(request.url.path)
        }
    )

# ===========================
# ML API ENDPOINTS
# ===========================

@app.post("/predict-churn", response_model=ChurnPredictionResponse)
async def predict_churn(request: ChurnPredictionRequest):
    """
    OBSERVE: Predict customer churn based on usage metrics
    """
    knowledge_ledger.increment_iteration()
    
    if knowledge_ledger.is_at_max_iterations():
        raise HTTPException(
            status_code=429,
            detail="Maximum iteration limit (5) reached for this task. Please reset and try again."
        )
    
    # OBSERVE
    observation = OODALoop.observe(request.model_dump(), "predict-churn")
    
    # Simple ML logic (in production, this would be a real ML model)
    usage_avg = sum(request.usage_metrics.values()) / len(request.usage_metrics)
    
    # Prediction logic
    will_churn = usage_avg < 50
    # Calculate confidence based on distance from threshold
    distance_from_threshold = abs(usage_avg - 50)
    confidence = min(distance_from_threshold / 50, 1.0)
    confidence = max(confidence, 0.3)  # Minimum confidence of 0.3
    confidence = min(confidence, 0.95)  # Maximum confidence of 0.95
    
    risk_level = RiskLevel.RISK if will_churn else RiskLevel.GROWTH
    
    # ORIENT
    orientation = OODALoop.orient(confidence, risk_level)
    
    # DECIDE
    decision = OODALoop.decide(orientation, risk_level)
    
    # ACT & Store in Knowledge Ledger
    action = OODALoop.act(decision, {"will_churn": will_churn, "confidence": confidence})
    knowledge_ledger.store("churn_prediction", action)
    
    response = ChurnPredictionResponse(
        prediction="will_churn" if will_churn else "will_retain",
        confidence=confidence,
        risk_level=risk_level
    )
    
    # Automatically trigger next action based on decision
    if decision == "security_audit" and orientation["proceed_with_standard_path"]:
        logger.info("Auto-triggering security audit due to RISK detection")
        knowledge_ledger.store("next_action", "security_audit")
    elif decision == "marketing_generator" and orientation["proceed_with_standard_path"]:
        logger.info("Auto-triggering marketing generator due to GROWTH detection")
        knowledge_ledger.store("next_action", "marketing_generator")
    
    return response

@app.post("/analyze-sentiment", response_model=SentimentAnalysisResponse)
async def analyze_sentiment(request: SentimentAnalysisRequest):
    """
    OBSERVE: Analyze sentiment of text
    """
    knowledge_ledger.increment_iteration()
    
    if knowledge_ledger.is_at_max_iterations():
        raise HTTPException(
            status_code=429,
            detail="Maximum iteration limit (5) reached for this task. Please reset and try again."
        )
    
    # OBSERVE
    observation = OODALoop.observe({"text_length": len(request.text)}, "analyze-sentiment")
    
    # Simple sentiment analysis (in production, use real NLP model)
    text_lower = request.text.lower()
    positive_words = ["good", "great", "excellent", "happy", "love", "best", "amazing"]
    negative_words = ["bad", "poor", "terrible", "hate", "worst", "awful", "horrible"]
    
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    if pos_count > neg_count:
        sentiment = "positive"
        confidence = min(0.6 + (pos_count * 0.1), 0.95)
        risk_level = RiskLevel.GROWTH
    elif neg_count > pos_count:
        sentiment = "negative"
        confidence = min(0.6 + (neg_count * 0.1), 0.95)
        risk_level = RiskLevel.RISK
    else:
        sentiment = "neutral"
        confidence = 0.5
        risk_level = RiskLevel.NEUTRAL
    
    # ORIENT
    orientation = OODALoop.orient(confidence, risk_level)
    
    # DECIDE
    decision = OODALoop.decide(orientation, risk_level)
    
    # ACT & Store
    action = OODALoop.act(decision, {"sentiment": sentiment, "confidence": confidence})
    knowledge_ledger.store("sentiment_analysis", action)
    
    response = SentimentAnalysisResponse(
        sentiment=sentiment,
        confidence=confidence,
        risk_level=risk_level
    )
    
    # Auto-trigger based on decision
    if decision == "security_audit" and orientation["proceed_with_standard_path"]:
        knowledge_ledger.store("next_action", "security_audit")
    elif decision == "marketing_generator" and orientation["proceed_with_standard_path"]:
        knowledge_ledger.store("next_action", "marketing_generator")
    
    return response

@app.post("/validate-logic", response_model=ValidationResponse)
async def validate_logic(request: ValidationRequest):
    """
    Validate logic and provide verified output
    Goal Completion: Verify the solution
    """
    # OBSERVE
    observation = OODALoop.observe(request.model_dump(), "validate-logic")
    
    # Validation logic
    is_valid = True
    messages = []
    
    # Check if required keys are present
    if not request.logic_data:
        is_valid = False
        messages.append("Logic data is empty")
    
    # Check ledger for previous results
    ledger_summary = knowledge_ledger.get_summary()
    if ledger_summary["entries"] == 0:
        messages.append("Warning: No previous operations in knowledge ledger")
    else:
        messages.append(f"Validated with {ledger_summary['entries']} previous operations")
    
    # Check iteration count
    if knowledge_ledger.iteration_count > 0:
        messages.append(f"Completed in {knowledge_ledger.iteration_count} iterations")
    
    message = "; ".join(messages) if messages else "Logic validated successfully"
    
    response = ValidationResponse(
        is_valid=is_valid,
        message=message,
        verified_at=datetime.now(UTC).isoformat()
    )
    
    # Store validation result
    knowledge_ledger.store("validation", {
        "is_valid": is_valid,
        "message": message
    })
    
    return response

# ===========================
# AUXILIARY TOOLS
# ===========================

@app.post("/security-audit", response_model=SecurityAuditResponse)
async def security_audit(request: SecurityAuditRequest):
    """
    DECIDE: Triggered when risk is detected
    Perform security audit on data
    """
    knowledge_ledger.increment_iteration()
    
    # OBSERVE
    observation = OODALoop.observe(request.model_dump(), "security-audit")
    
    # Security audit logic
    severity = "high" if len(request.risk_indicators) > 3 else "medium" if len(request.risk_indicators) > 1 else "low"
    
    recommendations = [
        "Enable multi-factor authentication",
        "Review access logs for anomalies",
        "Update security policies"
    ]
    
    if severity == "high":
        recommendations.append("Immediate security team notification required")
        recommendations.append("Consider temporary access restriction")
    
    response = SecurityAuditResponse(
        audit_status="completed",
        recommendations=recommendations,
        severity=severity
    )
    
    # Store in ledger
    knowledge_ledger.store("security_audit", {
        "status": "completed",
        "severity": severity,
        "recommendations_count": len(recommendations)
    })
    
    return response

@app.post("/marketing-generator", response_model=MarketingGeneratorResponse)
async def marketing_generator(request: MarketingGeneratorRequest):
    """
    DECIDE: Triggered when growth opportunity is detected
    Generate marketing campaigns
    """
    knowledge_ledger.increment_iteration()
    
    # OBSERVE
    observation = OODALoop.observe(request.model_dump(), "marketing-generator")
    
    # Marketing generation logic
    campaign_ideas = [
        f"Targeted email campaign for {request.target_audience}",
        f"Social media promotion highlighting growth trends",
        f"Referral program for engaged users"
    ]
    
    # Add specific campaigns based on growth indicators
    for indicator in request.growth_indicators[:2]:
        campaign_ideas.append(f"Campaign focused on {indicator}")
    
    estimated_reach = len(request.growth_indicators) * 1000 + 5000
    confidence = min(0.75 + (len(request.growth_indicators) * 0.05), 0.95)
    
    response = MarketingGeneratorResponse(
        campaign_ideas=campaign_ideas,
        estimated_reach=estimated_reach,
        confidence=confidence
    )
    
    # Store in ledger
    knowledge_ledger.store("marketing_campaign", {
        "ideas_count": len(campaign_ideas),
        "estimated_reach": estimated_reach,
        "confidence": confidence
    })
    
    return response

# ===========================
# UTILITY ENDPOINTS
# ===========================

@app.get("/knowledge-ledger")
async def get_knowledge_ledger():
    """Get the current state of the knowledge ledger"""
    return {
        "ledger": knowledge_ledger.ledger,
        "summary": knowledge_ledger.get_summary(),
        "at_max_iterations": knowledge_ledger.is_at_max_iterations()
    }

@app.post("/reset-ledger")
async def reset_ledger():
    """Reset the knowledge ledger for a new task"""
    knowledge_ledger.reset()
    return {"message": "Knowledge ledger reset successfully"}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Apex ML API",
        "version": "1.0.0",
        "description": "Autonomous ML Operations Agent with OODA Loop",
        "features": [
            "OODA Loop (Observe, Orient, Decide, Act)",
            "Auto-debugging (422 error handling)",
            "Contextual Memory (Knowledge Ledger)",
            "Security constraints (API key masking)",
            "Efficiency constraints (5 iteration limit)"
        ],
        "endpoints": {
            "ml_tools": ["/predict-churn", "/analyze-sentiment", "/validate-logic"],
            "auxiliary_tools": ["/security-audit", "/marketing-generator"],
            "utility": ["/knowledge-ledger", "/reset-ledger"]
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(UTC).isoformat(),
        "ledger_iterations": knowledge_ledger.iteration_count
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
