# 🛍️ E-commerce Product Personalization Guide

## 🎯 Overview

The AdMorph.AI E-commerce Personalization module transforms your existing agentic advertising framework into a powerful product personalization engine. Instead of creating Facebook/Instagram ads, the same AI agents now generate personalized product listings that adapt to different customer demographics in real-time.

## 🧠 How It Works

### **Same Brain, Different Output**

```
INPUT: Demographics JSON          OUTPUT: Personalized Product Listings
      ↓                                        ↓
Same AI Analysis                    Different Format
      ↓                                        ↓
Same Agent Logic                    E-commerce Optimized
```

### **Real-world Example**

**Product**: Wireless Headphones ($99.99)

**Customer A** (25-year-old fitness enthusiast):
- **Title**: "Wireless Sport Headphones - Sweat-Proof for Intense Workouts"
- **Description**: "Push your limits with these ultra-secure, sweat-resistant headphones..."
- **Features**: Sweat-proof, Secure fit, 20hr battery
- **Image**: Person running with headphones

**Customer B** (45-year-old business professional):
- **Title**: "Premium Wireless Headphones - Crystal Clear Calls & Noise Cancellation"
- **Description**: "Elevate your professional presence with premium audio quality..."
- **Features**: Noise cancellation, Clear calls, Premium quality
- **Image**: Business person in office with headphones

## 🚀 Quick Start

### 1. **Test the System**

```bash
# Run comprehensive test suite
python test_ecommerce_personalization.py
```

### 2. **Start the API Server**

```bash
# Start the backend service
cd admorph_backend
python -m api.main
```

### 3. **Access API Documentation**

Visit: `http://localhost:8000/docs`

## 📡 API Endpoints

### **Core Product Management**

```http
GET    /api/products/                    # List all products
GET    /api/products/{product_id}        # Get specific product
POST   /api/products/                    # Create new product
```

### **Personalization Engine**

```http
POST   /api/products/{product_id}/personalize           # Generate variants
GET    /api/products/jobs/{job_id}                      # Check job status
POST   /api/products/{product_id}/quick-personalize     # Demo with samples
```

### **Variant Management**

```http
GET    /api/products/{product_id}/variants              # Get all variants
GET    /api/products/variants/{variant_id}              # Get specific variant
POST   /api/products/variants/{variant_id}/performance  # Update metrics
```

### **Analytics & Testing**

```http
GET    /api/products/{product_id}/performance           # Performance metrics
POST   /api/products/ab-test                           # Run A/B tests
GET    /api/products/demo/demographics                  # Sample demographics
```

## 🛠️ Usage Examples

### **Example 1: Basic Personalization**

```python
import requests

# 1. Get sample demographics
demographics = requests.get("http://localhost:8000/api/products/demo/demographics").json()

# 2. Personalize a product
personalization_request = {
    "product_id": "wireless-headphones-001",
    "target_demographics": demographics[:2],  # Use first 2 demographics
    "personalization_goals": ["increase_conversion", "highlight_features"],
    "platform_context": "shopify",
    "brand_guidelines": {"tone": "friendly", "style": "modern"}
}

response = requests.post(
    "http://localhost:8000/api/products/wireless-headphones-001/personalize",
    json=personalization_request
)

job_id = response.json()["job_id"]

# 3. Check results
import time
time.sleep(30)  # Wait for processing

results = requests.get(f"http://localhost:8000/api/products/jobs/{job_id}").json()
print("Personalized variants:", len(results["result"]["generated_variants"]))
```

### **Example 2: Quick Demo**

```python
# Quick personalization with sample demographics
response = requests.post(
    "http://localhost:8000/api/products/wireless-headphones-001/quick-personalize"
)

variants = response.json()["result"]["generated_variants"]
for variant in variants:
    print(f"Demographic: {variant['demographic_segment']['name']}")
    print(f"Title: {variant['personalized_title']}")
    print(f"Features: {', '.join(variant['highlighted_features'])}")
    print("---")
```

### **Example 3: Performance Tracking**

```python
# Update variant performance
performance_update = {
    "views": 1000,
    "purchases": 45
}

response = requests.post(
    f"http://localhost:8000/api/products/variants/{variant_id}/performance",
    json=performance_update
)

updated_variant = response.json()
print(f"Conversion rate: {updated_variant['conversion_rate']:.1%}")
```

### **Example 4: A/B Testing**

```python
# Run A/B test between variants
ab_test_request = {
    "variant_ids": ["variant-1-id", "variant-2-id"],
    "test_config": {
        "duration_days": 14,
        "traffic_split": 50,
        "metric": "conversion_rate"
    }
}

response = requests.post(
    "http://localhost:8000/api/products/ab-test",
    json=ab_test_request
)

test_results = response.json()
print(f"Winner: {test_results['winner']}")
print(f"Improvement: {test_results['improvement']:.1f}%")
```

