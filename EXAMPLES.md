# Apex ML API - Example Usage Guide

This guide demonstrates how to use the Autonomous ML Operations Agent in various scenarios.

## Prerequisites

```bash
# Start the server
python main.py
# Or
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Scenario 1: Customer Churn Risk Detection

This scenario demonstrates the complete OODA loop for identifying and handling customer churn risk.

```python
import requests
import json

base_url = "http://localhost:8000"

# Step 1: OBSERVE & ORIENT - Predict customer churn
print("=== Step 1: Predicting Churn ===")
churn_response = requests.post(
    f"{base_url}/predict-churn",
    json={
        "user_id": "customer_at_risk",
        "usage_metrics": {
            "daily_usage": 15.0,
            "weekly_logins": 1.0,
            "feature_usage": 10.0
        }
    }
)

churn_result = churn_response.json()
print(f"Prediction: {churn_result['prediction']}")
print(f"Confidence: {churn_result['confidence']}")
print(f"Risk Level: {churn_result['risk_level']}")

# Step 2: DECIDE & ACT - If high confidence risk, trigger security audit
if churn_result['risk_level'] == 'risk' and churn_result['confidence'] >= 0.7:
    print("\n=== Step 2: Triggering Security Audit ===")
    audit_response = requests.post(
        f"{base_url}/security-audit",
        json={
            "data_source": "customer_at_risk_profile",
            "risk_indicators": [
                "low_usage",
                "decreased_engagement",
                "churn_risk"
            ]
        }
    )
    
    audit_result = audit_response.json()
    print(f"Audit Status: {audit_result['audit_status']}")
    print(f"Severity: {audit_result['severity']}")
    print("Recommendations:")
    for rec in audit_result['recommendations']:
        print(f"  - {rec}")

# Step 3: GOAL COMPLETION - Validate the workflow
print("\n=== Step 3: Validating Workflow ===")
validation_response = requests.post(
    f"{base_url}/validate-logic",
    json={
        "logic_data": {
            "workflow": "churn_risk_detection",
            "steps": ["predict", "audit", "validate"],
            "customer_id": "customer_at_risk"
        }
    }
)

validation_result = validation_response.json()
print(f"Is Valid: {validation_result['is_valid']}")
print(f"Message: {validation_result['message']}")
print(f"Verified At: {validation_result['verified_at']}")

# Check the knowledge ledger
print("\n=== Knowledge Ledger State ===")
ledger_response = requests.get(f"{base_url}/knowledge-ledger")
ledger = ledger_response.json()
print(f"Total Entries: {ledger['summary']['entries']}")
print(f"Iterations Used: {ledger['summary']['iterations']}")
print(f"Stored Keys: {', '.join(ledger['summary']['keys'])}")
```

## Scenario 2: Growth Opportunity Detection

This scenario shows how positive sentiment triggers marketing campaigns.

```python
import requests

base_url = "http://localhost:8000"

# Reset ledger for new task
requests.post(f"{base_url}/reset-ledger")

# Step 1: Analyze positive feedback
print("=== Step 1: Analyzing Customer Sentiment ===")
sentiment_response = requests.post(
    f"{base_url}/analyze-sentiment",
    json={
        "text": "This product is absolutely amazing! Best purchase I've made this year. Excellent features and great support!"
    }
)

sentiment_result = sentiment_response.json()
print(f"Sentiment: {sentiment_result['sentiment']}")
print(f"Confidence: {sentiment_result['confidence']}")
print(f"Risk Level: {sentiment_result['risk_level']}")

# Step 2: Generate marketing campaigns for growth opportunity
if sentiment_result['risk_level'] == 'growth' and sentiment_result['confidence'] >= 0.7:
    print("\n=== Step 2: Generating Marketing Campaigns ===")
    marketing_response = requests.post(
        f"{base_url}/marketing-generator",
        json={
            "growth_indicators": [
                "positive_sentiment",
                "high_satisfaction",
                "feature_praise",
                "support_appreciation"
            ],
            "target_audience": "satisfied_customers"
        }
    )
    
    marketing_result = marketing_response.json()
    print(f"Campaign Ideas:")
    for idea in marketing_result['campaign_ideas']:
        print(f"  - {idea}")
    print(f"Estimated Reach: {marketing_result['estimated_reach']}")
    print(f"Confidence: {marketing_result['confidence']}")

