"""
SIPDO Prompt Optimizer — Agent Instruction Sets

Each agent is a specialized system prompt that drives Claude/GPT through
the SIPDO closed-loop prompt optimization process.

Reference: SIPDO (Self-Improving Prompts through Data-Augmented Optimization)
           https://arxiv.org/abs/2505.19514

Author: CoreRAG Team
Version: 1.0.0
"""

import json
import time
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from logger import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# Agent System Prompts
# ---------------------------------------------------------------------------

DOCUMENT_ANALYST_PROMPT = """You are an expert document structure analyst. Your task is to analyze the provided document text and understand its structure.

Given:
- The full text of a document (PDF/DOCX content)
- A set of expected field names and their values
- Domain knowledge (if available): expert-level reference material about this document type, including standard field names, extraction rules, format conventions, and common pitfalls

Your job:
1. Identify the document's structural elements (sections, headers, tables, paragraphs, lists)
2. For EACH expected field, locate WHERE in the document the value appears (or could be derived from)
3. Note any patterns: formatting conventions, date formats, number formats, naming conventions
4. Identify any cross-references between sections
5. Flag any fields whose values span multiple locations or require combining information
6. If domain knowledge is provided, leverage it to better understand standard field names, extraction rules, and format requirements for this document type

Output a JSON object with this EXACT structure:
{
    "document_type": "brief description of document type",
    "structure": {
        "sections": ["list of identified section names/headers"],
        "has_tables": true/false,
        "has_lists": true/false,
        "page_count_estimate": number
    },
    "field_locations": {
        "field_name": {
            "found": true/false,
            "location_description": "where in the document this value appears",
            "surrounding_context": "brief excerpt of surrounding text",
            "format_pattern": "any formatting pattern observed (e.g., date format, currency format)"
        }
    },
    "cross_references": ["list of any cross-reference patterns found"],
    "extraction_challenges": ["list of potential extraction difficulties"]
}

Be precise and thorough. Output ONLY valid JSON, nothing else."""


FIELD_DECOMPOSER_PROMPT = """You are an expert at analyzing field complexity for document extraction tasks.

Given:
- Field names and their expected values
- A document analysis report

Your job:
1. For each field, determine if it is SIMPLE (directly extractable as a single value) or COMPLEX (composite, calculated, conditional, or spanning multiple locations)
2. For COMPLEX fields, propose helper sub-fields that are each individually simple to extract
3. For each complex field, generate Python post-processing code that combines the helper sub-fields into the final value

Classification rules:
- SIMPLE: A single value at one location (e.g., "borrower_name" = "Acme Corp")
- COMPLEX: Composite address, calculated amounts, conditional values, multi-part data, values requiring formatting transformation

Output a JSON object with this EXACT structure:
{
    "field_analysis": {
        "field_name": {
            "complexity": "simple" or "complex",
            "reason": "why it is simple or complex"
        }
    },
    "decompositions": {
        "complex_field_name": {
            "sub_fields": {
                "sub_field_name": "extraction instruction for this sub-field"
            },
            "python_postprocessing": "def compose_complex_field_name(fields: dict) -> str:\\n    ... python code ..."
        }
    }
}

Rules for Python post-processing code:
- Function takes a dict of extracted sub-field values
- Returns the composed final value as a string
- Handle None/missing values gracefully
- Use only standard Python (no external libraries)
- Keep code simple and readable

Output ONLY valid JSON, nothing else."""


PROMPT_ARCHITECT_PROMPT = """You are an expert prompt engineer specializing in document field extraction.

Given:
- A document structure analysis
- Field definitions (including any helper sub-fields for complex fields)
- Expected values for reference
- Domain knowledge (if available): expert-level reference material about this document type, including standard field names, extraction rules, format conventions, and typical pitfalls

Your job is to generate an extraction prompt that will reliably extract ALL specified fields from the document when given to an LLM (GPT-4o).

IMPORTANT: If domain knowledge is provided, incorporate its extraction rules, format conventions, and field definitions directly into the prompt. Domain knowledge contains battle-tested rules for specific document types that dramatically improve extraction accuracy.

The prompt MUST follow this structure (inspired by SIPDO research):
1. **Task Requirements**: Clear statement of what the LLM must do
2. **Field Definitions**: Each field with its extraction instruction
3. **Rule Explanation**: Document-specific rules for extraction (date formats, number formats, naming conventions)
4. **Rule Application**: Step-by-step how to apply the rules
5. **Result Verification**: Self-check instructions for the LLM
6. **Output Format**: Exact JSON output format expected

Design principles:
- Be explicit about formats (dates, currencies, etc.)
- Reference document structure (e.g., "look in the header section for...")
- Include negative examples where helpful ("do NOT include the dollar sign")
- Make instructions unambiguous — no room for interpretation
- The prompt should work with GPT-4o

Output a JSON object with this EXACT structure:
{
    "prompt_text": "the full extraction prompt as a single string",
    "prompt_set": {
        "preamble": "the preamble/context section of the prompt",
        "fields": {
            "field_name": "specific extraction instruction for this field"
        },
        "output_format": "json"
    }
}

Output ONLY valid JSON, nothing else."""


