#!/usr/bin/env python3
"""
Mexican Spanish Question Database
---------------------------------
Stores and manages dynamically generated questions
"""

import json, os
from datetime import datetime

class QuestionDatabase:
    def __init__(self, db_file='mexican_spanish_questions.json'):
        self.db_file = db_file
        self.questions = self.load_database()
    
    def load_database(self):
        """Load questions from JSON file"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {'question_sets': [], 'metadata': {}}
        return {'question_sets': [], 'metadata': {}}
    
    def save_database(self):
        """Save questions to JSON file"""
        self.questions['metadata']['last_updated'] = datetime.now().isoformat()
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.questions, f, ensure_ascii=False, indent=2)
    
    def add_question_set(self, questions, exam_name=None):
        """Add a new set of questions to database"""
        if not exam_name:
            exam_name = f"Examen_{len(self.questions['question_sets']) + 1}"
        
        question_set = {
            'name': exam_name,
            'created': datetime.now().isoformat(),
            'questions': questions,
            'count': len(questions)
        }
        
        self.questions['question_sets'].append(question_set)
        self.save_database()
        return len(self.questions['question_sets']) - 1
    
    def get_question_set(self, index=None):
        """Get a specific question set or the latest one"""
        if not self.questions['question_sets']:
            return None
        
        if index is None:
            index = -1  # Get latest
        
        try:
            return self.questions['question_sets'][index]
        except IndexError:
            return None
    
    def list_question_sets(self):
        """List all available question sets"""
        return [
            {
                'index': i,
                'name': qs['name'],
                'created': qs['created'],
                'count': qs['count']
            }
            for i, qs in enumerate(self.questions['question_sets'])
        ]
    
    def export_for_print(self, index=None):
        """Export questions in printable format"""
        question_set = self.get_question_set(index)
        if not question_set:
            return None
        
        export_text = f"EXAMEN: {question_set['name']}\n"
        export_text += f"Fecha: {question_set['created'][:10]}\n"
        export_text += "=" * 50 + "\n\n"
        
        for i, (question, options, answer) in enumerate(question_set['questions'], 1):
            export_text += f"{i}. {question}\n"
            if options:
                for key, value in options.items():
                    export_text += f"   {key}) {value}\n"
            export_text += f"   Respuesta: {answer}\n\n"
        
        return export_text

# Example usage integration
if __name__ == '__main__':
    db = QuestionDatabase()
    
    # Example: Add some sample questions
    sample_questions = [
        ("Lupita ha comido tacos muchas veces.", None, "ha comido"),
        ("Lo bueno de Xochimilco es la comida.", {'a': 'de', 'b': 'en', 'c': 'por'}, 'a'),
        ("No creo que Paco venga a tiempo.", None, "venga")
    ]
    
    set_id = db.add_question_set(sample_questions, "Muestra_Mexicana")
    print(f"Question set saved with ID: {set_id}")
    
    # List all sets
    print("\nAvailable question sets:")
    for qs in db.list_question_sets():
        print(f"  {qs['index']}: {qs['name']} ({qs['count']} questions)")
