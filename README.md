# Apex-ML-API

## Senior Autonomous ML Operations Agent

An autonomous ML operations agent that implements the OODA Loop (Observe, Orient, Decide, Act) pattern with auto-debugging, contextual memory, and intelligent decision-making capabilities.

## Features

### 🧠 OODA Loop Intelligence
1. **OBSERVE**: Access to specialized ML API tools (`/predict-churn`, `/analyze-sentiment`)
2. **ORIENT**: Analyzes incoming data and confidence scores (low confidence <0.7 triggers manual review)
3. **DECIDE**: Independently chooses next tool based on risk analysis:
   - **Risk detected** → Triggers Security-Audit tool
   - **Growth detected** → Triggers Marketing-Generator tool
4. **ACT**: Executes chosen action with failure analysis and retry logic

### 🔧 Independent Capabilities

#### Auto-Debugging
- Automatically handles HTTP 422 (Validation Error) with schema hints
- Provides detailed error analysis and debugging suggestions
- Reads error codes and suggests fixes

#### Contextual Memory (Knowledge Ledger)
- Stores results of successful tool executions
- Maintains workflow context across multiple operations
- Informs final results with historical data

#### Goal Completion
- Validates outputs through `/validate-logic` endpoint
- Ensures verified output before task completion
- Tracks iteration count and workflow status

### 🔒 Constraints

#### Security
- **API Key Protection**: Automatically masks API keys and tokens in logs
- **Sensitive Data**: Redacts user IDs and sensitive information
- **No Credential Exposure**: Zero tolerance for credential leaks

#### Efficiency
- **Iteration Limit**: Maximum 5 iterations per task to prevent infinite loops
- **Resource Management**: Automatic cleanup and reset capabilities
- **Performance Monitoring**: Real-time tracking of operation counts

## Installation

```bash
# Clone the repository
git clone https://github.com/yadavanujkumar/Apex-ML-API.git
cd Apex-ML-API

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Running the Server

```bash
# Start the server
python main.py

# Or use uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### ML Tools

#### 1. Predict Churn
```bash
curl -X POST "http://localhost:8000/predict-churn" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "usage_metrics": {
      "daily_usage": 45.0,
      "weekly_logins": 3.0
    }
  }'
```

**Response**:
```json
{
  "prediction": "will_churn",
  "confidence": 0.65,
  "risk_level": "risk"
}
```

#### 2. Analyze Sentiment
```bash
curl -X POST "http://localhost:8000/analyze-sentiment" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This product is amazing and I love using it!"
  }'
```

**Response**:
```json
{
  "sentiment": "positive",
  "confidence": 0.8,
  "risk_level": "growth"
}
```

#### 3. Validate Logic
```bash
curl -X POST "http://localhost:8000/validate-logic" \
  -H "Content-Type: application/json" \
  -d '{
    "logic_data": {
      "workflow": "churn_prediction",
      "steps": ["predict", "analyze", "validate"]
    }
  }'
```

**Response**:
```json
{
  "is_valid": true,
  "message": "Validated with 2 previous operations; Completed in 2 iterations",
  "verified_at": "2026-02-06T05:08:00.000Z"
}
```

### Auxiliary Tools

#### 4. Security Audit
```bash
curl -X POST "http://localhost:8000/security-audit" \
  -H "Content-Type: application/json" \
  -d '{
    "data_source": "user_database",
    "risk_indicators": ["suspicious_login", "multiple_failures"]
  }'
```

#### 5. Marketing Generator
```bash
curl -X POST "http://localhost:8000/marketing-generator" \
  -H "Content-Type: application/json" \
  -d '{
    "growth_indicators": ["increased_engagement", "positive_reviews"],
    "target_audience": "tech_enthusiasts"
  }'
```

### Utility Endpoints

#### Get Knowledge Ledger State
```bash
curl -X GET "http://localhost:8000/knowledge-ledger"
```

#### Reset Knowledge Ledger
```bash
curl -X POST "http://localhost:8000/reset-ledger"
```

#### Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

## Usage Examples

### Example 1: Complete Risk Detection Workflow