SYNTHETIC_DATA_GENERATOR_PROMPT = """You are an expert at generating synthetic document variations for stress-testing extraction prompts.

Given:
- Original document text
- Expected field values
- Current difficulty level (1-5, where 5 is hardest)
- Previous synthetic examples (if any)

Your job is to generate a REALISTIC variation of the document that tests the extraction prompt's robustness at the specified difficulty level.

Difficulty level guidelines:
- Level 1: Minor rephrasing — same structure, slightly different wording around values
- Level 2: Format changes — different date formats, number representations, abbreviations
- Level 3: Structural changes — values moved to different sections, additional noise text, table-to-paragraph conversions
- Level 4: Ambiguity injection — similar-looking values in other contexts, partial information, headers changed
- Level 5: Maximum stress — OCR-like artifacts, missing sections, values split across paragraphs, conflicting information near the target values

Rules:
- The expected values MUST still be present and extractable (possibly in a modified format consistent with the difficulty)
- The document must remain realistic and coherent
- Each variation should be DIFFERENT from previous ones
- Focus on areas that are most likely to confuse extraction

Output a JSON object with this EXACT structure:
{
    "synthetic_document": "the full modified document text",
    "modifications_made": ["list of specific modifications applied"],
    "expected_values": {
        "field_name": "the expected value in this variation (may differ in format but same semantically)"
    },
    "difficulty_justification": "why this is difficulty level N"
}

Output ONLY valid JSON, nothing else."""


ERROR_ANALYST_PROMPT = """You are an expert at diagnosing extraction prompt failures.

Given:
- The current extraction prompt
- The document text (or synthetic variation)
- Expected values for each field
- Actual extracted values (what the LLM returned)
- The list of fields that got WRONG values
- Domain knowledge (if available): expert-level reference material about this document type

Your job:
1. For each failed field, identify the ROOT CAUSE of the failure
2. Categorize the failure type
3. Propose a specific, minimal PATCH to the prompt that fixes the issue
4. If domain knowledge is provided, use its extraction rules to inform your diagnosis — domain rules often explain WHY certain fields have specific formats or naming conventions

Failure categories:
- AMBIGUITY: The instruction is ambiguous; similar values exist elsewhere
- MISSING_CONTEXT: The instruction doesn't point the LLM to the right section
- FORMAT_MISMATCH: The LLM extracted the right info but in wrong format
- WRONG_FIELD: The LLM confused this field with another
- INCOMPLETE: The LLM extracted only part of the value
- HALLUCINATION: The LLM made up a value not in the document
- STRUCTURAL: The document structure confused the extraction

Output a JSON object with this EXACT structure:
{
    "error_analysis": {
        "field_name": {
            "expected": "expected value",
            "actual": "what was extracted",
            "failure_type": "one of the categories above",
            "root_cause": "detailed explanation of why the extraction failed",
            "patch_recommendation": "specific change to make to the prompt instruction for this field"
        }
    },
    "global_recommendations": ["list of any prompt-wide changes needed"],
    "severity": "low/medium/high — overall severity of the failures"
}

Output ONLY valid JSON, nothing else."""


