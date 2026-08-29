"""
Talent Acquisition AI Engine & Funnel Intelligence Platform
Module: Adversarial Prompt-Injection Firewall & Zero-Trust PII Sanitizer (sanitizer.py)

Neutralizes malicious prompt injection attacks, strips hidden HTML/zero-width chars,
detects keyword stuffing anomalies, and tokenizes candidate PII before LLM context ingestion.
"""

import re
import unicodedata
from typing import Dict, Tuple, List


# -----------------------------------------------------------------------------
# ADVERSARIAL PATTERNS & INJECTION SIGNATURES
# -----------------------------------------------------------------------------

INJECTION_PATTERNS = [
    r"(?i)system\s*instruction",
    r"(?i)ignore\s+(all\s+)?(previous|prior)\s+(instructions|rules|prompts)",
    r"(?i)override\s+(triage|eval|score|assessment)",
    r"(?i)assign\s+(\d{2,3}%\s+)?(match\s+score|rating|grade)",
    r"(?i)role:\s*(admin|system|evaluator)",
    r"(?i)bypass_filter",
    r"(?i)direct_applicable",
    r"(?i)eval_pass:\s*true",
    r"<!--\s*\[.*?\]\s*-->",  # Hidden HTML comment blocks
]

ZERO_WIDTH_CHARS = [
    "\u200b",  # Zero-width space
    "\u200c",  # Zero-width non-joiner
    "\u200d",  # Zero-width joiner
    "\ufeff",  # Zero-width no-break space (BOM)
    "\u2060",  # Word joiner
]


class ZeroTrustSanitizer:
    """
    Enterprise-grade security firewall for candidate submissions.
    Ensures adversarial payloads never reach the LLM or scoring logic.
    """

    def __init__(self):
        self.compiled_injection_regexes = [re.compile(p) for p in INJECTION_PATTERNS]

    def strip_zero_width_characters(self, text: str) -> str:
        """Removes all invisible zero-width unicode characters."""
        if not text:
            return ""
        cleaned = text
        for char in ZERO_WIDTH_CHARS:
            cleaned = cleaned.replace(char, "")
        return cleaned

    def detect_prompt_injections(self, text: str) -> Tuple[bool, List[str]]:
        """
        Scans input text for prompt injection signatures and system override directives.
        Returns (is_injected, matched_signatures).
        """
        if not text:
            return False, []

        cleaned = self.strip_zero_width_characters(text)
        detected_signatures = []

        for regex in self.compiled_injection_regexes:
            matches = regex.findall(cleaned)
            if matches:
                detected_signatures.append(regex.pattern)

        return len(detected_signatures) > 0, detected_signatures

    def detect_keyword_stuffing(self, skills_list: List[str], max_allowed_frequency: int = 4) -> bool:
        """
        Detects artificial keyword repetition designed to inflate TF-IDF match scores.
        """
        if not skills_list:
            return False

        skill_counts = {}
        for s in skills_list:
            norm_s = s.strip().lower()
            skill_counts[norm_s] = skill_counts.get(norm_s, 0) + 1
            if skill_counts[norm_s] > max_allowed_frequency:
                return True
        return False

    def anonymize_pii_for_llm(self, candidate_id: str, raw_text: str) -> Tuple[str, Dict[str, str]]:
        """
        Replaces sensitive personally identifiable information (PII) with ephemeral tokens.
        Ensures compliance with GDPR / LGPD zero-PII transmission policies.
        """
        token_map = {
            "candidate_id": candidate_id,
            "anon_token": f"CAND_ANON_{hash(candidate_id) % 10000:04d}"
        }

        # Redact emails, phone numbers, and standard identity markers
        email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
        phone_pattern = r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"

        sanitized = re.sub(email_pattern, "[EMAIL_REDACTED]", raw_text)
        sanitized = re.sub(phone_pattern, "[PHONE_REDACTED]", sanitized)

        return sanitized, token_map

    def sanitize_candidate_submission(self, raw_resume_or_skills: str, candidate_id: str) -> Dict:
        """
        Full security pipeline execution for a candidate profile.
        """
        # Step 1: Strip zero-width evasion characters
        clean_text = self.strip_zero_width_characters(raw_resume_or_skills)

        # Step 2: Scan for prompt injections
        is_injected, signatures = self.detect_prompt_injections(clean_text)

        # Step 3: Parse and check keyword stuffing
        skills = [s.strip() for s in clean_text.split(";") if s.strip()]
        is_stuffing = self.detect_keyword_stuffing(skills)

        # Step 4: Tokenize PII
        sanitized_text, token_map = self.anonymize_pii_for_llm(candidate_id, clean_text)

        is_security_flagged = is_injected or is_stuffing

        return {
            "candidate_id": candidate_id,
            "anon_token": token_map["anon_token"],
            "clean_text": sanitized_text,
            "is_security_flagged": 1 if is_security_flagged else 0,
            "is_prompt_injection": 1 if is_injected else 0,
            "is_keyword_stuffing": 1 if is_stuffing else 0,
            "detected_signatures": signatures,
        }