```python
import requests

base_url = "http://localhost:8000"

# Step 1: Predict churn (OBSERVE & ORIENT)
response = requests.post(f"{base_url}/predict-churn", json={
    "user_id": "user_at_risk",
    "usage_metrics": {"daily_usage": 15.0}
})
result = response.json()
print(f"Risk Level: {result['risk_level']}")  # Output: risk

# Step 2: If risk detected, perform security audit (DECIDE & ACT)
if result['risk_level'] == 'risk' and result['confidence'] >= 0.7:
    audit_response = requests.post(f"{base_url}/security-audit", json={
        "data_source": "user_at_risk_data",
        "risk_indicators": ["low_usage", "churn_risk"]
    })
    audit = audit_response.json()
    print(f"Audit Status: {audit['audit_status']}")
    print(f"Recommendations: {audit['recommendations']}")

# Step 3: Validate the workflow (GOAL COMPLETION)
validation = requests.post(f"{base_url}/validate-logic", json={
    "logic_data": {"workflow": "risk_detection"}
})
print(f"Validated: {validation.json()['is_valid']}")
```

### Example 2: Growth Optimization Workflow

```python
import requests

base_url = "http://localhost:8000"

# Step 1: Analyze sentiment (OBSERVE & ORIENT)
response = requests.post(f"{base_url}/analyze-sentiment", json={
    "text": "This product is excellent! Best purchase ever!"
})
result = response.json()

# Step 2: If growth detected, generate marketing campaigns (DECIDE & ACT)
if result['risk_level'] == 'growth' and result['confidence'] >= 0.7:
    marketing = requests.post(f"{base_url}/marketing-generator", json={
        "growth_indicators": ["positive_sentiment", "high_engagement"],
        "target_audience": "satisfied_customers"
    })
    campaigns = marketing.json()
    print(f"Campaign Ideas: {campaigns['campaign_ideas']}")
    print(f"Estimated Reach: {campaigns['estimated_reach']}")
```

## Testing

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest test_main.py -v

# Run specific test categories
pytest test_main.py::TestOODALoop -v
pytest test_main.py::TestSecurityFeatures -v
pytest test_main.py::TestEfficiencyConstraints -v

# Run with coverage
pytest test_main.py --cov=main --cov-report=html
```

## Architecture

### OODA Loop Flow

```
┌─────────────┐
│  OBSERVE    │ ← Collect data from ML tools
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  ORIENT     │ ← Analyze confidence & risk
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  DECIDE     │ ← Choose next action
└──────┬──────┘   (security_audit | marketing_generator | manual_review)
       │
       ▼
┌─────────────┐
│    ACT      │ ← Execute & store in Knowledge Ledger
└─────────────┘
```

### Knowledge Ledger

The Knowledge Ledger maintains contextual memory:
- Stores successful operation results
- Tracks iteration count (max 5)
- Provides workflow history
- Informs validation decisions

### Security Features

1. **Automatic Masking**: API keys, tokens, and user IDs are automatically redacted in logs
2. **Validation Errors**: Detailed debugging hints without exposing sensitive data
3. **Secure Logging**: All logs pass through security filter

### Efficiency Controls

1. **Iteration Limiting**: Prevents infinite loops (max 5 iterations)
2. **Resource Cleanup**: Reset endpoint for starting fresh
3. **Performance Tracking**: Real-time monitoring of operation counts

## Development

### Project Structure

```
Apex-ML-API/
├── main.py           # Main application with OODA loop
├── test_main.py      # Comprehensive test suite
├── requirements.txt  # Python dependencies
├── .gitignore       # Git ignore rules
└── README.md        # This file
```

### Adding New ML Tools

To add a new ML endpoint following OODA principles:

1. **Create endpoint** with appropriate request/response models
2. **Implement OBSERVE** phase - log incoming data
3. **Implement ORIENT** phase - analyze confidence and risk
4. **Implement DECIDE** phase - route to appropriate tool
5. **Implement ACT** phase - execute and store in ledger
6. **Add tests** for all scenarios

## Configuration

Environment variables (optional):

```bash
export LOG_LEVEL=INFO
export MAX_ITERATIONS=5
export API_HOST=0.0.0.0
export API_PORT=8000
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Contact: [Repository Owner](https://github.com/yadavanujkumar)

## Acknowledgments

- Built with FastAPI for high performance
- Implements OODA Loop decision-making pattern
- Follows security best practices for ML operations