PROMPT_REFINER_PROMPT = """You are an expert prompt refiner. Your task is to apply surgical fixes to an extraction prompt based on error analysis.

Given:
- The current extraction prompt (both full text and structured prompt_set)
- Error analysis with per-field root causes and patch recommendations
- Global recommendations

Your job:
1. Apply EACH patch recommendation to the relevant field instruction
2. Apply any global recommendations to the preamble or overall structure
3. Keep changes MINIMAL — only fix what's broken, don't rewrite the entire prompt
4. Ensure the fix is GENERAL (handles the class of error, not just the specific instance)
5. Maintain the prompt structure (Task Requirements → Rules → Application → Verification → Output Format)

Design principles:
- Don't overfit to a single error case — make the fix generalizable
- Preserve instructions that already work correctly
- Add clarifying notes rather than rewriting entire sections
- If a format issue: add explicit format instructions with examples
- If an ambiguity issue: add disambiguation instructions
- If a structural issue: add section/location hints

Output a JSON object with this EXACT structure:
{
    "refined_prompt_text": "the full refined extraction prompt",
    "refined_prompt_set": {
        "preamble": "updated preamble",
        "fields": {
            "field_name": "updated extraction instruction"
        },
        "output_format": "json"
    },
    "changes_made": [
        {
            "field": "field_name or 'preamble'",
            "change_type": "added/modified/clarified",
            "description": "what was changed and why"
        }
    ]
}

Output ONLY valid JSON, nothing else."""


CONSISTENCY_AUDITOR_PROMPT = """You are a quality assurance auditor for extraction prompts.

Given:
- The final optimized extraction prompt
- The original document text
- Expected field values
- Actual extracted values from running the prompt

Your job:
1. Verify each field was extracted correctly
2. Check for consistency across fields (e.g., dates should be in consistent format)
3. Check for completeness (no fields missing)
4. Rate the overall prompt quality

Output a JSON object with this EXACT structure:
{
    "overall_accuracy": 0.0 to 1.0,
    "per_field": {
        "field_name": {
            "status": "pass" or "fail",
            "extracted": "what was extracted",
            "expected": "what was expected",
            "notes": "any observations"
        }
    },
    "consistency_checks": {
        "format_consistency": "pass/fail — are all similar fields in consistent format?",
        "completeness": "pass/fail — were all fields attempted?",
        "no_hallucination": "pass/fail — no made-up values?"
    },
    "prompt_quality_rating": "excellent/good/adequate/needs_improvement",
    "final_recommendations": ["any last suggestions for improvement"]
}

Output ONLY valid JSON, nothing else."""


# ---------------------------------------------------------------------------
# Claude/GPT Call Wrapper
# ---------------------------------------------------------------------------

@dataclass
class AgentCallResult:
    """Result from an agent call."""
    agent_name: str
    content: str
    parsed_json: Optional[Dict[str, Any]] = None
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    duration_seconds: float = 0.0
    success: bool = True
    error: Optional[str] = None


@dataclass
class TokenTracker:
    """Tracks cumulative token usage and costs."""
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    calls: int = 0
    # Anthropic Claude pricing (Sonnet 3.5)
    input_cost_per_1m: float = 3.00
    output_cost_per_1m: float = 15.00
    # GPT-4o pricing
    gpt_input_cost_per_1m: float = 2.50
    gpt_output_cost_per_1m: float = 10.00
    gpt_input_tokens: int = 0
    gpt_output_tokens: int = 0
    gpt_calls: int = 0

    def add_claude_usage(self, input_tokens: int, output_tokens: int):
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.calls += 1

    def add_gpt_usage(self, input_tokens: int, output_tokens: int):
        self.gpt_input_tokens += input_tokens
        self.gpt_output_tokens += output_tokens
        self.gpt_calls += 1

    @property
    def total_tokens(self) -> int:
        return (self.total_input_tokens + self.total_output_tokens +
                self.gpt_input_tokens + self.gpt_output_tokens)

    @property
    def estimated_cost(self) -> float:
        claude_cost = (
            self.total_input_tokens / 1_000_000 * self.input_cost_per_1m +
            self.total_output_tokens / 1_000_000 * self.output_cost_per_1m
        )
        gpt_cost = (
            self.gpt_input_tokens / 1_000_000 * self.gpt_input_cost_per_1m +
            self.gpt_output_tokens / 1_000_000 * self.gpt_output_cost_per_1m
        )
        return claude_cost + gpt_cost

    def summary(self) -> Dict[str, Any]:
        return {
            "claude_calls": self.calls,
            "claude_input_tokens": self.total_input_tokens,
            "claude_output_tokens": self.total_output_tokens,
            "gpt_calls": self.gpt_calls,
            "gpt_input_tokens": self.gpt_input_tokens,
            "gpt_output_tokens": self.gpt_output_tokens,
            "total_tokens": self.total_tokens,
            "estimated_cost_usd": round(self.estimated_cost, 4),
        }


