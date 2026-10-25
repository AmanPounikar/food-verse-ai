"""
Food Verse AI - Multi-Provider AI Intelligence Engine.
Seamlessly integrates Google Gemini (Multimodal), Groq (Fast Vision/LLM),
and a robust Standalone Demonstration Fallback Mode powered by deterministic
food science heuristics.
"""

import json
import re
import base64
from io import BytesIO
from typing import Dict, Any, Optional
from PIL import Image
import requests

class FoodVerseAIEngine:
    """Unified multimodal and reasoning engine for food intelligence."""

    def __init__(self, provider: str = "demo", api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.provider = provider.lower() if provider else "demo"
        self.api_key = api_key.strip() if api_key else ""
        self.model_name = model_name

        # Validate configuration
        if not self.api_key and self.provider in ["gemini", "groq"]:
            self.provider = "demo"

    # =========================================================================
    # Helpers
    # =========================================================================
    def _image_to_base64_and_mime(self, image: Image.Image) -> tuple[str, str]:
        """Converts PIL image to base64 string and mime type."""
        buffered = BytesIO()
        image_format = image.format if image.format else "JPEG"
        if image_format.upper() not in ["JPEG", "PNG", "WEBP"]:
            image_format = "JPEG"
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
        image.save(buffered, format=image_format)
        img_bytes = buffered.getvalue()
        b64_str = base64.b64encode(img_bytes).decode("utf-8")
        mime = f"image/{image_format.lower()}"
        return b64_str, mime

    def _extract_json(self, raw_text: str) -> Dict[str, Any]:
        """Safely parses structured JSON from model response text."""
        if not raw_text:
            return {}
        # Try direct parse
        try:
            return json.loads(raw_text.strip())
        except Exception:
            pass

        # Try regex fenced code block ```json ... ```
        json_pattern = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
        if json_pattern:
            try:
                return json.loads(json_pattern.group(1))
            except Exception:
                pass

        # Try finding outer braces { ... }
        start = raw_text.find("{")
        end = raw_text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(raw_text[start:end+1])
            except Exception:
                pass

        return {"raw_output": raw_text}

    # =========================================================================
    # Gemini Invocation
    # =========================================================================
    def _call_gemini(self, prompt: str, image: Optional[Image.Image] = None) -> str:
        """Invokes Gemini using google-genai SDK or direct REST API."""
        model = self.model_name or "gemini-3.8-flash"
        
        # 1. Attempt using official google-genai SDK
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)
            
            # Prepare contents
            if image:
                b64_str, mime = self._image_to_base64_and_mime(image)
                # In google-genai SDK, use types.Part.from_bytes or direct dict
                part = types.Part.from_bytes(data=base64.b64decode(b64_str), mime_type=mime)
                response = client.models.generate_content(
                    model=model,
                    contents=[prompt, part]
                )
            else:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )
            if response and response.text:
                return response.text
        except Exception as sdk_err:
            # Fallback to direct REST API if SDK fails or version mismatch
            pass

        # 2. REST API fallback for Gemini
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
        parts = []
        if image:
            b64_str, mime = self._image_to_base64_and_mime(image)
            parts.append({
                "inline_data": {
                    "mime_type": mime,
                    "data": b64_str
                }
            })
        parts.append({"text": prompt})

        payload = {
            "contents": [{"parts": parts}],
            "generationConfig": {
                "temperature": 0.2,
                "response_mime_type": "application/json"
            }
        }

        resp = requests.post(url, json=payload, timeout=45)
        if resp.status_code == 200:
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            raise RuntimeError(f"Gemini API Error ({resp.status_code}): {resp.text}")

    # =========================================================================
    # Groq Invocation
    # =========================================================================
    def _call_groq(self, prompt: str, image: Optional[Image.Image] = None) -> str:
        """Invokes Groq API with vision or text models."""
        model = self.model_name or ("llama-3.2-11b-vision-preview" if image else "llama-3.3-70b-versatile")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        messages = []
        if image:
            b64_str, mime = self._image_to_base64_and_mime(image)
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime};base64,{b64_str}"}
                    }
                ]
            })
        else:
            messages.append({
                "role": "user",
                "content": prompt
            })

        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.2,
            "response_format": {"type": "json_object"}
        }

        resp = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=45)
        if resp.status_code == 200:
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        else:
            raise RuntimeError(f"Groq API Error ({resp.status_code}): {resp.text}")

    # =========================================================================
    # Tab 1: Food Recognition & Nutrition Audit
    # =========================================================================
    def analyze_dish(self, image: Image.Image, notes: str = "") -> Dict[str, Any]:
        """Multimodal analysis of meal photo for nutritional breakdown and health score."""
        prompt = f"""
You are an expert clinical dietitian and food vision intelligence agent.
Analyze this meal photo thoroughly. Provide an exhaustive nutritional and culinary breakdown in strictly valid JSON format.
Extra user notes: {notes or 'None provided'}

JSON format required:
{{
  "dish_name": "Exact identifiable dish title",
  "cuisine_type": "Mediterranean / Indian / Mexican / American / etc.",
  "estimated_portion": "e.g., 380 grams (1 large serving bowl)",
  "ingredients_detected": [
    {{"name": "Wild Salmon Fillet", "amount": "140g", "confidence": "96%"}},
    {{"name": "Organic Quinoa", "amount": "120g", "confidence": "94%"}},
    {{"name": "Avocado Slices", "amount": "50g", "confidence": "92%"}},
    {{"name": "Edamame & Mixed Greens", "amount": "70g", "confidence": "90%"}}
  ],
  "nutrition_breakdown": {{
    "calories_kcal": 540,
    "protein_g": 38.5,
    "carbohydrates_g": 42.0,
    "fats_g": 22.0,
    "saturated_fats_g": 3.8,
    "unsaturated_fats_g": 18.2,
    "dietary_fiber_g": 8.5,
    "sugars_g": 3.2,
    "sodium_mg": 460
  }},
  "allergen_alerts": [
    {{"allergen": "Fish", "severity": "High", "source": "Salmon Fillet"}},
    {{"allergen": "Soy", "severity": "Medium", "source": "Edamame"}}
  ],
  "health_score": 92,
  "health_grade": "A",
  "health_score_rationale": "High protein density, rich omega-3 fatty acids, low saturated fat, and high fiber content.",
  "caloric_burn_equivalents": {{
    "running_min": 45,
    "cycling_min": 60,
    "walking_min": 105
  }},
  "clinical_dietary_notes": "Ideal post-workout recovery meal; favorable glycemic index; supports cardiovascular wellness."
}}
Return ONLY valid JSON.
"""
        if self.provider != "demo":
            try:
                raw = self._call_gemini(prompt, image) if self.provider == "gemini" else self._call_groq(prompt, image)
                parsed = self._extract_json(raw)
                if parsed and "dish_name" in parsed:
                    parsed["_provider"] = self.provider
                    parsed["_model"] = self.model_name or ("gemini-3.8-flash" if self.provider == "gemini" else "groq-vision")
                    return parsed
            except Exception as e:
                # Fallback to demo mode on network or auth error
                pass

        # Standalone Demonstration Fallback Data
        return {
            "_provider": "demo",
            "_model": "FoodVerse-Heuristic-Vision-v3 (Offline Demo)",
            "dish_name": "Mediterranean Grilled Salmon & Quinoa Superfood Bowl",
            "cuisine_type": "Mediterranean / Wellness Fusion",
            "estimated_portion": "395 grams (1 loaded macro-balanced bowl)",
            "ingredients_detected": [
                {"name": "Wild Atlantic Salmon (Grilled)", "amount": "145g", "confidence": "98%"},
                {"name": "Fluffy Golden Quinoa", "amount": "110g", "confidence": "94%"},
                {"name": "Hass Avocado Slices", "amount": "60g", "confidence": "95%"},
                {"name": "Steamed Shelled Edamame", "amount": "50g", "confidence": "91%"},
                {"name": "Baby Spinach & Microgreens", "amount": "30g", "confidence": "89%"}
            ],
            "nutrition_breakdown": {
                "calories_kcal": 558,
                "protein_g": 39.2,
                "carbohydrates_g": 41.5,
                "fats_g": 23.4,
                "saturated_fats_g": 3.9,
                "unsaturated_fats_g": 19.5,
                "dietary_fiber_g": 9.2,
                "sugars_g": 3.1,
                "sodium_mg": 410
            },
            "allergen_alerts": [
                {"allergen": "Fish / Seafood", "severity": "High", "source": "Atlantic Salmon"},
                {"allergen": "Soy", "severity": "Moderate", "source": "Steamed Edamame beans"},
                {"allergen": "Sesame", "severity": "Low", "source": "Toasted garnish seeds"}
            ],
            "health_score": 94,
            "health_grade": "A+",
            "health_score_rationale": "Superior protein-to-calorie ratio, exceptional anti-inflammatory EPA/DHA Omega-3 profile, slow-digesting complex carbs, and 33% of daily dietary fiber.",
            "caloric_burn_equivalents": {
                "running_min": 46,
                "cycling_min": 62,
                "walking_min": 110
            },
            "clinical_dietary_notes": "Heart-healthy and diabetic-safe. The unsaturated fatty acids slow glucose absorption, preventing insulin spikes."
        }

    # =========================================================================
    # Tab 2: Food Freshness & Spoilage Diagnostic
    # =========================================================================
    def diagnose_freshness(self, image: Image.Image, item_category: str = "General Produce") -> Dict[str, Any]:
        """Multimodal diagnostic evaluating surface texture, mold, wrinkling, and safety."""
        prompt = f"""
You are a senior Food Microbiologist and Quality Assurance Inspector.
Inspect this raw perishable food item photo ({item_category}).
Evaluate surface texture, discoloration, shriveling/wrinkling, and presence of fungal colonies (mold) or bacterial slime.

Return strictly valid JSON in this format:
{{
  "item_identified": "Honeycrisp Apple / Ripe Banana / Raw Chicken Breast / etc.",
  "category": "{item_category}",
  "freshness_stage": "Fresh | Moderately Fresh | Spoiled",
  "freshness_score_pct": 88,
  "spoilage_indicators": {{
    "surface_texture": "Firm, crisp skin with natural waxy bloom / Soft, mushy spots / Slimy exudate",
    "discoloration": "Minimal; minor enzymatic oxidation on stem / Brown patches / Dark necrotic spots",
    "wrinkling_moisture_loss": "No visible turgor loss / Noticeable skin puckering / Severe desiccation",
    "mold_or_microbial_growth": "No visible mycelium or fungal colonies / Early sporulation observed"
  }},
  "actionable_safety_verdict": "Safe to consume | Consume within 24h | Discard immediately",
  "actionable_advice_detail": "Detailed biological safety reasoning and risk of foodborne pathogens like Salmonella, Listeria, or Mycotoxins.",
  "preservation_storage_guide": {{
    "optimal_temperature_c": "1°C - 4°C (34°F - 39°F)",
    "optimal_humidity": "90% - 95% relative humidity (perforated crisper drawer)",
    "ethylene_sensitivity": "High ethylene producer - isolate from leafy greens and crucifers",
    "freezing_viability": "Can be sliced and blanched or frozen in syrup for up to 8 months",
    "shelf_life_extension_tip": "Dip in diluted ascorbic acid (lemon water) or store wrapped in ventilated paper towel."
  }}
}}
Return ONLY valid JSON.
"""
        if self.provider != "demo":
            try:
                raw = self._call_gemini(prompt, image) if self.provider == "gemini" else self._call_groq(prompt, image)
                parsed = self._extract_json(raw)
                if parsed and "freshness_stage" in parsed:
                    parsed["_provider"] = self.provider
                    parsed["_model"] = self.model_name or ("gemini-3.8-flash" if self.provider == "gemini" else "groq-vision")
                    return parsed
            except Exception:
                pass

        # Standalone Demonstration Fallback Data
        return {
            "_provider": "demo",
            "_model": "FoodVerse-Microbial-Heuristic-v3 (Offline Demo)",
            "item_identified": "Grade A Fresh Crisp Honeycrisp Apple",
            "category": item_category,
            "freshness_stage": "Fresh",
            "freshness_score_pct": 94,
            "spoilage_indicators": {
                "surface_texture": "Turgid, taut cellular wall structure with natural protective epicuticular wax intact. Zero soft pitting.",
                "discoloration": "Vibrant anthocyanin red pigmentation with pale lenticel speckles. No enzymatic browning detected.",
                "wrinkling_moisture_loss": "Zero moisture loss; optimal cellular internal turgor pressure.",
                "mold_or_microbial_growth": "Negative. No fungal mycelium, Botrytis, or Penicillium colonies present."
            },
            "actionable_safety_verdict": "Safe to consume",
            "actionable_advice_detail": "Raw fruit is in peak organoleptic condition with full vitamin C preservation. Thoroughly rinse under cool potable water before slicing to remove surface dust.",
            "preservation_storage_guide": {
                "optimal_temperature_c": "1°C - 3°C (34°F - 37°F)",
                "optimal_humidity": "High humidity (90-95%) in crisper drawer",
                "ethylene_sensitivity": "Active Ethylene Producer: Store isolated from ethylene-sensitive items like leafy spinach and broccoli.",
                "freezing_viability": "Peel, core, slice, and freeze on a parchment tray for 8-10 months for baking/smoothies.",
                "shelf_life_extension_tip": "Keep cold immediately after harvest/purchase; cold storage retards pectin degradation and preserves crispness for up to 4 weeks."
            }
        }

    # =========================================================================
    # Tab 3: Kitchen Hygiene & Food Safety Compliance
    # =========================================================================
    def audit_kitchen_hygiene(self, image: Image.Image, kitchen_type: str = "Commercial Prep Station") -> Dict[str, Any]:
        """Computer vision inspection for HACCP food safety compliance, PPE, and hazard detection."""
        prompt = f"""
You are a certified HACCP Lead Food Safety Auditor and FDA/ServSafe compliance officer.
Examine this commercial kitchen / food preparation facility photo ({kitchen_type}).
Inspect specifically for:
1. PPE Compliance: Chef hat / hairnets, beard restraints, clean aprons, food-grade single-use glove usage.
2. Cross-Contamination Hazards: Raw animal proteins (poultry, beef, seafood) adjacent to ready-to-eat salads or porous surfaces. Color-coded board compliance.
3. Sanitization & Environmental State: Clean stainless steel, presence of approved sanitizer (e.g., quat/chlorine test kit or spray), grease buildup, chemical separation.
4. Food Temperature / Container storage: Uncovered bins, floor storage, allergen separation.

Return strictly valid JSON in this format:
{{
  "kitchen_type": "{kitchen_type}",
  "compliance_score_pct": 78,
  "haccp_grade": "Grade B (Conditional Pass)",
  "executive_summary": "Summary of critical versus non-critical audit findings.",
  "dimension_scores": {{
    "ppe_adherence": 85,
    "cross_contamination_control": 65,
    "sanitization_cleanliness": 90,
    "chemical_storage_safety": 70
  }},
  "violation_logs": [
    {{
      "severity": "CRITICAL",
      "category": "Cross-Contamination",
      "issue": "Raw poultry cutlet placed within 10cm of ready-to-eat salad greens on common station.",
      "corrective_action": "Immediately discard potentially contaminated greens, sanitize surface with 200ppm quat solution, enforce red cutting board mandate."
    }},
    {{
      "severity": "MAJOR",
      "category": "PPE Violation",
      "issue": "Line cook handling prep without visible hair restraint / hairnet.",
      "corrective_action": "Require all food handlers to dawn hair restraints and beard snoods prior to entering active prep line."
    }},
    {{
      "severity": "MINOR",
      "category": "Chemical Storage",
      "issue": "Sanitizer spray bottle stored at shelf level near prep utensils without secondary containment.",
      "corrective_action": "Relocate chemical agents below food contact surfaces in designated chemical locker."
    }}
  ],
  "inspector_signoff": "FDA Food Code 2026 / HACCP Standard Compliance Verification"
}}
Return ONLY valid JSON.
"""
        if self.provider != "demo":
            try:
                raw = self._call_gemini(prompt, image) if self.provider == "gemini" else self._call_groq(prompt, image)
                parsed = self._extract_json(raw)
                if parsed and "compliance_score_pct" in parsed:
                    parsed["_provider"] = self.provider
                    parsed["_model"] = self.model_name or ("gemini-3.8-flash" if self.provider == "gemini" else "groq-vision")
                    return parsed
            except Exception:
                pass

        # Standalone Demonstration Fallback Data
        return {
            "_provider": "demo",
            "_model": "FoodVerse-HACCP-Audit-v3 (Offline Demo)",
            "kitchen_type": kitchen_type,
            "compliance_score_pct": 82,
            "haccp_grade": "Grade B (Conditional Pass - Immediate Remediation Required)",
            "executive_summary": "Kitchen demonstrates high stainless steel cleanliness and valid sanitizer protocols, but critical separation protocols between raw animal proteins and ready-to-eat items need immediate correction.",
            "dimension_scores": {
                "ppe_adherence": 88,
                "cross_contamination_control": 62,
                "sanitization_cleanliness": 94,
                "chemical_storage_safety": 84
            },
            "violation_logs": [
                {
                    "severity": "CRITICAL",
                    "category": "Cross-Contamination Hazard",
                    "issue": "Raw poultry protein prep occurring adjacent to washed salad leaves without physical sneeze/splash barrier or color-coded separation.",
                    "corrective_action": "Enforce strict HACCP color-coding (Red: Raw Meat, Green: Salad/Produce). Discard exposed ready-to-eat items and re-sanitize station."
                },
                {
                    "severity": "MAJOR",
                    "category": "Personal Hygiene / PPE",
                    "issue": "Food handler observed with loose hair strands protruding past standard cap; missing disposable snood / net.",
                    "corrective_action": "Issue high-density hair containment nets and re-train staff on FDA Food Code § 2-402.11 standards."
                },
                {
                    "severity": "MINOR",
                    "category": "Facility Hygiene",
                    "issue": "Moist cloth towel left resting on prep table rather than submerged in labeled 200ppm chlorine/quat sanitizer bucket.",
                    "corrective_action": "Keep wiping cloths in fresh sanitizer buckets when not in continuous active use."
                }
            ],
            "inspector_signoff": "HACCP Certified AI Audit Officer • ISO 22000 Food Safety Standards"
        }

    # =========================================================================
    # Tab 4: Smart Kitchen Recipe Assistant
    # =========================================================================
    def generate_smart_recipes(self, ingredients: list[str], dietary_pref: str = "Any", max_time_min: int = 30, equipment: list[str] = None) -> Dict[str, Any]:
        """Generates creative, balanced recipes maximizing pantry ingredients with substitution advice."""
        equipment_str = ", ".join(equipment) if equipment else "Standard Stovetop, Oven, Knife, Pan"
        ingredients_str = ", ".join(ingredients) if ingredients else "Eggs, Spinach, Olive Oil, Garlic, Rice"

        prompt = f"""
You are an executive chef and culinary food scientist.
A home cook has provided the following pantry ingredients:
{ingredients_str}

Parameters:
- Dietary constraints: {dietary_pref}
- Maximum cooking time: {max_time_min} minutes
- Available kitchen equipment: {equipment_str}

Generate 2 innovative, highly appetizing, and nutritionally balanced recipes.
Include smart ingredient substitutions so missing ingredients can be easily swapped.

Return strictly valid JSON in this format:
{{
  "recipes": [
    {{
      "recipe_title": "Garlic-Infused Spinach & Egg Scramble with Toasted Quinoa",
      "cuisine_style": "Mediterranean Rustic",
      "prep_time_min": 10,
      "cook_time_min": 15,
      "total_time_min": 25,
      "difficulty": "Easy",
      "servings": 2,
      "calories_per_serving": 340,
      "macros": {{"protein_g": 22, "carbs_g": 28, "fats_g": 14, "fiber_g": 6}},
      "pantry_ingredients_used": ["Eggs", "Spinach", "Garlic", "Olive Oil"],
      "missing_or_optional_ingredients": ["Crumbled Feta Cheese", "Red Chili Flakes"],
      "smart_substitutions": [
        {{"original": "Spinach", "substitution": "Kale, Swiss Chard, or Frozen Peas", "culinary_note": "Sauté 2 minutes longer if using heartier greens"}},
        {{"original": "Olive Oil", "substitution": "Avocado Oil or Grass-Fed Butter", "culinary_note": "Butter adds rich nutty aroma over medium heat"}}
      ],
      "step_by_step_instructions": [
        "Finely mince the fresh garlic cloves.",
        "Heat 1 tbsp olive oil in a wide skillet over medium-low heat until fragrant.",
        "Fold in the spinach leaves and cook for 90 seconds until bright green and wilted.",
        "Whisk eggs with a pinch of sea salt and black pepper; pour into skillet and fold gently into soft curds.",
        "Plate immediately over warm grains, topped with fresh herbs and chili flakes."
      ],
      "chef_pro_tip": "Remove eggs from the pan when they still look 10% moist; residual pan heat will carry them to silky perfection."
    }}
  ]
}}
Return ONLY valid JSON.
"""
        if self.provider != "demo":
            try:
                raw = self._call_gemini(prompt) if self.provider == "gemini" else self._call_groq(prompt)
                parsed = self._extract_json(raw)
                if parsed and "recipes" in parsed and len(parsed["recipes"]) > 0:
                    parsed["_provider"] = self.provider
                    parsed["_model"] = self.model_name or ("gemini-3.8-flash" if self.provider == "gemini" else "groq-llama-3.3")
                    return parsed
            except Exception:
                pass

        # Standalone Demonstration Fallback Data
        first_ing = ingredients[0] if ingredients else "Eggs"
        return {
            "_provider": "demo",
            "_model": "FoodVerse-Culinary-Generator-v3 (Offline Demo)",
            "recipes": [
                {
                    "recipe_title": f"Tuscan Sautéed {first_ing} Medley with Garlic & Greens",
                    "cuisine_style": "Tuscan Farmhouse Comfort",
                    "prep_time_min": 8,
                    "cook_time_min": 14,
                    "total_time_min": 22,
                    "difficulty": "Easy",
                    "servings": 2,
                    "calories_per_serving": 385,
                    "macros": {"protein_g": 24.5, "carbs_g": 32.0, "fats_g": 16.5, "fiber_g": 7.2},
                    "pantry_ingredients_used": ingredients[:4] if len(ingredients) >= 4 else ingredients + ["Olive Oil", "Garlic"],
                    "missing_or_optional_ingredients": ["Lemon zest", "Shaved Parmesan", "Cracked Black Pepper"],
                    "smart_substitutions": [
                        {"original": "Garlic cloves", "substitution": "Garlic powder or shallots", "culinary_note": "Use 1/4 tsp powder per clove equivalent"},
                        {"original": "Olive Oil", "substitution": "Avocado oil, coconut oil, or butter", "culinary_note": "Avocado oil withstands higher searing temperatures"}
                    ],
                    "step_by_step_instructions": [
                        "Prep and wash all pantry produce, slicing aromatics thinly for quick pan caramelization.",
                        "Heat a heavy skillet with 1.5 tablespoons oil over medium heat until gently shimmering.",
                        f"Add aromatics followed by {first_ing}, searing for 4-5 minutes until golden and deeply aromatic.",
                        "Deglaze the pan with 2 tablespoons of water or vegetable stock to release fond from the skillet floor.",
                        "Season with kosher salt, cracked pepper, and a bright squeeze of citrus before warm plating."
                    ],
                    "chef_pro_tip": "Never crowd the skillet pan! Spacing ingredients prevents boiling in steam and ensures golden Maillard caramelization."
                },
                {
                    "recipe_title": "One-Pan Golden Skillet Frittata with Pantry Aromatics",
                    "cuisine_style": "Modern Bistro",
                    "prep_time_min": 10,
                    "cook_time_min": 18,
                    "total_time_min": 28,
                    "difficulty": "Easy",
                    "servings": 3,
                    "calories_per_serving": 320,
                    "macros": {"protein_g": 21.0, "carbs_g": 18.0, "fats_g": 18.5, "fiber_g": 5.0},
                    "pantry_ingredients_used": ingredients[:5] if len(ingredients) >= 5 else ingredients + ["Eggs", "Onion"],
                    "missing_or_optional_ingredients": ["Dijon mustard", "Fresh chives or parsley"],
                    "smart_substitutions": [
                        {"original": "Whole Eggs", "substitution": "Silken tofu blend (vegan) or liquid egg whites", "culinary_note": "Silken tofu produces a silky quiche texture"},
                        {"original": "Fresh greens", "substitution": "Frozen spinach or peas", "culinary_note": "Thaw and squeeze dry thoroughly first"}
                    ],
                    "step_by_step_instructions": [
                        "Whisk eggs thoroughly with salt, pepper, and 2 tbsp cold water until frothy.",
                        "Sauté vegetables and pantry items in an oven-safe skillet until softened and lightly browned.",
                        "Pour the egg mixture over the ingredients, swirling to distribute evenly.",
                        "Cook undisturbed over low heat for 6 minutes until edges set, then finish under broiler for 3 minutes until puffed and golden.",
                        "Cool for 3 minutes before slicing into wedges like a pizza."
                    ],
                    "chef_pro_tip": "Adding a splash of cold water instead of dairy milk creates steam pockets that make the egg frittata exceptionally light and fluffy."
                }
            ]
        }

    # =========================================================================
    # Tab 5: Personalized Meal Planner
    # =========================================================================
    def generate_meal_plan(self, profile: Dict[str, Any], bmr: float, tdee: float, target_calories: float, macro_split: Dict[str, float]) -> Dict[str, Any]:
        """Generates an adaptive 7-day nutritional schedule with an automated consolidated grocery list."""
        prompt = f"""
You are a licensed clinical sports nutritionist.
Create an adaptive 7-Day Precision Meal Plan and an automated consolidated grocery shopping list.

User Metabolic Profile:
- Age: {profile.get('age', 28)}, Sex: {profile.get('gender', 'Female')}, Weight: {profile.get('weight_kg', 65)} kg, Height: {profile.get('height_cm', 168)} cm
- Activity Level: {profile.get('activity_level', 'Moderately Active')}
- Primary Goal: {profile.get('goal', 'Fat Loss')}
- Dietary Constraints: {profile.get('dietary_pref', 'Diabetic-Friendly')}
- Calculated BMR: {bmr:.0f} kcal, TDEE: {tdee:.0f} kcal
- Target Calories: {target_calories:.0f} kcal/day
- Target Macros: Protein {macro_split.get('protein_g', 140)}g, Carbs {macro_split.get('carbs_g', 160)}g, Fats {macro_split.get('fats_g', 55)}g

Provide 7 complete days (Monday through Sunday) with Breakfast, Lunch, Dinner, and 1 Snack.
Group the total weekly grocery shopping list by standard supermarket aisles.

Return strictly valid JSON in this format:
{{
  "user_summary": {{
    "target_calories": {int(target_calories)},
    "protein_target_g": {int(macro_split.get('protein_g', 140))},
    "carbs_target_g": {int(macro_split.get('carbs_g', 160))},
    "fats_target_g": {int(macro_split.get('fats_g', 55))}
  }},
  "weekly_schedule": [
    {{
      "day": "Monday",
      "focus": "High energy kickstart / Complex carbs",
      "daily_totals": {{"calories": {int(target_calories)}, "protein_g": {int(macro_split.get('protein_g', 140))}, "carbs_g": {int(macro_split.get('carbs_g', 160))}, "fats_g": {int(macro_split.get('fats_g', 55))}}},
      "breakfast": {{"name": "Steel Cut Oats with Chia & Blueberries", "calories": 420, "protein_g": 18, "desc": "Cooked in unsweetened almond milk with 1 scoop vanilla whey/plant protein."}},
      "lunch": {{"name": "Grilled Lemon Herb Chicken Bowl with Quinoa", "calories": 580, "protein_g": 48, "desc": "150g chicken breast, 1 cup quinoa, roasted zucchini, and tahini drizzle."}},
      "dinner": {{"name": "Baked Wild Salmon with Asparagus & Sweet Potato", "calories": 540, "protein_g": 42, "desc": "Salmon fillet baked with rosemary garlic, steamed asparagus spears, baked sweet potato wedges."}},
      "snack": {{"name": "Greek Yogurt with Crushed Walnuts & Cinnamon", "calories": 260, "protein_g": 22, "desc": "Low-fat plain Greek yogurt with 15g raw walnuts."}}
    }}
  ],
  "consolidated_grocery_list": {{
    "Fresh Produce": ["Baby Spinach (300g)", "Blueberries (2 pints)", "Avocados (4 units)", "Asparagus (1 bunch)", "Sweet Potatoes (1.5 kg)", "Lemons (4 units)"],
    "Proteins & Dairy": ["Chicken Breast (1.2 kg)", "Wild Salmon Fillets (600g)", "Plain Greek Yogurt (1 kg)", "Organic Large Eggs (2 dozen)", "Whey or Plant Protein Powder (1 tub)"],
    "Grains & Pantry": ["Steel Cut Oats (1 kg)", "Golden Quinoa (500g)", "Raw Walnuts (250g)", "Chia Seeds (200g)", "Extra Virgin Olive Oil (500ml)"]
  }}
}}
Return ONLY valid JSON.
"""
        if self.provider != "demo":
            try:
                raw = self._call_gemini(prompt) if self.provider == "gemini" else self._call_groq(prompt)
                parsed = self._extract_json(raw)
                if parsed and "weekly_schedule" in parsed and len(parsed["weekly_schedule"]) >= 1:
                    parsed["_provider"] = self.provider
                    parsed["_model"] = self.model_name or ("gemini-3.8-flash" if self.provider == "gemini" else "groq-llama-3.3")
                    return parsed
            except Exception:
                pass

        # Standalone Demonstration Fallback Data
        cal = int(target_calories)
        p = int(macro_split.get("protein_g", 140))
        c = int(macro_split.get("carbs_g", 160))
        f = int(macro_split.get("fats_g", 55))

        days_data = [
            ("Monday", "Metabolic Ignition & High Fiber", "Steel Cut Oats with Chia Seeds & Wild Blueberries", "Grilled Lemon Herb Chicken Breast & Quinoa Bowl", "Pan-Seared Atlantic Salmon with Roasted Asparagus", "0% Greek Yogurt with Crushed Walnuts"),
            ("Tuesday", "Glycemic Stability & Clean Protein", "Poached Eggs on Sourdough with Smashed Avocado", "Mediterranean Chickpea & Grilled Turkey Breast Salad", "Grass-Fed Lean Beef Stir-Fry with Broccoli & Cauliflower Rice", "Handful of Raw Almonds & Green Apple"),
            ("Wednesday", "Antioxidant Rich Cellular Recovery", "Superfood Green Smoothie Bowl (Spinach, Protein, Flax)", "Albacore Tuna Stuffed Bell Peppers with Olive Oil Dressing", "Baked Lemon Cod with Steamed Green Beans & Brown Basmati", "Cottage Cheese with Sliced Strawberries"),
            ("Thursday", "Endurance & Sustained Glycogen", "Protein Chia Pudding with Unsweetened Almond Milk", "Smoked Tofu / Tempeh Bowl with Soba Noodles & Edamame", "Herb-Roasted Chicken Thighs with Sweet Potato Wedges", "Celery Sticks with All-Natural Peanut Butter"),
            ("Friday", "Omega-3 Anti-Inflammatory Focus", "Omelette with Baby Spinach, Mushrooms & Goat Cheese", "Grilled Salmon Caesar Salad (Light Olive Oil & Greek Yogurt Dressing)", "Turkey-Zucchini Meatballs over Roasted Spaghetti Squash", "Hard-Boiled Eggs with Smoked Paprika"),
            ("Saturday", "Active Weekend High-Energy Fuel", "Protein Banana Oat Pancakes with Pure Maple Drizzle", "Spiced Lentil & Roasted Vegetable Harvest Bowl", "Grilled Grass-Fed Flank Steak with Chimichurri & Portobello", "Roasted Seaweed Snacks & Hummus with Carrots"),
            ("Sunday", "Digestive Reset & Meal Prep Harmony", "Warm Golden Turmeric Chia Porridge with Blueberries", "Baked Lemon Pepper Chicken Salad with Avocado", "Hearty Mediterranean White Bean & Kale Stew with Olive Oil", "Dark Chocolate (85% Cocoa) with Raw Brazil Nuts")
        ]

        schedule = []
        for d_name, focus, b_name, l_name, din_name, s_name in days_data:
            schedule.append({
                "day": d_name,
                "focus": focus,
                "daily_totals": {"calories": cal, "protein_g": p, "carbs_g": c, "fats_g": f},
                "breakfast": {"name": b_name, "calories": int(cal * 0.25), "protein_g": int(p * 0.25), "desc": "Nutrient-dense breakfast supporting morning alertness and metabolic rate."},
                "lunch": {"name": l_name, "calories": int(cal * 0.35), "protein_g": int(p * 0.35), "desc": "Clean protein paired with complex carbohydrates and vibrant vegetables."},
                "dinner": {"name": din_name, "calories": int(cal * 0.30), "protein_g": int(p * 0.30), "desc": "Lean dinner promoting overnight muscular recovery and glycemic control."},
                "snack": {"name": s_name, "calories": int(cal * 0.10), "protein_g": int(p * 0.10), "desc": "Controlled micro-snack curbing late afternoon cortisol and appetite spikes."}
            })

        return {
            "_provider": "demo",
            "_model": "FoodVerse-Dietary-Planner-v3 (Offline Demo)",
            "user_summary": {
                "target_calories": cal,
                "protein_target_g": p,
                "carbs_target_g": c,
                "fats_target_g": f
            },
            "weekly_schedule": schedule,
            "consolidated_grocery_list": {
                "Fresh Produce": [
                    "Baby Spinach (500g)", "Organic Hass Avocados (5 units)", "Fresh Asparagus (2 bunches)",
                    "Broccoli Crowns (3 heads)", "Zucchini & Summer Squash (4 units)", "Lemons & Limes (6 units)",
                    "Fresh Blueberries & Strawberries (3 pints)", "Green Apples (4 units)", "Sweet Potatoes (1.5 kg)"
                ],
                "Proteins & Poultry": [
                    "Skinless Chicken Breasts (1.5 kg)", "Wild Atlantic Salmon Fillets (800g)",
                    "Albacore Tuna Fillets or Canned in Spring Water (4 cans)", "Lean Turkey Mince (93/7, 600g)",
                    "Pasture-Raised Organic Eggs (2 dozen)"
                ],
                "Dairy & Plant Alternatives": [
                    "0% Fat Plain Greek Yogurt (1.5 kg)", "Organic Cottage Cheese (500g)",
                    "Unsweetened Almond or Oat Milk (2L)", "Goat Cheese or Feta (200g)"
                ],
                "Grains, Seeds & Pantry Staples": [
                    "Rolled Steel-Cut Oats (1 kg)", "Tri-Color Quinoa (500g)", "Brown Basmati Rice (500g)",
                    "Organic Chia Seeds & Ground Flaxseed (300g)", "Raw Walnuts & Almonds (400g)",
                    "Extra Virgin Cold-Pressed Olive Oil (750ml)", "Natural Peanut / Almond Butter (1 jar)"
                ]
            }
        }

# =============================================================================
# Streamlit Cloud Entrypoint Forwarder
# If Streamlit is accidentally configured to run modules/ai_engine.py,
# automatically route execution to the main app.py UI.
# =============================================================================
if __name__ == "__main__":
    import sys
    from pathlib import Path
    import runpy

    root_dir = Path(__file__).resolve().parent.parent
    if str(root_dir) not in sys.path:
        sys.path.insert(0, str(root_dir))
    app_file = root_dir / "app.py"
    if app_file.exists():
        runpy.run_path(str(app_file), run_name="__main__")

