import re

INJECTION_PATTERNS = [
    r"ignore\b.*\binstructions\b",
    r"you are now",
    r"repeat your (system|prompt|instructions)",
    r"\bact as\b",
    r"forget (all |your )?instructions",
    r"new persona",
    r"\bjailbreak\b",
    r"\bDAN mode\b",
]

PYTHON_TOKENS = [
    r"\bdef \w+\(",
    r"\bimport \w+",
    r"\bclass \w+:",
    r"\bprint\(",
    r"\belif\b",
    r"\bNone\b",
    r"\bTrue\b",
    r"\bFalse\b",
    r":\s*$",
]
TS_TOKENS = [
    r"\b(const|let|var)\b",
    r":\s*(string|number|boolean|any)\b",
    r"=>\s*\{",
    r"\binterface \w+",
    r"\bfunction\b",
    r"console\.(log|error|warn)\(",
]
JAVA_TOKENS = [
    r"\bpublic\b",
    r"\bprivate\b",
    r"\bvoid\b",
    r"\bclass \w+(\s+extends|\s+implements|\s*\{)",
    r"System\.out\.",
    r"@Override",
]

_ALL_PATTERNS = PYTHON_TOKENS + TS_TOKENS + JAVA_TOKENS


def detect_injection(text: str) -> bool:
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def is_supported_language(code: str) -> bool:
    if not code.strip():
        return False
    matches = sum(1 for p in _ALL_PATTERNS if re.search(p, code, re.MULTILINE))
    return matches >= 2