def _call_anthropic(
    system_prompt: str,
    user_message: str,
    api_key: str,
    agent_name: str,
    temperature: float = 0.0,
    max_tokens: int = 8000,
    model: str = "claude-sonnet-4-20250514",
) -> AgentCallResult:
    """Call Anthropic Claude API."""
    import anthropic

    start = time.time()
    try:
        client = anthropic.Anthropic(api_key=api_key, timeout=1800.0)
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        content = response.content[0].text
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        duration = time.time() - start

        # Try to parse as JSON
        parsed = None
        try:
            # Strip markdown code fences if present
            clean = content.strip()
            if clean.startswith("```"):
                clean = re.sub(r"^```(?:json)?\s*", "", clean)
                clean = re.sub(r"\s*```$", "", clean)
            parsed = json.loads(clean)
        except json.JSONDecodeError:
            logger.warning(f"Agent {agent_name}: response is not valid JSON, using raw text")

        logger.info(
            f"✅ Agent [{agent_name}] — {input_tokens} in / {output_tokens} out — {duration:.1f}s"
        )
        return AgentCallResult(
            agent_name=agent_name,
            content=content,
            parsed_json=parsed,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            duration_seconds=duration,
            success=True,
        )
    except Exception as e:
        duration = time.time() - start
        logger.error(f"❌ Agent [{agent_name}] failed: {e}")
        return AgentCallResult(
            agent_name=agent_name,
            content="",
            success=False,
            error=str(e),
            duration_seconds=duration,
        )


def _call_gpt(
    system_prompt: str,
    user_message: str,
    agent_name: str,
    temperature: float = 0.0,
    max_tokens: int = 8000,
    json_mode: bool = True,
) -> AgentCallResult:
    """Call GPT via existing Azure OpenAI / llm_call infrastructure."""
    from llm_call import llm_call

    start = time.time()
    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]
        response_format = {"type": "json_object"} if json_mode else None
        resp = llm_call(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=response_format,
        )
        content = resp.choices[0].message.content
        input_tokens = resp.usage.prompt_tokens
        output_tokens = resp.usage.completion_tokens
        duration = time.time() - start

        parsed = None
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            logger.warning(f"Agent [{agent_name}] GPT response is not valid JSON")

        logger.info(
            f"✅ Agent [{agent_name}] GPT — {input_tokens} in / {output_tokens} out — {duration:.1f}s"
        )
        return AgentCallResult(
            agent_name=agent_name,
            content=content,
            parsed_json=parsed,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            duration_seconds=duration,
            success=True,
        )
    except Exception as e:
        duration = time.time() - start
        logger.error(f"❌ Agent [{agent_name}] GPT failed: {e}")
        return AgentCallResult(
            agent_name=agent_name,
            content="",
            success=False,
            error=str(e),
            duration_seconds=duration,
        )


# ---------------------------------------------------------------------------
# High-Level Agent Functions
# ---------------------------------------------------------------------------

def agent_analyze_document(
    document_text: str,
    expected_values: Dict[str, str],
    api_key: str,
    tracker: TokenTracker,
    domain_knowledge: str = "",
) -> AgentCallResult:
    """Run the Document Analyst agent."""
    domain_section = ""
    if domain_knowledge:
        domain_section = f"\n\n## Domain Knowledge (Expert Reference)\n\n{domain_knowledge[:8000]}"
    user_msg = (
        f"## Document Text\n\n{document_text[:30000]}\n\n"
        f"## Expected Fields and Values\n\n{json.dumps(expected_values, indent=2)}"
        f"{domain_section}"
    )
    result = _call_anthropic(
        system_prompt=DOCUMENT_ANALYST_PROMPT,
        user_message=user_msg,
        api_key=api_key,
        agent_name="Document Analyst",
        temperature=0.0,
        max_tokens=4000,
    )
    if result.success:
        tracker.add_claude_usage(result.input_tokens, result.output_tokens)
    return result


