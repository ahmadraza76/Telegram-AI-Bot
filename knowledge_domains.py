# knowledge_domains.py
# Developer: Mr AHMAD
# Knowledge domain classification and expertise mapping for USTAAD-AI

import re
from typing import Dict, List, Optional, Tuple
from config import Config

class KnowledgeDomainClassifier:
    def __init__(self):
        self.domain_keywords = {
            "academic_stem": {
                "keywords": [
                    "mathematics", "math", "algebra", "calculus", "geometry", "statistics",
                    "physics", "chemistry", "biology", "science", "equation", "formula",
                    "theorem", "proof", "hypothesis", "experiment", "research", "study"
                ],
                "hindi_keywords": [
                    "गणित", "भौतिकी", "रसायन", "जीवविज्ञान", "विज्ञान", "सूत्र", "प्रमेय"
                ],
                "response_style": "academic_detailed"
            },
            
            "competitive_exams": {
                "keywords": [
                    "upsc", "jee", "neet", "cat", "gate", "ssc", "banking", "railway",
                    "civil services", "engineering entrance", "medical entrance",
                    "mba entrance", "government job", "exam preparation", "mock test"
                ],
                "hindi_keywords": [
                    "प्रतियोगी परीक्षा", "सरकारी नौकरी", "परीक्षा तैयारी"
                ],
                "response_style": "exam_focused"
            },
            
            "technology": {
                "keywords": [
                    "programming", "coding", "software", "development", "algorithm",
                    "database", "api", "framework", "javascript", "python", "java",
                    "machine learning", "ai", "artificial intelligence", "blockchain",
                    "cybersecurity", "cloud computing", "aws", "azure", "docker"
                ],
                "hindi_keywords": [
                    "प्रोग्रामिंग", "कोडिंग", "सॉफ्टवेयर", "तकनीक", "एल्गोरिदम"
                ],
                "response_style": "technical_practical"
            },
            
            "creative_arts": {
                "keywords": [
                    "writing", "poetry", "shayari", "story", "creative", "art", "design",
                    "music", "painting", "literature", "novel", "poem", "haiku",
                    "content creation", "blogging", "storytelling"
                ],
                "hindi_keywords": [
                    "लेखन", "कविता", "शायरी", "कहानी", "कला", "साहित्य", "रचना"
                ],
                "response_style": "creative_inspiring"
            },
            
            "business_finance": {
                "keywords": [
                    "business", "startup", "entrepreneur", "marketing", "finance",
                    "investment", "stock market", "economics", "management",
                    "strategy", "sales", "profit", "revenue", "budget"
                ],
                "hindi_keywords": [
                    "व्यापार", "व्यवसाय", "निवेश", "बाजार", "अर्थशास्त्र", "प्रबंधन"
                ],
                "response_style": "business_strategic"
            },
            
            "life_skills": {
                "keywords": [
                    "career", "job", "interview", "resume", "relationship", "motivation",
                    "productivity", "time management", "goal setting", "habit",
                    "communication", "leadership", "personal development"
                ],
                "hindi_keywords": [
                    "करियर", "नौकरी", "रिश्ते", "प्रेरणा", "लक्ष्य", "आदत", "नेतृत्व"
                ],
                "response_style": "motivational_practical"
            },
            
            "cultural_social": {
                "keywords": [
                    "culture", "tradition", "festival", "religion", "spirituality",
                    "philosophy", "history", "mythology", "bollywood", "cricket",
                    "indian culture", "customs", "rituals", "values"
                ],
                "hindi_keywords": [
                    "संस्कृति", "परंपरा", "त्योहार", "धर्म", "अध्यात्म", "दर्शन",
                    "इतिहास", "पुराण", "मूल्य", "रीति-रिवाज"
                ],
                "response_style": "cultural_respectful"
            },
            
            "current_affairs": {
                "keywords": [
                    "news", "politics", "government", "policy", "election", "current events",
                    "international", "national", "economy", "social issues", "environment"
                ],
                "hindi_keywords": [
                    "समाचार", "राजनीति", "सरकार", "नीति", "चुनाव", "अर्थव्यवस्था"
                ],
                "response_style": "informative_balanced"
            },
            
            "health_wellness": {
                "keywords": [
                    "health", "fitness", "exercise", "diet", "nutrition", "wellness",
                    "yoga", "meditation", "mental health", "stress", "lifestyle"
                ],
                "hindi_keywords": [
                    "स्वास्थ्य", "फिटनेस", "व्यायाम", "आहार", "योग", "ध्यान", "तनाव"
                ],
                "response_style": "health_advisory"
            }
        }
        
        self.response_templates = {
            "academic_detailed": {
                "prefix": "🎓 **Academic Analysis**\n\n",
                "style": "detailed_explanation",
                "include_examples": True,
                "include_practice": True
            },
            "exam_focused": {
                "prefix": "📚 **Exam Strategy**\n\n",
                "style": "strategic_preparation",
                "include_tips": True,
                "include_timeline": True
            },
            "technical_practical": {
                "prefix": "💻 **Technical Solution**\n\n",
                "style": "step_by_step",
                "include_code": True,
                "include_resources": True
            },
            "creative_inspiring": {
                "prefix": "🎨 **Creative Inspiration**\n\n",
                "style": "inspirational_guidance",
                "include_examples": True,
                "include_exercises": True
            },
            "business_strategic": {
                "prefix": "💼 **Business Insight**\n\n",
                "style": "strategic_analysis",
                "include_case_studies": True,
                "include_action_items": True
            },
            "motivational_practical": {
                "prefix": "💪 **Life Guidance**\n\n",
                "style": "practical_motivation",
                "include_action_plan": True,
                "include_mindset": True
            },
            "cultural_respectful": {
                "prefix": "🌍 **Cultural Wisdom**\n\n",
                "style": "respectful_informative",
                "include_context": True,
                "include_significance": True
            },
            "informative_balanced": {
                "prefix": "📰 **Current Analysis**\n\n",
                "style": "balanced_informative",
                "include_multiple_perspectives": True,
                "include_implications": True
            },
            "health_advisory": {
                "prefix": "🏥 **Health Guidance**\n\n",
                "style": "advisory_cautious",
                "include_disclaimer": True,
                "include_general_tips": True
            }
        }
    
    def classify_query(self, query: str, language: str = "en") -> Tuple[str, float]:
        """Classify user query into knowledge domain"""
        query_lower = query.lower()
        domain_scores = {}
        
        for domain, config in self.domain_keywords.items():
            score = 0
            
            # Check English keywords
            for keyword in config["keywords"]:
                if keyword in query_lower:
                    score += 1
            
            # Check Hindi keywords if applicable
            if language in ["hi", "ur", "bn"] and "hindi_keywords" in config:
                for keyword in config["hindi_keywords"]:
                    if keyword in query:
                        score += 1.5  # Higher weight for native language
            
            # Normalize score
            total_keywords = len(config["keywords"]) + len(config.get("hindi_keywords", []))
            if total_keywords > 0:
                domain_scores[domain] = score / total_keywords
        
        # Find best matching domain
        if domain_scores:
            best_domain = max(domain_scores, key=domain_scores.get)
            confidence = domain_scores[best_domain]
            
            # If confidence is too low, classify as general
            if confidence < 0.1:
                return "general", 0.5
            
            return best_domain, confidence
        
        return "general", 0.5
    
    def get_response_template(self, domain: str) -> Dict:
        """Get response template for domain"""
        if domain in self.domain_keywords:
            response_style = self.domain_keywords[domain]["response_style"]
            return self.response_templates.get(response_style, self.response_templates["academic_detailed"])
        
        return {
            "prefix": "🎯 **USTAAD-AI Response**\n\n",
            "style": "comprehensive",
            "include_examples": True
        }
    
    def get_domain_specific_prompt_addition(self, domain: str, confidence: float) -> str:
        """Get domain-specific addition to system prompt"""
        
        if confidence < 0.3:
            return ""
        
        domain_prompts = {
            "academic_stem": """
**Academic Excellence Mode Activated**
- Provide detailed, step-by-step explanations
- Include relevant formulas, theorems, and principles
- Offer practice problems and examples
- Explain concepts from basic to advanced levels
- Use academic terminology appropriately
""",
            
            "competitive_exams": """
**Exam Preparation Mode Activated**
- Focus on exam-specific strategies and tips
- Provide time management techniques
- Include previous year question patterns
- Offer study schedules and preparation plans
- Emphasize high-yield topics and shortcuts
""",
            
            "technology": """
**Tech Expert Mode Activated**
- Provide practical, implementable solutions
- Include code examples and best practices
- Explain concepts with real-world applications
- Offer troubleshooting steps and debugging tips
- Stay updated with latest technology trends
""",
            
            "creative_arts": """
**Creative Mentor Mode Activated**
- Inspire creativity and artistic expression
- Provide techniques and creative exercises
- Share examples from literature and arts
- Encourage experimentation and originality
- Offer constructive feedback and improvement tips
""",
            
            "business_finance": """
**Business Advisor Mode Activated**
- Provide strategic business insights
- Include market analysis and trends
- Offer practical implementation strategies
- Share case studies and success stories
- Focus on ROI and practical outcomes
""",
            
            "life_skills": """
**Life Coach Mode Activated**
- Provide motivational and practical guidance
- Include actionable steps and goal-setting
- Offer psychological insights and mindset tips
- Share success strategies and habit formation
- Focus on personal growth and development
""",
            
            "cultural_social": """
**Cultural Guide Mode Activated**
- Provide respectful cultural insights
- Include historical and social context
- Explain traditions and their significance
- Offer comparative cultural perspectives
- Maintain sensitivity to diverse viewpoints
""",
            
            "current_affairs": """
**News Analyst Mode Activated**
- Provide balanced, factual information
- Include multiple perspectives on issues
- Explain implications and consequences
- Offer historical context and background
- Maintain objectivity and avoid bias
""",
            
            "health_wellness": """
**Health Advisor Mode Activated**
- Provide general health information only
- Include disclaimers about medical advice
- Focus on lifestyle and wellness tips
- Encourage professional medical consultation
- Emphasize prevention and healthy habits
"""
        }
        
        return domain_prompts.get(domain, "")
    
    def enhance_response_with_domain_context(self, response: str, domain: str, language: str) -> str:
        """Enhance response with domain-specific context"""
        
        template = self.get_response_template(domain)
        
        # Add domain-specific prefix if not already present
        if not response.startswith(template["prefix"]):
            response = template["prefix"] + response
        
        # Add domain-specific enhancements
        enhancements = {
            "academic_stem": self._add_academic_enhancements,
            "competitive_exams": self._add_exam_enhancements,
            "technology": self._add_tech_enhancements,
            "creative_arts": self._add_creative_enhancements,
            "business_finance": self._add_business_enhancements,
            "life_skills": self._add_life_enhancements,
            "cultural_social": self._add_cultural_enhancements,
            "health_wellness": self._add_health_enhancements
        }
        
        if domain in enhancements:
            response = enhancements[domain](response, language)
        
        return response
    
    def _add_academic_enhancements(self, response: str, language: str) -> str:
        """Add academic-specific enhancements"""
        if language == "hi":
            response += "\n\n📚 **अध्ययन टिप**: इस concept को अच्छे से समझने के लिए practice problems जरूर करें!"
        else:
            response += "\n\n📚 **Study Tip**: Practice problems are essential for mastering this concept!"
        return response
    
    def _add_exam_enhancements(self, response: str, language: str) -> str:
        """Add exam-specific enhancements"""
        if language == "hi":
            response += "\n\n🎯 **परीक्षा रणनीति**: Time management और revision के लिए proper schedule बनाएं।"
        else:
            response += "\n\n🎯 **Exam Strategy**: Create a proper schedule for time management and revision."
        return response
    
    def _add_tech_enhancements(self, response: str, language: str) -> str:
        """Add technology-specific enhancements"""
        if language == "hi":
            response += "\n\n💡 **Tech Tip**: हमेशा latest documentation check करें और hands-on practice करते रहें!"
        else:
            response += "\n\n💡 **Tech Tip**: Always check the latest documentation and keep practicing hands-on!"
        return response
    
    def _add_creative_enhancements(self, response: str, language: str) -> str:
        """Add creative-specific enhancements"""
        if language == "hi":
            response += "\n\n🎨 **रचनात्मक सुझाव**: अपनी unique style develop करें और regular practice करते रहें।"
        else:
            response += "\n\n🎨 **Creative Tip**: Develop your unique style and keep practicing regularly."
        return response
    
    def _add_business_enhancements(self, response: str, language: str) -> str:
        """Add business-specific enhancements"""
        if language == "hi":
            response += "\n\n💼 **बिजनेस टिप**: Market research और customer feedback को हमेशा priority दें।"
        else:
            response += "\n\n💼 **Business Tip**: Always prioritize market research and customer feedback."
        return response
    
    def _add_life_enhancements(self, response: str, language: str) -> str:
        """Add life skills enhancements"""
        if language == "hi":
            response += "\n\n💪 **जीवन मंत्र**: छोटे steps लें, consistent रहें, और अपने progress को celebrate करें!"
        else:
            response += "\n\n💪 **Life Mantra**: Take small steps, stay consistent, and celebrate your progress!"
        return response
    
    def _add_cultural_enhancements(self, response: str, language: str) -> str:
        """Add cultural-specific enhancements"""
        if language == "hi":
            response += "\n\n🌍 **सांस्कृतिक ज्ञान**: हमारी traditions में गहरा wisdom छुपा है।"
        else:
            response += "\n\n🌍 **Cultural Wisdom**: Our traditions contain deep wisdom and knowledge."
        return response
    
    def _add_health_enhancements(self, response: str, language: str) -> str:
        """Add health-specific enhancements"""
        if language == "hi":
            response += "\n\n⚠️ **महत्वपूर्ण**: यह सामान्य जानकारी है। किसी भी health issue के लिए doctor से सलाह लें।"
        else:
            response += "\n\n⚠️ **Important**: This is general information. Consult a doctor for any health issues."
        return response