# Step 3: Validate the workflow
print("\n=== Step 3: Validating Growth Strategy ===")
validation_response = requests.post(
    f"{base_url}/validate-logic",
    json={
        "logic_data": {
            "workflow": "growth_optimization",
            "steps": ["sentiment_analysis", "marketing", "validate"]
        }
    }
)

print(f"Workflow Valid: {validation_response.json()['is_valid']}")
```

## Scenario 3: Low Confidence Handling

This shows how the system handles low-confidence predictions.

```python
import requests

base_url = "http://localhost:8000"

# Reset for new task
requests.post(f"{base_url}/reset-ledger")

print("=== Testing Low Confidence Scenario ===")
# Usage metrics that result in borderline prediction
response = requests.post(
    f"{base_url}/predict-churn",
    json={
        "user_id": "uncertain_customer",
        "usage_metrics": {
            "daily_usage": 48.0,
            "weekly_logins": 52.0
        }
    }
)

result = response.json()
print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']}")

if result['confidence'] < 0.7:
    print("\n⚠️  Low confidence detected!")
    print("System will route to manual review instead of automatic action.")
    print("This prevents incorrect automated decisions.")
```

## Scenario 4: Iteration Limit Protection

This demonstrates the efficiency constraint (5 iteration limit).

```python
import requests

base_url = "http://localhost:8000"

# Reset ledger
requests.post(f"{base_url}/reset-ledger")

print("=== Testing Iteration Limit ===")

# Make multiple requests
for i in range(6):
    response = requests.post(
        f"{base_url}/predict-churn",
        json={
            "user_id": f"user_{i}",
            "usage_metrics": {"daily_usage": 30.0 + i}
        }
    )
    
    if response.status_code == 200:
        print(f"Request {i+1}: Success")
    elif response.status_code == 429:
        print(f"Request {i+1}: Blocked - Maximum iterations reached")
        print(f"Error: {response.json()['detail']}")
        break

# Reset to continue working
print("\n=== Resetting Ledger ===")
reset_response = requests.post(f"{base_url}/reset-ledger")
print(reset_response.json()['message'])

# Now requests work again
response = requests.post(
    f"{base_url}/predict-churn",
    json={
        "user_id": "user_new",
        "usage_metrics": {"daily_usage": 45.0}
    }
)
print(f"After reset: {response.status_code == 200 and 'Success' or 'Failed'}")
```

## Scenario 5: Auto-Debugging

This shows the auto-debugging capability for validation errors.

```python
import requests

base_url = "http://localhost:8000"

print("=== Testing Auto-Debugging ===")

# Intentionally send invalid request (missing required field)
response = requests.post(
    f"{base_url}/predict-churn",
    json={
        "user_id": "test_user"
        # Missing: usage_metrics
    }
)

if response.status_code == 422:
    error = response.json()
    print("Validation Error Detected!")
    print(f"Error Type: {error['error']}")
    print(f"Debug Hint: {error['debug_hint']}")
    print(f"Documentation: {error['documentation']}")
    print("\nDetailed Errors:")
    for detail in error['detail']:
        print(f"  - Field: {detail['loc']}")
        print(f"    Message: {detail['msg']}")

# Send request with invalid data type
print("\n=== Testing Type Validation ===")
response = requests.post(
    f"{base_url}/predict-churn",
    json={
        "user_id": 12345,  # Should be string
        "usage_metrics": {"daily_usage": "not_a_number"}  # Should be float
    }
)

if response.status_code == 422:
    error = response.json()
    print("Type validation errors caught!")
    print(f"Hint: {error['debug_hint']}")
```

## Scenario 6: Security - Sensitive Data Masking

The system automatically masks sensitive data in logs.

```python
import requests

base_url = "http://localhost:8000"

print("=== Testing Security Features ===")

# Make request with sensitive data
# The API will process it but mask it in logs
response = requests.post(
    f"{base_url}/predict-churn",
    json={
        "user_id": "sensitive_user_12345",  # Will be masked in logs
        "usage_metrics": {
            "daily_usage": 55.0,
            "api_key": "secret_key_abc123"  # Will be masked in logs
        }
    }
)

print(f"Request processed: {response.status_code == 200}")
print("Note: Sensitive data like user_id and api_key are masked in server logs")
print("Check server logs to see masking in action: ***REDACTED***")
```

## Health Check and Monitoring

```python
import requests