def agent_decompose_fields(
    expected_values: Dict[str, str],
    document_analysis: Dict[str, Any],
    api_key: str,
    tracker: TokenTracker,
) -> AgentCallResult:
    """Run the Field Decomposer agent."""
    user_msg = (
        f"## Expected Fields and Values\n\n{json.dumps(expected_values, indent=2)}\n\n"
        f"## Document Analysis\n\n{json.dumps(document_analysis, indent=2)}"
    )
    result = _call_anthropic(
        system_prompt=FIELD_DECOMPOSER_PROMPT,
        user_message=user_msg,
        api_key=api_key,
        agent_name="Field Decomposer",
        temperature=0.0,
        max_tokens=4000,
    )
    if result.success:
        tracker.add_claude_usage(result.input_tokens, result.output_tokens)
    return result


def agent_generate_seed_prompt(
    document_analysis: Dict[str, Any],
    field_decomposition: Dict[str, Any],
    expected_values: Dict[str, str],
    api_key: str,
    tracker: TokenTracker,
    domain_knowledge: str = "",
) -> AgentCallResult:
    """Run the Prompt Architect agent."""
    # Build the fields dict including any helper sub-fields
    all_fields = {}
    decompositions = field_decomposition.get("decompositions", {})
    field_analysis = field_decomposition.get("field_analysis", {})

    for field_name, value in expected_values.items():
        fa = field_analysis.get(field_name, {})
        if fa.get("complexity") == "complex" and field_name in decompositions:
            # Add sub-fields instead of the complex field
            for sub_name, sub_instr in decompositions[field_name].get("sub_fields", {}).items():
                all_fields[sub_name] = sub_instr
        else:
            all_fields[field_name] = f"Extract the value for '{field_name}'"

    domain_section = ""
    if domain_knowledge:
        domain_section = (
            f"\n\n## Domain Knowledge (Expert Reference)\n\n"
            f"Use the following domain expertise to craft extraction rules, "
            f"format conventions, and field-specific instructions in the prompt:\n\n"
            f"{domain_knowledge}"
        )

    user_msg = (
        f"## Document Analysis\n\n{json.dumps(document_analysis, indent=2)}\n\n"
        f"## Field Definitions (including sub-fields for complex fields)\n\n"
        f"{json.dumps(all_fields, indent=2)}\n\n"
        f"## Expected Values (for reference — use to understand format and content)\n\n"
        f"{json.dumps(expected_values, indent=2)}\n\n"
        f"## Field Decomposition Report\n\n"
        f"{json.dumps(field_decomposition, indent=2)}"
        f"{domain_section}"
    )
    result = _call_anthropic(
        system_prompt=PROMPT_ARCHITECT_PROMPT,
        user_message=user_msg,
        api_key=api_key,
        agent_name="Prompt Architect",
        temperature=0.3,
        max_tokens=8000,
    )
    if result.success:
        tracker.add_claude_usage(result.input_tokens, result.output_tokens)
    return result


def agent_generate_synthetic_data(
    document_text: str,
    expected_values: Dict[str, str],
    difficulty: int,
    previous_synthetics: List[str],
    api_key: str,
    tracker: TokenTracker,
) -> AgentCallResult:
    """Run the Synthetic Data Generator agent."""
    prev_summary = "\n".join(
        f"- Variation {i + 1}: {s[:200]}..."
        for i, s in enumerate(previous_synthetics[-3:])
    ) if previous_synthetics else "None yet."

    user_msg = (
        f"## Original Document Text\n\n{document_text[:20000]}\n\n"
        f"## Expected Field Values\n\n{json.dumps(expected_values, indent=2)}\n\n"
        f"## Current Difficulty Level: {difficulty} (out of 5)\n\n"
        f"## Previous Synthetic Variations (summary)\n\n{prev_summary}"
    )
    result = _call_anthropic(
        system_prompt=SYNTHETIC_DATA_GENERATOR_PROMPT,
        user_message=user_msg,
        api_key=api_key,
        agent_name="Synthetic Data Generator",
        temperature=0.7,
        max_tokens=10000,
    )
    if result.success:
        tracker.add_claude_usage(result.input_tokens, result.output_tokens)
    return result