## 🎯 Data Models

### **BaseProduct**
```python
{
    "product_id": "wireless-headphones-001",
    "name": "Premium Wireless Headphones",
    "base_price": 99.99,
    "category": "Electronics",
    "brand": "AudioTech",
    "features": ["Bluetooth 5.0", "20hr battery", "Noise cancellation"],
    "specifications": {"driver_size": "40mm", "weight": "250g"},
    "base_images": ["image1.jpg", "image2.jpg"],
    "inventory_count": 150
}
```

### **ProductVariant**
```python
{
    "variant_id": "variant-123",
    "product_id": "wireless-headphones-001",
    "demographic_segment": {...},
    "personalized_title": "Wireless Sport Headphones - Sweat-Proof for Workouts",
    "personalized_description": "Push your limits with these ultra-secure...",
    "highlighted_features": ["Sweat-proof", "Secure fit", "20hr battery"],
    "price_positioning": "performance",
    "call_to_action": "Get Yours Now",
    "urgency_messaging": "Limited time offer",
    "social_proof": "Trusted by 10,000+ athletes",
    "personalization_score": 0.92,
    "conversion_rate": 0.045,
    "view_count": 1250,
    "purchase_count": 56
}
```

### **DemographicSegment**
```python
{
    "segment_id": "fitness-enthusiasts",
    "name": "Fitness Enthusiasts",
    "age_range": [22, 40],
    "gender": "all",
    "interests": ["Fitness", "Health", "Sports"],
    "behaviors": ["Health-conscious", "Active lifestyle", "Goal-oriented"],
    "location": "United States",
    "income_level": "Middle",
    "education": "High School"
}
```

## 🔧 Integration with Frontend

### **React/Next.js Integration**

```typescript
// API service for product personalization
class ProductPersonalizationService {
  private baseURL = 'http://localhost:8000/api/products';
  
  async personalizeProduct(productId: string, demographics: any[]) {
    const response = await fetch(`${this.baseURL}/${productId}/personalize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        target_demographics: demographics,
        personalization_goals: ['increase_conversion'],
        platform_context: 'shopify'
      })
    });
    
    return response.json();
  }
  
  async getPersonalizationResult(jobId: string) {
    const response = await fetch(`${this.baseURL}/jobs/${jobId}`);
    return response.json();
  }
  
  async getProductVariants(productId: string) {
    const response = await fetch(`${this.baseURL}/${productId}/variants`);
    return response.json();
  }
}
```

### **Real-time Updates with WebSocket**

```typescript
// WebSocket for real-time personalization updates
const ws = new WebSocket('ws://localhost:8000/ws/personalization');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'personalization_progress') {
    updateProgressBar(data.progress);
  }
  
  if (data.type === 'personalization_complete') {
    displayPersonalizedVariants(data.variants);
  }
};
```

## 📊 Performance Optimization

### **Caching Strategy**
- Cache demographic analysis results
- Store frequently requested product variants
- Use Redis for session-based personalization

### **Batch Processing**
- Process multiple demographics simultaneously
- Queue personalization requests for high traffic
- Implement rate limiting for API protection

### **A/B Testing Best Practices**
- Run tests for minimum 2 weeks
- Ensure statistical significance (95% confidence)
- Test one variable at a time
- Monitor both conversion and revenue metrics

## 🎉 Success Metrics

### **Expected Improvements**
- **15-40% increase** in conversion rates
- **25-60% improvement** in engagement metrics
- **20-35% boost** in average order value
- **30-50% reduction** in bounce rates

### **Key Performance Indicators**
- Conversion rate by demographic segment
- Time spent on personalized product pages
- Click-through rates on personalized CTAs
- Revenue per visitor improvement

## 🚀 Next Steps

1. **Test the system** with your product catalog
2. **Integrate with your e-commerce platform** (Shopify, WooCommerce, etc.)
3. **Set up performance tracking** and analytics
4. **Launch A/B tests** to optimize personalization
5. **Scale to your entire product catalog**

## 🆘 Troubleshooting

### **Common Issues**
- **Personalization fails**: Check OpenAI API key and quota
- **No variants generated**: Verify demographic data format
- **Performance tracking not working**: Ensure variant IDs are correct
- **A/B test errors**: Check that variants exist before testing

### **Debug Mode**
```bash
# Run with debug logging
ADMORPH_LOG_LEVEL=DEBUG python -m admorph_backend.api.main
```

**Your e-commerce personalization system is ready to boost conversions!** 🛍️🚀