base_url = "http://localhost:8000"

# Check API health
health = requests.get(f"{base_url}/health").json()
print(f"Status: {health['status']}")
print(f"Current Iterations: {health['ledger_iterations']}")

# Get API information
info = requests.get(f"{base_url}/").json()
print(f"\nAPI Name: {info['name']}")
print(f"Version: {info['version']}")
print("Features:")
for feature in info['features']:
    print(f"  - {feature}")

# Check knowledge ledger state
ledger = requests.get(f"{base_url}/knowledge-ledger").json()
print(f"\nLedger State:")
print(f"  Entries: {ledger['summary']['entries']}")
print(f"  Iterations: {ledger['summary']['iterations']}")
print(f"  At Max: {ledger['at_max_iterations']}")
```

## Complete Workflow Example

```python
import requests
import time

base_url = "http://localhost:8000"

def run_complete_workflow():
    """Complete autonomous workflow demonstration"""
    
    # Reset for clean start
    requests.post(f"{base_url}/reset-ledger")
    
    print("🤖 Starting Autonomous ML Operations Agent Workflow\n")
    
    # 1. OBSERVE - Collect data
    print("📊 OBSERVE: Analyzing customer data...")
    churn_data = {
        "user_id": "demo_customer",
        "usage_metrics": {
            "daily_usage": 12.0,
            "weekly_logins": 0.5,
            "support_tickets": 3.0
        }
    }
    
    churn_response = requests.post(
        f"{base_url}/predict-churn",
        json=churn_data
    )
    churn_result = churn_response.json()
    
    # 2. ORIENT - Analyze confidence and risk
    print(f"\n🎯 ORIENT: Risk Level = {churn_result['risk_level']}")
    print(f"           Confidence = {churn_result['confidence']:.2f}")
    
    # 3. DECIDE - Choose action
    print(f"\n🤔 DECIDE: {'High risk detected!' if churn_result['risk_level'] == 'risk' else 'Growth opportunity!'}")
    
    # 4. ACT - Execute
    if churn_result['risk_level'] == 'risk' and churn_result['confidence'] >= 0.7:
        print("\n⚡ ACT: Executing security audit...")
        audit_response = requests.post(
            f"{base_url}/security-audit",
            json={
                "data_source": "demo_customer_profile",
                "risk_indicators": ["low_usage", "high_support_load"]
            }
        )
        action_result = audit_response.json()
        print(f"    Audit completed: {action_result['audit_status']}")
        print(f"    Severity: {action_result['severity']}")
    
    # 5. VALIDATE
    print("\n✅ VALIDATE: Verifying workflow...")
    validation = requests.post(
        f"{base_url}/validate-logic",
        json={
            "logic_data": {
                "workflow": "autonomous_decision",
                "customer": "demo_customer"
            }
        }
    )
    
    print(f"    Workflow valid: {validation.json()['is_valid']}")
    
    # 6. Check ledger
    ledger = requests.get(f"{base_url}/knowledge-ledger").json()
    print(f"\n📚 KNOWLEDGE LEDGER:")
    print(f"    Stored {ledger['summary']['entries']} operations")
    print(f"    Used {ledger['summary']['iterations']} iterations")
    
    print("\n✨ Workflow completed successfully!")

# Run the workflow
run_complete_workflow()
```

## Output Examples

The above scripts will produce output similar to:

```
🤖 Starting Autonomous ML Operations Agent Workflow

📊 OBSERVE: Analyzing customer data...

🎯 ORIENT: Risk Level = risk
           Confidence = 0.76

🤔 DECIDE: High risk detected!

⚡ ACT: Executing security audit...
    Audit completed: completed
    Severity: medium

✅ VALIDATE: Verifying workflow...
    Workflow valid: True

📚 KNOWLEDGE LEDGER:
    Stored 3 operations
    Used 2 iterations

✨ Workflow completed successfully!
```

## Tips for Production Use

1. **Always reset ledger** between independent tasks to prevent iteration limit issues
2. **Check confidence scores** before trusting automated decisions (>= 0.7 recommended)
3. **Monitor the ledger** to track operation history and debug issues
4. **Use validation** to ensure workflow integrity before final decisions
5. **Implement error handling** around API calls for production robustness
6. **Review logs** regularly - sensitive data is automatically masked