def agent_analyze_errors(
    current_prompt: str,
    document_text: str,
    expected_values: Dict[str, str],
    actual_values: Dict[str, str],
    failed_fields: List[str],
    api_key: str,
    tracker: TokenTracker,
    domain_knowledge: str = "",
) -> AgentCallResult:
    """Run the Error Analyst agent."""
    domain_section = ""
    if domain_knowledge:
        domain_section = f"\n\n## Domain Knowledge (Expert Reference)\n\n{domain_knowledge[:5000]}"
    user_msg = (
        f"## Current Extraction Prompt\n\n{current_prompt}\n\n"
        f"## Document Text\n\n{document_text[:15000]}\n\n"
        f"## Expected Values\n\n{json.dumps(expected_values, indent=2)}\n\n"
        f"## Actual Extracted Values\n\n{json.dumps(actual_values, indent=2)}\n\n"
        f"## Failed Fields\n\n{json.dumps(failed_fields)}"
        f"{domain_section}"
    )
    result = _call_anthropic(
        system_prompt=ERROR_ANALYST_PROMPT,
        user_message=user_msg,
        api_key=api_key,
        agent_name="Error Analyst",
        temperature=0.0,
        max_tokens=4000,
    )
    if result.success:
        tracker.add_claude_usage(result.input_tokens, result.output_tokens)
    return result


def agent_refine_prompt(
    current_prompt_text: str,
    current_prompt_set: Dict[str, Any],
    error_analysis: Dict[str, Any],
    api_key: str,
    tracker: TokenTracker,
) -> AgentCallResult:
    """Run the Prompt Refiner agent."""
    user_msg = (
        f"## Current Prompt (full text)\n\n{current_prompt_text}\n\n"
        f"## Current Prompt Set (structured)\n\n{json.dumps(current_prompt_set, indent=2)}\n\n"
        f"## Error Analysis\n\n{json.dumps(error_analysis, indent=2)}"
    )
    result = _call_anthropic(
        system_prompt=PROMPT_REFINER_PROMPT,
        user_message=user_msg,
        api_key=api_key,
        agent_name="Prompt Refiner",
        temperature=0.3,
        max_tokens=8000,
    )
    if result.success:
        tracker.add_claude_usage(result.input_tokens, result.output_tokens)
    return result


def agent_audit_consistency(
    final_prompt: str,
    document_text: str,
    expected_values: Dict[str, str],
    actual_values: Dict[str, str],
    api_key: str,
    tracker: TokenTracker,
) -> AgentCallResult:
    """Run the Consistency Auditor agent."""
    user_msg = (
        f"## Final Optimized Prompt\n\n{final_prompt}\n\n"
        f"## Original Document Text\n\n{document_text[:20000]}\n\n"
        f"## Expected Values\n\n{json.dumps(expected_values, indent=2)}\n\n"
        f"## Actual Extracted Values\n\n{json.dumps(actual_values, indent=2)}"
    )
    result = _call_anthropic(
        system_prompt=CONSISTENCY_AUDITOR_PROMPT,
        user_message=user_msg,
        api_key=api_key,
        agent_name="Consistency Auditor",
        temperature=0.0,
        max_tokens=4000,
    )
    if result.success:
        tracker.add_claude_usage(result.input_tokens, result.output_tokens)
    return result


# ---------------------------------------------------------------------------
# GPT Evaluation Helper
# ---------------------------------------------------------------------------

EXTRACTION_SYSTEM_PROMPT = """You are a precise document field extraction assistant.
You will be given a document and extraction instructions.
Extract the requested fields and return them as a JSON object.
If a field cannot be found, set its value to null.
Return ONLY a valid JSON object with field names as keys and extracted values as strings."""


def evaluate_prompt_with_gpt(
    prompt_text: str,
    prompt_set: Dict[str, Any],
    document_text: str,
    tracker: TokenTracker,
) -> AgentCallResult:
    """Evaluate an extraction prompt by running it against GPT with the document."""
    fields_list = "\n".join(
        f"- {k}: {v}" for k, v in prompt_set.get("fields", {}).items()
    )
    preamble = prompt_set.get("preamble", "")

    user_msg = (
        f"{preamble}\n\n"
        f"## Extraction Instructions\n\n{prompt_text}\n\n"
        f"## Fields to Extract\n\n{fields_list}\n\n"
        f"## Document\n\n{document_text[:25000]}\n\n"
        f"Extract ALL the fields listed above from the document. "
        f"Return a JSON object with field names as keys."
    )

    result = _call_gpt(
        system_prompt=EXTRACTION_SYSTEM_PROMPT,
        user_message=user_msg,
        agent_name="GPT Evaluator",
        temperature=0.0,
        max_tokens=4000,
        json_mode=True,
    )
    if result.success:
        tracker.add_gpt_usage(result.input_tokens, result.output_tokens)
    return result
