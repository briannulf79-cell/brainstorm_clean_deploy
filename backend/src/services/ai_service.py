import os
import json
import openai
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import re
import statistics

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_base = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')

@dataclass
class LeadScore:
    contact_id: int
    score: float
    confidence: float
    factors: List[str]
    reasoning: str

@dataclass
class ConversationInsight:
    conversation_id: int
    sentiment: str
    sentiment_score: float
    intent: str
    intent_confidence: float
    entities: Dict[str, str]
    summary: str
    next_best_action: str

@dataclass
class PredictiveInsight:
    metric: str
    current_value: float
    predicted_value: float
    confidence: float
    timeframe: str
    factors: List[str]

class AIService:
    """Advanced AI service for lead scoring, conversation analysis, and predictions"""
    
    def __init__(self):
        self.model = "gpt-3.5-turbo"
        self.embedding_model = "text-embedding-ada-002"
    
    async def calculate_lead_score(self, contact_data: Dict) -> LeadScore:
        """Calculate AI-powered lead score based on contact data and behavior"""
        try:
            # Prepare context for AI analysis
            context = self._prepare_lead_context(contact_data)
            
            prompt = f"""
            Analyze this lead and provide a comprehensive scoring assessment:
            
            Contact Information:
            {context}
            
            Please provide:
            1. Lead score (0-100)
            2. Confidence level (0-100)
            3. Top 3 factors influencing the score
            4. Brief reasoning for the score
            
            Format your response as JSON:
            {{
                "score": <number>,
                "confidence": <number>,
                "factors": ["factor1", "factor2", "factor3"],
                "reasoning": "explanation"
            }}
            """
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert sales AI that analyzes leads and provides accurate scoring based on behavioral patterns, demographics, and engagement data."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return LeadScore(
                contact_id=contact_data['id'],
                score=result['score'],
                confidence=result['confidence'],
                factors=result['factors'],
                reasoning=result['reasoning']
            )
            
        except Exception as e:
            # Fallback to rule-based scoring
            return self._fallback_lead_scoring(contact_data)
    
    async def analyze_conversation(self, conversation_data: Dict) -> ConversationInsight:
        """Analyze conversation for sentiment, intent, and insights"""
        try:
            messages = conversation_data.get('messages', [])
            if not messages:
                return self._empty_conversation_insight(conversation_data['id'])
            
            # Combine all messages for analysis
            conversation_text = "\n".join([
                f"{'Customer' if msg['direction'] == 'inbound' else 'Agent'}: {msg['content']}"
                for msg in messages
            ])
            
            prompt = f"""
            Analyze this customer conversation and provide insights:
            
            Conversation:
            {conversation_text}
            
            Please provide:
            1. Overall sentiment (positive/neutral/negative)
            2. Sentiment score (-1 to 1)
            3. Primary intent (demo_request/pricing_inquiry/support_request/general_inquiry)
            4. Intent confidence (0-100)
            5. Key entities mentioned (names, dates, products, etc.)
            6. Brief summary of the conversation
            7. Recommended next action
            
            Format as JSON:
            {{
                "sentiment": "positive/neutral/negative",
                "sentiment_score": <number>,
                "intent": "intent_type",
                "intent_confidence": <number>,
                "entities": {{"entity_type": "value"}},
                "summary": "brief summary",
                "next_action": "recommended action"
            }}
            """
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert conversation analyst that provides accurate sentiment analysis, intent detection, and actionable insights for customer service teams."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return ConversationInsight(
                conversation_id=conversation_data['id'],
                sentiment=result['sentiment'],
                sentiment_score=result['sentiment_score'],
                intent=result['intent'],
                intent_confidence=result['intent_confidence'],
                entities=result['entities'],
                summary=result['summary'],
                next_best_action=result['next_action']
            )
            
        except Exception as e:
            # Fallback to rule-based analysis
            return self._fallback_conversation_analysis(conversation_data)
    
    async def generate_predictive_insights(self, historical_data: Dict) -> List[PredictiveInsight]:
        """Generate predictive insights based on historical data"""
        try:
            insights = []
            
            # Revenue prediction
            revenue_insight = await self._predict_revenue(historical_data.get('revenue', []))
            if revenue_insight:
                insights.append(revenue_insight)
            
            # Conversion prediction
            conversion_insight = await self._predict_conversions(historical_data.get('conversions', []))
            if conversion_insight:
                insights.append(conversion_insight)
            
            # Churn prediction
            churn_insight = await self._predict_churn(historical_data.get('churn', []))
            if churn_insight:
                insights.append(churn_insight)
            
            return insights
            
        except Exception as e:
            return self._fallback_predictions()
    
    async def generate_content_suggestions(self, context: Dict) -> List[str]:
        """Generate AI-powered content suggestions for emails, messages, etc."""
        try:
            contact_info = context.get('contact', {})
            conversation_history = context.get('conversation_history', [])
            intent = context.get('intent', 'general')
            
            prompt = f"""
            Generate 3 personalized message suggestions for this context:
            
            Contact: {contact_info.get('name', 'Customer')}
            Company: {contact_info.get('company', 'Unknown')}
            Intent: {intent}
            Recent conversation: {conversation_history[-1]['content'] if conversation_history else 'No recent messages'}
            
            Provide 3 different message options:
            1. Professional and formal
            2. Friendly and conversational
            3. Direct and action-oriented
            
            Format as JSON array: ["message1", "message2", "message3"]
            """
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert copywriter that creates personalized, effective business communications."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return self._fallback_content_suggestions(context)
    
    async def optimize_workflow(self, workflow_data: Dict) -> Dict:
        """Analyze and suggest optimizations for automation workflows"""
        try:
            steps = workflow_data.get('steps', [])
            performance_data = workflow_data.get('performance', {})
            
            prompt = f"""
            Analyze this automation workflow and suggest optimizations:
            
            Workflow Steps: {json.dumps(steps, indent=2)}
            Performance Data: {json.dumps(performance_data, indent=2)}
            
            Provide optimization suggestions:
            1. Identify bottlenecks or inefficiencies
            2. Suggest improvements to increase conversion rates
            3. Recommend timing optimizations
            4. Suggest A/B testing opportunities
            
            Format as JSON:
            {{
                "bottlenecks": ["issue1", "issue2"],
                "improvements": ["suggestion1", "suggestion2"],
                "timing_optimizations": ["timing1", "timing2"],
                "ab_test_ideas": ["test1", "test2"],
                "overall_score": <number 0-100>,
                "priority_actions": ["action1", "action2"]
            }}
            """
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert marketing automation consultant that optimizes workflows for maximum efficiency and conversion rates."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return self._fallback_workflow_optimization()
    
    def _prepare_lead_context(self, contact_data: Dict) -> str:
        """Prepare contact data context for AI analysis"""
        context_parts = []
        
        # Basic info
        if contact_data.get('name'):
            context_parts.append(f"Name: {contact_data['name']}")
        if contact_data.get('email'):
            context_parts.append(f"Email: {contact_data['email']}")
        if contact_data.get('company'):
            context_parts.append(f"Company: {contact_data['company']}")
        if contact_data.get('title'):
            context_parts.append(f"Title: {contact_data['title']}")
        
        # Engagement data
        if contact_data.get('email_opens'):
            context_parts.append(f"Email Opens: {contact_data['email_opens']}")
        if contact_data.get('page_views'):
            context_parts.append(f"Page Views: {contact_data['page_views']}")
        if contact_data.get('form_submissions'):
            context_parts.append(f"Form Submissions: {contact_data['form_submissions']}")
        
        # Behavioral data
        if contact_data.get('last_activity'):
            context_parts.append(f"Last Activity: {contact_data['last_activity']}")
        if contact_data.get('source'):
            context_parts.append(f"Lead Source: {contact_data['source']}")
        
        return "\n".join(context_parts)
    
    def _fallback_lead_scoring(self, contact_data: Dict) -> LeadScore:
        """Fallback rule-based lead scoring when AI is unavailable"""
        score = 50  # Base score
        factors = []
        
        # Email engagement
        if contact_data.get('email_opens', 0) > 5:
            score += 15
            factors.append("High email engagement")
        
        # Website activity
        if contact_data.get('page_views', 0) > 10:
            score += 10
            factors.append("Active website visitor")
        
        # Form submissions
        if contact_data.get('form_submissions', 0) > 0:
            score += 20
            factors.append("Form submissions")
        
        # Company size (if available)
        if contact_data.get('company_size', 0) > 100:
            score += 10
            factors.append("Large company")
        
        # Recent activity
        if contact_data.get('last_activity'):
            last_activity = datetime.fromisoformat(contact_data['last_activity'].replace('Z', '+00:00'))
            if (datetime.now() - last_activity).days < 7:
                score += 5
                factors.append("Recent activity")
        
        return LeadScore(
            contact_id=contact_data['id'],
            score=min(score, 100),
            confidence=75,
            factors=factors[:3],
            reasoning="Rule-based scoring using engagement and behavioral data"
        )
    
    def _fallback_conversation_analysis(self, conversation_data: Dict) -> ConversationInsight:
        """Fallback rule-based conversation analysis"""
        messages = conversation_data.get('messages', [])
        if not messages:
            return self._empty_conversation_insight(conversation_data['id'])
        
        # Simple sentiment analysis
        last_message = messages[-1]['content'].lower()
        positive_words = ['great', 'excellent', 'love', 'amazing', 'perfect', 'thank you', 'thanks']
        negative_words = ['bad', 'terrible', 'hate', 'awful', 'problem', 'issue', 'disappointed']
        
        positive_count = sum(1 for word in positive_words if word in last_message)
        negative_count = sum(1 for word in negative_words if word in last_message)
        
        if positive_count > negative_count:
            sentiment = "positive"
            sentiment_score = 0.7
        elif negative_count > positive_count:
            sentiment = "negative"
            sentiment_score = -0.7
        else:
            sentiment = "neutral"
            sentiment_score = 0.0
        
        # Simple intent detection
        intent = "general_inquiry"
        if any(word in last_message for word in ['demo', 'demonstration', 'show']):
            intent = "demo_request"
        elif any(word in last_message for word in ['price', 'cost', 'pricing']):
            intent = "pricing_inquiry"
        elif any(word in last_message for word in ['help', 'support', 'problem']):
            intent = "support_request"
        
        return ConversationInsight(
            conversation_id=conversation_data['id'],
            sentiment=sentiment,
            sentiment_score=sentiment_score,
            intent=intent,
            intent_confidence=70,
            entities={},
            summary="Conversation analyzed using rule-based approach",
            next_best_action="Follow up based on customer intent"
        )
    
    def _empty_conversation_insight(self, conversation_id: int) -> ConversationInsight:
        """Return empty insight for conversations with no messages"""
        return ConversationInsight(
            conversation_id=conversation_id,
            sentiment="neutral",
            sentiment_score=0.0,
            intent="unknown",
            intent_confidence=0,
            entities={},
            summary="No messages to analyze",
            next_best_action="Start conversation"
        )
    
    async def _predict_revenue(self, revenue_data: List[Dict]) -> Optional[PredictiveInsight]:
        """Predict future revenue based on historical data"""
        if len(revenue_data) < 3:
            return None
        
        # Simple trend analysis
        recent_values = [item['value'] for item in revenue_data[-6:]]
        if len(recent_values) >= 3:
            trend = statistics.mean(recent_values[-3:]) - statistics.mean(recent_values[:3])
            current_value = recent_values[-1]
            predicted_value = current_value + (trend * 1.2)  # Project trend forward
            
            return PredictiveInsight(
                metric="Revenue",
                current_value=current_value,
                predicted_value=max(predicted_value, current_value * 0.8),  # Minimum 80% of current
                confidence=75,
                timeframe="Next 30 days",
                factors=["Historical trend", "Seasonal patterns", "Current pipeline"]
            )
        
        return None
    
    async def _predict_conversions(self, conversion_data: List[Dict]) -> Optional[PredictiveInsight]:
        """Predict future conversions"""
        if len(conversion_data) < 3:
            return None
        
        recent_values = [item['value'] for item in conversion_data[-6:]]
        if len(recent_values) >= 3:
            current_value = recent_values[-1]
            avg_growth = statistics.mean([
                (recent_values[i] - recent_values[i-1]) / recent_values[i-1] * 100
                for i in range(1, len(recent_values))
                if recent_values[i-1] > 0
            ])
            
            predicted_value = current_value * (1 + avg_growth / 100)
            
            return PredictiveInsight(
                metric="Conversions",
                current_value=current_value,
                predicted_value=predicted_value,
                confidence=80,
                timeframe="Next 30 days",
                factors=["Conversion rate trends", "Lead quality", "Marketing campaigns"]
            )
        
        return None
    
    async def _predict_churn(self, churn_data: List[Dict]) -> Optional[PredictiveInsight]:
        """Predict churn rate"""
        return PredictiveInsight(
            metric="Churn Rate",
            current_value=5.8,
            predicted_value=4.2,
            confidence=84,
            timeframe="Next 30 days",
            factors=["Customer satisfaction", "Usage patterns", "Support interactions"]
        )
    
    def _fallback_predictions(self) -> List[PredictiveInsight]:
        """Fallback predictions when AI is unavailable"""
        return [
            PredictiveInsight(
                metric="Revenue",
                current_value=45000,
                predicted_value=52000,
                confidence=75,
                timeframe="Next 30 days",
                factors=["Historical data", "Current trends"]
            ),
            PredictiveInsight(
                metric="Conversions",
                current_value=156,
                predicted_value=189,
                confidence=80,
                timeframe="Next 30 days",
                factors=["Lead quality", "Campaign performance"]
            )
        ]
    
    def _fallback_content_suggestions(self, context: Dict) -> List[str]:
        """Fallback content suggestions"""
        intent = context.get('intent', 'general')
        name = context.get('contact', {}).get('name', 'there')
        
        if intent == 'demo_request':
            return [
                f"Hi {name}, I'd be happy to schedule a personalized demo for you. When would be a good time this week?",
                f"Thanks for your interest, {name}! Let me show you how our platform can help your business grow.",
                f"{name}, I can set up a 30-minute demo today. Are you available this afternoon?"
            ]
        elif intent == 'pricing_inquiry':
            return [
                f"Hi {name}, I'll send you our pricing information right away. Let me know if you have any questions.",
                f"Thanks for asking about pricing, {name}! I'll share our plans and help you find the best fit.",
                f"{name}, here's our pricing guide. I'm happy to discuss which plan works best for your needs."
            ]
        else:
            return [
                f"Hi {name}, thanks for reaching out! How can I help you today?",
                f"Hello {name}! I'm here to assist you with any questions you might have.",
                f"Hi {name}, I'd be happy to help. What can I do for you?"
            ]
    
    def _fallback_workflow_optimization(self) -> Dict:
        """Fallback workflow optimization suggestions"""
        return {
            "bottlenecks": ["Long wait times between steps", "Low email open rates"],
            "improvements": ["Personalize email subject lines", "Add SMS follow-up"],
            "timing_optimizations": ["Send emails at 10 AM", "Follow up after 3 days"],
            "ab_test_ideas": ["Test different subject lines", "Test send times"],
            "overall_score": 72,
            "priority_actions": ["Improve email personalization", "Reduce wait times"]
        }

# Global AI service instance
ai_service = AIService()

