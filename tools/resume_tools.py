# File: tools/resume_tools.py
from langchain.tools import BaseTool
import re
from typing import Dict, List, Tuple, Optional
from pydantic import Field

class ResumeAnalyzer:
    COMMON_BUZZWORDS = {
        'synergy', 'dynamic', 'proactive', 'leverage', 'thinking outside the box',
        'results-driven', 'best of breed', 'go-getter', 'team player', 'passionate',
        'detail-oriented', 'proven track record', 'innovative', 'ninja', 'guru',
        'rockstar', 'thought leader', 'game changer', 'disruptive', 'full-stack',
        'strategic', 'growth hacking', 'change agent', 'cutting-edge', 'solution',
        'results-oriented', 'entrepreneurial mindset', 'visionary', 'scalable',
        'bleeding edge', 'robust', 'agile', 'lean', 'synergistic', 'paradigm shift'
    }
    
    @staticmethod
    def analyze_length(text: str) -> Dict:
        words = text.split()
        word_count = len(words)
        
        length_analysis = {
            "word_count": word_count,
            "is_too_long": word_count > 500,
            "is_too_short": word_count < 200,
            "message": ""
        }
        
        if length_analysis["is_too_long"]:
            length_analysis["message"] = f"Your resume is {word_count} words - that's longer than a Netflix terms of service! Try cutting it down."
        elif length_analysis["is_too_short"]:
            length_analysis["message"] = f"Only {word_count} words? Even my error messages are longer than that!"
        
        return length_analysis
    
    @staticmethod
    def detect_buzzwords(text: str) -> List[str]:
        found_buzzwords = []
        lower_text = text.lower()
        
        for buzzword in ResumeAnalyzer.COMMON_BUZZWORDS:
            if buzzword in lower_text:
                found_buzzwords.append(buzzword)
        
        return found_buzzwords

class TextExtractionTool(BaseTool):
    name: str = Field(default="text_extraction")
    description: str = Field(default="Extracts and cleans text from resume content")
    
    def _run(self, text: str) -> str:
        cleaned = re.sub(r'\s+', ' ', text).strip()
        cleaned = re.sub(r'[^\w\s@.\-,()]', '', cleaned)
        return cleaned
    
    async def _arun(self, text: str) -> str:
        raise NotImplementedError

class ResumeCriticTool(BaseTool):
    name: str = Field(default="resume_critic")
    description: str = Field(default="Analyzes resume content and generates detailed critique")
    
    def _run(self, text: str) -> Dict:
        analyzer = ResumeAnalyzer()
        
        length_analysis = analyzer.analyze_length(text)
        buzzwords = analyzer.detect_buzzwords(text)
        
        return {
            "length_analysis": length_analysis,
            "buzzwords": buzzwords,
            "buzzword_count": len(buzzwords),
            "text": text
        }
    
    async def _arun(self, text: str) -> Dict:
        raise NotImplementedError
